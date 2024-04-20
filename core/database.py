from core.db_base import Base, createEngine


def create_tables(engine=createEngine):
    Base.metadata.create_all(engine)


def drop_tables(engine=createEngine):
    Base.metadata.drop_all(engine)
