from django.urls import include, path
from . import views
from Bootes.views import *

urlpatterns = [
     path('', views.DataSearch, name='DataSearch'),
]
