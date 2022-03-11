from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from forms import LoginForm
from models import User


def create_routes(app):

    bcrypt = Bcrypt(app)

    @app.get("/")
    def home():
        return "Hellooo!"

    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        return render_template('login.html', title='Login', form=form)

    @app.get("/logout")
    def logout():
        logout_user()
        redirect(url_for('/'))
