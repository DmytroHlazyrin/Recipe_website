from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from .forms import (
    CategorySearchForm,
    CookCreationForm,
    CookSearchForm,
    CookForm,
    DishSearchForm,
    DishForm,
    CompositionFormSet,
    ReviewForm,
)
from .models import Dish, Cook, Category, Review


class CategoryListView(generic.ListView):
    model = Category
    context_object_name = "category_list"
    template_name = "catalog/category_list.html"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        queryset = queryset.annotate(
            num_dishes=Count("dishes")
        ).order_by("-num_dishes")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = CategorySearchForm(initial={"name": name})
        context["category_list_with_dishes_count"] = [
            (
                category,
                category.num_dishes
            ) for category in context["category_list"]
        ]
        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = "catalog/category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        queryset = Dish.objects.filter(category=category)
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get("query")
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | Q(
                        ingredients__name__icontains=query
                    )
                ).distinct()
        context["num_dishes"] = queryset.count()
        context["dishes"] = queryset
        context["search_form"] = form
        return context


class CategoryCreateView(LoginRequiredMixin, generic.CreateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("catalog:category-list")


class CategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Category
    fields = "__all__"
    success_url = reverse_lazy("catalog:category-list")


class CategoryDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Category
    success_url = reverse_lazy("catalog:category-list")


class SignUpView(generic.CreateView):
    form_class = CookCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    template_name = "catalog/cook_detail.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("dishes__category")


class CookFavoritesListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    context_object_name = "favorite_dishes"
    template_name = "catalog/cook_favorites_list.html"
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = DishSearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        user = self.request.user
        queryset = user.favorite_dishes.all()
        form = DishSearchForm(self.request.GET or None)
        if form.is_valid():
            query = form.cleaned_data.get("query")
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | Q(
                        ingredients__name__icontains=query
                    )
                ).distinct()
        else:
            print("Form errors:", form.errors)
        return queryset


@login_required
def add_to_favorites(request, pk):
    dish = Dish.objects.get(pk=pk)
    request.user.add_to_favorites(dish)
    messages.success(
        request, f"{dish.name} has been added to your favorites!"
    )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def remove_from_favorites(request, pk):
    dish = Dish.objects.get(pk=pk)
    request.user.remove_from_favorites(dish)
    messages.success(
        request, f"{dish.name} has been removed from your favorites!"
    )
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class CookListView(generic.ListView):
    model = Cook
    context_object_name = "cook_list"
    template_name = "catalog/cook_list.html"
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = CookSearchForm(self.request.GET or None)
        context["cook_list_with_dishes_count"] = [
            (cook, cook.dishes_count) for cook in context["cook_list"]
        ]
        return context

    def get_queryset(self):
        queryset = Cook.objects.annotate(dishes_count=Count("dishes"))
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            if username:
                queryset = queryset.filter(username__icontains=username)
        return queryset


@login_required
def update_profile(request):
    if request.method == "POST":
        form = CookForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("catalog:cook-detail", pk=request.user.pk)
    else:
        form = CookForm(instance=request.user)
    return render(
        request, "catalog/cook_form.html", {"form": form}
    )


class DishDetailView(generic.DetailView):
    model = Dish
    template_name = "catalog/dish_detail.html"

    def get_queryset(self):
        queryset = Dish.objects.prefetch_related(
            "dish_ingredients__ingredient"
        )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DishListView(generic.ListView):
    model = Dish
    template_name = "catalog/dish_list.html"
    context_object_name = "dish_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        num_dish = Dish.objects.count()
        context["num_dish"] = num_dish
        context["search_form"] = DishSearchForm(self.request.GET or None)
        return context

    def get_queryset(self):
        queryset = Dish.objects.select_related("author")
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get("query")
            if query:
                queryset = queryset.filter(
                    Q(name__icontains=query) | Q(
                        ingredients__name__icontains=query
                    )
                ).distinct()
        return queryset


@login_required()
def dish_create(request):
    if request.method == "POST":
        form = DishForm(request.POST, request.FILES)
        formset = CompositionFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            dish = form.save(commit=False)
            dish.author = request.user
            dish.save()
            form.save_m2m()
            formset.instance = dish
            formset.save()
            return redirect("catalog:dish-detail", pk=dish.pk)
    else:
        form = DishForm()
        formset = CompositionFormSet()

    return render(
        request, "catalog/dish_form.html",
        {"form": form, "formset": formset}
    )


@login_required
def update_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    if dish.author == request.user:
        if request.method == "POST":
            form = DishForm(request.POST, request.FILES, instance=dish)
            formset = CompositionFormSet(
                request.POST, request.FILES, instance=dish
            )
            if form.is_valid() and formset.is_valid():
                form.save()
                formset.save()
                return redirect("catalog:dish-detail", pk=dish.pk)
        else:
            form = DishForm(instance=dish)
            formset = CompositionFormSet(instance=dish)

        context = {
            "form": form,
            "formset": formset,
            "dish": dish,
        }
        return render(request, "catalog/dish_form.html", context)
    else:
        return redirect("catalog:dish-detail", pk=pk)


class ReviewCreateView(LoginRequiredMixin, generic.CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "catalog/review_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.dish = get_object_or_404(Dish, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dish"] = get_object_or_404(Dish, pk=self.kwargs["pk"])
        return context

    def get_success_url(self):
        return reverse_lazy(
            "catalog:dish-detail", kwargs={"pk": self.kwargs["pk"]}
        )


class ReviewUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "catalog/review_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["dish"] = self.object.dish
        return context

    def get_success_url(self):
        return reverse_lazy(
            "catalog:dish-detail", kwargs={"pk": self.object.dish.pk}
        )


class ReviewDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Review
    template_name = "catalog/review_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "catalog:dish-detail", kwargs={"pk": self.object.dish.pk}
        )
