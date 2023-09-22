from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, \
    VARCHAR, ForeignKey, create_engine, DATETIME, Text, String, Date, Float
from sqlalchemy.orm import relationship
from db.CRUD.settings import DATABASE_URL


Base = declarative_base()


class User(Base):
    __tablename__: str = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(VARCHAR(255), nullable=False, unique=True)
    password_hash = Column(VARCHAR(255), nullable=False)


class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


class UserRoleAssociation(Base):
    __tablename__ = 'user_role_association'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    role_id = Column(Integer, ForeignKey('roles.role_id'))

    # user = relationship('User', back_populates='roles')
    # role = relationship('Role', back_populates='users')


class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    Cur_Name = Column(String, nullable=False)
    Cur_ID = Column(Integer, nullable=False)
    Cur_DateStart = Column(Date, nullable=False)
    Cur_DateEnd = Column(Date, nullable=False)
    Cur_Scale = Column(Float, nullable=False)
    Cur_Offrate = Column(Float)


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def create_session(func):
    def wrapper(**kwargs):
        with Session() as session:
            return func(session=session, **kwargs)
    return wrapper


