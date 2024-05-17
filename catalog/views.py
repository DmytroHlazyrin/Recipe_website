from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from .forms import CategorySearchForm, CookForm, CookCreationForm, CookSearchForm
from .models import Dish, Cook, Category, Composition, Review, Ingredient


def index(request):
    """View function for the home page of the site."""

    num_cook = Cook.objects.count()
    num_dish = Dish.objects.count()
    num_category = Category.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_cook": num_cook,
        "num_dish": num_dish,
        "num_category": num_category,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)


class CategoryListView(generic.ListView):
    model = Category
    context_object_name = "category_list"
    template_name = "catalog/category_list.html"
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = CategorySearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        queryset = Category.objects.all()
        form = CategorySearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return queryset


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        num_dishes = Dish.objects.filter(category=category).count()
        context['num_dishes'] = num_dishes
        context['dishes'] = Dish.objects.filter(category=category)
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


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = CookForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('catalog:cook-detail', pk=request.user.pk)
    else:
        form = CookForm(instance=request.user)
    return render(request, 'catalog/update_profile.html', {'form': form})


class SignUpView(generic.CreateView):
    form_class = CookCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__category")
    template_name = 'catalog/cook_detail.html'


class CookListView(generic.ListView):
    model = Cook
    context_object_name = "cook_list"
    template_name = "catalog/cook_list.html"
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CookListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(
            initial={"username": username}
        )
        context['cook_list'] = [
            (cook, cook.dishes.count()) for cook in Cook.objects.all()
        ]
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return queryset
