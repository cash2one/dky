from flask_wtf import Form
from wtforms import StringField, BooleanField,SelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired


class NewGroupForm(Form):
    name = StringField('社团名称', validators=[DataRequired()])
    description = StringField('社团描述', widget=TextArea())
    category = SelectField('社团分类', coerce=int)