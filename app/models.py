from app import db

route_stops = db.Table('route_stops',
    db.Column('stop_id', db.Integer, db.ForeignKey('stop.id')),
    db.Column('route_id', db.String, db.ForeignKey('route.id'))
)

class Stop(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    boarding = db.Column(db.Float)
    alighting = db.Column(db.Float)
    on_street = db.Column(db.String(120))
    cross_street = db.Column(db.String(120))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    routes = db.relationship('Route', secondary=route_stops,
        backref=db.backref('stops', lazy='dynamic'))

    def __repr__(self):
        return '<Stop %r>' % (self.id)

    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Route(db.Model):
    id = db.Column(db.Integer, primary_key = True)

    def __repr__(self):
        return '<Route %r>' % (self.id)

    def to_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}