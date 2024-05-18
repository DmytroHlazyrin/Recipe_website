# Generated by Django 5.0.6 on 2024-05-16 10:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_step_dish_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dish",
            name="recipe",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="dishes",
                to="catalog.step",
            ),
        ),
    ]