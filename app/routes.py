import random
import string

from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, AddInformationUserForm, CreateTeamForm, JoinTeamForm, \
    CreateEventForm, JoinEventForm , JoinEventCategoryForm
from app.models import User, Team, Event, Category
import re
from sqlalchemy.sql import select

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/add-info-user", methods=["POST", "GET"])
def add_info_user():
    form = AddInformationUserForm()
    if form.validate_on_submit():
        dofbirth = form.birthday_year.data + "-" + form.birthday_month.data + "-" + form.birthday_day.data
        if form.gender.data == "Man":
            genderTemp = "Man"
        else:
            genderTemp = "Woman"
        db.session.query(User).filter_by(id=current_user.id).update(
            {"firstname": form.firstname.data, "lastname": form.lastname.data,
             "telephone": form.number.data, "address": form.address.data,
             "day_of_birth": dofbirth, "gender": genderTemp})
        db.session.commit()
        # user = current_user.firstname
        # print(user)
        # user = current_user.lastname
        # print(user)
        flash('Congratulations, you are add information user!')
        return render_template('successfulRegistration.html', form=form)
    return render_template('addInformationUser.html', form=form)


@app.route("/success", methods=["POST", "GET"])
def successful_registration():
    print('Congratulations, you are add information user!')
    return render_template('successfulRegistration.html')


@app.route("/create-team", methods=["POST", "GET"])
def create_team():
    form = CreateTeamForm()
    if form.validate_on_submit():
        rand_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10));

        team = Team(name=form.name_team.data, key_access=rand_key)
        db.session.add(team)
        db.session.commit()

        user_id = current_user
        user_id.user_team.append(team)
        db.session.add(user_id)
        db.session.commit()

        flash('Congratulations, you are create team "' + form.name_team.data + '", ваш ключ : ' + rand_key)
        return redirect(url_for('index'))
    return render_template('create_team.html', form=form)


@app.route("/team", methods=["POST", "GET"])
def team_menu():
    return render_template('team.html')


@app.route("/team_join", methods=["POST", "GET"])
def team_join():
    form = JoinTeamForm()
    if form.validate_on_submit():
        key_db = db.session.query(Team).filter(Team.key_access == form.access_key.data).first()
        # SXZV2O744X
        if key_db != None:
            user_id = current_user
            user_id.user_team.append(key_db)
            db.session.add(user_id)
            db.session.commit()
            return render_template('team.html')
        else:
            flash('Your key is not correct!')
            return render_template('team_join.html', form=form)
    return render_template('team_join.html', form=form)


@app.route("/event", methods=["POST", "GET"])
def event_menu():
    return render_template('event.html')


@app.route("/create-event", methods=["POST", "GET"])
def create_event():
    form = CreateEventForm()
    if form.validate_on_submit():
        event = Event(name=form.name_event.data, description=form.description.data)
        db.session.add(event)
        db.session.commit()
        if form.category1.data != "":
            category = Category(name=form.category1.data, event_id = event.id)
            db.session.add(category)
            db.session.commit()
        if form.category2.data != "":
            category = Category(name=form.category2.data, event_id = event.id)
            db.session.add(category)
            db.session.commit()
        if form.category3.data != "":
            category = Category(name=form.category3.data, event_id = event.id)
            db.session.add(category)
            db.session.commit()
        if form.category4.data != "":
            category = Category(name=form.category4.data, event_id = event.id)
            db.session.add(category)
            db.session.commit()
        if form.category5.data != "":
            category = Category(name=form.category5.data, event_id = event.id)
            db.session.add(category)
            db.session.commit()
        return render_template('event.html', form=form)
    return render_template('create_event.html', form=form)


@app.route("/event_join", methods=["POST", "GET"])
def event_join():
    event_groups = select([Event])
    result = db.session.execute(event_groups)
    active_event_list = []
    active_event_list.append((0, ""))
    for row in result:
        active_event_list.append((row[0].__str__(), row[1]))

    form = JoinEventForm()
    form.active_event.choices = active_event_list

    if form.validate_on_submit():
        return render_template('join_event_category.html',form = form)
    return render_template('join_event.html', form=form)

@app.route("/join_event_category", methods=["POST", "GET"])
def join_event_category():
    form = JoinEventCategoryForm()
    print(form.active_event.choices[int(form.active_event.data)][1])
    if form.validate_on_submit():

        print(form.active_event.choices[int(form.active_event.data)][1])
        #db.session.query(Team).filter_by(id=current_user.id).update(
         #   {"event_id": form.active_event.data, "category_id": form.category.data })
        #db.session.commit()
        return render_template('event.html', form=form)
    return render_template('join_event_category.html', form=form)
