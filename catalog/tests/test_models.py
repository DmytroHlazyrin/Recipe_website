from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from catalog.models import (
    Ingredient, Category, Review, Dish, Composition, Cook
)


class IngredientModelTest(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Salt")

    def test_ingredient_creation(self):
        ingredient = Ingredient.objects.get(name="Salt")
        self.assertEqual(ingredient.name, "Salt")


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Dessert", description="Sweet dishes"
        )

    def test_category_creation(self):
        category = Category.objects.get(name="Dessert")
        self.assertEqual(category.name, "Dessert")
        self.assertEqual(category.description, "Sweet dishes")


class DishModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.category = Category.objects.create(name="Test Category")
        self.dish = Dish.objects.create(
            name="Test Dish",
            author=self.user,
            description="Test Description",
            recipe="Test Recipe",
            cooking_time=timezone.timedelta(minutes=30),
            servings=4,
            category=self.category,
        )

    def test_dish_creation(self):
        dish = Dish.objects.get(name="Test Dish")
        self.assertEqual(dish.author, self.user)
        self.assertEqual(dish.servings, 4)


class CompositionModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="password"
        )
        self.ingredient = Ingredient.objects.create(name="Salt")
        self.category = Category.objects.create(name="Test Category")
        self.dish = Dish.objects.create(
            name="Test Dish",
            author=self.user,
            description="Test Description",
            recipe="Test Recipe",
            cooking_time=timezone.timedelta(minutes=30),
            servings=4,
            category=self.category,
        )
        self.composition = Composition.objects.create(
            dish=self.dish, ingredient=self.ingredient, amount=2, measure="tsp"
        )

    def test_composition_creation(self):
        composition = Composition.objects.get(
            dish=self.dish, ingredient=self.ingredient
        )
        self.assertEqual(composition.amount, 2)
        self.assertEqual(composition.measure, "tsp")


class CookModelTests(TestCase):

    def setUp(self):
        self.cook = Cook.objects.create_user(
            username="testcook",
            email="cook@test.com",
            password="12345",
            bio="Test bio",
        )

    def test_cook_creation(self):
        self.assertEqual(self.cook.username, "testcook")
        self.assertEqual(self.cook.email, "cook@test.com")
        self.assertEqual(self.cook.bio, "Test bio")
        self.assertTrue(self.cook.check_password("12345"))

    def test_add_to_favorites(self):
        category = Category.objects.create(name="Test Category")
        dish = Dish.objects.create(
            author=self.cook,
            name="Test Dish",
            description="Test Description",
            recipe="Test Recipe",
            cooking_time=timezone.timedelta(minutes=30),
            servings=4,
            category=category,
        )
        self.cook.add_to_favorites(dish)
        self.assertIn(dish, self.cook.favorite_dishes.all())

    def test_remove_from_favorites(self):
        category = Category.objects.create(name="Test Category")
        dish = Dish.objects.create(
            author=self.cook,
            name="Test Dish",
            description="Test Description",
            recipe="Test Recipe",
            cooking_time=timezone.timedelta(minutes=30),
            servings=4,
            category=category,
        )
        self.cook.add_to_favorites(dish)
        self.cook.remove_from_favorites(dish)
        self.assertNotIn(dish, self.cook.favorite_dishes.all())


class ReviewModelTests(TestCase):

    def setUp(self):
        self.cook = Cook.objects.create_user(
            username="testcook",
            email="cook@test.com",
            password="12345",
            bio="Test bio",
        )
        self.category = Category.objects.create(name="Test Category")
        self.dish = Dish.objects.create(
            author=self.cook,
            name="Test Dish",
            description="Test Description",
            recipe="Test Recipe",
            cooking_time=timezone.timedelta(minutes=30),
            servings=4,
            category=self.category,
        )
        self.review = Review.objects.create(
            author=self.cook,
            dish=self.dish,
            rating=5,
            review_body="Great dish!",
            date=timezone.now(),
        )

    def test_review_creation(self):
        self.assertEqual(self.review.author, self.cook)
        self.assertEqual(self.review.dish, self.dish)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.review_body, "Great dish!")
