from django.db import models
from django.db.models import Q
from django.utils.functional import cached_property

from base.models import BaseModel

from math import floor

from .constants import CPM


class Type(BaseModel):
    name = models.CharField(max_length=12)

    @cached_property
    def image(self):
        return 'img/types/{0}.png'.format(self.name.lower())

    @cached_property
    def attacking(self):
        return self.attacking_matchups.order_by('defending_type__name')

    def __str__(self):
        return self.name.title()


class TypeMatchup(BaseModel):
    attacking_type = models.ForeignKey(Type, related_name='attacking_matchups',
        on_delete=models.DO_NOTHING)
    defending_type = models.ForeignKey(Type, related_name='defending_matchups',
        on_delete=models.DO_NOTHING)
    multiplier = models.DecimalField(max_digits=4, decimal_places=3)

    @cached_property
    def bg_class(self):
        if self.multiplier > 1:
            return 'bg-success'
        if self.multiplier < 1:
            if self.multiplier < 0.6:
                return 'bg-danger'
            return 'bg-warning'
        return 'bg-light'


class SilphCup(BaseModel):
    name = models.CharField(max_length=32)
    types = models.ManyToManyField(Type, related_name='cups')


class Pokemon(BaseModel):
    number = models.IntegerField()
    name = models.CharField(max_length=32)
    base_attack = models.IntegerField()
    base_defense = models.IntegerField()
    base_stamina = models.IntegerField()
    primary_type = models.ForeignKey(Type,
        on_delete=models.DO_NOTHING,
        related_name='primary_typed')
    secondary_type = models.ForeignKey(Type, blank=True, null=True,
        on_delete=models.DO_NOTHING,
        related_name='secondary_typed')

    @cached_property
    def image(self):
        return 'https://db.pokemongohub.net/images/official/detail/{0}.png'.format(
            str(self.number).zfill(3)
        )

    @cached_property
    def video(self):
        return 'https://db.pokemongohub.net/videos/normal/{0}.mp4'.format(
            self.name
        )

    @cached_property
    def primary_type_name(self):
        return str(self.primary_type)

    @cached_property
    def secondary_type_name(self):
        if self.secondary_type:
            return str(self.secondary_type)
        return None

    @cached_property
    def cups(self):
        return SilphCup.objects.filter(Q(types=self.primary_type) | Q(types=self.secondary_type))

    def effectiveness(self, attacking):
        effectiveness = TypeMatchup.objects.get(
            attacking_type=attacking,
            defending_type=self.primary_type
        ).multiplier
        if self.secondary_type:
            effectiveness *= TypeMatchup.objects.get(
                attacking_type=attacking,
                defending_type=self.secondary_type
            ).multiplier
        return effectiveness

    @cached_property
    def weaknesses(self):
        for t in Type.objects.all():
            eff = self.effectiveness(t)
            if self.effectiveness(t) > 1:
                yield t, eff

    @cached_property
    def resistances(self):
        for t in Type.objects.all():
            eff = self.effectiveness(t)
            if self.effectiveness(t) < 1:
                yield t, eff

    def attack(self, level, att_iv):
        return (self.base_attack + att_iv) * CPM[level]

    def defense(self, level, def_iv):
        return (self.base_defense + def_iv) * CPM[level]

    def stamina(self, level, sta_iv):
        return (self.base_stamina + sta_iv) * CPM[level]

    def cp(self, *args):
        return self.all_stats(*args)[0]

    def stat_sum(self, *args):
        return self.all_stats(*args)[1]

    def stat_product(self, *args):
        return self.all_stats(*args)[2]

    def all_stats(self, level, att_iv, def_iv, sta_iv):
        _att = self.attack(level, att_iv)
        _def = self.defense(level, def_iv)
        _sta = self.stamina(level, sta_iv)
        cp = int(max(floor(_att * _def**0.5 *  _sta**0.5) / 10, 10))
        return (
            cp,
            _att,
            _def,
            floor(_sta),
            round(_att * _def * floor(_sta))
        )

    @cached_property
    def max_cp(self):
        return self.cp(40, 15, 15, 15)

    @cached_property
    def max_stat_sum(self):
        return self.stat_sum(40, 15, 15, 15)

    @cached_property
    def max_stat_product(self):
        return self.stat_product(40, 15, 15, 15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Pokemon'
