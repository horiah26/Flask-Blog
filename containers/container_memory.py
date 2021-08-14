"""General purpose container"""
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
    
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.config_db import ConfigDB
from config.config import Config
from database.database import Database
from services.auth import Authentication
from services.hasher import Hasher
from config.alchemy_url import AlchURL

from repos.post.post_repo_memory import RepoPostsMemory
from repos.post.seed import get as post_seed
from repos.post.image_repo import ImageRepo

from repos.user.user_repo_memory import RepoUserMemory
from repos.user.seed import get as user_seed

class ContainerMemory(containers.DeclarativeContainer):
    """General purpose container"""

    config = providers.Configuration()
    
    hasher = providers.Factory(
        Hasher
    )

    config_db = providers.Factory(
        ConfigDB
    )

    config = providers.Factory(
        Config
    )

    user_repo = providers.Singleton(
        RepoUserMemory,
        seed = user_seed()
    )

    img_repo = providers.Singleton(
        ImageRepo
    )

    post_repo = providers.Singleton(
        RepoPostsMemory,
        seed = post_seed(),
        user_repo = user_repo
    )
    
    auth = providers.Factory(
        Authentication,
        user_repo = user_repo
    )

    database = providers.Factory(
        Database,
        config = config,
        config_db = config_db
    )

