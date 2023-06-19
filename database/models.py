import asyncio

import databases
import orm

database = databases.Database("sqlite:///db.sqlite")
models = orm.ModelRegistry(database=database)


class User(orm.Model):
    tablename = "users"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "uid": orm.Integer(unique=True),
        "last_publication": orm.Integer(default=0)
    }


class Publication(orm.Model):
    tablename = "publications"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "author": orm.ForeignKey(User),
        "data_channel": orm.JSON()
    }


async def main(*args):
    return await models.create_all()

