from lib.config import CURSOR
from lib.song import Song

class TestClass:
    '''Class Song in song.py'''

    def test_creates_songs_table(self):
        '''has classmethod "create_table()" that creates a table "songs" if table does not exist.'''
        Song.create_table()
        assert(CURSOR.execute("SELECT * FROM songs"))

    def test_initializes_with_name_and_album(self):
        '''takes a name and album as __init__ arguments and saves them as instance attributes.'''
        song = Song("Hold On", "Born to Sing")
        assert(song.name == "Hold On" and song.album == "Born to Sing")

    def test_saves_song_to_table(self):
        '''has instancemethod "save()" that saves a song to music.db.'''

        
        CURSOR.execute('''DROP TABLE IF EXISTS songs''')
        Song.create_table()

        song = Song("Hold On", "Born to Sing")
        song.save()
        db_song = CURSOR.execute(
            'SELECT * FROM songs WHERE name=? AND album=?',
            ('Hold On', 'Born to Sing')
        ).fetchone()
        assert(db_song[1] == song.name and db_song[2] == song.album)

    def test_creates_and_returns_song(self):
        '''has classmethod "create()" that creates a Song instance, saves it, and returns it.'''

        CURSOR.execute('''DROP TABLE IF EXISTS songs''')
        Song.create_table()

        song = Song.create("Hold On", "Born to Sing")
        db_song = CURSOR.execute(
            'SELECT * FROM songs WHERE name=? AND album=?',
            ('Hold On', 'Born to Sing')
        ).fetchone()

        assert(db_song[0] == song.id and db_song[1] == song.name and db_song[2] == song.album)
