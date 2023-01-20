from django.db import models
from django.db.models import Max
from .utils import validate_code

class Company(models.Model):
    name = models.CharField(max_length=120)
    company_code = models.PositiveSmallIntegerField(validators=[validate_code])

    def get_a_phone_number(self):
        max_number = OperatorNumber.objects.filter(
            company__id=self.id
        ).aggregate(
            Max("phone_number")
        )["phone_number__max"]
        # bangladesh standard phone number
        if not max_number:
            phone_number = "{country_code}{company_code}{max_value}".format(
                country_code="880",
                company_code=self.company_code,
                max_value="00000000",
            )
        else:
            phone_number = max_number + 1
        operator_number = OperatorNumber(phone_number=phone_number, company=self)
        operator_number.save()
        return operator_number

    def get_a_phone_number_for_customer(self, customer):
        cp = CustomerPhone(
            customer=customer,
            phone=self.get_a_phone_number(),
        )
        cp.save()
        return cp


class Plan(models.Model):
    name = models.CharField(max_length=120)
    price = models.PositiveIntegerField()
    month = models.IntegerField(default=1)
    can_cancel = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class OperatorNumber(models.Model):
    phone_number = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        unique_together = [["phone_number", "company"],]

class Customer(models.Model):
    name = models.CharField(max_length=120)

class CustomerPhone(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cells_own")
    phone = models.OneToOneField(OperatorNumber, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

class Subscription(models.Model):
    phone = models.ForeignKey(CustomerPhone, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    from_active_date = models.DateField()
    end_subs_date = models.DateField()
    is_active = models.BooleanField(default=False)