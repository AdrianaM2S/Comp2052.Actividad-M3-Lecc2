from flask import Flask, render_template
from flask_principal import Principal, Permission, RoleNeed, Identity, identity_changed, AnonymousIdentity

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"

# Flask-Main Configuration
Principal(app)

# Creates permissions based on roles
admin_permission = Permission(RoleNeed('admin'))
user_permission = Permission(RoleNeed('user'))
edit_permission = Permission(RoleNeed('edit'))

# Gives the user the role of admin, user or edit (modify as needed)
current_user = {"role": "user"}

# Identity configuration based on user role
@app.before_request
def set_identity():
    if current_user["role"] == "admin":
        identity_changed.send(app, identity=Identity('admin'))
    elif current_user["role"] == "user":
        identity_changed.send(app, identity=Identity('user'))
    elif current_user["role"] == "edit":
        identity_changed.send(app, identity=Identity('edit'))
    else:
        identity_changed.send(app, identity=AnonymousIdentity())

# Main page accessible to everyone
@app.route('/')
def index():
    return "Welcome to the Main Page!"

# Protected route for administrators
@app.route('/admin')
def admin():
    if current_user["role"] == "admin":
        return "Admin Panel: Access allowed for administrators"
    else:
        return "Access Denied: You don't have the necessary permissions", 403

# Protected route for regular users
@app.route('/user')
def user():
        if current_user["role"] == "user":
            return "User Panel: Access allowed for regular users"
        else:
            return "Access Denied: You don't have the necessary permissions", 403

# Protected route for editors
@app.route('/edit')
def edit():
    if current_user["role"] == "edit":
        return "Edit Page: Access Allowed"
    else:
        return "Access Denied: You don't have the necessary permissions", 403

if __name__ == '__main__':
    app.run(debug=True)