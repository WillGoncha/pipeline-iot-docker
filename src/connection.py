from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg://iot_user:iot_password@127.0.0.1:5432/iot_database"

engine = create_engine(DATABASE_URL)