# Generated by Django 4.2.13 on 2024-05-18 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0011_remove_cook_add_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="cook",
            name="bio",
            field=models.TextField(blank=True, null=True),
        ),
    ]
