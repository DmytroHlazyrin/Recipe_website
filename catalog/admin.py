from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import Cook, Category, Dish, Ingredient, Composition, Review, Step


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ["name", "author", "cooking_time", "calories", "category"]
    list_filter = ["category",]
    search_fields = ["name", "author", ]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ["name", ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["author", "dish", "rating", "review_body", "date", ]
    search_fields = ["author", "dish", ]


admin.site.register(Cook, UserAdmin)
admin.site.register(Category)
admin.site.register(Composition)
admin.site.register(Step)
