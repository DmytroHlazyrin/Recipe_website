from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from catalog.models import Cook, Dish, Category, Review

class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username='testuser2000',
            password='12345'
        )
        self.client.login(
            username='testuser2000',
            password='12345'
        )
        self.cook = Cook.objects.create(
            username='testcook',
            email='cook@test.com',
            bio='Test bio',
            add_date=timezone.now()
        )
        self.category = Category.objects.create(
            name='Test category',
            description='Test description'
        )
        self.dish = Dish.objects.create(
            author=self.cook,
            name='Test dish',
            description='Test description',
            recipe='Test recipe',
            cooking_time=timezone.timedelta(minutes=30),
            servings=4,
            category=self.category
        )
        self.review = Review.objects.create(
            author=self.user,
            dish=self.dish,
            rating=5,
            review_body='Great dish!',
            date=timezone.now()
        )

    def test_cook_detail_view(self):
        url = reverse('catalog:cook-detail', kwargs={'pk': self.cook.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.cook.username)
        self.assertContains(response, self.cook.bio)

    def test_dish_detail_view(self):
        url = reverse('catalog:dish-detail', kwargs={'pk': self.dish.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dish.name)
        self.assertContains(response, self.dish.description)

    def test_category_detail_view(self):
        url = reverse('catalog:category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_category_list_view(self):
        url = reverse('catalog:category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.category.name)

    def test_review_create_view(self):
        url = reverse('catalog:review-add', kwargs={'pk': self.dish.pk})
        response = self.client.post(url, {
            'rating': 4,
            'review_body': 'Nice dish!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.dish.reviews.count(), 2)

    def test_review_update_view(self):
        url = reverse('catalog:review-edit', kwargs={'pk': self.review.pk})
        response = self.client.post(url, {
            'rating': 3,
            'review_body': 'Okay dish.',
        })
        self.assertEqual(response.status_code, 302)
        updated_review = Review.objects.get(pk=self.review.pk)
        self.assertEqual(updated_review.rating, 3)
        self.assertEqual(updated_review.review_body, 'Okay dish.')

    def test_review_delete_view(self):
        url = reverse('catalog:review-delete', kwargs={'pk': self.review.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

    def test_dish_create_view(self):
        url = reverse('catalog:dish-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.dish in Dish.objects.all())



