from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user

from FlaskApp.__init__ import db, login_manager
from FlaskApp.forms import LoginForm, RegistrationForm, SearchForm
from FlaskApp.models import WebUser
from FlaskApp.utility import hprint

view = Blueprint("view", __name__)

@login_manager.user_loader
def load_user(username):
    user = WebUser.query.filter_by(username=username).first()
    return user or current_user


@view.route("/", methods=["GET"])
def render_landing_page():
    query = "CREATE TABLE IF NOT EXISTS web_user(username VARCHAR PRIMARY KEY NOT NULL, preferred_name VARCHAR, password VARCHAR NOT NULL);"
    db.session.execute(query)
    query = "CREATE TABLE IF NOT EXISTS registration(module_code VARCHAR PRIMARY KEY NOT NULL, student_id VARCHAR NOT NULL);"
    db.session.execute(query)
    query = "DELETE FROM registration;"
    db.session.execute(query)
    query = "INSERT INTO registration (module_code, student_id) VALUES ('CS6666', 'A1');"
    db.session.execute(query)
    query = "CREATE TABLE IF NOT EXISTS modules(module_code VARCHAR PRIMARY KEY NOT NULL, name VARCHAR NOT NULL, prof_id VARCHAR NOT NULL, quota INT NOT NULL);"
    db.session.execute(query)
    query = "DELETE FROM modules;"
    db.session.execute(query)
    query = "INSERT INTO modules (module_code, name, prof_id, quota) VALUES ('CS1111', 'Intro to Coding', 'Dr Heng', 600), ('CS2222', 'Basic Coding', 'Dr Eng', 500), ('CS3333', 'Intermediate Coding', 'Dr Ling', 400), ('CS4444', 'Advanced Coding', 'Dr Ping', 300), ('CS5555', 'Master Coding', 'Dr Ming', 200), ('CS6666', 'Godlike Coding', 'Dr Ee', 1);"
    db.session.execute(query)
    db.session.commit()
    return "<h1>CS2102</h1>\
    <h2>Flask App started successfully!</h2>"


@view.route("/search", methods = ["GET", "POST"])
def render_search_page():
    form = SearchForm()
    filters = ['Quota Met', 'Quota Not Met', 'Currently Available', 'Not Available', 'No Prerequisites', 'Has Prerequisites', 'None']
    if form.validate_on_submit():
        hprint("valid")
        search = form.search.data
        filter = request.form.get('filter_list')
        if filter == 'None':
            query = "SELECT module_code, name, prof_id, quota FROM modules WHERE module_code LIKE '%{}%'".format(search)
        elif filter == 'Quota Met':
            query = """
                SELECT m1.module_code, m1.name, m1.prof_id, m1.quota
                FROM modules m1
                LEFT JOIN
                (SELECT m.module_code, COUNT(*) as num
                FROM modules m
                INNER JOIN registration r 
                ON m.module_code = r.module_code
                GROUP BY m.module_code) a
                ON m1.module_code = a.module_code
                WHERE m1.quota <= a.num AND m1.module_code LIKE '%{}%';
            """.format(search)
        elif filter == 'Quota Not Met':
            query = """
                SELECT m1.module_code, m1.name, m1.prof_id, m1.quota
                FROM modules m1
                LEFT JOIN
                (SELECT m.module_code, COUNT(*) as num
                FROM modules m
                INNER JOIN registration r 
                ON m.module_code = r.module_code
                GROUP BY m.module_code) a
                ON m1.module_code = a.module_code
                WHERE (m1.quota > a.num OR a.num IS NULL) AND m1.module_code LIKE '%{}%';
            """.format(search)
        elif filter == 'Currently Available':
            query = """
                SELECT m1.module_code, m1.name, m1.prof_id, m1.quota
                FROM modules m1
                LEFT JOIN
                rounds r
                ON m.start_date >= r.start_date AND m.start_date < r.end_date
                WHERE m.module_code LIKE '%{}%'
            """.format(search)
        elif filter == 'Not Available':
            query = """
                SELECT m1.module_code, m1.name, m1.prof_id, m1.quota
                FROM modules m1
                LEFT JOIN
                rounds r
                ON m.start_date < r.start_date OR m.start_date >= r.end_date
                WHERE m.module_code LIKE '%{}%'
            """.format(search)
        elif filter == 'No Prerequisites':
            query = """
                SELECT m1.module_code, m1.name, m1.prof_id, m1.quota
                FROM modules m1 WHERE m1.module_code LIKE '%{}%' AND m1.module_code NOT IN
                (SELECT m.module_code FROM modules m
                INNER JOIN prerequisites p
                ON m1.module_code = p.module_code)
            """.format(search)
        elif filter == 'Has Prerequisites':
            query = """
                SELECT m1.module_code, m1.name, m1.prof_id, m1.quota
                FROM modules m1
                INNER JOIN prerequisites p
                ON m1.module_code = p.module_code
                WHERE m1.module_code LIKE '%{}%'
            """.format(search)
        result = db.session.execute(query).fetchall()
        return render_template("search.html", form = form, data = result, filters = filters)
    else:
        hprint(form.errors)
    return render_template("search.html", form = form, filters = filters)


@view.route("/registration", methods=["GET", "POST"])
def render_registration_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        preferred_name = form.preferred_name.data
        password = form.password.data
        query = "SELECT * FROM web_user WHERE username = '{}'".format(username)
        exists_user = db.session.execute(query).fetchone()
        if exists_user:
            form.username.errors.append("{} is already in use.".format(username))
        else:
            query = "INSERT INTO web_user(username, preferred_name, password) VALUES ('{}', '{}', '{}')"\
                .format(username, preferred_name, password)
            db.session.execute(query)
            db.session.commit()
            return "You have successfully signed up!"
    return render_template("registration-simple.html", form=form)


@view.route("/login", methods=["GET", "POST"])
def render_login_page():
    form = LoginForm()
    if form.is_submitted():
        hprint("username entered: {}".format(form.username.data))
        hprint("password entered: {}".format(form.password.data))
    if form.validate_on_submit():
        user = WebUser.query.filter_by(username=form.username.data).first()
        password = WebUser.query.filter_by(password=form.password.data).first()
        if user and password:
            # TODO: You may want to verify if password is correct
            login_user(user)
            return redirect(url_for("view.render_privileged_page"))
    return render_template("login.html", form=form)


@view.route("/privileged-page", methods=["GET"])
@login_required
def render_privileged_page():
    return "<h1>Hello, {}!</h1>".format(current_user.preferred_name or current_user.username)
