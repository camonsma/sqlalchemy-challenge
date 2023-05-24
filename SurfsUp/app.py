# Import the dependencies.
#Similar to class activites for flash import the source class or libraries needed.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
#Precipation query and result display#############################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    latest_date = dt.date(2017, 8 ,23)
# Calculate the date one year from the last date in data set.
    one_year_past = latest_date - dt.timedelta(days=365)
 #   print(str(one_year_past))

    results = session.query(Measurement.date, Measurement.prcp ).\
    filter(Measurement.date >= one_year_past).\
    filter(Measurement.date <= latest_date).all()

    session.close()

    # Convert list of tuples into normal list
    precipitation = list(np.ravel(results))

    return jsonify(precipitation)
#Station method or function 
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
#reuse the pandas or jupyter notebook code here in flask good use of "reuse"
    active_stations = session.query(Station.station, func.count(Measurement.station)).\
    filter(Station.station == Measurement.station).group_by(Station.station).\
    order_by(func.count(Measurement.station).desc()).all()
  
    session.close()

    # Convert list of tuples into normal list
    stations = list(np.ravel(active_stations))

    return jsonify(stations)

#TOBS or temperatures############################################################################
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
#reuse the pandas or jupyter notebook code here in flask good use of "reuse"
    latest_date = dt.date(2017, 8 ,23)
# Calculate the date one year from the last date in data set.
    one_year_past = latest_date - dt.timedelta(days=365)
 
    temp_results = session.query(Measurement.date, Measurement.tobs ).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= one_year_past).\
    filter(Measurement.date <= latest_date).all()  
    session.close()

    # Convert list of tuples into normal list
    temps = list(np.ravel(temp_results))

    return jsonify(temps)

#Query based on dates from the input screen.##################################
@app.route("/api/v1.0/<start>")
def temp_average(start):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""
    session = Session(engine)
    one_day_result = session.query(Measurement.date, Measurement.tobs ).\
    filter(Measurement.date == start).all()
    session.close()

    one_day = list(np.ravel(one_day_result.sort(['tobs'])))

    return jsonify(one_day)
#######################################################################################
#Query based on dates from the input screen.##################################
@app.route("/api/v1.0/<start>/<end>")
def more_stuff(start, end):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""
    session = Session(engine)
    n_day_result = session.query(Measurement.date, Measurement.tobs ).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()

    n_day = list(np.ravel(n_day_result.sort(['tobs'])))

    return jsonify(n_day)

####END OF THE ROUTES OR METHODS FOR THE EXECUTION CLASS#######################################

#The app call to the main or execution function for python
if __name__ == '__main__':
    app.run(debug=True)