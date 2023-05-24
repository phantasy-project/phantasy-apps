CREATE TABLE IF NOT EXISTS mps_threshold_nd (
    id INTEGER PRIMARY KEY,
    timestamp REAL NOT NULL,
    user TEXT NOT NULL,
    ion_name TEXT NOT NULL,
    ion_number INTEGER NOT NULL,
    ion_mass INTEGER NOT NULL,
    ion_charge INTEGER NOT NULL,
    ion_charge1 INTEGER NOT NULL,
    beam_power REAL NOT NULL,
    beam_energy REAL NOT NULL,
    beam_dest TEXT NOT NULL,
    tags TEXT,
    note TEXT,
    data BLOB NOT NULL
);
