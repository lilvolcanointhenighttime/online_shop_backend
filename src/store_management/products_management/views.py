from django.shortcuts import render
from rest_framework import generics

from .models import Product, ProductCategory

from .serializers import ProductSerializer, ProductCategorySerializer

from .services import db_select_all

generics.RetrieveUpdateDestroyAPIView
class ProductAPIView(generics.ListCreateAPIView):
    queryset = db_select_all(Product)
    serializer_class = ProductSerializer

class ProductCategoryAPIView(generics.ListCreateAPIView):
    queryset = db_select_all(ProductCategory)
    serializer_class = ProductCategorySerializer
