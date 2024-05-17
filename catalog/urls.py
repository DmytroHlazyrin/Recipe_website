from django.urls import path

from .views import index, CategoryListView, CookDetailView, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView, update_profile, SignUpView, CookListView

urlpatterns = [
    path("", index, name="index"),
    path(
        "cook/<int:pk>/", CookDetailView.as_view(), name="cook-detail"
    ),
    path(
        "cook/<int:pk>/update", update_profile, name="cook-update"
    ),
    path(
        "cooks/", CookListView.as_view(), name="cook-list"
    ),
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path(
        "categories/create/",
        CategoryCreateView.as_view(),
        name="category-create"
    ),
    path(
        "categories/<int:pk>/update/",
        CategoryUpdateView.as_view(),
        name="category-update"
    ),
    path(
        "categories/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category-delete"
    ),
]

app_name = "catalog"
