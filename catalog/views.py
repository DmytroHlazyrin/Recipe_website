from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import CookCreationForm, CategorySearchForm
from .models import Dish, Cook, Category, Composition, Review, Ingredient, Step


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


class CookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm


class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook
    queryset = Cook.objects.all().prefetch_related("dishes__category")


class CategoryListView(generic.ListView):
    model = Category
    context_object_name = "category_list"
    template_name = "catalog/category_list.html"
    paginate_by = 5

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




