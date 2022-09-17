from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

import ipdb

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(100)]
            )  # values like 0% - 100%
    can_be_used_count = models.PositiveIntegerField()
    active = models.BooleanField()

    def validate_coupon_used_count(self):
        ipdb.set_trace()
        if self.validate_coupon() == True:
            self.can_be_used_count -= 1

    def deactivate_coupon(self):
        self.active = False

    def validate_coupon(self):
        coupon = self
        if coupon.can_be_used_count == 0:
            coupon.deactivate_coupon()
        return True

    def __str__(self):
        return self.code

