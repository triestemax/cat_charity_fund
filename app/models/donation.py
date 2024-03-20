from sqlalchemy import Column, ForeignKey, Integer, Text


from app.models.base import ProjectDonationBase


class Donation(ProjectDonationBase):
    """Модель пожертвования."""
    user_id = Column(
        Integer,
        ForeignKey('user.id', name='fk_donation_user_id_user'),
    )
    comment = Column(Text)

    def __repr__(self):
        return (
            f'Сделано пожертвование {self.full_amount} '
            f'и оставлен комментарий {self.comment}'
        )
