from django.urls import path

from .views import index, CategoryListView, CookCreateView, CookDetailView, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView

urlpatterns = [
    path("", index, name="index"),
    path("cooks/create/", CookCreateView.as_view(), name="cook-create"),
    path(
        "cooks/<int:pk>/", CookDetailView.as_view(), name="cook-detail"
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
