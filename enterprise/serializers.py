from random import choice
from rest_framework import serializers
from .models import Company, Customer, CustomerPhone, OperatorNumber, Plan, Subscription
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import timedelta


def get_companies():
    try:
        choices = list(Company.objects.all().values_list("id", "name"))
    except Exception:
        choices = []
    return choices

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name", "company_code"]
        model = Company

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["id", "name"]
        model = Customer

    def create(self, validated_data):
        customer = Customer.objects.create(**validated_data)
        company = choice(Company.objects.all())
        phone_number = CustomerPhone(
            customer=customer,
            phone=company.get_a_phone_number(),
            is_primary=True,
        )
        phone_number.save()
        return customer

class OperatorNumberSerializer(serializers.ModelSerializer):
    company = CompanySerializer(many=False)

    class Meta:
        fields = ["phone_number", "company"]
        model = OperatorNumber

class CustomerNumberSerializer(serializers.ModelSerializer):
    phone = OperatorNumberSerializer(many=False)

    class Meta:
        fields = ["phone"]
        model = CustomerPhone

class CustomerDetailSerializer(serializers.ModelSerializer):
    my_phone = serializers.SerializerMethodField()
    new_phone = serializers.BooleanField(default=False, write_only=True)
    company = serializers.ChoiceField(choices=get_companies(), write_only=True)

    class Meta:
        fields = ["name", "my_phone", "new_phone", "company"]
        model = Customer

    def get_my_phone(self, obj):
        return CustomerNumberSerializer(obj.cells_own.all(), many=True).data

    def update(self, instance, validated_data):
        new_phone = validated_data.pop("new_phone", False)
        company = get_object_or_404(
            Company,
            id=validated_data.pop("company", None)
        )
        if new_phone and company:
            company.get_a_phone_number_for_customer(instance)
        return super().update(instance, validated_data)

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["name", "price", "month", "can_cancel"]
        model = Plan

class SubscriptionDetailSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(many=False)
    phone = CustomerNumberSerializer(many=False)

    class Meta:
        model = Subscription
        fields = ["plan", "phone", "from_active_date", "end_subs_date", "is_active"]
        read_only_fields = ("phone", "from_active_date", "end_subs_date", "is_active")

class SubscriptionSerializer(serializers.ModelSerializer):
    cancel = serializers.BooleanField(default=False, write_only=True)

    class Meta:
        fields = ["plan", "cancel"]
        model = Subscription

    def create(self, validated_data):
        Subscription.objects.filter(
            phone__phone__company__id=self.context["cp"].phone.company.id,
            end_subs_date__lte=now()
        ).update(is_active=False)

        is_exists = Subscription.objects.filter(
            phone__phone__company__id=self.context["cp"].phone.company.id,
            is_active=True
        ).exists()

        if is_exists:
            raise ValidationError(
                _('%(value)s is already subscribed.'),
                params={'value': self.context["cp"].phone.phone_number},
            )
        validated_data["from_active_date"] = now()
        validated_data["end_subs_date"] = now() + timedelta(days=validated_data["plan"].month*30)
        validated_data["phone"] = self.context["cp"]
        validated_data["is_active"] = True
        validated_data.pop("cancel", None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if not validated_data.pop("cancel", None):
            return instance

        if not instance.is_active:
            raise ValidationError(
                _('%(value)s is not active subscribed.'),
                params={'value': instance.phone.phone_number},
            )

        if instance.plan.can_cancel:
            raise ValidationError(
                _('%(value)s Plan can not be cancelled..'),
                params={'value': instance.phone.phone_number},
            )

        if instance.end_subs_date <= now().date():
            if instance.is_active:
                instance.is_active = False
                instance.save()

            raise ValidationError(
                _('%(value)s Subscription is already over.'),
                params={'value': instance.phone.phone_number},
            )

        if instance.plan.id != validated_data["plan"].id:
            raise ValidationError(
                _('%(value)s is Not a valid plan selected.'),
                params={'value': instance.phone.phone_number},
            )

        validated_data.pop("plan", None)
        validated_data["is_active"] = False
        return super().update(instance, validated_data)
