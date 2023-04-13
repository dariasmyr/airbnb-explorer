import os

import pandas as pd
from sqlalchemy import create_engine, Float, Table, Column, Integer, String, MetaData
import logging
import csv


class Database:
    def __init__(self, db_url):
        self.conn = None
        self.engine = create_engine(db_url)
        self.metadata = MetaData()
        self.listings = Table('Listings', self.metadata,
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
                              Column('availability_365', Integer, nullable=False))

    def connect(self):
        try:
            self.conn = self.engine.connect()
        except Exception as e:
            print("An error occurred while connecting to the database. Please see the logs for details.")
            logging.error(e)
            return

    def create_database(self):
        try:
            self.connect()
            self.metadata.create_all(self.engine)
            print("Database created successfully.")
        except Exception as e:
            print("An error occurred while creating the database. Please see the logs for details.")
            logging.error(e)
            return

    def save_data_to_db(self, cleaned_data):
        try:
            self.connect()
            with open(cleaned_data, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    try:
                        ins = self.listings.insert().values(
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
                    self.conn.execute(ins)
                    print("Row loaded successfully to database.")
                self.conn.commit()
        except Exception as e:
            print("An error occurred while loading data to database. Please see the logs for details.")
            logging.error(e)
            return
        print("Data loaded successfully to database.")

    def get_dataframe(self):
        df = pd.read_sql_table('Listings', self.conn)
        return df
