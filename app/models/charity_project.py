from sqlalchemy import Column, String, Text

from app.core.db import Base, CommonFields

MAX_STRING_LENGTH = 100


class CharityProject(Base, CommonFields):

    name = Column(String(MAX_STRING_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
