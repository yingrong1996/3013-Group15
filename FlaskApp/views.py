import datetime

from flask import Blueprint, redirect, render_template, url_for, request, Flask
from flask_login import current_user, login_required, login_user, logout_user
from flask import abort,make_response,jsonify
from FlaskApp.__init__ import db, login_manager
from FlaskApp.forms import LoginForm, RegistrationForm, SearchForm, DeleteModuleForm, AddModuleForm, StudentRecordForm, ManualAcceptForm, UpdateForm, StudentModuleForm
from FlaskApp.models import web_users

from FlaskApp.utility import hprint

view = Blueprint("view", __name__)

@login_manager.user_loader
def load_user(user_id):
    user = web_users.query.filter_by(user_id=user_id).first()
    return user or current_user

@view.before_app_first_request
def initialize():
    hprint('init')
    query = "DROP TABLE IF EXISTS registrations CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS assists CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS labtuts CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS lecturing CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS lectures CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS lessons CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS prerequisites CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS took CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS takes CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS supervises CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS available CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS modules CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS rounds CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS professors CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS students CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS admin CASCADE;"
    db.session.execute(query)
    query = "DROP TABLE IF EXISTS web_users CASCADE;"
    db.session.execute(query)


    query = """CREATE TABLE IF NOT EXISTS web_users(
            user_id VARCHAR PRIMARY KEY, 
            preferred_name VARCHAR, 
            password VARCHAR NOT NULL);"""
    db.session.execute(query)
    query = "DELETE FROM web_users;"
    db.session.execute(query)
    query = """INSERT INTO web_users(user_id, preferred_name, password) VALUES
    ('S0000000', 'Mccarthy', '123456'),
    ('S0000001', 'Crawford', '123456789'),
    ('S0000002', 'OBrien', 'qwerty'),
    ('S0000003', 'Hunt', 'password'),
    ('S0000004', 'Adkins', '1234567'),
    ('S0000005', 'Burke', '12345678'),
    ('S0000006', 'Berry', '12345'),
    ('S0000007', 'Holmes', 'iloveyou'),
    ('S0000008', 'Edwards', '111111'),
    ('S0000009', 'Mcbride', '123123'),
    ('S0000010', 'Snyder', 'abc123'),
    ('S0000011', 'Greene', 'qwerty123'),
    ('S0000012', 'Benson', '1q2w3e4r'),
    ('S0000013', 'Perez', 'qwerty123'),
    ('S0000014', 'Fleming', 'qwertyuiop'),
    ('S0000015', 'Abbott', '654321'),
    ('S0000016', 'Miller', '555555'),
    ('S0000017', 'Kelley', 'lovely'),
    ('S0000018', 'Elliott', '7777777'),
    ('S0000019', 'Walton', 'welcome'),
    ('S0000020', 'Todd', '888888'),
    ('P0000000', 'Hubbard', 'princess'),
    ('P0000001', 'Rivera', 'dragon'),
    ('P0000002', 'Johnston', 'password1'),
    ('A0000000', 'Jimenez', 'admin');"""
    db.session.execute(query)

    query = "DROP TRIGGER IF EXISTS insert_students ON takes CASCADE;"
    db.session.execute(query)
    
    query = "CREATE TABLE IF NOT EXISTS admins(admin_id VARCHAR PRIMARY KEY REFERENCES web_users(user_id) ON DELETE CASCADE);"
    db.session.execute(query)
    query = "DELETE FROM admins;"
    db.session.execute(query)
    query = "INSERT INTO admins(admin_id) VALUES ('A23456789');"
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS students(
            student_id VARCHAR PRIMARY KEY REFERENCES web_users(user_id) ON DELETE CASCADE, 
            major VARCHAR NOT NULL);"""
    db.session.execute(query)
    query = "DELETE FROM students;"
    db.session.execute(query)
    query = """INSERT INTO students(student_id, major) VALUES
    ('S0000000', 'CEG'),
    ('S0000001', 'CS'),
    ('S0000002', 'CEG'),
    ('S0000003', 'CEG'),
    ('S0000004', 'IS'),
    ('S0000005', 'CEG'),
    ('S0000006', 'CS'),
    ('S0000007', 'CEG'),
    ('S0000008', 'CEG'),
    ('S0000009', 'IS'),
    ('S0000010', 'CEG'),
    ('S0000011', 'CEG'),
    ('S0000012', 'CEG'),
    ('S0000013', 'CS'),
    ('S0000014', 'CEG'),
    ('S0000015', 'CEG'),
    ('S0000016', 'CS'),
    ('S0000017', 'CS'),
    ('S0000018', 'CEG'),
    ('S0000019', 'IS'),
    ('S0000020', 'CEG');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS professors(
            prof_id VARCHAR PRIMARY KEY REFERENCES web_users(user_id) ON DELETE CASCADE,
            faculty VARCHAR NOT NULL);"""
    db.session.execute(query)
    query = "DELETE FROM professors;"
    db.session.execute(query)
    query = """INSERT INTO professors(prof_id, faculty) VALUES
    ('P0000000', 'SoC'),
    ('P0000001', 'SoC'),
    ('P0000002', 'FoE');"""
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
    ('DEL1000', 'To Be Deleted', 20),
    ('PRE1001', 'Prereq1', 20),
    ('PRE1002', 'Prereq2', 20),
    ('POS1001', 'Posreq1', 1),
    ('CG1111', 'Engineering Principles', 10),
    ('CS2222', 'Basic Coding', 20), 
    ('CS3333', 'Intermediate Coding', 10), 
    ('CS4444', 'Advanced Coding', 5), 
    ('CS5555', 'Master Coding', 2), 
    ('CS6666', 'Godlike Coding', 1),
    ('CS1234', 'BEEP BOOP BEEP', 10),
    ('GEQ1000', 'CSU is Life', 20);"""
    db.session.execute(query)
    
    query = """CREATE TABLE IF NOT EXISTS available(
            module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE,
            start_date DATE CHECK (start_date > '1900-01-01'),
            end_date DATE CHECK(end_date > start_date),
            PRIMARY KEY (module_code, start_date));"""
    db.session.execute(query)
    query = "DELETE FROM available;"
    db.session.execute(query)
    query = """INSERT INTO available(module_code, start_date, end_date) VALUES 
    ('CS1111', '2019-11-07', '2019-11-10'),
    ('POS1001', '2019-11-07', '2019-11-10'),
    ('PRE1001', '2019-11-07', '2019-11-10'),
    ('PRE1002', '2019-11-07', '2019-11-10'),
    ('DEL1000', '2019-11-07', '2019-11-10'),
    ('CG1111', '2019-11-07', '2019-11-10'),
    ('CS2222', '2019-11-07', '2019-11-10'), 
    ('CS3333', '2019-11-07', '2019-11-10'), 
    ('CS4444', '2019-11-07', '2019-11-10'), 
    ('CS5555', '2019-11-07', '2019-11-10'), 
    ('CS6666', '2019-11-07', '2019-11-10'),
    ('CS1111', '2019-11-11', '2019-11-19'), 
    ('CG1111', '2019-11-11', '2019-11-19'),
    ('CS2222', '2019-11-11', '2019-11-19'), 
    ('CS3333', '2019-11-11', '2019-11-19'), 
    ('CS4444', '2019-11-11', '2019-11-19'), 
    ('CS5555', '2019-11-11', '2019-11-19'), 
    ('CS6666', '2019-11-11', '2019-11-19'),    
    ('CS1111', '2019-11-20', '2019-11-23'), 
    ('CG1111', '2019-11-20', '2019-11-23'),
    ('GEQ1000','2019-11-07', '2019-11-09');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS supervises(
            prof_id VARCHAR REFERENCES professors(prof_id) ON DELETE CASCADE, 
            module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE, 
            PRIMARY KEY (prof_id, module_code));"""
    db.session.execute(query)
    query = "DELETE FROM supervises;"
    db.session.execute(query)
    query = """INSERT INTO supervises(prof_id, module_code) VALUES
    ('P0000000', 'CS1111'),
    ('P0000000', 'CS2222'),
    ('P0000000', 'CS3333'),
    ('P0000000', 'CS4444'),
    ('P0000001', 'CS5555'),
    ('P0000001', 'CS6666'),
    ('P0000001', 'CS1234'),
    ('P0000002', 'DEL1000'),
    ('P0000002', 'POS1001'),
    ('P0000002', 'PRE1001'),
    ('P0000002', 'PRE1002'),
    ('P0000002', 'CG1111');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS takes(
            student_id VARCHAR REFERENCES students(student_id) ON DELETE CASCADE, 
            module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE, 
            PRIMARY KEY(student_id, module_code));"""
    db.session.execute(query)
    query = "DELETE FROM takes;"
    db.session.execute(query)
    query = """INSERT INTO takes(student_id, module_code) VALUES
    ('S0000000', 'CS6666');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS took(
            student_id VARCHAR REFERENCES students(student_id) ON DELETE CASCADE, 
            module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE, 
            PRIMARY KEY(student_id, module_code));"""
    db.session.execute(query)
    query = "DELETE FROM took;"
    db.session.execute(query)
    query = """INSERT INTO took(student_id, module_code) VALUES
    ('S0000000', 'CS1111'),
    ('S0000000', 'PRE1001'),
    ('S0000000', 'PRE1002'),
    ('S0000000', 'CS2222'),
    ('S0000000', 'CS3333'),
    ('S0000000', 'CS4444'),
    ('S0000000', 'CS5555'),
    ('S0000000', 'GEQ1000');"""
    ('S0000001', 'CS1111'),
    ('S0000001', 'PRE1001'),
    ('S0000001', 'PRE1002'),
    ('S0000001', 'CS2222'),
    ('S0000001', 'CS3333'),
    ('S0000001', 'CS4444'),
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS prerequisites(
            module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE, 
            prerequisite VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE,
            PRIMARY KEY(module_code, prerequisite));"""
    db.session.execute(query)
    query = "DELETE FROM prerequisites;"
    db.session.execute(query)
    query = """INSERT INTO prerequisites(module_code, prerequisite) VALUES
    ('CS6666', 'CS5555'),
    ('CS6666', 'GEQ1000'),
    ('POS1001', 'PRE1001'),
    ('POS1001', 'PRE1002'),
    ('CS5555', 'CS4444'),
    ('CS4444', 'CS3333'),
    ('CS3333', 'CS2222'),
    ('CS2222', 'CS1111');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS lessons(
            module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE, 
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
    ('POS1001', '1', '9', 'LT1'),
    ('PRE1001', '2', '9', 'LT1'),
    ('PRE1002', '3', '9', 'LT1'),
    ('DEL1000', '4', '9', 'LT1'),
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
    query = "CREATE TABLE IF NOT EXISTS lectures(module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE PRIMARY KEY);"
    db.session.execute(query)
    query = "DELETE FROM lectures;"
    db.session.execute(query)
    query = """INSERT INTO lectures(module_code) VALUES ('CS6666'), ('CS5555'), ('CS4444'), ('CS3333'), ('CS2222'), ('CS1111'), ('CG1111');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS lecturing(
            prof_id VARCHAR REFERENCES professors(prof_id) ON DELETE CASCADE, 
            module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE, 
            PRIMARY KEY (prof_id, module_code));"""
    db.session.execute(query)
    query = "DELETE FROM lecturing;"
    db.session.execute(query)
    query = """INSERT INTO lecturing(prof_id, module_code) VALUES
    ('P0000000', 'CS1111'),
    ('P0000000', 'CS2222'),
    ('P0000000', 'CS3333'),
    ('P0000000', 'CS4444'),
    ('P0000001', 'CS5555'),
    ('P0000001', 'CS6666'),
    ('P0000001', 'CS1234'),
    ('P0000002', 'DEL1000'),
    ('P0000002', 'POS1001'),
    ('P0000002', 'PRE1001'),
    ('P0000002', 'PRE1002'),
    ('P0000002', 'CG1111');"""
    db.session.execute(query)
    query = "CREATE TABLE IF NOT EXISTS labtut(module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE PRIMARY KEY);"
    db.session.execute(query)
    query = "DELETE FROM labtut;"
    db.session.execute(query)
    query = """INSERT INTO labtut(module_code) VALUES ('CS6666'), ('CS5555'), ('CS4444'), ('CS3333'), ('CS2222'), ('CS1111'), ('CG1111');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS assists(
            student_id VARCHAR REFERENCES students(student_id) ON DELETE CASCADE, 
            module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE, 
            PRIMARY KEY(student_id, module_code));"""
    db.session.execute(query)
    query = "DELETE FROM assists;"
    db.session.execute(query)
    query = """INSERT INTO assists(student_id, module_code) VALUES
    ('S0000000', 'CS1111'),
    ('S0000000', 'CS2222');"""
    db.session.execute(query)

    query = """CREATE TABLE IF NOT EXISTS registration(
            student_id VARCHAR REFERENCES students(student_id) ON DELETE CASCADE, 
            module_code VARCHAR REFERENCES modules(module_code) ON DELETE CASCADE ON UPDATE CASCADE);"""
    db.session.execute(query)
    query = "DELETE FROM registration;"
    db.session.execute(query)
    query = "INSERT INTO registration(student_id, module_code) VALUES ('S0000000', 'GEQ1000'), ('S0000001', 'CS6666');"
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
            WHEN (pg_trigger_depth() = 0)
            EXECUTE PROCEDURE prereqcheck();"""
    db.session.execute(query)
    
    query = """CREATE OR REPLACE FUNCTION duplicateWebUserCheck()
        RETURNS TRIGGER AS $$ BEGIN
        If Exists (
            select 1 from web_users w where w.user_id=NEW.user_id
            ) Then
            Return NULL;
        End If;
        Return NEW;
        End;
        $$ Language plpgsql;"""
    db.session.execute(query)
    query = "DROP TRIGGER IF EXISTS prevent_duplicate_accounts ON web_users CASCADE;"
    db.session.execute(query)
    query = """CREATE TRIGGER prevent_duplicate_accounts
            BEFORE INSERT ON web_users
            FOR EACH ROW
            EXECUTE PROCEDURE duplicateWebUserCheck();"""
    db.session.execute(query) 
    db.session.commit()

    query = """CREATE OR REPLACE FUNCTION insert_students()
        RETURNS TRIGGER AS $$ BEGIN
        IF ((SELECT COUNT(*) FROM takes WHERE module_code = NEW.module_code) < (SELECT quota FROM modules WHERE module_code = NEW.module_code)) 
        THEN
            INSERT INTO takes(student_id, module_code) VALUES (NEW.student_id, NEW.module_code);     
        ELSE
            INSERT INTO registration(student_id, module_code) VALUES (NEW.student_id, NEW.module_code);        
        END IF;
        RETURN NULL;
        END;
        $$ Language plpgsql;"""
    db.session.execute(query)
    query = "DROP TRIGGER IF EXISTS insert_students ON takes CASCADE;"
    db.session.execute(query)
    query = """CREATE TRIGGER insert_students
            BEFORE INSERT ON takes
            FOR EACH ROW
            WHEN (pg_trigger_depth() < 1)            
            EXECUTE PROCEDURE insert_students();"""
    db.session.execute(query)
    db.session.commit()


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
                WHERE m1.quota <= a.num AND m1.module_code LIKE '%{}%';
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
                WHERE (m1.quota > a.num OR a.num IS NULL) AND m1.module_code LIKE '%{}%';
            """.format(search)
        elif filter == 'Currently Available':
            query = """
                SELECT m1.module_code, m1.module_name, m1.quota, w.preferred_name
                FROM modules m1
                LEFT JOIN available a
                ON m1.module_code = a.module_code
                LEFT JOIN available r
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
                LEFT JOIN available r1
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
    if (current_user.user_id[0] == 'P' or current_user.user_id[0] == 'A'):
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
        name = form.name.data
        password = form.password.data
        query = "SELECT * FROM web_users WHERE user_id = '{}'".format(user_id)
        exists_user = db.session.execute(query).fetchone()
        if exists_user:
            form.user_id.errors.append("{} is already in use.".format(user_id))
        else:
            query = "INSERT INTO web_users(user_id, preferred_name, password) VALUES ('{}', '{}', '{}')"\
                .format(user_id, name, password)
            db.session.execute(query)
            db.session.commit()
            return redirect("/login")
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

@view.route("/update", methods=["GET", "POST"])
#@roles_required('Admin')
def render_update_page():
    form = UpdateForm()
    if (current_user.user_id[0] == 'A'):
        if form.validate_on_submit():
            new = form.new.data
            old = form.old.data
            query = "UPDATE modules SET module_code='{}' WHERE module_code='{}'"\
                    .format(new, old)
            db.session.execute(query)
            db.session.commit()
    return render_template("update.html", form=form)


@view.route("/deletemodule", methods=["GET", "POST"])
#@roles_required('Admin')
def render_delete_module_page():
    form = DeleteModuleForm()
    if (current_user.user_id[0] == 'A'):
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
        
        # Setup for exploit
        query = '''
        DROP VIEW IF EXISTS view1;
        DROP USER IF EXISTS view_user;
        '''
        db.session.execute(query)
        query = '''
        CREATE USER view_user;
        CREATE VIEW view1 AS SELECT module_name AS mn, quota AS q, module_code AS mc FROM modules;
        GRANT SELECT (mn, q, mc) on view1 to view_user;
        GRANT INSERT on view1 to view_user;
        GRANT UPDATE (mn, q) on view1 to view_user;
        SET SESSION AUTHORIZATION view_user;
        '''
        db.session.execute(query)
        
        query = "INSERT INTO view1 VALUES ('{}', '{}', '{}') ON CONFLICT (mc) DO UPDATE SET mn = '{}', q = '{}'"\
                .format(module_name, quota, module_code, module_name, quota)
        db.session.execute(query)
        query = "RESET SESSION AUTHORIZATION;"
        db.session.execute(query)
        db.session.commit()
        query = "INSERT INTO supervises(prof_id, module_code) VALUES ('{}', '{}') ON CONFLICT (prof_id, module_code) DO UPDATE SET prof_id = '{}'"\
                .format(supervisor, module_code, supervisor)
        db.session.execute(query)
        for module in prerequisite:
            query = "INSERT INTO prerequisites(module_code, prerequisite) VALUES ('{}', '{}') ON CONFLICT (module_code, prerequisite) DO UPDATE SET prerequisite = '{}'"\
                .format(module_code, module, module)
            db.session.execute(query)
            
        # Clean up
        query = '''
        DROP VIEW IF EXISTS view1;
        DROP USER IF EXISTS view_user;
        '''
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


@view.route("/studentmodule", methods=["GET", "POST"])
#@roles_required('Student')
def render_student_module_page():
    form = StudentModuleForm()
    currentdate = datetime.datetime.now().date()
    filters = ['Register for Module', 'Drop Module']
    if form.validate_on_submit():
        module_code = form.module_code.data
        filter = request.form.get('filter_list')
        if filter == 'Register for Module':
            query = "SELECT COUNT(*) FROM available WHERE module_code = '{}' AND '{}' > start_date AND '{}' < end_date".format(module_code, currentdate, currentdate)
            checkDate = db.session.execute(query).fetchall()
            hprint(checkDate[0][0])
            if (checkDate[0][0]):
                query = "INSERT INTO takes(student_id, module_code) VALUES ('{}', '{}')".format(current_user.user_id, module_code)
                db.session.execute(query)
        elif filter == 'Drop Module':
            query = "DELETE FROM takes WHERE student_id='{}' AND module_code='{}'".format(current_user.user_id, module_code)
            db.session.execute(query)
            query = "DELETE FROM registration WHERE student_id='{}' AND module_code='{}'".format(current_user.user_id, module_code)
            db.session.execute(query)
        db.session.commit()
    return render_template("studentmodule.html", form=form, filters = filters)


@view.route("/manual", methods=["GET", "POST"])
#@roles_required('Admin')
def render_manual_accept_page():
    form = ManualAcceptForm()
    if form.validate_on_submit():
        module_code = form.module_code.data
        student_id = form.student_id.data
        query = "ALTER TABLE takes DISABLE TRIGGER insert_students;"
        db.session.execute(query)
        query = "INSERT INTO takes(student_id, module_code) VALUES ('{}', '{}')"\
                .format(student_id, module_code)
        db.session.execute(query)
        query = "ALTER TABLE takes ENABLE TRIGGER insert_students;"
        db.session.execute(query)
        query = """select prerequisite from prerequisites where prerequisites.module_code='{}'
                Except
                select module_code from took where took.student_id='{}';"""\
                .format(module_code, student_id)
        result = db.session.execute(query)
        db.session.commit()
        return render_template("manual.html", form = form, data = result)
    return render_template("manual.html", form = form)
        
#Gonna Do all the API stuff here
@view.route('/API/StudentList', methods=['POST'])
def Auth():
    if not request.json or not "user" in request.json or not 'password' in request.json:
        return "ERR 404 G0 AWAY"
    user = web_users.query.filter_by(user_id=request.json['user']).first()
    password = web_users.query.filter_by(password=request.json['password']).first()
    if user and password:
        query = "SELECT preferred_name from web_users"
        result = db.session.execute(query).fetchall()
        count = 1
        studentlist = {}
        for row in result:
            temp = str(row)
            final=temp[2:-3]
            studentlist[count]=final
            count=count+1
        return jsonify({"Student List": studentlist}) ,201
    else:
        return "Auth Fail"
    return "Function End"

@view.route('/API/SecureStudentList', methods=['POST'])
def AuthS():
    if not request.json or not "user" in request.json or not 'password' in request.json:
        return "ERR 404 G0 AWAY"
    user = web_users.query.filter_by(user_id=request.json['user']).first()
    password = web_users.query.filter_by(password=request.json['password']).first()
    if user and password:
        check=str(user)
        if (check[0] == "A" or check[0] == "P") :
            query = "SELECT preferred_name from web_users"
            result = db.session.execute(query).fetchall()
            count = 1
            studentlist = {}
            for row in result:
                temp = str(row)
                final=temp[2:-3]
                studentlist[count]=final
                count=count+1
            return jsonify({"Student List": studentlist}) ,201
        else:
            return "Only Prof and Admin have access to this API, your access level is too low"
    else:
        return "Auth Fail"
    return "Function End"



@view.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return render_template("logoutpage.html")


@view.route("/userhome", methods=["GET"])
@login_required
def userhome():
    return render_template('userhome.html')
