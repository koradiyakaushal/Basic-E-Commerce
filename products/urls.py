from django.urls import path, include,re_path
# from django.views.generic import ListView
from .views import ProductListView, ProductSlugDetailView

app_name = 'products'

urlpatterns = [
    path('',ProductListView.as_view(),name='list'),
    re_path('(?P<slug>[\w-]+)/$',ProductSlugDetailView.as_view(),name='detail'),
]
