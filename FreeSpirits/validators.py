# -*- coding: utf-8 -*-

from wtforms.validators import ValidationError


class Unique(object):
    """
    A custom validator to check if the model already has a duplicate field
    """
    def __init__(self, model, field, message=u'This element already exists.'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)
