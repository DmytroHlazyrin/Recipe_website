# Generated by Django 5.0.6 on 2024-05-16 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_alter_ingredient_options_remove_review_dish_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cook",
            options={"verbose_name": "cook", "verbose_name_plural": "cooks"},
        ),
        migrations.AddField(
            model_name="category",
            name="description",
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name="category",
            name="image",
            field=models.URLField(blank=True, null=True),
        ),
    ]
