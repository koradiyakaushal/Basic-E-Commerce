from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
# Create your views here.
from .models import Product
from carts.models import Cart

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'products/list.html'
    
class ProductSlugDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/detail.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProductSlugDetailView, self).get_context_data(*args, **kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context
    
    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        try:
            instance = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Not found..")
        return instance