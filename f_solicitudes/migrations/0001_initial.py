# Generated by Django 5.0.6 on 2024-06-05 15:52

import f_solicitudes.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=55)),
                ('ap1', models.CharField(max_length=55)),
                ('ap2', models.CharField(blank=True, max_length=55)),
                ('dni', models.CharField(max_length=9, validators=[f_solicitudes.models.val_dni])),
                ('texto', models.TextField(max_length=512)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
