import datetime

from flask import Blueprint, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user

from FlaskApp.__init__ import db, login_manager
from FlaskApp.forms import LoginForm, RegistrationForm, SearchForm, DeleteModuleForm, AddModuleForm, StudentForm, ManualAcceptForm
from FlaskApp.models import web_users

from FlaskApp.utility import hprint

view = Blueprint("view", __name__)

@login_manager.user_loader
def load_user(user_id):
    user = web_users.query.filter_by(user_id=user_id).first()
    return user or current_user


@view.route("/", methods=["GET"])
def render_landing_page():
    query = """CREATE TABLE IF NOT EXISTS web_users(
            user_id VARCHAR PRIMARY KEY, 
            preferred_name VARCHAR, 
            password VARCHAR NOT NULL);"""
    db.session.execute(query)
    query = "DELETE FROM web_users;"
    db.session.execute(query)
    query = """INSERT INTO web_users(user_id, preferred_name, password) VALUES
    ('A23456789', 'Ali', 'adminpassword'),
    ('S34567890', 'Bob', 'studentpassword'),
    ('P45678901', 'Charlie', 'profpassword'),
    ('S37132455', 'Hoyt', 'gWg7qwSJ2S'),
    ('S49083365', 'Alfonso', 'Xq1l1FxphUdK'),
    ('S69940317', 'Audrey', '9UeGk6Eo6s'),
    ('S10702156', 'Kadeem', 'TH4ZShsSQyk'),
    ('S10797599', 'Addison', 'VOoQPnLk'),
    ('S29260258', 'Alan', 'DixPKZrX'),
    ('S77113792', 'Chloe', 'mX5SXrRebF'),
    ('S45831058', 'Tanisha', 'HUHm9WtawRLb'),
    ('S46268848', 'Shoshana', 'rSpsosmlp'),
    ('S90704597', 'Jennifer', 'UrfPZ2'),
    ('S62553855', 'Ariel', 'HgCEKcsoUNn'),
    ('S38183148', 'Meredith', 'TrZqjhC92'),
    ('S69415105', 'Branden', 'Ap556lVx'),
    ('S06577699', 'Edan', '5P2CwQGDfve'),
    ('S04174038', 'Colin', 'xd6aCxamOm'),
    ('S72184175', 'Desirae', 'rK2YHcf465yh'),
    ('S84819297', 'Wyoming', 'BBFgjUGP'),
    ('S17317326', 'Burke', '6tEm5s6C0fL'),
    ('S23192964', 'Isaiah', 'wd87rDD'),
    ('S29167213', 'Hop', 'ADhPXqD'),
    ('S27096888', 'Xenos', 'ZjiViM0NAQG'),
    ('S80890371', 'Yuli', 'nftGRs3d9A3'),
    ('S75527240', 'Dominic', 'NGa2jrc5'),
    ('S38624753', 'Francesca', 'RcUyDxc'),
    ('S85884267', 'Richard', 'nNhS8mtMDOu5'),
    ('S73452376', 'Dakota', '90vdWR'),
    ('S97672292', 'Gloria', 'Xx8IvrGrCkD'),
    ('S40008988', 'Jack', 'k25vMvb9l'),
    ('S61330047', 'Justine', 'VJZzwjR'),
    ('S93854165', 'Thomas', 'tL2PVYheeA9x'),
    ('S35540141', 'Melvin', 'Wh4fP54uDdP'),
    ('S62075673', 'Ezekiel', 'ug7hHIi'),
    ('S61409011', 'Jade', 'kSlr1OM'),
    ('S60121089', 'Xander', 'wWQgnkb6'),
    ('S91590043', 'Tiger', '87HPquwlyi9t'),
    ('S45630599', 'Baxter', 'gutyswlT6lZ5'),
    ('S16005132', 'Ulla', 'iRpDnzLJJs54'),
    ('S58494691', 'Hedy', 'nDbPWJ90uVLP'),
    ('S28946726', 'Aladdin', 'JGIWEaW33Rx'),
    ('S01154352', 'Cherokee', 'HGGJxTMD'),
    ('P48491547', 'Maia', 'Ll97fw8M'),
    ('P68799892', 'Carol', 'CSmbs3wN'),
    ('P62707222', 'Azalia', 'kE9AXLUzZxi7'),
    ('P35809956', 'Nayda', 'OJfhCpgkLeG'),
    ('P53579939', 'Ray', 'Y8Tbyc9ge7');"""
    db.session.execute(query)

    query = "CREATE TABLE IF NOT EXISTS admins(admin_id VARCHAR PRIMARY KEY REFERENCES web_users(user_id) ON DELETE CASCADE);"
    db.session.execute(query)
    query = "DELETE FROM admins;"
    db.session.execute(query)
    query = "INSERT INTO admins(admin_id) VALUES ('A23456789');"
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS students(
            student_id VARCHAR PRIMARY KEY REFERENCES web_users(user_id) on delete cascade, 
            major VARCHAR NOT NULL);"""
    db.session.execute(query)
    query = "DELETE FROM students;"
    db.session.execute(query)
    query = """INSERT INTO students(student_id, major) VALUES
    ('S34567890', 'CEG'),
    ('S37132455', 'CS'),
    ('S49083365', 'IS'),
    ('S69940317', 'CEG'),
    ('S10702156', 'CS'),
    ('S10797599', 'IS'),
    ('S29260258', 'CEG'),
    ('S77113792', 'CS'),
    ('S45831058', 'IS'),
    ('S46268848', 'CEG'),
    ('S90704597', 'CS'),
    ('S62553855', 'IS'),
    ('S38183148', 'CEG'),
    ('S69415105', 'CS'),
    ('S06577699', 'IS'),
    ('S04174038', 'CEG'),
    ('S72184175', 'CS'),
    ('S84819297', 'IS'),
    ('S17317326', 'CEG'),
    ('S23192964', 'CS'),
    ('S29167213', 'IS'),
    ('S27096888', 'CEG'),
    ('S80890371', 'CS'),
    ('S75527240', 'IS'),
    ('S38624753', 'CEG'),
    ('S85884267', 'CS'),
    ('S73452376', 'IS'),
    ('S97672292', 'CEG'),
    ('S40008988', 'CS'),
    ('S61330047', 'IS'),
    ('S93854165', 'CEG'),
    ('S35540141', 'CS'),
    ('S62075673', 'IS'),
    ('S61409011', 'CEG'),
    ('S60121089', 'CS'),
    ('S91590043', 'IS'),
    ('S45630599', 'CEG'),
    ('S16005132', 'CS'),
    ('S58494691', 'IS'),
    ('S28946726', 'CEG'),
    ('S01154352', 'CS');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS professors(
            prof_id VARCHAR PRIMARY KEY REFERENCES web_users(user_id) on delete cascade,
            faculty VARCHAR NOT NULL);"""
    db.session.execute(query)
    query = "DELETE FROM professors;"
    db.session.execute(query)
    query = """INSERT INTO professors(prof_id, faculty) VALUES
    ('P45678901', 'SoC'),
    ('P48491547', 'SoC'),
    ('P68799892', 'SoC'),
    ('P62707222', 'SoC'),
    ('P35809956', 'FoE'),
    ('P53579939', 'FoE');"""
    db.session.execute(query)
    
    query = """CREATE TABLE IF NOT EXISTS rounds(
            start_date DATE CHECK (start_date > '1900-01-01') PRIMARY KEY, 
            end_date DATE CHECK(end_date > start_date));"""
    db.session.execute(query)
    query = "DELETE FROM rounds;"
    db.session.execute(query)
    query = "INSERT INTO rounds(start_date, end_date) VALUES ('2019-11-07', '2019-11-10'), ('2019-11-20', '2019-11-23');"
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS modules(
            module_code VARCHAR,
            module_name VARCHAR NOT NULL,
            quota INT NOT NULL CHECK (quota>0),
            PRIMARY KEY (module_code));"""
    db.session.execute(query)
    query = "DELETE FROM modules;"
    db.session.execute(query)
    query = """INSERT INTO modules(module_code, module_name, quota) VALUES 
    ('CS1111', 'Intro to Coding', 20), 
    ('CG1111', 'Engineering Principles', 10),
    ('CS2222', 'Basic Coding', 20), 
    ('CS3333', 'Intermediate Coding', 10), 
    ('CS4444', 'Advanced Coding', 5), 
    ('CS5555', 'Master Coding', 2), 
    ('CS6666', 'Godlike Coding', 1),
    ('GEQ1000', 'CSU is Life', 20);"""
    db.session.execute(query)
    
    query = """CREATE TABLE IF NOT EXISTS available(
            module_code VARCHAR,
            start_date DATE REFERENCES rounds(start_date) on delete cascade,
            PRIMARY KEY (module_code, start_date));"""
    db.session.execute(query)
    query = "DELETE FROM available;"
    db.session.execute(query)
    query = """INSERT INTO available(module_code, start_date) VALUES 
    ('CS1111', '2019-11-07'), 
    ('CG1111', '2019-11-07'),
    ('CS2222', '2019-11-07'), 
    ('CS3333', '2019-11-07'), 
    ('CS4444', '2019-11-07'), 
    ('CS5555', '2019-11-07'), 
    ('CS6666', '2019-11-07'),
    ('CS1111', '2019-11-20'), 
    ('CG1111', '2019-11-20'),
    ('GEQ1000','2019-11-07');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS supervises(
            prof_id VARCHAR REFERENCES professors(prof_id) on delete cascade, 
            module_code VARCHAR REFERENCES modules(module_code) on delete cascade, 
            PRIMARY KEY (prof_id, module_code));"""
    db.session.execute(query)
    query = "DELETE FROM supervises;"
    db.session.execute(query)
    query = """INSERT INTO supervises(prof_id, module_code) VALUES
    ('P45678901', 'CS1111'),
    ('P45678901', 'CS2222'),
    ('P48491547', 'CS4444'),
    ('P68799892', 'CS3333'),
    ('P62707222', 'CS5555'),
    ('P62707222', 'CS6666'),    
    ('P35809956', 'CG1111');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS takes(
            student_id VARCHAR REFERENCES students(student_id) on delete cascade, 
            module_code VARCHAR REFERENCES modules(module_code) on delete cascade, 
            PRIMARY KEY(student_id, module_code));"""
    db.session.execute(query)
    query = "DELETE FROM takes;"
    db.session.execute(query)
    # ('S34567890', 'CS6666')
    query = """INSERT INTO takes(student_id, module_code) VALUES
    ('S37132455', 'CS5555'),
    ('S49083365', 'CS5555'),
    ('S69940317', 'CS4444'),
    ('S10702156', 'CS4444'),
    ('S10797599', 'CS3333'),
    ('S29260258', 'CS3333'),
    ('S77113792', 'CS3333'),
    ('S45831058', 'CS3333'),
    ('S46268848', 'CS3333'),
    ('S90704597', 'CS3333'),
    ('S62553855', 'CS2222'),
    ('S38183148', 'CS2222'),
    ('S69415105', 'CS2222'),
    ('S06577699', 'CS2222'),
    ('S04174038', 'CS2222'),
    ('S72184175', 'CS2222'),
    ('S84819297', 'CS2222'),
    ('S17317326', 'CS2222'),
    ('S23192964', 'CS2222'),
    ('S29167213', 'CS2222'),
    ('S27096888', 'CS2222'),
    ('S80890371', 'CS2222'),
    ('S75527240', 'CS2222'),
    ('S38624753', 'CG1111'),
    ('S85884267', 'CG1111'),
    ('S73452376', 'CS1111'),
    ('S97672292', 'CS1111'),
    ('S40008988', 'CS1111'),
    ('S61330047', 'CS1111'),
    ('S93854165', 'CS1111'),
    ('S35540141', 'CS1111'),
    ('S62075673', 'CS1111'),
    ('S61409011', 'CS1111'),
    ('S60121089', 'CS1111'),
    ('S91590043', 'CS1111'),
    ('S45630599', 'CS1111'),
    ('S16005132', 'CS1111'),
    ('S58494691', 'CS1111'),
    ('S01154352', 'CS1111');"""
    # ('S28946726', 'CS1111')
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS took(
            student_id VARCHAR REFERENCES students(student_id) on delete cascade, 
            module_code VARCHAR REFERENCES modules(module_code) on delete cascade, 
            PRIMARY KEY(student_id, module_code));"""
    db.session.execute(query)
    query = "DELETE FROM took;"
    db.session.execute(query)
    query = """INSERT INTO took(student_id, module_code) VALUES
    ('S34567890', 'CS1111'),
    ('S34567890', 'CS2222'),
    ('S34567890', 'CS3333'),
    ('S34567890', 'CS4444'),
    ('S34567890', 'CS5555'),
    ('S37132455', 'CS1111'),
    ('S37132455', 'CS2222'),
    ('S37132455', 'CS3333'),
    ('S37132455', 'CS4444'),
    ('S49083365', 'CS1111'),
    ('S49083365', 'CS2222'),
    ('S49083365', 'CS3333'),
    ('S49083365', 'CS4444'),
    ('S69940317', 'CS1111'),
    ('S69940317', 'CS2222'),
    ('S69940317', 'CS3333'),
    ('S10702156', 'CS1111'),
    ('S10702156', 'CS2222'),
    ('S10702156', 'CS3333'),
    ('S10797599', 'CS1111'),
    ('S10797599', 'CS2222'),
    ('S29260258', 'CS1111'),
    ('S29260258', 'CS2222'),
    ('S77113792', 'CS1111'),
    ('S77113792', 'CS2222'),
    ('S45831058', 'CS1111'),
    ('S45831058', 'CS2222'),
    ('S46268848', 'CS1111'),
    ('S46268848', 'CS2222'),
    ('S90704597', 'CS1111'),
    ('S90704597', 'CS2222'),
    ('S62553855', 'CS1111'),
    ('S38183148', 'CS1111'),
    ('S69415105', 'CS1111'),
    ('S06577699', 'CS1111'),
    ('S04174038', 'CS1111'),
    ('S72184175', 'CS1111'),
    ('S84819297', 'CS1111'),
    ('S17317326', 'CS1111'),
    ('S23192964', 'CS1111'),
    ('S29167213', 'CS1111'),
    ('S27096888', 'CS1111'),
    ('S80890371', 'CS1111'),
    ('S75527240', 'CS1111');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS prerequisites(
            module_code VARCHAR REFERENCES modules(module_code) on delete cascade, 
            prerequisite VARCHAR REFERENCES modules(module_code) on delete cascade, 
            PRIMARY KEY(module_code, prerequisite));"""
    db.session.execute(query)
    query = "DELETE FROM prerequisites;"
    db.session.execute(query)
    query = """INSERT INTO prerequisites(module_code, prerequisite) VALUES
    ('CS6666', 'CS5555'),
    ('CS6666', 'GEQ1000'),
    ('CS5555', 'CS4444'),
    ('CS4444', 'CS3333'),
    ('CS3333', 'CS2222'),
    ('CS2222', 'CS1111');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS lessons(
            module_code VARCHAR REFERENCES modules(module_code) on delete cascade, 
            day INT CHECK (day > 0 AND day < 6), 
            time INT CHECK (time >= 0 AND time <= 23), 
            location VARCHAR, 
            PRIMARY KEY (day, time, location));"""
    db.session.execute(query)
    query = "DELETE FROM lessons;"
    db.session.execute(query)
    query = """INSERT INTO lessons(module_code, day, time, location) VALUES
    ('CS6666', '1', '10', 'LT1'),
    ('CS6666', '1', '11', 'LT1'),
    ('CS6666', '3', '10', 'COM1-01'),
    ('CS5555', '2', '10', 'LT1'),
    ('CS5555', '2', '11', 'LT1'),
    ('CS5555', '2', '1', 'COM1-02'),
    ('CS4444', '2', '1', 'LT1'),
    ('CS4444', '4', '11', 'LT1'),
    ('CS4444', '3', '2', 'COM1-01'),
    ('CS3333', '2', '4', 'LT1'),
    ('CS3333', '2', '5', 'LT1'),
    ('CS3333', '4', '12', 'COM1-02'),
    ('CS2222', '1', '12', 'LT1'),
    ('CS2222', '4', '1', 'COM1-02'),
    ('CS1111', '4', '12', 'LT1'),
    ('CS1111', '4', '1', 'LT1'),
    ('CS1111', '3', '11', 'COM1-01'),
    ('CS1111', '2', '5', 'COM1-02'),
    ('CS1111', '5', '10', 'COM1-B1'),
    ('CS1111', '5', '11', 'COM1-B1'),
    ('CG1111', '3', '10', 'LT1'),
    ('CG1111', '3', '11', 'LT1'),
    ('CG1111', '5', '12', 'COM1-B1'),
    ('CG1111', '5', '13', 'COM1-B1');"""
    db.session.execute(query)

    query = "CREATE TABLE IF NOT EXISTS lectures(module_code VARCHAR REFERENCES modules(module_code) on delete cascade PRIMARY KEY);"
    db.session.execute(query)
    query = "DELETE FROM lectures;"
    db.session.execute(query)
    query = """INSERT INTO lectures(module_code) VALUES ('CS6666'), ('CS5555'), ('CS4444'), ('CS3333'), ('CS2222'), ('CS1111'), ('CG1111');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS lecturing(
            prof_id VARCHAR REFERENCES professors(prof_id) on delete cascade, 
            module_code VARCHAR REFERENCES modules(module_code) on delete cascade, 
            PRIMARY KEY (prof_id, module_code));"""
    db.session.execute(query)
    query = "DELETE FROM lecturing;"
    db.session.execute(query)
    query = """INSERT INTO lecturing(prof_id, module_code) VALUES
    ('P45678901', 'CS1111'),
    ('P45678901', 'CS2222'),    
    ('P48491547', 'CS4444'),
    ('P68799892', 'CS3333'),
    ('P62707222', 'CS5555'),
    ('P62707222', 'CS6666'),    
    ('P35809956', 'CG1111'),
    ('P68799892', 'CS4444');"""
    db.session.execute(query)

    query = "CREATE TABLE IF NOT EXISTS labtut(module_code VARCHAR REFERENCES modules(module_code) on delete cascade PRIMARY KEY);"
    db.session.execute(query)
    query = "DELETE FROM labtut;"
    db.session.execute(query)
    query = """INSERT INTO labtut(module_code) VALUES ('CS6666'), ('CS5555'), ('CS4444'), ('CS3333'), ('CS2222'), ('CS1111'), ('CG1111');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS assists(
            student_id VARCHAR REFERENCES students(student_id) on delete cascade, 
            module_code VARCHAR REFERENCES modules(module_code) on delete cascade, 
            PRIMARY KEY(student_id, module_code));"""
    db.session.execute(query)
    query = "DELETE FROM assists;"
    db.session.execute(query)
    query = """INSERT INTO assists(student_id, module_code) VALUES
    ('S37132455', 'CS1111'),
    ('S49083365', 'CS1111');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS registration(
            student_id VARCHAR REFERENCES students(student_id) on delete cascade, 
            module_code VARCHAR REFERENCES modules(module_code) on delete cascade);"""
    db.session.execute(query)
    query = "DELETE FROM registration;"
    db.session.execute(query)
    query = "INSERT INTO registration(student_id, module_code) VALUES ('S10797599', 'GEQ1000'), ('S29167213', 'CS6666');"
    db.session.execute(query)
    query = """CREATE OR REPLACE FUNCTION prereqcheck()
            RETURNS TRIGGER AS $$ BEGIN
            If Exists (
                select prerequisite from prerequisites where prerequisites.module_code=NEW.module_code
                Except
                select module_code from took where took.student_id=NEW.student_id
            ) Then
                Return NULL;
            End If;
            Return NEW;
            End;
            $$ Language plpgsql;"""
    db.session.execute(query)
    query = "DROP TRIGGER IF EXISTS prereq ON Takes CASCADE;"
    db.session.execute(query)
    query = """CREATE TRIGGER prereq
            BEFORE INSERT ON Takes
            FOR EACH ROW
            EXECUTE PROCEDURE prereqcheck();"""
    db.session.execute(query)
    db.session.commit()
    return "<h1>CS2102</h1>\
    <h2>Flask App started successfully!</h2>"

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
            # TODO: You may want to verify if password is correct
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

@view.route("/student", methods = ["GET", "POST"])
#@roles_required('Student')
def render_student_page():
    form = StudentForm()
    filters = ['Modules Currently Taking', 'Modules Taken in Past Semesters', 'Modules Pending Approval', 'Apply for Module']
    if form.validate_on_submit():
        user_name = form.user_name.data
        filter = request.form.get('filter_list')
        if filter == 'Modules Currently Taking':
            query = "SELECT * FROM takes WHERE student_id = '{}';".format(user_name)
        elif filter == 'Modules Taken in Past Semesters':
            query = "SELECT * FROM took WHERE student_id = '{}'".format(user_name)
        elif filter == 'Modules Pending Approval':
            query = "SELECT * FROM registration WHERE student_id = '{}'".format((user_name))

        result = db.session.execute(query).fetchall()
        return render_template("student.html", form = form, data = result, filters = filters)

    return render_template("student.html", form = form, filters = filters)

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
