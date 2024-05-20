from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import (
    Cook, Category, Dish, Ingredient, Composition, Review
)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = [
        "id", "name", "author", "cooking_time", "calories", "category"
    ]
    list_filter = [
        "category",
    ]
    search_fields = [
        "name",
        "author",
    ]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = [
        "name",
    ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [
        "author",
        "dish",
        "rating",
        "review_body",
        "date",
    ]
    search_fields = [
        "author",
        "dish",
    ]


@admin.register(Cook)
class CookAdmin(admin.ModelAdmin):
    list_display = (
                       "id",
                       "bio",
                   ) + UserAdmin.list_display
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("avatar", "bio")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {"fields": ("first_name", "last_name", "avatar", "bio")},
            ),
        )
    )


admin.site.register(Category)
admin.site.register(Composition)
