from unwrap.user.routes import user_bp
from unwrap.admin.routes import admin_bp
from unwrap import app


app.register_blueprint(user_bp)
app.register_blueprint(admin_bp,url_prefix="/admin")
if __name__ == '__main__':
    app.run(debug=True)