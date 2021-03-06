# Generated by Django 2.1.5 on 2019-01-17 19:46

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number', models.IntegerField()),
                ('name', models.CharField(max_length=32)),
                ('base_attack', models.IntegerField()),
                ('base_defense', models.IntegerField()),
                ('base_stamina', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=12)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='pokemon',
            name='type_one',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='primary_typed', to='pokemon.Type'),
        ),
        migrations.AddField(
            model_name='pokemon',
            name='type_two',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='secondary_typed', to='pokemon.Type'),
        ),
    ]
