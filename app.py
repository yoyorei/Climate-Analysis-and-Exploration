import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
        f"start (string): A date string in the format %Y-%m-%d<br/>"
        f"end (string): A date string in the format %Y-%m-%d"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(Measurement.date,Measurement.tobs).all()

    precipitation = []
    for data in results:
        precipitation_dict = {}
        precipitation_dict[data[0]] = data[1]
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station, Station.name).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    query_data = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date>=query_date).all()

    return jsonify(query_data)


@app.route("/api/v1.0/<start>")
def temperature(start):

    start_date=str(start)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    calc_tobs = list(np.ravel(results))

    return jsonify(calc_tobs)


@app.route("/api/v1.0/<start>/<end>")
def temp(start,end):
    start_date=str(start)
    end_date=str(end)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    calc_tobs = list(np.ravel(results))

    return jsonify(calc_tobs)

if __name__ == "__main__":
    app.run(debug=True)