from django.urls import path
from ajax_select import urls as ajax_select_urls
from .views import CategoryListView, CookDetailView, CategoryCreateView, CategoryUpdateView, \
    CookListView, update_profile, CategoryDetailView, DishDetailView, DishListView, dish_create, add_to_favorites, \
    CookFavoritesListView, remove_from_favorites, ReviewCreateView, ReviewUpdateView, ReviewDeleteView, \
    update_dish

urlpatterns = [
    path("", DishListView.as_view(), name="index"),
    path(
        "cook/<int:pk>/",
        CookDetailView.as_view(),
        name="cook-detail"
    ),
    path(
        'favorites/<int:pk>/',
        CookFavoritesListView.as_view(),
        name="cook-favorites"
    ),
    path(
        'add-to-favorites/<int:pk>/',
        add_to_favorites,
        name='add-to-favorites'
    ),
    path(
        'remove-from-favorites/<int:pk>/',
        remove_from_favorites,
        name='remove-from-favorites'
    ),
    path(
        "cooks/",
        CookListView.as_view(),
        name="cook-list"
    ),
    path(
        "cook/update",
        update_profile,
        name="cook-update"
    ),
    path(
        "categories/",
        CategoryListView.as_view(),
        name="category-list"
    ),
    path(
        "category/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail"
    ),
    path(
        "category/create/",
        CategoryCreateView.as_view(),
        name="category-create"
    ),
    path(
        "category/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category-update"
    ),
    path(
        "dish/<int:pk>/",
        DishDetailView.as_view(),
        name="dish-detail"
    ),
    path(
        'dish/create/',
        dish_create,
        name='dish-create'
    ),
    path("dish/<int:pk>/update", update_dish, name='dish-update'),
    path('dish/<int:pk>/review/add/', ReviewCreateView.as_view(), name='review-add'),
    path('review/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review-edit'),
    path('review/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]

app_name = "catalog"
