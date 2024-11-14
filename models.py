from extensions import db


class StudentModel(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer() ,unique = True)
    name = db.Column(db.String(),nullable=False)
    dob = db.Column(db.Date(), nullable=False)
    contact_info = db.Column(db.String(), nullable=False)
 
    def __init__(self, user_id,name,dob,contact_info):
        self.user_id_id = user_id
        self.name = name
        self.dob = dob
        self.contact_info = contact_info
 
    def __repr__(self):
        return f"{self.name}:{self.user_id}"