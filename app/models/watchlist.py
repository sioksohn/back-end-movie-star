from app import db

class Watchlist(db.Model):
    __tablename__ = "watchlist"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    viewer_id = db.Column(db.Integer, db.ForeignKey('viewer.id'), primary_key=True,nullable=False )
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), primary_key=True,nullable=False)
    viewer = db.relationship("Viewer", back_populates="watchlists")
    content = db.relationship("Content", back_populates="watchlists")
    #viewer_rate = db.Column(db.Float)

    def to_dict(self):
        watchlist_dict = {
            "id": self.id,
            "viewer_id": self.viewer_id,
            "content_id": self.content_id,
            # "viewer_rate": self.viewer_rate      
        }
        return watchlist_dict

    @classmethod
    def from_dict(cls, request_body):
        new_obj = cls(
            viewer_id = request_body["viewer_id"],
            content_id = request_body["content_id"]
            # viewer_rate = request_body["viewer_rate"]
        )
        return new_obj