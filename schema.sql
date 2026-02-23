CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
    id INTEGER PRIMARY KEY,
    glider_type TEXT,
    callsign TEXT,
    compsign TEXT,
    glider_class TEXT,
    options TEXT,
    image BLOB,
    user_id INTEGER REFERENCES users
);

CREATE TABLE reservations (
    id INTEGER PRIMARY KEY,
    begin_date TEXT,
    end_date TEXT,
    info TEXT,
    user_id INTEGER REFERENCES users,
    item_id INTEGER REFERENCES items
);