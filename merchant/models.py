from django.db import models

from useradmin.models import BaseTimestamp


class Merchant(BaseTimestamp):
    """Merchant model."""
    user = models.OneToOneField("accounts.user", related_name='merchant', on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    gst_detail = models.CharField(max_length=255)

    def __str__ (self):
        # Return merchant's email and company name.
        return f"{self.user.email} | {self.company_name}"    