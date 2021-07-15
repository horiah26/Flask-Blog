"""Abstract class for posts repo"""
from abc import ABC, abstractmethod

class IPost (ABC):
    """Abstract class for posts repo"""
    @abstractmethod
    def get(self, post_id):
        """Get post by id"""

    @abstractmethod
    def get_all(self):
        """Get all posts"""

    @abstractmethod
    def update(self, post_id, title, text):
        """Update post"""

    @abstractmethod
    def delete(self, post_id):
        """Delete post"""
    @abstractmethod
    def get_previews(self):
        """Returns preview of all posts"""
