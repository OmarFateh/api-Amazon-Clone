# -*- coding: utf-8 -*-
from decimal import Decimal


def arabic_slugify(string):
    """Slugify a given string."""
    string = string.replace(" ", "-")
    string = string.replace(",", "-")
    string = string.replace("&", "-")
    string = string.replace("(", "-")
    string = string.replace(")", "")
    string = string.replace("؟", "")
    string = string.replace("!", "")
    return string.lower()


def unique_slug_generator(instance, new_slug=None):
    """Generate a unique slug for a given instance."""
    # check if the given arguments have a value of new slug
    # if yes, assign the given value to the slug field. 
    if new_slug is not None:
        slug = new_slug
    # if not, generate a slug using arabic slugify function.
    else:
        slug = arabic_slugify(instance.name)
    # get the instance class. 
    Klass = instance.__class__
    # check if there's any item with the same slug.
    qs = Klass.objects.filter(slug=slug).order_by('-id') 
    if qs.count() == 1 and qs.first().id == instance.id: 
        return slug   
    # if yes, generate a new slug of a random string and return recursive function with the new slug.
    elif qs.exists():
        new_slug = f'{slug}-{qs.first().id}'
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug 


def datetime_to_string(datetime):
    """Take a datetime object and return a nicely formatted string, eg: Aug 06, 2020 at 07:21 PM."""
    return datetime.strftime("%b %d, %Y at %I:%M %p")


def compare_max_discount_price(max_price=None, discount_price=None, is_update=None, instance=None):
    """Take max & disscount price and compare between them."""
    if max_price and discount_price and discount_price > Decimal(max_price):
        return True
    if is_update:
        if max_price and instance.discount_price and instance.discount_price > Decimal(max_price):
            return True
        if discount_price and instance.max_price and discount_price > instance.max_price:
            return True
    return False