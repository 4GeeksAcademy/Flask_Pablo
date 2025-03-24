from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum
import enum

# Elimine del segun "from" un "Boolean"
db = SQLAlchemy()

# Definimos un Enum para los tipos de media (imagen, video, etc.)
class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"

class Follower(db.Model):
    __tablename__ = "Follower"
    
    # Definimos las relaciones muchos a muchos
    user_from_id: Mapped[int] = mapped_column(db.ForeignKey('User.id'), primary_key=True)
    user_to_id: Mapped[int] = mapped_column(db.ForeignKey('User.id'), primary_key=True)

    # Relacionamos los dos usuarios que son parte de la relación
    user_from = db.relationship("User", foreign_keys=[user_from_id], back_populates="following")
    user_to = db.relationship("User", foreign_keys=[user_to_id], back_populates="followers")

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id
        }

class User(db.Model):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20))
    firstname: Mapped[str] = mapped_column(String(15))
    lastname: Mapped[str] = mapped_column(String(15))
    email: Mapped[str] = mapped_column()

    # Relación con los seguidores y a los que sigue a través de Follower
    followers = db.relationship("Follower", foreign_keys="[Follower.user_to_id]", back_populates="user_to", lazy="dynamic")
    following = db.relationship("Follower", foreign_keys="[Follower.user_from_id]", back_populates="user_from", lazy="dynamic")

    Comment = db.relationship("Comment", back_populates="User")
    Post = db.relationship("Post", back_populates="User")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }
    
class Comment (db.Model):
    __tablename__="Comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(db.ForeignKey('User.id')) #Conectado al parametro "id" del "class User"
    post_id: Mapped[int] = mapped_column(db.ForeignKey('Post.id')) #Conectado al parametro "id" del "class Post"

    User = db.relationship("User", back_populates="Comment") #Relaciona con el class "User"
    Post = db.relationship("Post", back_populates="Comment") #Relaciona con el class "Post"

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id
        }
    
class Post (db.Model):
    __tablename__="Post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey('User.id')) #Conectado al parametro "id" del "class User"

    Comment = db.relationship("Comment", back_populates="Post") #Relaciona con el class "Comment"
    User = db.relationship("User", back_populates="Post") #Relaciona con el class "User"
    Media = db.relationship("Media", back_populates="Post") #Relaciona con el class "Media"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }
    
class Media(db.Model):
    __tablename__ = "Media"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Usamos el Enum para definir el tipo de media
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)  # Aquí está el cambio
    
    url: Mapped[str] = mapped_column()  # URL del archivo de media
    post_id: Mapped[int] = mapped_column(db.ForeignKey('Post.id'))  # Conectado al "id" de la clase "Post"

    # Relación con la clase "Post" (un post puede tener múltiples archivos de media)
    Post = db.relationship("Post", back_populates="Media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.value,  # Devuelve el valor del enum como cadena
            "url": self.url,
            "post_id": self.post_id
        }