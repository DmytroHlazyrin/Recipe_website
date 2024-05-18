from django.urls import path

from .views import index, CategoryListView, CookDetailView, CategoryCreateView, CategoryUpdateView, \
    CategoryDeleteView, SignUpView, CookListView, update_profile, CategoryDetailView

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
    path("category/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
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
]

app_name = "catalog"
