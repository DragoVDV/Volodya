from flask_sqlalchemy import SQLAlchemy


from db_setup import db  # Use absolute import


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Establishing a relationship with the Person model
    people = db.relationship('Person', backref='city', lazy=True)

class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=False)

    # Optionally, you can define a method for a more readable string representation
    def __repr__(self):
        return f'<Person {self.name}>'
