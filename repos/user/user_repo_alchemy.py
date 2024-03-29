"""SQLAlchemy repo"""
from datetime import datetime
import psycopg2

from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.user import User
from models.date import Date

from .IUserRepo import IUserRepo


class RepoUserAlchemy(IUserRepo):
    """SQLAlchemy repo"""

    def __init__(self, config, alch_url, seed=None):
        """Initializes class and adds users from seed if present"""

        db = create_engine(alch_url.get_url())

        session = sessionmaker(db)
        self.session = session()

        base = automap_base()
        base.prepare(db, reflect=True)

        self.Post = base.classes.posts
        self.User = base.classes.users

        if seed is not None and config.config_file_exists() and self.get_all() is not None and len(self.get_all()) <= 1:
            for user in seed:
                if user.username != 'admin':
                    self.insert(user)

    def insert(self, user):
        """Add a new user"""
        new_user = self.User(username=user.username, name=user.name, email=user.email, password=user.password,
                             img_id=user.img_id, date_created=user.date.created, date_modified=user.date.modified)
        self.session.add(new_user)
        self.session.commit()

    def get(self, username):
        """Returns user by id"""
        user = self.session.query(self.User).get(username)
        if user is None:
            return None
        return User(user.username, user.name, user.email, user.password, user.img_id,
                    Date(user.date_created, user.date_modified))

    def get_all(self):
        """Returns all users"""
        users = []
        query = self.session.query(self.User).all()
        for user in query:
            users.append(User(user.username, user.name, user.email, user.password, user.img_id,
                              Date(user.date_created, user.date_modified)))
        return users

    def update(self, username, name, email, img_id, password):
        """Updates user by id"""
        user = self.session.query(self.User).filter(self.User.username == username).one()
        user.username = username
        user.name = name
        user.email = email
        user.password = password
        user.img_id = img_id
        user.date_modified = datetime.now().strftime("%B %d %Y - %H:%M")
        self.session.commit()

    def delete(self, username):
        """Deletes user by id"""
        user = self.session.query(self.User).filter(self.User.username == username).one()
        self.session.delete(user)
        self.session.commit()

    def get_users_with_posts(self):
        """Returns all users"""
        users = []
        query = self.session.query(self.User).join(self.Post, self.User.username == self.Post.owner)
        for user in query:
            users.append(
                User(user.username, user.name, user.email, user.password, Date(user.date_created, user.date_modified)))
        return users
