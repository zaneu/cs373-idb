# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Email

from .models import User
from .validators import Unique


class UserSignupForm(Form):
    """
    The user signup form located at /signup
    """
    unique_email = Unique(User,
                          User.email,
                          message=u'Account already exist')

    first_name = TextField('First Name', validators=[DataRequired()])
    last_name = TextField('Last Name', validators=[DataRequired()])
    email = TextField('Email', validators=[DataRequired(), Email(),
                                           unique_email])
    password = PasswordField('Password', validators=[DataRequired()])


class UserLoginForm(Form):
    """
    The user login form located at /login
    """
    email = TextField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.user = None

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            email=self.email.data).first()
        if user is None:
            self.email.errors.append('Unknown email')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password or email')
            return False

        self.user = user
        return True
