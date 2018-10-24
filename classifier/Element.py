from classifier.config import db, ma


class Element(db.Model):
    __tablename__ = "elements"
    id = db.Column(db.Integer, primary_key=True)
    elementName = db.Column(db.String(50))
    isEnd = db.Column(db.Integer)
    isIndexed = db.Column(db.Integer)
    isRoot = db.Column(db.Integer)
    parentElementId = db.Column(db.Integer)


class ElementSchema(ma.ModelSchema):
    class Meta:
        model = Element
        sqla_session = db.session
