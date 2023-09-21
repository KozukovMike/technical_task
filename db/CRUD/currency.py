from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError

from statements.bd_models import create_session, Currency  # Подключаем модель Currency

class CRUDCurrency:

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
            select(Currency)
            .where(Currency.id == instance_id)
        )
        instance = instance.first()
        if instance:
            return instance[0]

    @staticmethod
    @create_session
    def all(session=None):
        instances = session.execute(
            select(Currency)
            .order_by(Currency.id)
        )
        return [i[0] for i in instances]

    @staticmethod
    @create_session
    def update(instance, session=None):
        instance = instance.__dict__
        del instance['_sa_instance_state']
        session.execute(
            update(Currency)
            .where(Currency.id == instance['id'])
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
            delete(Currency)
            .where(Currency.id == instance_id)
        )
        session.commit()

    @staticmethod
    @create_session
    def delete_all(session=None):
        session.execute(delete(Currency))
        session.commit()