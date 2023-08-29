/*
CREATE TABLE IF NOT EXISTS software (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL
);
*/

/*
Table for snapshot data model
*/

CREATE TABLE IF NOT EXISTS snapshot (
    id INTEGER PRIMARY KEY,
    timestamp REAL NOT NULL,
    datetime TEXT NOT NULL,
    note TEXT,
    user TEXT NOT NULL,
    ion_name TEXT NOT NULL,
    ion_number INTEGER NOT NULL,
    ion_mass INTEGER NOT NULL,
    ion_charge INTEGER NOT NULL,
    machine TEXT NOT NULL,
    segment TEXT NOT NULL,
    tags TEXT,
    app TEXT NOT NULL,
    version TEXT NOT NULL,
    data_format TEXT NOT NULL,
    data BLOB NOT NULL,
    date TEXT NOT NULL,
    parent TEXT
);

CREATE INDEX IF NOT EXISTS datetime_idx ON snapshot (datetime);
