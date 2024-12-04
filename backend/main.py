from fastapi import FastAPI, HTTPException
from models import UserCreate, PlaylistCreate, SongCreate, PasswordUpdate, BulkSongUpdate, User, Login, PlaylistUpdate
from db import get_db
import bcrypt

app = FastAPI()

# USER CRUD FUNCTIONS
# 1. Create a new user
@app.post("/users/")
def create_user(user: UserCreate):
    """Create a new user without encrypting the password (not recommended)."""
    db = get_db()
    cursor = db.cursor()

    # Directly store the plain password (not secure)
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                   (user.username, user.email, user.password))
    db.commit()
    db.close()

    return {"msg": "User created successfully"}

# # 4. Update user details
# @app.put("/users/{user_id}")
# def update_user(user_id: int, user: UserCreate):
#     """Update user details."""
#     db = get_db()
#     cursor = db.cursor()
#     hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
#     cursor.execute("UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s", 
#                    (user.username, user.email, hashed_password, user_id))
#     db.commit()
#     return {"msg": "User updated successfully"}

# # 5. Delete a user
# @app.delete("/users/{user_id}")
# def delete_user(user_id: int):
#     """Delete a user by ID."""
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
#     db.commit()
#     return {"msg": "User deleted"}

# @app.post("/login/")
# def login_user(login: Login):
#     """
#     Authenticate the user by validating their username and password.
#     """
#     db = get_db()
#     cursor = db.cursor()

#     # Query to find the user by username
#     cursor.execute("SELECT username, password FROM users WHERE username = ?", (login.username,))
#     user = cursor.fetchone()
#     db.close()

#     # Check if user exists and if the password matches
#     if not user or user[1] != login.password:
#         raise HTTPException(status_code=400, detail="Invalid username or password")
    
#     return {"msg": "Login successful", "username": user[0]}

# # 2. Get all users
# @app.get("/users/")
# def get_all_users():
#     """Retrieve all users."""
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM users")
#     users = cursor.fetchall()
#     db.close()
#     return users

# # 3. Get a specific user by ID
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     """Retrieve user details by user ID."""
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
#     user = cursor.fetchone()
#     db.close()
#     return user

# # 6. Update user password
# @app.put("/users/{user_id}/password")
# def update_password(user_id: int, password_data: PasswordUpdate):
#     """Update the user's password."""
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
#     user = cursor.fetchone()
    
#     if not bcrypt.checkpw(password_data.old_password.encode('utf-8'), user['password'].encode('utf-8')):
#         raise HTTPException(status_code=400, detail="Old password is incorrect")

#     hashed_password = bcrypt.hashpw(password_data.new_password.encode('utf-8'), bcrypt.gensalt())
#     cursor.execute("UPDATE users SET password = %s WHERE id = %s", 
#                    (hashed_password, user_id))
#     db.commit()
#     db.close()
#     return {"msg": "Password updated successfully"}

# PLAYLIST CRUD FUNCTIONS
# 7. Create a new playlist
@app.post("/playlists/")
def create_playlist(playlist: PlaylistCreate):
    """Create a new playlist for a user."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO playlists (name, user_id) VALUES (?, ?)", 
                   (playlist.name, playlist.user_id))
    db.commit()
    db.close()
    return {"msg": "Playlist created"}

# 8. Get all playlists
@app.get("/playlists/")
def get_all_playlists():
    """Retrieve all playlists."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM playlists")
    playlists = cursor.fetchall()  # Rows are now accessible as dictionaries
    db.close()
    return playlists 

# 9. Get a specific playlist by ID
@app.get("/playlists/{playlist_id}")
def get_playlist(playlist_id: int):
    """Retrieve playlist details by playlist ID."""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM playlists WHERE id = ?", (playlist_id,))
    playlist = cursor.fetchone()
    db.close()
    return playlist

# 10. Update playlist details
@app.put("/playlists/{playlist_id}")
def update_playlist(playlist_id: int, playlist: PlaylistUpdate):
    """Update playlist details."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE playlists SET name = ? WHERE id = ?", 
                   (playlist.name, playlist_id))
    db.commit()
    db.close()
    return {"msg": "Playlist updated"}

# 11. Delete a playlist
@app.delete("/playlists/{playlist_id}")
def delete_playlist(playlist_id: int):
    """Delete a playlist by ID."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM playlists WHERE id = ?", (playlist_id,))
    db.commit()
    db.close()
    return {"msg": "Playlist deleted"}

# # SONG CRUD FUNCTIONS
# # 12. Add a new song
# @app.post("/songs/")
# def add_song(song: SongCreate):
#     """Add a new song to the database."""
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("INSERT INTO songs (title, artist, album, duration) VALUES (%s, %s, %s, %s)", 
#                    (song.title, song.artist, song.album, song.duration))
#     db.commit()
#     db.close()
#     return {"msg": "Song added"}

# # 13. Get all songs
# @app.get("/songs/")
# def get_all_songs():
#     """Retrieve all songs."""
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM songs")
#     songs = cursor.fetchall()
#     db.close()
#     return songs

# # 14. Get a specific song by ID
# @app.get("/songs/{song_id}")
# def get_song(song_id: int):
#     """Retrieve song details by song ID."""
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM songs WHERE id = %s", (song_id,))
#     song = cursor.fetchone()
#     db.close()
#     return song

# # 15. Search for songs by title
# @app.get("/songs/search/")
# def search_songs(title: str):
#     """Search for songs by title."""
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM songs WHERE title LIKE %s", (f"%{title}%",))
#     songs = cursor.fetchall()
#     db.close()
#     return songs

# # 16. Update song details
# @app.put("/songs/{song_id}")
# def update_song(song_id: int, song: SongCreate):
#     """Update song details."""
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("UPDATE songs SET title = %s, artist = %s, album = %s, duration = %s WHERE id = %s", 
#                    (song.title, song.artist, song.album, song.duration, song_id))
#     db.commit()
#     db.close()
#     return {"msg": "Song updated"}

# # 17. Delete a song
# @app.delete("/songs/{song_id}")
# def delete_song(song_id: int):
#     """Delete a song by ID."""
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("DELETE FROM songs WHERE id = %s", (song_id,))
#     db.commit()
#     db.close()
#     return {"msg": "Song deleted"}

# # PLAYLIST_SONGS CRUD FUNCTIONS
# # 18. Add a song to a playlist
# @app.post("/playlists/{playlist_id}/songs/{song_id}")
# def add_song_to_playlist(playlist_id: int, song_id: int):
#     """Add a song to a specified playlist."""
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)", 
#                    (playlist_id, song_id))
#     db.commit()
#     db.close()
#     return {"msg": "Song added to playlist"}

# # 19. Remove asong from a playlist
# @app.delete("/playlists/{playlist_id}/songs/{song_id}")
# def remove_song_from_playlist(playlist_id: int, song_id: int):
#     """Remove a song from a specified playlist."""
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("DELETE FROM playlist_songs WHERE playlist_id = %s AND song_id = %s", 
#                    (playlist_id, song_id))
#     db.commit()
#     db.close()
#     return {"msg": "Song removed from playlist"}

# # 20. Get all songs in a playlist
# @app.get("/playlists/{playlist_id}/songs/")
# def get_songs_in_playlist(playlist_id: int):
#     """Retrieve all songs in a specified playlist."""
#     db = get_db()
#     cursor = db.cursor(dictionary=True)
#     cursor.execute("""
#         SELECT songs.* FROM songs 
#         JOIN playlist_songs ON songs.id = playlist_songs.song_id
#         WHERE playlist_songs.playlist_id = %s
#     """, (playlist_id,))
#     songs = cursor.fetchall()
#     db.close()
#     return songs

# # 21. Bulk add songs to a playlist
# @app.post("/playlists/{playlist_id}/bulk-add-songs/")
# def bulk_add_songs_to_playlist(playlist_id: int, song_ids: BulkSongUpdate):
#     """Bulk add songs to a specified playlist."""
#     db = get_db()
#     cursor = db.cursor()
#     for song_id in song_ids.song_ids:
#         cursor.execute("INSERT INTO playlist_songs (playlist_id, song_id) VALUES (%s, %s)", 
#                        (playlist_id, song_id))
#     db.commit()
#     db.close()
#     return {"msg": "Songs added to playlist"}

# # 22. Bulk remove songs from a playlist
# @app.post("/playlists/{playlist_id}/bulk-remove-songs/")
# def bulk_remove_songs_from_playlist(playlist_id: int, song_ids: BulkSongUpdate):
#     """Bulk remove songs from a specified playlist."""
#     db = get_db()
#     cursor = db.cursor()
#     for song_id in song_ids.song_ids:
#         cursor.execute("DELETE FROM playlist_songs WHERE playlist_id = %s AND song_id = %s", 
#                        (playlist_id, song_id))
#     db.commit()
#     db.close()
#     return {"msg": "Songs removed from playlist"}

