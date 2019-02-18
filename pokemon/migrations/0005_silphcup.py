# Generated by Django 2.1.5 on 2019-02-18 03:34

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon', '0004_typematchup'),
    ]

    operations = [
        migrations.CreateModel(
            name='SilphCup',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32)),
                ('types', models.ManyToManyField(related_name='cups', to='pokemon.Type')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
