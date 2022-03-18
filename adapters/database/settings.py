from pydantic import BaseSettings


class Settings(BaseSettings):
    @property
    def DB_URL(self):
        # dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        # if os.path.exists(dotenv_path):
        #     load_dotenv(dotenv_path)
        #
        PG_USER = 'postgres'
        PG_PASSWORD = 'admin'
        PG_DBNAME = 'Project'
        PG_HOST= 'localhost'
        PG_PORT = '5432'

        return f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}"
