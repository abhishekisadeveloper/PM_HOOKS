# base.py exists so there is only one BCCI. Every model signs up there, so SQLAlchemy can see the entire squad together — create all tables at once, and let Task point its bat at Project.
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
