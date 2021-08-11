"""SQLAlchemy repo"""
import datetime
import psycopg2

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dependency_injector.wiring import inject, Provide

from models.user import User

from .IUserRepo import IUserRepo

class RepoUserAlchemy(IUserRepo):
    """SQLAlchemy repo"""
    @inject
    def __init__(self, seed = None, alch_url = Provide['alch_url']):
        """Initializes class and adds users from seed if present"""

        db = create_engine(alch_url.get_url())
        base = declarative_base()

        Session = sessionmaker(db)
        self.session = Session()

        Base = automap_base()
        Base.prepare(db, reflect=True)

        self.Post = Base.classes.posts
        self.User = Base.classes.users

        if seed is not None and self.get_all() is not None and len(self.get_all()) == 0:
            for post in seed:
                self.insert(post)


    def insert(self, user):
        """Add a new user"""
        new_user = self.User(username = user.username, name = user.name, email = user.email, password = user.password, date_created = user.date_created, date_modified = user.date_modified)
        self.session.add(new_user)
        self.session.commit()

    def get(self, username):
        """Returns user by id"""
        user = self.session.query(self.User).get(username)
        if user is None:
            return None
        return User(user.username, user.name, user.email, user.password, user.date_created, user.date_modified)

    def get_all(self):
        """Returns all users"""
        users = []
        query = self.session.query(self.User).all()
        for user in query:
            users.append(User(user.username, user.name, user.email, user.password, user.date_created, user.date_modified))
        return users

    def update(self, username, name, email, password):
        """Updates user by id"""
        user = self.session.query(self.User).filter(self.User.username == username).one()
        user.username = username
        user.name = name
        user.email = email
        user.password = password
        user.date_modified = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        self.session.commit()

    def delete(self, username):
        """Deletes user by id"""
        user = self.session.query(self.User).filter(self.User.username == username).one()
        self.session.delete(user)
        self.session.commit()
