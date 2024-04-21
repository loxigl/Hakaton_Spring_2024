from core.db_base import Base, createEngine


def create_tables(engine=createEngine):
    for names in Base.metadata.tables:
        print(names)
    Base.metadata.create_all(engine, checkfirst=True)


def drop_tables(engine=createEngine):
    Base.metadata.drop_all(engine, checkfirst=True)
