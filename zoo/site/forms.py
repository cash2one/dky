from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email


class UserRegisterForm(Form):
    email = StringField('电子邮箱',validators=[DataRequired(), Email()])
    password = PasswordField('密码',validators=[DataRequired()] )
    username = StringField('用户名', validators=[DataRequired()])


class UserLoginForm(Form):
    login = StringField('电子邮箱 / 用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField("记住我", default=True)

