import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum

Base = declarative_base()

class EDTItem(Base):
    __tablename__ = ''
    id = Column(Integer, primary_key=True)
    etudiant = Column(String, nullable=False)
    semestre = Column(String, nullable=False)
    uv = Column(String, nullable=False)
    type = Column(Enum('D', 'T', 'C'), nullable=False)
    num = Column(Integer, nullable=False)
    jour = Column(Enum("Lundi", "Mardi", "Mercredi" "Jeudi", "Vendredi" "Samedi", "Dimanche"), nullable=False)
    # debut = Column()
    # debut = Column()
    frequence = Column(Integer, nullable=False)
    semaine = Column(Enum('A', 'B'))
    salle = Column(String, nullable=False)
