import os


class Config:
    DB_USER = os.getenv("MYSQL_USER", "todo_user")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "todo_password")
    DB_HOST = os.getenv("MYSQL_HOST", "mysql")
    DB_PORT = os.getenv("MYSQL_PORT", "3306")
    DB_NAME = os.getenv("MYSQL_DATABASE", "todo_db")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False