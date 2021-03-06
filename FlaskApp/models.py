from FlaskApp.__init__ import db


class web_users(db.Model):
    user_id = db.Column(db.String, primary_key=True)
    preferred_name = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id
