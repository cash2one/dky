from flask import Blueprint,flash,request,render_template,redirect,url_for
from .forms import UserRegisterForm, UserLoginForm
from flask_login import login_user, logout_user, login_required
from zoo.user.models import User
from zoo.group.models import Group


site = Blueprint("site", __name__)


@site.route("/")
@login_required
def index():
    users = User.query.limit(15).all();
    groups = Group.query.limit(15).all();
    return render_template("site/index.html", users=users, groups=groups)


@site.route("/register", methods=['GET','POST'])
def register():
    form = UserRegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(email=form.email.data, password=form.password.data, username=form.username.data)
            user.set_avatar_auto()
            user.save()
            flash("注册成功，请登录")
        return redirect(url_for('site.login'))
    else:
        return render_template("site/register.html", form=form)


@site.route("/login", methods=['GET', 'POST'])
def login():
    form = UserLoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            print(form.remember_me)
            user, authenticated = User.authenticate(form.login.data, form.password.data)
            if user and authenticated:
                login_user(user, remember=form.remember_me.data)
                flash('登录成功，'+ user.username +"欢迎回来！", 'info')
                return redirect(url_for('site.index'))
            else:
                error = '登录失败，邮箱或密码错误。'
                return render_template("site/login.html", error=error, form=form)
    else:
        return render_template("site/login.html", form=form)


@site.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('site.login'))