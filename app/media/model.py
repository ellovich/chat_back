from app.database import BaseAlchemyModel
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey

class Media(BaseAlchemyModel):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    file_data = Column(LargeBinary)
    user_id = Column(Integer, ForeignKey('user.id'))