import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from metrics import Metrics

import matplotlib

matplotlib.use('Agg')

PATH_TO_TEMPLATE = os.path.join(os.path.dirname(__file__), '../templates')
PATH_TO_STATIC = os.path.join(os.path.dirname(__file__), '../static')

app = Flask(__name__, template_folder=PATH_TO_TEMPLATE, static_folder=PATH_TO_STATIC)
print(app.template_folder)
print(app.static_folder)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/data_bak.sqlite3'
db = SQLAlchemy(app)


class Listings(db.Model):
    __tablename__ = 'Listings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    host_id = db.Column(db.Integer, nullable=False)
    host_name = db.Column(db.String(255), nullable=False)
    neighbourhood_group = db.Column(db.String(255), nullable=False)
    neighbourhood = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    room_type = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    minimum_nights = db.Column(db.Integer, nullable=False)
    number_of_reviews = db.Column(db.Integer, nullable=False)
    last_review = db.Column(db.String, nullable=False)
    reviews_per_month = db.Column(db.Float, nullable=False)
    calculated_host_listings_count = db.Column(db.Integer, nullable=False)
    availability_365 = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Listings %r>' % self.id


@app.route('/table')
def index():
    listings = Listings.query.limit(100).all()
    return render_template('table.html', title="Listings in NYC", listings=listings)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
