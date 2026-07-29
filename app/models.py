from .database import Base
import sqlalchemy as sa 
from .database import Base
from datetime import datetime

class Post(Base):
    __tablename__ = "posts"
    id = sa.Column(sa.Integer, primary_key = True, nullable = False)
    title = sa.Column(sa.String, nullable = False)
    content = sa.Column(sa.String, nullable = False)
    published = sa.Column(sa.Boolean, server_default = 'True', nullable = False)
    created_at = sa.Column(sa.TIMESTAMP, server_default = sa.func.now(), nullable = False)


# SQLALCHEMY ORM
