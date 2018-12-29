from werkzeug.security import generate_password_hash
from .... import create_app
from ....db_con import init_db
from .base_model import BaseModel



class UserModel(BaseModel):
    """ This class encapsulates the functions of the user model """

    def __init__(self, username="user", first_name="first", last_name="last",email="em@ai.l", password="pass" ):
        """ initialize the user model """

        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = generate_password_hash(password)
        self.email = email
        self.db = init_db()

    def get_user_by_username(self, username):
        """ returns user from the db given a username """
        database = self.db

        curr = database.cursor()
        curr.execute(
            """SELECT user_id, first_name, last_name, password FROM users WHERE username = '%s'; """ % (username))

        data = curr.fetchone()

        curr.close()

        return data

    def check_exists(self, username):
        """ Check if the record exists """
        curr = self.db.cursor()
        curr.execute(
            """ SELECT username FROM users WHERE username = '%s';""" % (username))
        return curr.fetchone() is not None


    def save_user(self):
        """ Add user details to the database """
        user = {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name, 
            "email": self.email,
            "password": self.password
        }

        # Chek if user already exists

        if self.check_exists(user['username']):
            return False


        curr = self.db.cursor()
        # WARNING: DON'T COPY THIS AS IT IS INSTEAD USER 'VALUES(%s, %s, %s, %s) % (first_name, last_name , username,...)
        curr.execute (""" INSERT INTO users (first_name, last_name, username, email, password) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s) RETURNING user_id;""")
        user_id = curr.fetchone()[0]
        self.db.commit()
        curr.close()
        return int(user_id)


    def get_all_users(self):
        """ returns all the users in the database by first and last name"""
        database = self.db

        curr = database.cursor()
        curr.execute(
            """SELECT first_name, last_name, FROM users;""")

        data = curr.fetchall()

        curr.close()

        return data
