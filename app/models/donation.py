from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base

from .base import CommonFields


class Donation(Base, CommonFields):

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    def __repr__(self):
        base_repr = super().__repr__()
        return (
            f'{base_repr}, user_id={self.user_id}, '
            f'comment_length={len(self.comment) if self.comment else 0}>'
        )
