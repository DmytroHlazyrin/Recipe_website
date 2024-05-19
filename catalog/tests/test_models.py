from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from catalog.models import Ingredient, Category, Review, Dish, Composition, Cook
from django.contrib.auth import get_user_model


class IngredientModelTest(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name='Salt')

    def test_ingredient_creation(self):
        ingredient = Ingredient.objects.get(name='Salt')
        self.assertEqual(ingredient.name, 'Salt')


class CategoryModelTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='Dessert', description='Sweet dishes')

    def test_category_creation(self):
        category = Category.objects.get(name='Dessert')
        self.assertEqual(category.name, 'Dessert')
        self.assertEqual(category.description, 'Sweet dishes')


class ReviewModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.dish = Dish.objects.create(name='Test Dish', author=self.user, description='Test Description',
                                        recipe='Test Recipe', cooking_time=timezone.timedelta(minutes=30),
                                        servings=4, category=self.category)
        self.review = Review.objects.create(author=self.user, dish=self.dish, rating=5, review_body='Great dish!',
                                            date=timezone.now())

    def test_review_creation(self):
        review = Review.objects.get(author=self.user, dish=self.dish)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.review_body, 'Great dish!')


class DishModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.dish = Dish.objects.create(name='Test Dish', author=self.user, description='Test Description',
                                        recipe='Test Recipe', cooking_time=timezone.timedelta(minutes=30),
                                        servings=4, category=self.category)

    def test_dish_creation(self):
        dish = Dish.objects.get(name='Test Dish')
        self.assertEqual(dish.author, self.user)
        self.assertEqual(dish.servings, 4)


class CompositionModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='password')
        self.ingredient = Ingredient.objects.create(name='Salt')
        self.category = Category.objects.create(name='Test Category')
        self.dish = Dish.objects.create(name='Test Dish', author=self.user, description='Test Description',
                                        recipe='Test Recipe', cooking_time=timezone.timedelta(minutes=30),
                                        servings=4, category=self.category)
        self.composition = Composition.objects.create(dish=self.dish, ingredient=self.ingredient, amount=2,
                                                      measure='tsp')

    def test_composition_creation(self):
        composition = Composition.objects.get(dish=self.dish, ingredient=self.ingredient)
        self.assertEqual(composition.amount, 2)
        self.assertEqual(composition.measure, 'tsp')


class CookModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser2000', password='password', email='test@example.com')

    def test_cook_creation(self):
        cook = Cook.objects.get(username='testuser2000')
        self.assertEqual(cook.email, 'test@example.com')
