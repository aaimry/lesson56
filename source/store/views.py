from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from store.forms import ProductsForm, SearchForm, AddToBasketForm, OrderForm
from store.models import Products, Basket, Order, ProductBasket


class ProductView(ListView):
    model = Products
    context_object_name = "product"
    template_name = "products.html"
    paginate_by = 5
    paginate_orphans = 0

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(title__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset.order_by("title")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = SearchForm()
        if self.search_value:
            context['form'] = SearchForm(initial={"search": self.search_value})
            context['search'] = self.search_value
        return context

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class ProductDetailView(DetailView):
    template_name = 'product_check.html'
    context_object_name = 'products_list'
    model = Products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        check_list = get_object_or_404(Products, pk=kwargs.get('object').id)
        context['check_list'] = check_list
        return context


class ProductCreateView(CreateView):
    template_name = 'products_add.html'
    model = Products
    form_class = ProductsForm


class ProductUpdateView(UpdateView):
    form_class = ProductsForm
    template_name = "update_product.html"
    model = Products
    context_object_name = 'product'


class ProductDeleteView(DeleteView):
    model = Products
    template_name = "product_delete.html"
    context_object_name = 'product'

    def get_success_url(self):
        return reverse('index')


class BasketView(ListView):
    model = Basket
    context_object_name = "product"
    template_name = 'basket.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        total = 0
        for product in Basket.objects.all():
            total += product.quantity * product.product.price
        kwargs['total'] = total
        form = OrderForm()
        kwargs['form'] = form
        return super().get_context_data(**kwargs)


class AddToBasketView(View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Products, pk=self.kwargs.get('pk'))
        if product.residue > 0:
            try:
                basket = Basket.objects.get(product=product)
                basket.quantity += 1
                basket.save()
                product.residue -= 1
                product.save()
            except Basket.DoesNotExist:
                basket = Basket.objects.create(product=product, quantity=1)
                product.residue -= 1
                product.save()
            return redirect(request.META.get('HTTP_REFERER'))


class DeleteFromBasketView(View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Products, pk=self.kwargs.get('pk'))
        basket = Basket.objects.get(product=product)
        basket.quantity -= 1
        basket.save()
        product.residue += 1
        product.save()
        return redirect('basket')


class MakeOrderView(View):
    template_name = 'make_order.html'
    model = Order
    form_class = OrderForm

    def post(self, request, *args, **kwargs):
        basket = Basket.objects.all()
        form = OrderForm(data=request.POST)
        order = form.save()
        for basket in Basket.objects.all():
            product_basket = ProductBasket.objects.create(product=basket.product, quantity=basket.quantity, order=order)
            product_basket.delete()
        return redirect('index')
