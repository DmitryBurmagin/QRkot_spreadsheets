from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base

from .base import CommonFields


class Donation(Base, CommonFields):

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    def __repr__(self):
        return (
            f'{super().__repr__()}, user_id={self.user_id}, '
            f'comment_length={len(self.comment)}'
        )
