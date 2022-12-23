CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(255) NOT NULL
);

CREATE TABLE members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    sex CHAR(1) NOT NULL,
    has_dress BOOLEAN NOT NULL DEFAULT FALSE,
    section VARCHAR(8) NOT NULL,
    balance DECIMAL(10,2) NOT NULL DEFAULT 0.00
);


CREATE TABLE transactions (
    transaction_id INTEGER PRIMARY KEY,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255),
    category VARCHAR(255),
    date DATETIME NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES members(member_id),
    FOREIGN KEY (receiver_id) REFERENCES members(member_id)
);

CREATE TABLE expenses (
    expense_id INTEGER PRIMARY KEY,
    payer_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    description VARCHAR(255),
    category VARCHAR(255),
    date DATE NOT NULL,
    FOREIGN KEY (payer_id) REFERENCES members(member_id),
    FOREIGN KEY (recipient_id) REFERENCES members(member_id)
);
