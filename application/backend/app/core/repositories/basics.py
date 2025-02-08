from sqlalchemy import insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.core.interfaces.repository import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: Session):
        self.session = session

    async def add_one(self, data: dict):
        stmt = insert(self.model).values(**data).returning(self.model.id)
        response = self.session.execute(stmt)

        return response

    async def find_all(self):
        stmt = select(self.model)
        response = self.session.execute(stmt)
        response = [model[0].to_read_model() for model in response]

        return response

    async def find_one(self, filter_data: dict):
        stmt = select(self.model).filter_by(**filter_data)
        response = self.session.execute(stmt)

        response_model = response.scalar_one_or_none()
        if response_model is not None:
            response_model = response_model.to_read_model()

        return response_model

    async def find_some(self, filter_data: dict):
        stmt = select(self.model).filter_by(**filter_data)
        response = self.session.execute(stmt)
        response = [model[0].to_read_model() for model in response]

        return response

    async def update_one(self, filter_data: dict, data: dict):
        stmt = select(self.model).filter_by(**filter_data)
        response = self.session.execute(stmt)

        try:
            model_object = response.scalars().one()
        except NoResultFound:
            return None

        for key, value in data.items():
            setattr(model_object, key, value)

        self.session.add(model_object)
        return model_object.to_read_model()

    async def update_many(self, filter_data: dict, data: dict):
        stmt = select(self.model).filter_by(**filter_data)
        result = self.session.execute(stmt)

        if not len(result.scalars().all()):
            return None

        for model in result:
            for key, value in data.items():
                setattr(model, key, value)

        self.session.add(result)
        return [model[0].to_read_model() for model in result]

    async def delete(self, filter_data: dict):
        stmt = select(self.model).filter_by(**filter_data)
        response = self.session.execute(stmt)

        try:
            model_object = response.scalars().one()
        except NoResultFound:
            return None

        self.session.delete(model_object)
        return model_object.to_read_model()
