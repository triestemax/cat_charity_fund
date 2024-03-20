from datetime import datetime
from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer


from app.core.db import Base


class ProjectDonationBase(Base):
    """Базовая абстрактная модель родителя
    для моделей проекта и пожертвования."""
    __abstract__ = True

    full_amount = Column(
        Integer,
        CheckConstraint('full_amount > 0'),
        nullable=False,
    )
    invested_amount = Column(
        Integer,
        CheckConstraint('invested_amount >= 0'),
        nullable=False,
        default=0,
    )
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now)
    close_date = Column(DateTime)
