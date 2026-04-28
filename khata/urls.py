from django.urls import path
from .views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('add/', EntryCreateView.as_view(), name='add'),
]