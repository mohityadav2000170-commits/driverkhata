from django.urls import path
from .views import *
from .views import SignupView


urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('add/', EntryCreateView.as_view(), name='add'),
    path('signup/', SignupView.as_view(), name='signup'), 
]