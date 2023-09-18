/*
Snapshot table
*/

CREATE TABLE IF NOT EXISTS snapshot (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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


/*
Attachment table
*/

CREATE TABLE IF NOT EXISTS attachment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created DATETIME DEFAULT CURRENT_TIMESTAMP,
    name TEXT NOT NULL,
    uri TEXT NOT NULL,
    ftyp TEXT NOT NULL,
    note TEXT,
    UNIQUE (name)
);


/*
Snapshot_Attachment table
*/

CREATE TABLE IF NOT EXISTS snp_attach (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_name TEXT,
    attachment_id INTEGER,
    UNIQUE (snapshot_name, attachment_id),
    FOREIGN KEY (snapshot_name) REFERENCES snapshot (datetime)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (attachment_id) REFERENCES attachment (id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


/*
Index: datetime_idx on datetime column
*/

CREATE UNIQUE INDEX IF NOT EXISTS datetime_idx ON snapshot (datetime);
