from django.db import models
import random
# Create your models here.


class CitizenCard(models.Model):
    card_number = models.CharField(max_length=15, unique=True, blank=True)
    name = models.CharField(max_length=100)
    dob = models.DateField(default="2000-01-01")
    address = models.CharField(max_length=200)
    gender = models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=10)
    phone_number = models.CharField(max_length=15)
    state = models.CharField(max_length=50,default="Karnataka")
    city = models.CharField(max_length=50, default="Unknown")
    pincode = models.CharField(max_length=10,default="000000")
    income = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_widow = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    age = models.IntegerField(default=0)    

    def save(self, *args, **kwargs):
        if not self.card_number:
            self.card_number = self.generate_card_number()
        super().save(*args, **kwargs)

    def generate_card_number(self):
        return "IND" + str(random.randint(1000000000, 9999999999))

    def __str__(self):
        return self.name