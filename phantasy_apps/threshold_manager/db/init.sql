CREATE TABLE IF NOT EXISTS mps_threshold (
    id INTEGER PRIMARY KEY NOT NULL,
    timestamp REAL NOT NULL,
    datetime TEXT NOT NULL,
    user TEXT NOT NULL,
    isrc_name TEXT NOT NULL,
    ion_name TEXT NOT NULL,
    ion_number INTEGER NOT NULL,
    ion_mass INTEGER NOT NULL,
    ion_charge INTEGER NOT NULL,
    ion_charge_state INTEGER NOT NULL,
    beam_power REAL NOT NULL,
    beam_energy REAL NOT NULL,
    beam_bound TEXT NOT NULL,
    beam_dest TEXT NOT NULL,
    tags TEXT,
    note TEXT,
    data BLOB NOT NULL
);
