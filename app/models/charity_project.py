from sqlalchemy import Column, String, Text


from app.models.base import ProjectDonationBase


class CharityProject(ProjectDonationBase):
    """Модель благотворительного проекта."""
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Благотворительный проект {self.name}: {self.description}'
        )
