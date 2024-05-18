from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import CategorySearchForm, CookForm, CookCreationForm, CookSearchForm, CookForm, DishSearchForm
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

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name", "")
        if name:
            queryset = queryset.filter(name__icontains=name)
        queryset = queryset.annotate(num_dishes=Count('dishes'))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = CategorySearchForm(initial={"name": name})
        context["category_list_with_dishes_count"] = [
            (category, category.num_dishes) for category in context["category_list"]
        ]
        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'catalog/category_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        queryset = Dish.objects.filter(category=category)
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get('query')
            if query:
                queryset = queryset.filter(Q(name__icontains=query) | Q(ingredients__name__icontains=query))
        context['num_dishes'] = queryset.count()
        context['dishes'] = queryset
        context['search_form'] = form
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
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = CookSearchForm(self.request.GET or None)
        context["cook_list_with_dishes_count"] = [
            (cook, cook.dishes_count) for cook in context["cook_list"]
        ]
        return context

    def get_queryset(self):
        queryset = Cook.objects.annotate(dishes_count=Count('dishes'))
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if username:
                queryset = queryset.filter(username__icontains=username)
        return queryset


@login_required
def update_profile(request, pk):
    if request.method == 'POST':
        form = CookForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('catalog:cook-detail', pk=request.user.pk)
    else:
        form = CookForm(instance=request.user)
    return render(request, 'catalog/cook_form.html', {'form': form})




