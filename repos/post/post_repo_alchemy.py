"""SQLAlchemy repo"""

import datetime
import math
from static import constant

from sqlalchemy.sql import func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dependency_injector.wiring import inject, Provide
from .IPostRepo import IPostRepo

from models.post import Post
from models.post_preview import PostPreview
from models.user import User

class RepoPostsAlchemy(IPostRepo):
    """SQLAlchemy repo"""
    @inject
    def __init__(self, seed = None, alch_url = Provide['alch_url']):
        """Initializes class and adds posts from seed if present"""
        db = create_engine(alch_url.get_url())
        base = declarative_base()

        Session = sessionmaker(db)
        self.session = Session()
        print(self.session)

        Base = automap_base()
        Base.prepare(db, reflect=True)

        self.Post = Base.classes.posts
        self.User = Base.classes.users

        if seed is not None and self.get_all() is not None and len(self.get_all()) == 0:
            print(len(self.get_all()))
            for post in seed:
                self.insert(post)
                
    def insert(self, post):
        """Add a new post"""
        new_post = self.Post(post_id = post.post_id, title = post.title, text = post.text, owner = post.owner, date_created = post.date_created, date_modified = post.date_modified)
        self.session.add(new_post)
        self.session.commit()

    def get(self, post_id):
        """Returns post by id"""
        post = self.session.query(self.Post.post_id, self.Post.title, self.Post.text, self.Post.owner, self.Post.date_created, self.Post.date_modified, self.User.name).join(self.User, self.User.username == self.Post.owner).filter(self.Post.post_id == post_id).first()
        return (Post(post[0], post[1], post[2], post[3], post[4], post[5]), post[6])

    def get_all(self):
        """Returns all posts"""
        return self.session.query(self.Post).all()

    def update(self, post_id, title, text):
        """Updates post by id"""
        post = self.session.query(self.Post).filter(self.Post.post_id == post_id).first()
        post.title = title
        post.text = text
        post.date_modified = datetime.datetime.now().strftime("%B %d %Y - %H:%M")
        self.session.commit()

    def delete(self, post_id):
        """Deletes post by id"""
        post = self.session.query(self.Post).filter(self.Post.post_id == post_id).first()
        self.session.delete(post)
        self.session.commit()

    def get_previews(self, username = None, per_page = 6, page_num = 1):
        """Returns previews of posts posts"""
        offset_nr = (page_num - 1) * per_page
        previews = []
        if username:
            for post_id, title, prev_text, name, username, date_created, date_modified in self.session.query(self.Post.post_id, self.Post.title, func.substr(self.Post.text, 0, constant.PREVIEW_LENGTH), self.User.name, self.Post.owner, self.Post.date_created, self.Post.date_modified).join(self.User, self.User.username == self.Post.owner).filter(self.User.username == username).order_by(self.Post.post_id.desc()).slice(offset_nr, offset_nr + per_page):
                previews.append(PostPreview(post_id, title, prev_text, name, username, date_created, date_modified))
        else:
            for post_id, title, prev_text, name, username, date_created, date_modified in self.session.query(self.Post.post_id, self.Post.title, func.substr(self.Post.text, 0, constant.PREVIEW_LENGTH), self.User.name, self.Post.owner, self.Post.date_created, self.Post.date_modified).join(self.User, self.User.username == self.Post.owner).order_by(self.Post.post_id.desc()).limit(per_page).offset(offset_nr):
                previews.append(PostPreview(post_id, title, prev_text, name, username, date_created, date_modified))
     
                        
        if username:
            total_posts = self.session.query(self.Post.post_id).filter(self.Post.owner == username).count()
        else:
            total_posts = self.session.query(self.Post.post_id).count()
            
        total_pages = math.ceil(total_posts / per_page)
        return (previews, total_pages)

    def next_id(self):
        """Returns next id"""
        return self.session.query(func.max(self.Post.post_id)).first()[0] + 1
