# Mapping Python Classes to a Database

## Learning Goals

- Create Python objects using SQL database records.
- Create SQL database records using Python objects.

***

## Key Vocab

- **Object-Relational Mapping (ORM)**: a technique used to convert database
records into objects in an object-oriented language.

***

## Introduction

When building an ORM to connect our Python program to a database, we equate a
**class** with a database **table** and the **instances** that the class
produces to **rows** in that table.

Why map classes to tables? Our end goal is to persist information regarding our
objects to a database. In order to persist that data efficiently and in an
organized manner, we need to first map or equate our Python class to a database
table.

***

## Writing an ORM

Let's say we are building a music player app that allows users to store their
music and browse their songs by song.

**NOTE: Remember to run `pipenv install` to install the dependencies and
`pipenv shell` to enter your virtual environment before running your code.**

This program will have a `Song` class. Each song instance will have a name and
an album attribute. The starter code for this class is in the `lib/song.py`
file:

```py
class Song:

    def __init__(self, name, album):
        self.name = name
        self.album = album
```

In order to "map" this `Song` class to a songs database table, we need to create
our database, then we need to create our songs table. In building an ORM, it is
convention to pluralize the name of the class to create the name of the table.
Therefore, the `Song` class maps to the "songs" table.

### Creating the Database

Before we can create a songs table we need to create our music database. Whose
responsibility is it to create the database? It is not the responsibility of our
`Song` class. Remember, classes are mapped to _tables inside a database_, not to
the database as a whole. We may want to build other classes that we equate with
other database tables later on.

It is the responsibility of our program as a whole to create and establish the
database. Accordingly, you'll see that Python packages have modules solely for
configuration of reused (constant) variables:

```py
# lib/config.py
import sqlite3

CONN = sqlite3.connect('music.db')
CURSOR = CONN.cursor()
```

Here we set up a constant, `CONN`, that is equal to a hash that contains our
connection to the database, as well as a constant `CURSOR` that allows us to
interact with the database. In our `lib/song.py` file, we can therefore access
these constants like this:

```py
from config import CONN, CURSOR
```

The starter code for these files is set up, so you can explore it and code along
with the rest of this lesson.

<details>
  <summary>
    <em>Which constant will we use to execute SQL statements: <code>CONN</code>
        or <code>CURSOR</code>?</em>
  </summary>

  <h3><code>CURSOR</code></h3>
  <p><code>sqlite3.Connection</code> objects represent our connection to the
     database, but <code>sqlite3.Cursor</code> objects are necessary to execute
     most statements.</p>
</details>
<br/>

### Creating the Table

According to the ORM convention in which a class is mapped to or equated with a
database table, we need to create a songs table. We will accomplish this by
writing a class method in our `Song` class that creates this table.

**To "map" our class to a database table, we will create a table with the same
name as our class and give that table column names that match the
instance attributes of the class.**

Update the `Song` class as follows so that it maps instance attributes to table
columns:

```py
class Song:

    def __init__(self, name, album):
        self.id = None
        self.name = name
        self.album = album

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """

        CURSOR.execute(sql)
```

Let's break down this code.

#### The `id` Attribute

Notice that we are initializing an individual `Song` instance with an `id`
attribute that has a default value of `None`. Why are we doing this? First of
all, songs need an `id` attribute only because they will be saved into the
database and we know that each table row needs an `id` value which is the
primary key.

When we create a new song, we _do not set that song's id_. A song gets an `id`
only when it gets saved into the database (more on inserting songs into the
database later). We therefore set the default value of the `id` argument for the
`__init__` method equal to `None`, so that we can create new song instances that
do not have an `id` value. We'll leave that up to the database to handle later
on.

Why leave it up to the database? Remember that in the world of relational
databases, the `id` of a given record must be unique. If we could replicate a
record's `id`, we would have a very disorganized database. Only the database
itself, through the magic of SQL, can ensure that the `id` of each record is
unique.

#### The `create_table()` Method

Above, we created a class method, `create_table()`, that crafts a SQL statement
to create a songs table and give that table column names that match the
attributes of an individual instance of `Song`. Why is the `create_table()`
method a class method? Well, it is _not_ the responsibility of an individual
song to create the table it will eventually be saved into. It is the job of the
class as a whole to create the table that it is mapped to.

Now that our songs table exists, we can learn how to save data regarding
individual songs into that table.

You can try out this code now to create the table in the `music.db` file.
Check out the code in the `debug.py` file:

```py
#!/usr/bin/env python3

from config import CONN, CURSOR
from song import Song

import ipdb; ipdb.set_trace()
```

In this file, we're importing in the `sqlite3.Connection` and `sqlite3.Cursor`
objects that we instantiated in `lib/config.py`. We're also importing the
`Song` class so that we can use its methods during our `pdb` session.

Run `python debug.py` to enter `pdb`, then run the `create_table()` method:

```py
Song.create_table()
```

Creating a table doesn't return any data, so SQLite returns `None`. If you'd
like to confirm that the table was created successfully, you can run a special
`PRAGMA` command to show the information about the `songs` table:

```py
CURSOR.execute("PRAGMA table_info(songs)").fetchall()
# => [(0, 'id', 'INTEGER', 0, None, 1), (1, 'name', 'TEXT', 0, None, 0), (2, 'album', 'TEXT', 0, None, 0)]
```

The output isn't easy to read, but you'll see the different column names (`id`,
`name`, `album`) along with their data types (`INTEGER`, `TEXT`, `TEXT`).
Success!

<details>
  <summary>
    <em>If we wanted to make a method to <code>DROP</code> a table, should we
        make an instance method or a class method?</em>
  </summary>

  <h3>A class method.</h3>
  <p>Instance methods should only include behaviors that affect instances or
     are carried out by instances- these map to <em>rows</em> in a table. As a
     <code>DROP</code> command affects the table itself, it should be carried
     out by a class method.</p>
</details>
<br/>

***

## Mapping Class Instances to Table Rows

When we say that we are saving data to our database, what data are we referring
to? If individual instances of a class are "mapped" to rows in a table, does
that mean that the instances themselves, these individual Python objects, are
saved into the database?

Actually, **we are not saving Python objects in our database.** We are going to
take the individual attributes of a given instance, in this case a song's name
and album, and save _those attributes that describe an individual song_ to the
database as one, single row.

For example, let's say we have a song:

```py
blinding_lights = Song("Blinding Lights", "After Hours")

blinding_lights.name
# => "Blinding Lights"

blinding_lights.album
# => "After Hours"
```

This song has its two attributes, `name` and `album`, set equal to the above
values. In order to save the song `blinding_lights` into the songs table, we
will use the name and album of the song to create a new row in that table. The
SQL statement we want to execute would look something like this:

```sql
INSERT INTO songs (name, album)
VALUES ("Blinding Lights", "After Hours");
```

What if we had another song that we wanted to save?

```py
hello = Song("Hello", "25")

hello.name
# => "Hello"

hello.album
# => "25"
```

In order to save `hello` into our database, we do not insert the Python object
stored in the `hello` variable. Instead, we use `hello`'s name and album values
to create a new row in the songs table:

```sql
INSERT INTO songs (name, album)
VALUES ("Hello", "25");
```

We can see that the operation of saving the attributes of a particular song into
a database table is common enough. Every time we want to save a record, though,
we are repeating the same exact steps and using the same code. The only things
that are different are the values that we are inserting into our songs table.
Let's abstract this functionality into an instance method, `save()`.

### Inserting Data into a table with the `save()` Method

Let's build an instance method, `save()`, that saves a given instance of our
`Song` class into the songs table of our database.

```py
class Song:

    # ... rest of Song methods

    def save(self):
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.album))

```

Let's break down the code in this method a bit further.

#### The `save()` Method

In order to `INSERT` data into our songs table, we need to craft a SQL `INSERT`
statement. Ideally, it would look something like this:

```sql
INSERT INTO songs (name, album)
VALUES songs_name, songs_album
```

Above, we used the heredoc to craft our multi-line SQL statement. How are we
going to pass in, or interpolate, the name and album of a given song into our
Python string?

We use something called **bound parameters**.

> **Important:** using f-strings or the `str.format()` method will not work with
> statements sent through the `sqlite3` module. `sqlite3` will interpret any
> values interpolated in this fashion as _columns_. Weird!

#### Bound Parameters

Bound parameters protect our program from getting confused by
[SQL injections](https://en.wikipedia.org/wiki/SQL_injection) and special
characters. Instead of interpolating variables into a string of SQL, we are
using the `?` characters as placeholders. Then, the special magic provided to us
by the `sqlite3` module's `Cursor.execute()` method will take the values we pass
in as an argument and apply them as the values of the question marks.

#### How `save()` works

So, our `save()` method inserts a record into our database that has the name and
album values of the song instance we are trying to save. We are not saving the
Python object itself. We are creating a new row in our songs table that has the
values that characterize that song instance.

**Important:** Notice that we _didn't_ insert an ID number into the table with
the above statement. Remember that the `INTEGER PRIMARY KEY` datatype will
assign and auto-increment the id attribute of each record that gets saved.

## Creating Instances vs. Creating Table Rows

The moment in which we create a new `Song` instance with the `__init__`
method is _different than the moment in which we save a representation of that
song to our database_. The `__init__` method creates a new instance of the
song class, a new Python object. The `save()` method takes the attributes that
characterize a given song and saves them in a new row of the songs table in our
database.

At what point in time should we actually save a new record? While it is possible
to save the record right at the moment the new object is created, i.e. in the
`__init__` method, this is not a great idea. We don't want to force our
objects to be saved every time they are created, or make the creation of an
object dependent upon/always coupled with saving a record to the database. As
our program grows and changes, we may find the need to create objects and not
save them. A dependency between instantiating an object and saving that record
to the database would preclude this or, at the very least, make it harder to
implement.

So, we'll keep our `__init__` and `save()` methods separate:

```py
class Song:

    def __init__(self, name, album):
        self.id = None
        self.name = name
        self.album = album

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """
        
        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.album))
```

Now, we can create and save songs like this. Try this out by running
`python debug.py` and running this code in the `pdb` session (make sure to exit out
of `pdb` with `exit()` or `ctrl+D` in order to reload the code if you left it
open earlier):

```py
hello = Song("Hello", "25")
hello.save()

despacito = Song("Despacito", "Vida")
despacito.save()
```

That last line of the `save()` method returns an empty array once more since
`INSERT`ing new rows in a database doesn't return any data, but you can check if
all the records were indeed saved by running this in `pdb`:

```py
songs = CURSOR.execute('SELECT * FROM songs')
[row for row in songs]
# => [(1, 'Hello', '25'), (2, 'Despacito', 'Vida')]
```

### Giving Our `Song` Instance an `id`

When we `INSERT` the data concerning a particular `Song` instance into our
database table, we create a new row in that table. That row would look something
like this:

| id | name | album |
| --- | --- | --- |
| 1 | Hello | 25 |

Notice that the database table's row has a column for `name`, `album` and also
`id`. Recall that we created our table to have a column for the primary key, ID,
of a given record. So, as each record gets inserted into the database, it is
given an ID number automatically.

In this way, our `hello` instance is stored in the database with the name and
album that we gave it, _plus_ an ID number that the database assigns to it.

We want our `hello` instance to completely reflect the database row it is
associated with so that we can retrieve it from the table later on with ease.
So, once the new row with `hello`'s data is inserted into the table, let's grab
the `ID` of that newly inserted row and assign it to be the value of `hello`'s
`id` attribute.

```py
class Song:

    # ... rest of Song methods

    def save(self):
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.album))
        CONN.commit()

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM songs").fetchone()[0]
```

At the end of our `save()` method, we use a SQL query to grab the value of the
`id` column of the last inserted row, and set that equal to the given song
instance's `id` attribute. Don't worry too much about how that SQL query works
for now, we'll learn more about it later. The important thing to understand is
the process of:

- Instantiating a new instance of the `Song` class.
- Inserting a new row into the database table that contains the information
  regarding that instance.
- Grabbing the `id` of that newly inserted row and assigning the given `Song`
  instance's `id` attribute equal to the `id` of its associated database table
  row.

Let's revisit our code that instantiated and saved some songs by running
`python debug.py` and entering the following code:

```py
hello = Song("Hello", "25")
hello.save()

despacito = Song("Despacito", "Vida")
despacito.save()

hello.id
# => 1
despacito.id
# => 2
```

Here we:

- Create the songs table.
- Create two new song instances.
- Use the `save()` method to persist them to the database.

This approach still leaves a little to be desired, however. Here, we have to
first create the new song and then save it, every time we want to create and
save a song. This is repetitive and tedious. As programmers (you might
remember), we are lazy. If we can accomplish something with fewer lines of code
we do it. **Any time we see the same code being used again and again, we think
about abstracting that code into a method.**

Since first creating an object and then saving a record representing that object
is so common, let's write a method that does just that.

### The `create()` Method

This class method will wrap the code we used above to create a new `Song`
instance and save it. We use a class method here because our instance does not
exist at the time the method is called.

```py
class Song:

    # ... rest of Song methods

    @classmethod
    def create(cls, name, album):
        song = Song(name, album)
        song.save()
        return song
```

Here, we use keyword arguments to pass a name and album into our `create()`
method. We use that name and album to instantiate a new song. Then, we use the
`save` method to persist that song to the database.

Notice that at the end of the method, we are returning the `Song` instance that
we instantiated. The return value of `create()` should always be the object that
we created. Why? Imagine you are working with your program and you create a new
song:

```py
Song.create("Hello", "25")
```

Now, we would have to run a separate query on our database to grab the record
that we just created. That is way too much work for us. It would be much easier
for our `create()` method to simply return the new object for us to work with:

```py
song = Song.create("Hello", "25")
song.name
# => "Hello"
song.album
# => "25"
```

Excellent! Run `pipenv install` and `pipenv shell` if you have not yet to set up
your virtual environment. Run `pytest -x` now to pass the tests, then submit the
assignment using `git`.

> **Note: You may have to delete your existing database for all of the tests to
> pass- SQLite sometimes "locks" databases that have been accessed by multiple
> modules.**

***

## Conclusion

The important concept to grasp here is the idea that we are _not_ saving Python
objects into our database. We are using the attributes of a given Python object
to create a new row in our database table.

Think of it like making butter cookies. You have a cookie cutter, which in our
case would be our class. It describes what a cookie should look like. Then you
use it to cut out a cookie, or instantiate a class object. But that's not
enough, you have to show it to your friends. So you take a picture of it and
post to your MyFace account and share it with everybody else, like how your
database can share information with other parts of your program.

The picture doesn't do anything to the cookie itself, but merely captures
certain aspects of it. It's a butter cookie, it looks fresh and delicious, and
it has little sprinkles on it. Those aspects are captured in the picture, but
the cookie and the picture are still two different things. After you eat the
cookie, or in our case after you delete the Python object, the database will not
change at all until the record is deleted, and vice versa.

***

## Solution Code

```py
from config import CONN, CURSOR

class Song:

    def __init__(self, name, album):
        self.id = None
        self.name = name
        self.album = album

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                album TEXT
            )
        """

        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO songs (name, album)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.album))
        CONN.commit()

        self.id = CURSOR.execute("SELECT last_insert_rowid() FROM songs").fetchone()[0]

    @classmethod
    def create(cls, name, album):
        song = Song(name, album)
        song.save()
        return song

```

***

## Resources

- [sqlite3 - DB-API 2.0 interface for SQLite databases - Python](https://docs.python.org/3/library/sqlite3.html)
