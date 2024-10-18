DROP TABLE IF EXISTS clients;
CREATE TABLE clients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    adresse TEXT NOT NULL
);

DROP TABLE IF EXISTS livres;
CREATE TABLE livres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL
);

DROP TABLE IF EXISTS empruntretour;
CREATE TABLE empruntretour (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        book_id INTEGER,
        emprunt_date DATE,
        return_date DATE,
        returned BOOLEAN DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES clients(id),
        FOREIGN KEY (book_id) REFERENCES livres(id)



