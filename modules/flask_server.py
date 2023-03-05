import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from stats_advanced import Metrics
from io import StringIO
import base64

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


@app.route('/chart')
def chart():
    metrics = Metrics()
    chart_data = metrics.mean_price_per_neighbourhood()
    return render_template('charts.html', chart_data=chart_data)


@app.route('/plots')
def plots():
    metrics = Metrics()
    # Create the plots
    fig1 = metrics.mean_price_per_neighbourhood()
    fig2 = metrics.correlation_with_price()
    fig3 = metrics.heatmap_correlation()
    fig4 = metrics.heatmap_density_of_listings()
    fig5 = metrics.most_common_room_type()
    fig6 = metrics.percentage_of_available_listings_from()

    # Save the plots to SVG files
    io1 = StringIO()
    fig1.savefig(io1, format='svg', bbox_inches='tight')
    io1.seek(0)
    plot_url1 = base64.b64encode(io1.getvalue().encode()).decode()

    io2 = StringIO()
    fig2.savefig(io2, format='svg', bbox_inches='tight')
    io2.seek(0)
    plot_url2 = base64.b64encode(io2.getvalue().encode()).decode()

    io3 = StringIO()
    fig3.savefig(io3, format='svg', bbox_inches='tight')
    io3.seek(0)
    plot_url3 = base64.b64encode(io3.getvalue().encode()).decode()

    io4 = StringIO()
    fig4.savefig(io4, format='svg', bbox_inches='tight')
    io4.seek(0)
    plot_url4 = base64.b64encode(io4.getvalue().encode()).decode()

    io5 = StringIO()
    fig5.savefig(io5, format='svg', bbox_inches='tight')
    io5.seek(0)
    plot_url5 = base64.b64encode(io5.getvalue().encode()).decode()

    io6 = StringIO()
    fig6.savefig(io6, format='svg', bbox_inches='tight')
    io6.seek(0)
    plot_url6 = base64.b64encode(io6.getvalue().encode()).decode()

    # Render the HTML page with the plots
    return render_template('plots.html', plot_url1=plot_url1, plot_url2=plot_url2, plot_url3=plot_url3, plot_url4=plot_url4, plot_url5=plot_url5, plot_url6=plot_url6)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
