# Generated by Django 4.2.13 on 2024-05-17 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0009_cook_avatar_alter_category_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="cook",
            name="add_date",
            field=models.DateTimeField(auto_now_add=True, default="2024-05-16"),
            preserve_default=False,
        ),
    ]
