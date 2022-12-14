# Generated by Django 4.0.6 on 2022-08-02 16:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(unique=True, verbose_name='Series unique id')),
                ('name', models.CharField(default=uuid.uuid4, max_length=36, unique=True, verbose_name='Series name')),
            ],
        ),
        migrations.CreateModel(
            name='PassengerPlane',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=uuid.uuid4, max_length=36, unique=True, verbose_name='Plane name')),
                ('capacity', models.IntegerField(verbose_name='People capacity')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='planes', to='planes.series', to_field='code')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
