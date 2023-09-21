from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from statements.bd_models import create_session, User


class CRUDUser:

    @staticmethod
    @create_session
    def add(instance, session=None):
        session.add(instance)
        try:
            session.commit()
        except IntegrityError:
            return None
        else:
            session.refresh(instance)
            return instance

    @staticmethod
    @create_session
    def get(instance_id, session=None):
        instance = session.execute(
            select(User)
            .where(User.user_id == instance_id)
        )
        instance = instance.first()
        if instance:
            return instance[0]

    @staticmethod
    @create_session
    def get_by_username(instance, session=None):
        instance = session.execute(
            select(User)
            .where(User.username == instance)
        )
        instance = instance.first()
        if instance:
            return instance[0]

    @staticmethod
    @create_session
    def all(session=None):
        instances = session.execute(
            select(User)
            .order_by(User.user_id)
        )
        return [i[0] for i in instances]

    @staticmethod
    @create_session
    def update(instance, session=None):
        instance = instance.__dict__
        del instance['_saUrl_instance_state']
        session.execute(
            update(User)
            .where(User.user_id == instance['user_id'])
            .values(**instance)
        )
        try:
            session.commit()
        except IntegrityError:
            return False
        else:
            return True

    @staticmethod
    @create_session
    def delete(instance_id, session=None):
        session.execute(
            delete(User)
            .where(User.user_id == instance_id)
        )
        session.commit()
