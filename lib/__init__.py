import sqlite3

CONN = sqlite3.connect('music.db')
CURSOR = CONN.cursor()