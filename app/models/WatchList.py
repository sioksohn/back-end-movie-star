from app import db

class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'))
    #user_rate = db.Column(db.Float)
    user = db.relationship("User", back_populates="watchLists")
    content = db.relationship("Content", back_populates="watchLists")

    def to_dict(self):
        watchlist_dict = {
            "id": self.id,
            "user_id": self.user_id,
            "content_id": self.content_id,
            # "user_rate": self.user_rate      
        }
        return watchlist_dict

    @classmethod
    def from_dict(cls, request_body):
        new_obj = cls(
            user_id = request_body["user_id"],
            content_id = request_body["content_id"]
            # user_rate = request_body["user_rate"]
        )
        return new_obj