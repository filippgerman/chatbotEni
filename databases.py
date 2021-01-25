from sqlalchemy import create_engine, Table, MetaData, Column, BIGINT, String, Integer, FLOAT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import pymysql

pymysql.install_as_MySQLdb()
engine = create_engine("mysql://huston:fil@localhost/pars", encoding="utf8")

Base = declarative_base()
Session = sessionmaker(bind=engine)


class Einstein(Base):
    __tablename__ = 'Einstein'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(1000, collation='utf8mb4_unicode_ci'), index=True)
    number_game = Column(Integer)
    points = Column(FLOAT)

    def __init__(self, name, number_game, points):
        self.name = name
        self.number_game = number_game
        self.points = points


class KvizPlease(Base):
    __tablename__ = 'KvizPlease'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(100, collation='utf8mb4_unicode_ci'), index=True)
    number_game = Column(Integer)
    points = Column(FLOAT)

    def __init__(self, name, number_game, points):
        self.name = name
        self.number_game = number_game
        self.points = points


class Kvizium(Base):
    __tablename__ = 'Kvizium'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(1000, collation='utf8mb4_unicode_ci'), index=True)
    number_game = Column(Integer)
    points = Column(FLOAT)

    def __init__(self, name, number_game, points):
        self.name = name
        self.number_game = number_game
        self.points = points


class BrainBoy(Base):
    __tablename__ = 'BrainBoy'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(1000, collation='utf8mb4_unicode_ci'), index=True)
    number_game = Column(Integer)
    points = Column(FLOAT)

    def __init__(self, name, number_game, points):
        self.name = name
        self.number_game = number_game
        self.points = points


class Mozgva(Base):
    __tablename__ = 'Mozgva'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(100, collation='utf8mb4_unicode_ci'), index=True)
    number_game = Column(Integer)
    points = Column(FLOAT)

    def __init__(self, name, number_game, points):
        self.name = name
        self.number_game = number_game
        self.points = points


class Squiz(Base):
    __tablename__ = 'Squiz'

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    name = Column(String(100, collation='utf8mb4_unicode_ci'), index=True)
    number_game = Column(Integer)
    points = Column(FLOAT)

    def __init__(self, name, number_game, points):
        self.name = name
        self.number_game = number_game
        self.points = points


Base.metadata.create_all(engine)
session = Session()

