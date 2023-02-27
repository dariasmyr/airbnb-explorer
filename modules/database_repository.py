from sqlalchemy import create_engine, Float
from sqlalchemy import Table, Column, Integer, String, MetaData
import logging
import csv

print('Connecting to database...')
engine = create_engine("sqlite+pysqlite:///:/../data/data.sqlite3", echo=True)
print('Connected to database!')

metadata = MetaData()

listings = Table('Listings', metadata,
                 Column('id', Integer, primary_key=True, nullable=False),
                 Column('name', String(255), nullable=False),
                 Column('host_id', Integer, nullable=False),
                 Column('host_name', String(255), nullable=False),
                 Column('neighbourhood_group', String(255), nullable=False),
                 Column('neighbourhood', String(255), nullable=False),
                 Column('latitude', Float, nullable=False),
                 Column('longitude', Float, nullable=False),
                 Column('room_type', String(255), nullable=False),
                 Column('price', Integer, nullable=False),
                 Column('minimum_nights', Integer, nullable=False),
                 Column('number_of_reviews', Integer, nullable=False),
                 Column('last_review', String, nullable=False),
                 Column('reviews_per_month', Float, nullable=False),
                 Column('calculated_host_listings_count', Integer, nullable=False),
                 Column('availability_365', Integer, nullable=False)
                 )

metadata.create_all(engine)


def load_data_to_db():
    file_path = 'data/cleared_data.csv'
    try:
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            conn = engine.connect()
            for row in reader:
                try:
                    ins = listings.insert().values(
                        id=int(row[0]),
                        name=row[1],
                        host_id=int(row[2]),
                        host_name=row[3],
                        neighbourhood_group=row[4],
                        neighbourhood=row[5],
                        latitude=float(row[6]),
                        longitude=float(row[7]),
                        room_type=row[8],
                        price=int(row[9]),
                        minimum_nights=int(row[10]),
                        number_of_reviews=int(row[11]),
                        last_review=row[12],
                        reviews_per_month=float(row[13]),
                        calculated_host_listings_count=int(row[14]),
                        availability_365=int(row[15])
                    )
                except Exception as e:
                    print("An error occurred while loading row to database. Please see the logs for details.")
                    logging.error(e)
                conn.execute(ins)
                print("Row loaded successfully to database.")
            conn.commit()
            conn.close()
    except Exception as e:
        print("An error occurred while loading data to database. Please see the logs for details.")
        logging.error(e)
        return
    print("Data loaded successfully to database.")


load_data_to_db()
