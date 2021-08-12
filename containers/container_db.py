"""Database container"""
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

from repos.post.post_repo_db import RepoPostsDB
from repos.post.seed import get as post_seed

from repos.user.user_repo_db import RepoUserDB
from repos.user.seed import get as user_seed

class ContainerDB(containers.DeclarativeContainer):
    """Database container"""

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
    

    database = providers.Factory(
        Database,
        config = config,
        config_db = config_db
    )
        
    post_repo = providers.Singleton(
        RepoPostsDB,
        db = database,
        seed = post_seed()
    )

    user_repo = providers.Singleton(
        RepoUserDB,
        db = database,
        seed = user_seed()
    )

    auth = providers.Factory(
        Authentication,
        user_repo = user_repo
    )