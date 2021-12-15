from django.db import models


class TitleCharField(models.CharField):
    """Custom model field to title the value of CharField."""
    def __init__(self, *args, **kwargs):
        self.is_title = kwargs.pop('title', False)
        super(TitleCharField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        value = super(TitleCharField, self).get_prep_value(value)
        if self.is_title:
            return value.title()
        return value