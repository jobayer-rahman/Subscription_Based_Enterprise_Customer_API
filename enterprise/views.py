from rest_framework import generics
from .models import Company, Customer, CustomerPhone, Subscription
from django.shortcuts import get_object_or_404
from .serializers import (
    CompanySerializer,
    CustomerSerializer,
    CustomerDetailSerializer,
    SubscriptionSerializer,
    SubscriptionDetailSerializer
)

class CompanyCreateListAPIView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CustomerCreateListAPIView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CustomerSerializer
        return CustomerDetailSerializer

class CustomerUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerDetailSerializer

    def get_object(self):
        return get_object_or_404(CustomerPhone, phone__phone_number=self.kwargs['pk']).customer

class CustomerApplySubscription(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubscriptionSerializer
        return SubscriptionDetailSerializer

    def get_queryset(self):
        return Subscription.objects.filter(
            phone__phone__phone_number=self.kwargs['pk']
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request, "cp": CustomerPhone.objects.get(phone__phone_number=self.kwargs['pk'])})
        return context

class CustomerCancelSubscription(generics.RetrieveUpdateDestroyAPIView):
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return SubscriptionSerializer
        return SubscriptionDetailSerializer

    def get_object(self):
        return Subscription.objects.filter(
            phone__phone__phone_number=self.kwargs['pk'],
            is_active=True,
        ).first()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request, "cp": CustomerPhone.objects.get(phone__phone_number=self.kwargs['pk'])})
        return context

