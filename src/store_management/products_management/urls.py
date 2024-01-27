from django.urls import path

from . import views

urlpatterns = [
    path('api/product', view=views.ProductAPIView.as_view()),
    path('api/category', view=views.ProductCategoryAPIView.as_view()),
]

# handler404 = views.page_not_found