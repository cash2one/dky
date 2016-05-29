from flask import Blueprint,request,render_template,redirect,url_for,abort,flash
from zoo.utils.access_control import admin_required
from zoo.category.models import Category

category = Blueprint("category", __name__)

@category.route("/new", methods=["POST"])
@admin_required
def new():
    category = Category(name=request.form['name'])
    category.save()
    return redirect(url_for('admin.category_manage'))

@category.route("/delete/<int:category_id>")
@admin_required
def delete(category_id):
    category = Category.query.get(category_id)
    if not category:
        abort(404)
    else:
        category.delete()
        flash("活动删除成功", "success")
        return redirect(url_for("admin.category_manage"))