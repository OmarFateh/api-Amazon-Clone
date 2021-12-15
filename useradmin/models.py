from django.db import models


class BaseTimestamp(models.Model):
    """Timestamp abstract model."""
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class UserAdmin(BaseTimestamp):
    """User Admin model."""
    user = models.OneToOneField("accounts.user", on_delete=models.CASCADE)

    def __str__ (self):
        # Return admin's email.
        return self.user.email    