from sqlalchemy import create_engine
from sqlalchemy import text


print('Connecting to database...')
engine = create_engine("sqlite+pysqlite:///:/../data/data.sqlite3", echo=True)
print('Connected to database!')

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())

