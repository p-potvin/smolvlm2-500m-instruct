from tortoise import Tortoise, fields, models
import os

class AIModel(models.Model):
    id = fields.IntField(pk=True)
    friendly_name = fields.CharField(max_length=255)
    model_name = fields.CharField(max_length=255)
    path = fields.CharField(max_length=1024)
    type = fields.CharField(max_length=255)

    class Meta:
        table = "ai_models"

async def init_db(db_url: str):
    # Register both db and api_server modules for Tortoise ORM
    await Tortoise.init(
        db_url=db_url,
        modules={"models": ["db", "api_server"]}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()
