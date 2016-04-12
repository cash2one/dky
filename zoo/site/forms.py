from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email


class UserRegisterForm(Form):
    email = StringField('电子邮箱',validators=[DataRequired(), Email()])
    password = PasswordField('密码',validators=[DataRequired()] )
    username = StringField('用户名', validators=[DataRequired()])


class UserLoginForm(Form):
    login = StringField('电子邮箱 / 用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    role = RadioField('登录身份', choices=[(3, '普通用户'),(2, '社长'), (1, '管理员')],coerce=int,default=3)


