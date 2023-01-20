from django.urls import path
from .views import (
    CustomerCreateListAPIView,
    CustomerUDAPIView,
    CustomerApplySubscription,
    CustomerCancelSubscription,
    CompanyCreateListAPIView,
    CompanyUDAPIView
)


urlpatterns = [
    path('customer/', CustomerCreateListAPIView.as_view(), name="customer-view"),
    path('customer/<int:pk>/', CustomerUDAPIView.as_view(), name="customer-ud"),
    path('customer/<int:pk>/subs/', CustomerApplySubscription.as_view(), name="customer-subs"),
    path('customer/<int:pk>/subs/cancel/', CustomerCancelSubscription.as_view(), name="customer-subs-cancel"),
    path('company/', CompanyCreateListAPIView.as_view(), name="company-view"),
    path('company/<int:pk>/', CompanyUDAPIView.as_view(), name="company-ud"),
]
