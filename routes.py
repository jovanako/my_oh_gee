import os
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_required, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from forms import LoginForm, SearchForm, VenueForm
from models import ANY_ENTRY_REQUIREMENT_ID, ANY_VENUE_TYPE_ID, EntryRequirement, User, Venue, VenueType
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from PIL import Image


def create_routes(app):

    bcrypt = Bcrypt(app)

    @app.get("/")
    def home():
        form = SearchForm(request.args)
        form.venue_type.choices = get_venue_type_choices()
        form.entry_requirement.choices = get_entry_requirements_choices()

        venues = Venue.get_venues_in_vicinity(
            search=form.search.data, venue_type_id=form.venue_type.data, entry_requirement_id=form.entry_requirement.data, lat=53, lng=12)
        venues = [venue.to_dict() for venue in venues]
        return render_template('search.html', title='Search', form=form, venues=venues, GOOGLE_API_KEY=os.environ.get('GOOGLE_API_KEY'))

    @app.route("/venue", methods=['GET', 'POST'])
    @login_required
    def venue():
        form = VenueForm(CombinedMultiDict((request.files, request.form)))
        form.venue_type.choices = get_venue_type_choices()
        form.entry_requirement.choices = get_entry_requirements_choices()

        if form.is_submitted():
            venue = Venue(
                name=form.name.data,
                geom=f'SRID=4326;POINT({form.latitude.data} {form.longitude.data})',
                address=form.address.data,
                requirement=EntryRequirement.query.get(
                    form.entry_requirement.data),
                venue_type=VenueType.query.get(form.venue_type.data),
                webpage=form.web_page.data,
                image_path=save_image(form.image.data),
                creator=current_user)

            Venue.save(venue)
            return redirect(url_for('home'))

        return render_template('venue.html', form=form)

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
        return redirect(url_for('home'))

    def get_venue_type_choices():
        venue_type_choices = [(vt.id, vt.name)
                              for vt in VenueType.query.all()]
        venue_type_choices.insert(0, (ANY_VENUE_TYPE_ID, 'Any venue type'))
        return venue_type_choices

    def get_entry_requirements_choices():
        entry_requirement_choices = [
            (er.id, er.name) for er in EntryRequirement.query.all()]
        entry_requirement_choices.insert(
            ANY_ENTRY_REQUIREMENT_ID, (0, 'Any entry requirement'))
        return entry_requirement_choices

    def save_image(image):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.root_path, 'static/venue_pics', filename)
        output_size = (125, 125)

        i = Image.open(image)
        i.thumbnail(output_size)
        i.save(image_path)

        return filename
