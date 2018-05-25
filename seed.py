"""Utility file to seed points database from tsv files in seed_data"""

from sqlalchemy import func
from models import Waypoint

from models import connect_to_db, db
from server import app

import glob
import os
import re
import string
path = "./seed_data/*.tsv"


def load_waypoints():
    """Load waypoints from all tsv in seed_data"""

    print "Waypoints"

    # Delete all rows in table to prevent duplicates
    # in case of need to re-seed
    Waypoint.query.delete()

    # Read all .tsv files in seed_data and insert data

    for fname in glob.glob(path):
        with open(fname) as f:
            content = f.readlines()[1:]
            for row in content:
                row = row.rstrip()
                row = re.split(r'\t+', row)
                if "##" in row[-1]:
                    not_useful = row[-1].find("##")
                    if not_useful >= 32:
                        row[-1] = row[-1][:not_useful]
                if "NULL" in row[-1]:
                    continue
                if "Bound" in row[-1]:
                    continue
                print row[-1]
                lat_long = row[-1].split(",")
                lat= lat_long[0]
                lng = lat_long[-1]

                printable = set(string.printable)
                latitude = filter(lambda x: x in printable, lat)
                latitude = latitude[0:2]+" "+latitude[2:4]+" "+latitude[4:-1]

                printable = set(string.printable)
                longitude = filter(lambda x: x in printable, lng)
                longitude = "-"+longitude[0:3]+" "+longitude[3:5]+" "+longitude[5:-1]

                point = [row[0], latitude, longitude]
                waypoint = Waypoint(latitude=point[1],
                                    longitude=point[2],
                                    location=point[0],
                                    )
                # Add waypoint to db session
                db.session.add(waypoint)
    # Commit waypoints
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # # In case tables haven't been created, create them
    db.create_all()

    # Import data type
    load_waypoints()
       