from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
db = SQLAlchemy()
class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    url = db.Column(db.String(50))
    programa = db.Column(db.String())
    
class MenuSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Menu
        load_instance = True
    id = fields.String()
    nombre = fields.String()
    url = fields.String()
    programa = fields.String()
    