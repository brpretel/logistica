import databases
import sqlalchemy
from decouple import config

DATABASE_URL = f"postgresql://postgres:v5ZtSSMP4DogMNQW8YdO@containers-us-west-177.railway.app:6326/railway"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()