import os
import sys
import asyncio
from dotenv import load_dotenv
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db import AIModel, init_db, close_db

def prettify_name(name: str) -> str:
    return name.replace('_', ' ').replace('-', ' ').title()

def get_model_type(path: str) -> str:
    # Get the immediate parent directory name
    return os.path.basename(os.path.dirname(path))

def get_model_name(filename: str) -> str:
    return os.path.splitext(os.path.basename(filename))[0]

def find_model_files(root_dir: str):
    model_files = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for fname in filenames:
            if fname.endswith('.safetensors') or fname.endswith('.pth'):
                full_path = os.path.join(dirpath, fname)
                model_files.append(full_path)
    return model_files

async def insert_models_to_db(model_files):
    for path in model_files:
        model_name = get_model_name(path)
        model_type = get_model_type(path)
        friendly_name = prettify_name(model_name)
        await AIModel.create(
            friendly_name=friendly_name,
            model_name=model_name,
            path=path,
            type=model_type
        )
        print(f"Inserted: {friendly_name} ({model_type}) -> {path}")

async def main():
    load_dotenv()
    db_url = os.getenv("DB_URL", "postgres://postgres:postgres@localhost:5432/vaultwares")
    models_dir = os.getenv("MODELS_DIR", "ai_model")
    await init_db(db_url)
    try:
        model_files = find_model_files(models_dir)
        await insert_models_to_db(model_files)
    finally:
        await close_db()

if __name__ == "__main__":
    asyncio.run(main())
