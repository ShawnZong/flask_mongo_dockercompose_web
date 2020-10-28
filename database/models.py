from .db import db


class Professor(db.Document):
    ENUM_DESIGNATION = ('Professor', 'Assistant Professor',
                        'Associate Professor')
    name = db.StringField(max_length=20, required=True, unique=True)
    designation = db.StringField(required=True, choices=ENUM_DESIGNATION)
    email = db.StringField(max_length=20)
    interests = db.ListField(db.StringField())
    researchGroups = db.ListField(db.ReferenceField('ResearchGroup'))
    # complete the remaining code


class ResearchGroup(db.Document):
    name = db.StringField(max_length=20, required=True, unique=True)
    description = db.StringField(max_length=1000)
    founder = db.ReferenceField('Professor', required=True)
    # complete the remaining code


class Student(db.Document):
    name = db.StringField(max_length=20, required=True, unique=True)
    studentNumber = db.StringField(max_length=20, required=True, unique=True)
    researchGroups = db.ListField(db.ReferenceField('ResearchGroup'))
    # complete the remaining code
