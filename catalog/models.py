from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Ingredient(models.Model):
    name = models.CharField(max_length=35, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    image = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dish = models.ForeignKey("Dish", on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    review_body = models.TextField(max_length=1000)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.dish} review by {self.author} ({self.date})"


class Dish(models.Model):
    image = models.URLField(null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dishes")
    name = models.CharField(max_length=255)
    description = models.TextField()
    recipe = models.TextField(max_length=10000)
    cooking_time = models.DurationField()
    servings = models.IntegerField()
    addition_date = models.DateField(auto_now_add=True)
    calories = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dishes")
    ingredients = models.ManyToManyField(Ingredient, through="Composition")

    def __str__(self):
        return f"{self.name} by {self.author}"

    @property
    def formatted_cooking_time(self):
        hours, minutes = divmod(self.cooking_time.seconds // 60, 60)
        if hours > 0:
            return f"{hours} h {minutes} min"
        else:
            return f"{minutes} min"

    class Meta:
        verbose_name_plural = "Dishes"


class Composition(models.Model):
    MEASURE_CHOICES = (
        ("tsp", "tea spoon"),
        ("tbsp", "table spoon"),
        ("glass", "glass"),
        ("ml", "millilitre"),
        ("l", "litre"),
        ("g", "gram"),
        ("kg", "kilogram"),
        ("piece", "piece"),
        ("pinch", "pinch"),
    )
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dish_ingredients")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name="ingredient_dishes")
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    measure = models.CharField(max_length=15, choices=MEASURE_CHOICES)

    def __str__(self):
        return self.dish.name


class Cook(AbstractUser):
    favorite_dishes = models.ManyToManyField(Dish)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def get_absolute_url(self):
        return reverse("catalog:cook-detail", kwargs={"pk": self.pk})

    def add_to_favorites(self, dish):
        if dish not in self.favorite_dishes.all():
            self.favorite_dishes.add(dish)

    def remove_from_favorites(self, dish):
        if dish in self.favorite_dishes.all():
            self.favorite_dishes.remove(dish)
