from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from forms import LoginForm, SearchForm
from models import ANY_ENTRY_REQUIREMENT_ID, ANY_VENUE_TYPE_ID, EntryRequirement, User, Venue, VenueType


def create_routes(app):

    bcrypt = Bcrypt(app)

    @app.get("/")
    def home():
        form = SearchForm(request.args)
        venue_type_choices = [(vt.id, vt.name)
                              for vt in VenueType.query.all()]
        venue_type_choices.insert(0, (ANY_VENUE_TYPE_ID, 'Place to visit'))
        form.venue_type.choices = venue_type_choices

        entry_requirement_choices = [
            (er.id, er.name) for er in EntryRequirement.query.all()]
        entry_requirement_choices.insert(
            ANY_ENTRY_REQUIREMENT_ID, (0, 'Entry requirement'))
        form.entry_requirement.choices = entry_requirement_choices

        venues = Venue.get_venues_in_vicinity(
            search=form.search.data, venue_type_id=form.venue_type.data, entry_requirement_id=form.entry_requirement.data, lat=53, lng=12)
        return render_template('search.html', title='Search', form=form, venues=venues)

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
