from os import stat
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

end_date = dt.date(2017, 8, 23)
start_date = end_date - dt.timedelta(days = 365)

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """All the Hawaii Information you could ever want, as long as it's about precipitation"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"//api/v1.0/<start>/<end>"

    )




@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)



    """Return a list of all precipitation"""
    # Query all stations

   
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start_date).all()

    prec_df = pd.DataFrame(precipitation, columns = ['Date', 'Precipitation']).set_index('Date')

    # Sort the dataframe by date
    prec_df = prec_df.sort_values('Date')

    session.close()

    return jsonify(precipitation)






@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)
       
    # Query all stations

    station_names = session.query(Station.name).all()


    session.close()

    return jsonify(station_names)

    # Create a dictionary from the row data and append to a list of all_stations
    # all_stations = []
    # for name, age, sex in results:
    #     passenger_dict = {}
    #     passenger_dict["name"] = name
    #     passenger_dict["age"] = age
    #     passenger_dict["sex"] = sex
    #     all_stations.append(passenger_dict)

    # return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    ordered_stations = session.query(Measurement.station, Station.name, func.count(Measurement.station))\
    .filter(Measurement.station == Station.station)\
    .group_by(Measurement.station)\
    .order_by(func.count(Measurement.station)\
    .desc()).all()

    # The whole row
    most_active_row = ordered_stations[0]
  
    # Just the station ID
    most_active = ordered_stations[0][0]
    
       
    # Query all stations

    station_tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs).order_by(Measurement.date.desc()).\
        filter(Measurement.station == most_active).filter(Measurement.date >= start_date).all()


    session.close()

    return jsonify(station_tobs)


@app.route("/api/v1.0/<start>")
def start():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)
       
    # Query all stations

    start_query = session.query(Measurement.date).filter(Measurement.date > start_date)


    session.close()

    return jsonify(start_query)


@app.route("/api/v1.0/<start>/<end>")
def end():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)
       
    # Query all stations

    start_query = session.query(Measurement.date).filter(Measurement.date > start_date)


    session.close()

    return jsonify(start_query)

if __name__ == '__main__':
    app.run(debug=True)
