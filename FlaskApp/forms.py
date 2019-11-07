from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, ValidationError


def is_valid_name(form, field):
    if not all(map(lambda char: char.isalpha(), field.data)):
        raise ValidationError('This field should only contain alphabets')


def agrees_terms_and_conditions(form, field):
    if not field.data:
        raise ValidationError('You must agree to the terms and conditions to sign up')


class RegistrationForm(FlaskForm):
    username = StringField(
        label='Name',
        validators=[InputRequired(), is_valid_name],
        render_kw={'placeholder': 'Name'}
    )
    preferred_name = StringField(
        label='Preferred name',
        validators=[is_valid_name],
        render_kw={'placeholder': 'Preferred name'}
    )
    password = PasswordField(
        label='Password',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Password'}
    )


class LoginForm(FlaskForm):
    username = StringField(
        label='Name',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Name', 'class': 'input100'}
    )
    password = PasswordField(
        label='Password',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Password', 'class': 'input100'}
    )


class SearchForm(FlaskForm):
    search = StringField(
        label='Search',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Search'}
    )


class AddModuleForm(FlaskForm):
    module_code = StringField(
        label='Module code',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Module code'}
    )
    module_name = StringField(
        label='Module name',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Module name'}
    )
    quota = StringField(
        label='Quota',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Quota'}
    )

class DeleteModuleForm(FlaskForm):
    module_code = StringField(
        label='Module code',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Module code'}
    )
    module_name = StringField(
        label='Module name',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Module name'}
    )

##class UpdateModuleForm(FlaskForm):
##    module_code = StringField(
##        label='Module code',
##        validators=[InputRequired()],
##        render_kw={'placeholder': 'Module code'}
##    )
##    module_name = StringField(
##        label='Module name',
##        validators=[InputRequired()],
##        render_kw={'placeholder': 'Module name'}
##    )
##    quota = StringField(
##        label='Quota',
##        validators=[InputRequired()],
##        render_kw={'placeholder': 'Quota'}
##    )
