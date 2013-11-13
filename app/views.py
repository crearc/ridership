from app import app, models, db
from flask import render_template, url_for, json
from sqlalchemy.sql import select, func

@app.route('/')
@app.route('/index')
def index():
    routes = models.Route.query.all()
    return render_template("index.html",
        title='Home',
        routes=routes)

@app.route('/agg')
def aggregates():
    # Average difference in boarding/alighting
    boarding_avg = models.Stop.query.\
            with_entities(func.avg(models.Stop.boarding).label('average')).all()[0][0]
    alighting_avg = models.Stop.query.\
            with_entities(func.avg(models.Stop.alighting).label('average')).all()[0][0]

    boarding_sum = models.Stop.query.\
            with_entities(func.sum(models.Stop.boarding).label('sum')).all()[0][0]
    alighting_sum = models.Stop.query.\
            with_entities(func.sum(models.Stop.boarding).label('sum')).all()[0][0]

    diff = boarding_avg - alighting_avg
    print boarding_avg, alighting_avg, diff, boarding_sum, alighting_sum

    # routes = models.Route.query.all()
    # for route in routes:
    #     avg_ridership_per_route = models.Stop.query.\
    #         with_entities(func.avg(models.Stop.alighting).label('average')).\
    #         filter(Stop.routes == route.id)

    # print avg_ridership_per_route


    # q = db.session.query(models.Route).join((models.Stop, models.Route.stops)) \
    #     .with_entities(func.avg(models.Stop.boarding).label('avg')).filter(models.Route == '24')

    routes = models.Route.query.all()
    avgs = []
    for route in routes:
        b_sum = 0
        a_sum = 0
        for stop in route.stops:
            b_sum += stop.boarding
            a_sum += stop.alighting
        avgs.append((route, b_sum/len(route.stops.all()), a_sum/len(route.stops.all())))



    return render_template("agg.html",
        title='Aggregates',
        aggs=[boarding_avg,alighting_avg, diff],
        route_avgs=avgs)

@app.route('/api/routes/<id>', methods=['GET'])
def route_lookup(id):
    route = models.Route.query.get(id)
    serialized = []
    for stop in route.stops.all():
        serialized.append(stop.to_dict())
    return json.dumps(serialized)
