from django.urls import path
from .views import ProfileDetailView, BusinessProfileListView, CustomerProfileListView

urlpatterns = [
    path('<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('business/', BusinessProfileListView.as_view(), name='business-profile-list'),
    path('customer/', CustomerProfileListView.as_view(), name='customer-profile-list'),
]