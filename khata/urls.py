from django.urls import path
from .views import DashboardView, EntryCreateView, SignupView, delete_account



urlpatterns = [
    path('', DashboardView.as_view(), name='home'),
    path('add/', EntryCreateView.as_view(), name='add'),
    path('signup/', SignupView.as_view(), name='signup'), 
    path('delete-account/', delete_account, name='delete_account'),
]