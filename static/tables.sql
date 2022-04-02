CREATE TABLE accounts(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name TEXT NOT NULL,
    lastname TEXT NOT NULL,
    login TEXT NOT NULL,
    hash TEXT NOT NULL,
    currency TEXT NOT NULL,
    pay_sys TEXT NOT NULL,
    card_num INTEGER NOT NULL,
    expiration TEXT NOT NULL,
    cash NUMERIC NOT NULL,
    m_limit INTEGER NOT NULL DEFAULT 1000
);

CREATE TABLE transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER,
    sum REAL NOT NULL,
    address INTEGER NOT NULL,
    op_type TEXT NOT NULL,
    time TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES accounts(id)
);

CREATE TABLE cards(
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id INTEGER DEFAULT 1,
    number INTEGER NOT NULL,
    pay_sys TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES accounts(id)
);

INSERT INTO cards (number, pay_sys) VALUES (4485054045916395, 'visa'), (4556563968987880, 'visa'), (4556818991043014, 'visa'), (4388735003674780, 'visa'), (4556525245641838, 'visa'), (5268007744372278, 'mastercard'), (5295838234055628, 'mastercard'), (5486913509985129, 'mastercard'), (5369814032240432, 'mastercard'), (5241785112881366, 'mastercard');

