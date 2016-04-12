from flask import Blueprint,flash,request,render_template,redirect,url_for
from .forms import UserRegisterForm, UserLoginForm
from flask_login import login_user, logout_user, login_required
from zoo.user.models import User
from zoo.group.models import Group
from zoo.configs.default import DefaultConfig


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
    form = UserLoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            if form.role.data == 3:
                user, authenticated = User.authenticate(form.login.data, form.password.data, form.role.data)
                if user and authenticated:
                    login_user(user, remember=True)
                    flash('登录成功，'+ user.username +"欢迎回来！", 'info')
                    return redirect(url_for('site.index'))
                else:
                    error = '登录失败，邮箱/用户名或密码错误。'
                    return render_template("site/login.html", error=error, form=form)
            elif form.role.data == 2:
                user, authenticated = User.authenticate(form.login.data, form.password.data, form.role.data)
                if user and authenticated:
                    if user.role == 2:
                        login_user(user, remember=True)
                        flash('社长身份登录成功，'+ user.username +"欢迎回来！", 'info')
                        return redirect(url_for('site.index'))
                    elif user.role == 3:
                        return render_template("group/new.html")
                    else:
                        flash('作为管理员，您不能以社长身份登陆', 'info')
                        return redirect(url_for('site.login'))
                else:
                    error = '登录失败，邮箱/用户名或密码错误。'
                    return render_template("site/login.html", error=error, form=form)
            elif form.role.data == 1:
                user, authenticated = User.authenticate(form.login.data, form.password.data, form.role.data)
                if user and authenticated:
                    if user.role == 1:
                        login_user(user, remember=True)
                        flash('管理员登陆成功', 'info')
                        return render_template("admin/index.html")
                    else:
                        flash('你不是管理员', 'info')
                        return redirect(url_for('site.login'))
                else:
                    error = '管理员登录失败，邮箱/用户名或密码错误。'
                    return render_template("site/login.html", error=error, form=form)
        else:
            print(form.errors)
            return redirect(url_for('site.login'))
    else:
        return render_template("site/login.html", form=form)


@site.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('site.login'))