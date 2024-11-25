

from flask import render_template, url_for, flash, redirect, request, Blueprint,abort
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import func, update

admin_bp=Blueprint('admin',__name__,template_folder='templates',static_folder='static')



@admin_bp.before_request
def before_request():
    if current_user.is_authenticated and current_user.email=="admin@qq.com":
        print("admin login")
    else:
        abort(403)





@admin_bp.route("/")
@admin_bp.route("/index")
def index():
    return "this is index"




