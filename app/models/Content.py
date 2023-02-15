from app import db

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    poster = db.Column(db.String)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    media_type = db.Column(db.String, nullable=False)
    vote_average = db.Column(db.Float, nullable=False)
    watchlists = db.relationship("Watchlist", back_populates="content") #users
    # genre = db.Column(db.String)     

    def to_dict(self):
        content_dict = {
            "id" :self.id, 
            "poster" :self.poster,
            "title" :self.title, 
            "date" :self.date, 
            "media_type" :self.media_type, 
            "vote_average" :self.vote_average   
        }

        watched_users = []
        for watched_user in self.watchlists:
            watched_users.append(watched_user.to_dict())
        content_dict["watchlists"] = watched_users
        
        return content_dict

    @classmethod
    def from_dict(cls, request_body):
        new_content = cls(
            poster = request_body["poster"],
            title = request_body["title"],
            date = request_body["date"],
            media_type = request_body["media_type"],
            vote_average = request_body["vote_average"]
        )
        return new_content