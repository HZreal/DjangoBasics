from pay.views import order
from django.urls import path
urlpatterns = [
    path('', order),
]