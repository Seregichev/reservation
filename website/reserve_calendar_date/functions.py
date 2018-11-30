# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from random import randint

def reservation_objects_create(Object, **kwargs):
    created = None
    errors = None
    number = randint(1, 999999)
    try:
        created = Object.objects.create(number=number, **kwargs)
    except IntegrityError:
        e = 0
        created = None
        while not created or e > 100:
            number = randint(1, 999999)
            if not Object.objects.filter(number=number).exists():
                created = Object.objects.create(number=number, **kwargs)
    except ValidationError as e:
            errors = e.message

    return created, errors