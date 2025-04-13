# Generated by Django 5.1.7 on 2025-03-13 01:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WomenPeriodApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('FechaInicio', models.DateField(verbose_name='Fecha Inicio Mes')),
                ('FechaFin', models.DateField(verbose_name='Fecha Fin Mes')),
                ('FechaRegistro', models.DateTimeField(verbose_name='fecha registro')),
                ('Mes', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='WomenPeriodApp.meses')),
            ],
            options={
                'db_table': 'Calendario',
            },
        ),
    ]
