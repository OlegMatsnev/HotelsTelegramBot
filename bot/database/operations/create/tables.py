from bot.database.models import get_all_models
from bot.database import db

db.connect()
all_models = get_all_models()


def create_tables():
    with db:
        cursor = db.cursor()
        # Проверяем и удаляем существующие таблицы
        for model in all_models:
            table_name = model._meta.table_name
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

        # Создаем новые таблицы
        db.create_tables(all_models)


if __name__ == "__main__":
    create_tables()
