import io
import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from matplotlib import pyplot as plt

from stats_advanced import Metrics
import base64

import matplotlib

matplotlib.use('Agg')

PATH_TO_TEMPLATE = os.path.join(os.path.dirname(__file__), '../templates')
PATH_TO_STATIC = os.path.join(os.path.dirname(__file__), '../static')

app = Flask(__name__, template_folder=PATH_TO_TEMPLATE, static_folder=PATH_TO_STATIC)
print(app.template_folder)
print(app.static_folder)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data/data.sqlite3'
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


@app.route('/')
def index():
    listings = Listings.query.all()
    return render_template('index.html', listings=listings)


@app.route('/search')
def search():
    # Get the query parameters
    sort_by = request.args.get('sort_by', 'id')
    sort_dir = request.args.get('sort_dir', 'asc')
    search_term = request.args.get('search_term', '')

    # Construct the query
    query = Listings.query.filter(Listings.name.ilike(f'%{search_term}%'))

    # Add sorting to the query
    sort_attr = getattr(Listings, sort_by)
    if sort_dir == 'asc':
        query = query.order_by(sort_attr.asc())
    else:
        query = query.order_by(sort_attr.desc())

    # Execute the query
    listings = query.all()

    # Render the template with the listings
    return render_template('search.html', listings=listings, sort_by=sort_by, sort_dir=sort_dir,
                           search_term=search_term)


@app.route('/chart')
def chart():
    metrics = Metrics()
    chart_data = metrics.mean_price_per_neighbourhood()
    return render_template('charts.html', chart_data=chart_data)


@app.route('/plots')
def plots():
    # Get data from get_all_visualizations method in stats_advanced.py and pass it to the template
    metrics = Metrics()
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(20, 20))
    mean_price_per_neighbourhood_svg = metrics.mean_price_per_neighbourhood()
    correlation_with_price_svg = metrics.correlation_with_price()
    heatmap_correlation_svg = metrics.heatmap_correlation()
    heatmap_density_of_listings_svg = metrics.heatmap_density_of_listings()
    most_common_room_type_svg = metrics.most_common_room_type()

    return render_template('plots.html',
                           mean_price_per_neighbourhood_svg=mean_price_per_neighbourhood_svg,
                           correlation_with_price_svg=correlation_with_price_svg,
                           heatmap_correlation_svg=heatmap_correlation_svg,
                           heatmap_density_of_listings_svg=heatmap_density_of_listings_svg,
                           most_common_room_type_svg=most_common_room_type_svg
                           )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
