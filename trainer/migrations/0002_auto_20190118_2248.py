# Generated by Django 2.1.5 on 2019-01-18 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='delinquent',
            field=models.IntegerField(blank=True, help_text='Dark Type', null=True, verbose_name='Delinquent'),
        ),
        migrations.AddField(
            model_name='trainer',
            name='fairy_tale_girl',
            field=models.IntegerField(blank=True, help_text='Fairy Type', null=True, verbose_name='Fairy Tale Girl'),
        ),
    ]