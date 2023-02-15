from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    watchLists = db.relationship("WatchList", back_populates="user") #contents

def to_dict(self):
    user_dict = {
        "id": self.id,
        "name": self.name,
        "email": self.email,
        "password": self.password
    }
    watched_contents = []
    for watched_content in self.watchLists:
        watched_contents.append(watched_content.to_dict())
    content_dict["watchLists"] = watched_contents
    
    user_dict["watchLists"] = watched_contents

@classmethod
def from_dict(cls, request_body):
    new_user = cls(
        name = request_body["name"],
        email = request_body["email"],
        password = request_body["password"]
    )
    return new_user