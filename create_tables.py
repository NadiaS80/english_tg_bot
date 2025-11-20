import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from config import DB_DSN

engine = sq.create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):

    __tablename__ = 'user'

    id = sq.Column(sq.BigInteger, primary_key = True)
    level_id = sq.Column(sq.Integer, sq.ForeignKey('level.id'), nullable=True)

    level = relationship('Level', backref='users')

class Level(Base):

    __tablename__ = 'level'

    id = sq.Column(sq.Integer, primary_key = True)
    name = sq.Column(sq.String(length=2))

class CommonWord(Base):

    __tablename__ = 'common_word'

    id = sq.Column(sq.Integer, primary_key = True)
    russian_word = sq.Column(sq.String(length=55))
    english_word = sq.Column(sq.String(length=45))
    example = sq.Column(sq.String(length=500))
    id_level = sq.Column(sq.Integer, sq.ForeignKey('level.id'), nullable=False)

    level = relationship('Level', backref='common_words')

class UserWord(Base):

    __tablename__ = 'user_word'

    id = sq.Column(sq.Integer, primary_key = True)
    russian_word = sq.Column(sq.String(length=55), nullable=True)
    english_word = sq.Column(sq.String(length=45))
    example = sq.Column(sq.String(length=500), nullable=True)
    id_user = sq.Column(sq.BigInteger, sq.ForeignKey('user.id'), nullable=False)

    user = relationship('User', backref='user_words')

def create_tables(engine):
    Base.metadata.create_all(engine) 

def delete_tables(engine):
    Base.metadata.drop_all(engine)