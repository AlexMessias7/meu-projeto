# Generated by Django 5.1.3 on 2024-11-20 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pedido",
            name="quantidade",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="consultorio",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.departamento"
            ),
        ),
        migrations.AlterField(
            model_name="pedido",
            name="material",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.produto"
            ),
        ),
    ]
