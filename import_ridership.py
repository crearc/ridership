from app import db, models
import csv  
from ast import literal_eval as make_tuple

with open('ridership_raw.csv', 'rb') as f:
    # Clear Database
    models.Stop.query.delete()
    models.Route.query.delete()
    db.session.commit()

    reader = csv.reader(f)
    reader.next()
    for row in reader:
        routes = [r for r in row[3].split(',')]
        location = make_tuple(str(row[6]))
        # Create routes connected to this stop
        route_objects = []
        for route in routes:
            if route == '':
                continue
            r = models.Route.query.get(route.strip())
            if r:
                route_objects.append(r)
                continue
            r = models.Route(id=route.strip())
            db.session.add(r)
            route_objects.append(r)
        # Now create stop
        s = models.Stop(id=int(row[0]),
                        on_street=row[1],
                        cross_street=row[2],
                        boarding=row[4],
                        alighting=row[5],
                        lat=location[0],
                        lng=location[1],
                        routes=route_objects
                        )
        db.session.add(s)
        print s
        db.session.commit()