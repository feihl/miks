from pydantic import BaseModel
from typing import Optional, List

# User model for creating and updating users
class UserCreate(BaseModel):
    username: str
    password: str
    email: str

# Playlist model for creating and updating playlists
class PlaylistCreate(BaseModel):
    name: str
    user_id: int

class PlaylistUpdate(BaseModel):
    name: str

# Song model for creating and updating songs
class SongCreate(BaseModel):
    title: str
    artist: Optional[str]
    album: Optional[str]
    duration: Optional[int]

# Model for updating user passwords
class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

# Bulk song addition/removal for playlists
class BulkSongUpdate(BaseModel):
    song_ids: List[int]

# Pydantic model for login
class Login(BaseModel):
    username: str
    password: str

# User database model example
class User:
    # Replace with your ORM model definition
    username: str
    hashed_password: str
