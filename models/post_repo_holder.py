"""A class that holds posts so they can be operated on by routes in blueprints"""
from flask import current_app
from repos.post.IPostRepo import IPostRepo
from containers.repo_container import RepoContainer
from containers.container import Container

class PostRepoHolder():
    """A class that holds posts so they can be operated on by routes in blueprints"""
    def __init__(self):
        self.posts = None

    def create_repo(self):
        """Creates the repo"""
        db_type = current_app.config["DB_TYPE"]
        if db_type == 'db':
            self.posts = RepoContainer().post_repo_db_factory()
        elif db_type == 'memory':
            self.posts = RepoContainer().post_repo_memory_factory()
        elif db_type == 'alchemy':
            self.posts = RepoContainer().post_repo_alchemy_factory()

        else:
            print('DB_TYPE not valid. Must be \'db\', \'alchemy\' or \'memory\'')

    def get(self):
        """Returns all posts"""
        if self.posts is None:
            self.create_repo()
        return self.posts
