from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required,Length

class LoginForm(FlaskForm):
    username = StringField('Username:',validators=[Required(),Length(1,64)])
    password = PasswordField('Password:',validators=[Required()])
