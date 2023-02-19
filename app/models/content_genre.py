from app import db

class ContentGenre(db.Model):
    __tablename__ = "content_genre"    
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), primary_key=True, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True, nullable=False )

    def to_dict(self):
        content_genre_dict = {
            "content_id": self.content_id,
            "genre_id": self.genre_id,    
        }
        return content_genre_dict

    @classmethod
    def from_dict(cls, request_body):
        new_obj = cls(
            content_id = request_body["content_id"],
            genre_id = request_body["genre_id"],
        )
        return new_obj