import datetime

from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user

from FlaskApp.__init__ import db, login_manager
from FlaskApp.forms import LoginForm, RegistrationForm, SearchForm, DeleteModuleForm, AddModuleForm, StudentRecordForm, ManualAcceptForm
from FlaskApp.models import web_users

from FlaskApp.utility import hprint

view = Blueprint("view", __name__)

@login_manager.user_loader
def load_user(user_id):
    user = web_users.query.filter_by(user_id=user_id).first()
    return user or current_user


@view.route("/", methods=["GET"])
def render_landing_page():
    return redirect("/registration")

@view.route("/prerequisites", methods = ["GET", "POST"])
def render_prerequisite_page():
    query = "SELECT * FROM prerequisites;"
    result = db.session.execute(query)
    return render_template("prerequisite.html", data = result)

@view.route("/search", methods = ["GET", "POST"])
def render_search_page():
    form = SearchForm()
    filters = ['Quota Met', 'Quota Not Met', 'Currently Available', 'Not Available', 'No Prerequisites', 'Has Prerequisites', 'None']
    if form.validate_on_submit():
        date = datetime.datetime.now().date()
        search = form.search.data
        filter = request.form.get('filter_list')
        if filter == 'None':
            query = """
                SELECT m.module_code, m.module_name, m.quota, w.preferred_name
                FROM modules m
                LEFT JOIN supervises s
                ON m.module_code = s.module_code
                LEFT JOIN web_users w
                ON s.prof_id = w.user_id
                WHERE m.module_code LIKE '%{}%'
            """.format(search)
        elif filter == 'Quota Met':
            query = """
                SELECT m1.module_code, m1.module_name, w.preferred_name, m1.quota
                FROM modules m1
                LEFT JOIN
                (SELECT m.module_code, COUNT(*) as num
                FROM modules m
                INNER JOIN registration r 
                ON m.module_code = r.module_code
                GROUP BY m.module_code) a
                ON m1.module_code = a.module_code
                LEFT JOIN supervises s
                ON m1.module_code = s.module_code
                LEFT JOIN web_users w
                ON s.prof_id = w.user_id
                WHERE m1.quota <= a.num AND m1.module_code LIKE '%CS%';
            """.format(search)
        elif filter == 'Quota Not Met':
            query = """
                SELECT m1.module_code, m1.module_name, w.preferred_name, m1.quota
                FROM modules m1
                LEFT JOIN
                (SELECT m.module_code, COUNT(*) as num
                FROM modules m
                INNER JOIN registration r 
                ON m.module_code = r.module_code
                GROUP BY m.module_code) a
                ON m1.module_code = a.module_code
                LEFT JOIN supervises s
                ON m1.module_code = s.module_code
                LEFT JOIN web_users w
                ON s.prof_id = w.user_id
                WHERE (m1.quota > a.num OR a.num IS NULL) AND m1.module_code LIKE '%CS%';
            """.format(search)
        elif filter == 'Currently Available':
            query = """
                SELECT m1.module_code, m1.module_name, m1.quota, w.preferred_name
                FROM modules m1
                LEFT JOIN available a
                ON m1.module_code = a.module_code
                LEFT JOIN rounds r
                ON a.start_date = r.start_date AND r.start_date <= '{}' AND r.end_date > '{}'
                LEFT JOIN supervises s
                ON m1.module_code = s.module_code
                LEFT JOIN web_users w
                ON s.prof_id = w.user_id
                WHERE r.start_date IS NOT NULL AND r.end_date IS NOT NULL AND m1.module_code LIKE '%{}%';
            """.format(date, date, search)
        elif filter == 'Not Available':
            query = """
                SELECT m1.module_code, m1.module_name, m1.quota, w.preferred_name
                FROM modules m1
                LEFT JOIN supervises s
                ON m1.module_code = s.module_code
                LEFT JOIN web_users w
                ON s.prof_id = w.user_id
                WHERE m1.module_code LIKE '%{}%'
                AND m1.module_code NOT IN
                (SELECT m2.module_code
                FROM modules m2
                LEFT JOIN available a1
                ON m2.module_code = a1.module_code
                LEFT JOIN rounds r1
                ON a1.start_date = r1.start_date AND r1.start_date <= '{}' AND r1.end_date > '{}'
                WHERE r1.start_date IS NOT NULL AND r1.end_date IS NOT NULL AND m2.module_code LIKE '%{}%');
            """.format(search, date, date, search)
        elif filter == 'No Prerequisites':
            query = """
                SELECT m1.module_code, m1.module_name, m1.quota, w.preferred_name
                FROM modules m1
                LEFT JOIN supervises s
                ON m1.module_code = s.module_code
                LEFT JOIN web_users w
                ON s.prof_id = w.user_id
                WHERE m1.module_code LIKE '%{}%' AND m1.module_code NOT IN
                (SELECT m.module_code FROM modules m
                INNER JOIN prerequisites p
                ON m1.module_code = p.module_code)
            """.format(search)
        elif filter == 'Has Prerequisites':
            query = """
                SELECT m1.module_code, m1.module_name, m1.quota, w.preferred_name
                FROM modules m1
                LEFT JOIN supervises s
                ON m1.module_code = s.module_code
                LEFT JOIN web_users w
                ON s.prof_id = w.user_id
                WHERE m1.module_code LIKE '%{}%' AND m1.module_code IN
                (SELECT m.module_code FROM modules m
                INNER JOIN prerequisites p
                ON m1.module_code = p.module_code)
            """.format(search)
        result = db.session.execute(query).fetchall()
        return render_template("search.html", form = form, data = result, filters = filters)
    return render_template("search.html", form = form, filters = filters)

@view.route("/prof", methods = ["GET", "POST"])
#@roles_required('Professor')
def render_prof_page():
    query1 = """
        SELECT m.module_code, m.module_name, w.preferred_name, m.quota
        FROM modules m
        INNER JOIN supervises s
        ON m.module_code = s.module_code
        INNER JOIN web_users w
        ON s.prof_id = w.user_id
        WHERE s.prof_id = '{}'
    """.format(current_user.user_id)
    query2 = """
        SELECT m.module_code, m.module_name, w.preferred_name, m.quota
        FROM modules m
        INNER JOIN lecturing l
        ON m.module_code = l.module_code
        INNER JOIN web_users w
        ON l.prof_id = w.user_id
        WHERE l.prof_id = '{}'
    """.format(current_user.user_id)
    result1 = db.session.execute(query1).fetchall()
    result2 = db.session.execute(query2).fetchall()
    return render_template("prof.html", data1 = result1, data2 = result2)

@view.route("/stulist", methods = ["GET", "POST"])
#@roles_required('Professor')
def render_stulist_page():
    form = SearchForm()
    if form.validate_on_submit():
        date = datetime.datetime.now()
        search = form.search.data
        query = """
            SELECT m.module_code, m.module_name, w.preferred_name 
            FROM modules m
            INNER JOIN takes t
            ON m.module_code = t.module_code
            INNER JOIN web_users w
            ON t.student_id = w.user_id
            WHERE m.module_code LIKE '%{}%'
        """.format(search)
        result = db.session.execute(query).fetchall()
        return render_template("stulist.html", form = form, data = result)
    else:
        hprint(form.errors)
    return render_template("stulist.html", form = form)


@view.route("/registration", methods=["GET", "POST"])
def render_registration_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user_id = form.user_id.data
        preferred_name = form.preferred_name.data
        password = form.password.data
        query = "SELECT * FROM web_users WHERE user_id = '{}'".format(user_id)
        exists_user = db.session.execute(query).fetchone()
        if exists_user:
            form.user_id.errors.append("{} is already in use.".format(user_id))
        else:
            query = "INSERT INTO web_users(user_id, preferred_name, password) VALUES ('{}', '{}', '{}')"\
                .format(user_id, preferred_name, password)
            db.session.execute(query)
            db.session.commit()
            return "You have successfully signed up!"
    return render_template("registration-simple.html", form=form)


@view.route("/login", methods=["GET", "POST"])
def render_login_page():
    form = LoginForm()
    if form.is_submitted():
        print("username entered: {}".format(form.user_id.data))
        print("password entered: {}".format(form.password.data))
    if form.validate_on_submit():
        user = web_users.query.filter_by(user_id=form.user_id.data).first()
        password = web_users.query.filter_by(password=form.password.data).first()
        if user and password:
            login_user(user)
            return redirect("/userhome")
    return render_template("login_test.html", form=form)


@view.route("/deletemodule", methods=["GET", "POST"])
#@roles_required('Admin')
def render_delete_module_page():
    form = DeleteModuleForm()
    if form.validate_on_submit():
        module_code = form.module_code.data
        module_name = form.module_name.data
        query = "DELETE FROM modules WHERE module_code='{}' OR module_name='{}'"\
                .format(module_code, module_name)
        db.session.execute(query)
        db.session.commit()
    return render_template("deletemodule.html", form=form)


@view.route("/addmodule", methods=["GET", "POST"])
#@roles_required('Admin')
def render_add_module_page():
    form = AddModuleForm()
    if form.validate_on_submit():
        module_code = form.module_code.data
        module_name = form.module_name.data
        quota = form.quota.data
        supervisor = form.supervisor.data
        prerequisite = form.prerequisite.data.replace(',', ' ')
        prerequisite = prerequisite.split()
        query = "INSERT INTO modules(module_code, module_name, quota) VALUES ('{}', '{}', '{}')"\
                .format(module_code, module_name, quota)
        db.session.execute(query)
        query = "INSERT INTO supervises(prof_id, module_code) VALUES ('{}', '{}')"\
                .format(supervisor, module_code)
        db.session.execute(query)
        for module in prerequisite:
            query = "INSERT INTO prerequisites(module_code, prerequisite) VALUES ('{}', '{}')"\
                .format(module_code, module)
            db.session.execute(query)
        db.session.commit()
    return render_template("addmodule.html", form=form)

@view.route("/studentrecord", methods = ["GET", "POST"])
#@roles_required('Student')
def render_student_page():
    form = StudentRecordForm()
    filters = ['Modules Currently Taking', 'Modules Taken in Past Semesters', 'Modules Pending Approval']
    if form.validate_on_submit():
        module_code = form.module_code.data
        filter = request.form.get('filter_list')
        if filter == 'Modules Currently Taking':
            query = "SELECT * FROM takes WHERE student_id = '{}' AND module_code LIKE '%{}%';".format(current_user.user_id, module_code)
        elif filter == 'Modules Taken in Past Semesters':
            query = "SELECT * FROM took WHERE student_id = '{}' AND module_code LIKE '%{}%';".format(current_user.user_id, module_code)
        elif filter == 'Modules Pending Approval':
            query = "SELECT * FROM registration WHERE student_id = '{}' AND module_code LIKE '%{}%';".format(current_user.user_id, module_code)
        result = db.session.execute(query).fetchall()
        return render_template("studentrecord.html", form = form, data = result, filters = filters)

    return render_template("studentrecord.html", form = form, filters = filters)

@view.route("/manual", methods=["GET", "POST"])
#@roles_required('Admin')
def render_manual_accept_page():
    form = ManualAcceptForm()
    if form.validate_on_submit():
        module_code = form.module_code.data
        student_id = form.student_id.data
        query = "INSERT INTO takes(student_id, module_code) VALUES ('{}', '{}')"\
                .format(student_id, module_code)
        db.session.execute(query)
        query = """select prerequisite from prerequisites where prerequisites.module_code='{}'
                Except
                select module_code from took where took.student_id='{}';"""\
                .format(module_code, student_id)
        result = db.session.execute(query)
        db.session.commit()
        return render_template("manual.html", form = form, data = result)
    return render_template("manual.html", form = form)
        

    
@view.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return render_template("logoutpage.html")


@view.route("/userhome", methods=["GET"])
@login_required
def userhome():
    return render_template('userhome.html')
