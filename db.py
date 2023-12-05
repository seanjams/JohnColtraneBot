import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, desc, Column, DateTime, Enum, Integer, JSON, String
from sqlalchemy.sql import func
from utils import todays_date, yesterdays_date

from config import app

db = SQLAlchemy()

# Base class for models with app context
class Model(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    def save(self):
        with app.app_context():
            db.session.add(self)
            db.session.commit()


class JobStatus(enum.Enum):
    error = 0
    success = 1


class JobRun(Model):
    __tablename__ = "job_runs"

    name = Column(String, nullable=False)
    status = Column(Enum(JobStatus), nullable=False)
    data = Column(JSON)

    def json(self):
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "name": self.name,
            "status": self.status.name,
        }


# class LightStatus(Model):
#     __tablename__ = "light_status"

#     name = Column(String, nullable=False)
#     on = Column(Boolean, default=False)
#     hue = Column(Integer, nullable=False)
#     brightness = Column(Integer, nullable=False)
#     saturation = Column(Integer, nullable=False)

#     def json(self):
#         return {
#             "id": self.id,
#             "created_at": self.created_at.isoformat(),
#             "name": self.name,
#             "on": self.on,
#             "hue": self.hue,
#             "brightness": self.brightness,
#             "saturation": self.saturation,
#         }
    
#     @classmethod
#     def get_last_saved(cls):
#         with app.app_context():
#             return cls.query.filter(
#                 cls.created_at.between(yesterdays_date(), todays_date())
#             ).order_by(desc('created_at')).first()

