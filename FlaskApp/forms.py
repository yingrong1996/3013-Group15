from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, ValidationError, Optional


def is_valid_name(form, field):
    if not all(map(lambda char: char.isalpha(), field.data)):
        raise ValidationError('This field should only contain alphabets')


def agrees_terms_and_conditions(form, field):
    if not field.data:
        raise ValidationError('You must agree to the terms and conditions to sign up')


class RegistrationForm(FlaskForm):
    user_id = StringField(
        label='User ID',
        validators=[InputRequired()],
        render_kw={'placeholder': 'user_id'}
    )
    name = StringField(
        label='Name',
        validators=[InputRequired(), is_valid_name],
        render_kw={'placeholder': 'Name'}
    )
    password = PasswordField(
        label='Password',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Password'}
    )


class LoginForm(FlaskForm):
    user_id = StringField(
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
    
class UpdateForm(FlaskForm):
    new = StringField(
        label='new',
        validators=[InputRequired()],
        render_kw={'placeholder': 'new'}
    )
    old = StringField(
        label='old',
        validators=[InputRequired()],
        render_kw={'placeholder': 'old'}
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
    supervisor = StringField(
        label='Supervisor',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Prof ID'}
    )
    prerequisite = StringField(
        label='prerequisite',
        validators=[Optional()],
        render_kw={'placeholder': 'prerequisite_code1, prerequisite_code2...'}
    )


class ManualAcceptForm(FlaskForm):
    student_id = StringField(
        label='Student ID',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Student ID'}
    )
    module_code = StringField(
        label='Module code',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Module code'}
    )
      
class StudentRecordForm(FlaskForm):
    module_code = StringField(
        label='Module code',
        validators=[Optional()],
        render_kw={'placeholder': 'Module code'}
    )

class StudentModuleForm(FlaskForm):
    module_code = StringField(
        label='Module code',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Module code'}
    )
