CREATE TABLE rooms (
    id_room INT AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    price DECIMAL(20,2) NOT NULL,
    stars INT NOT NULL,
    PRIMARY KEY (id_room)
);

CREATE TABLE users (
    id_user INT AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    admin TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id_user)
);

CREATE TABLE reserves (
    id_reserve INT AUTO_INCREMENT,
    id_room INT NOT NULL,
    id_user INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id_reserve),
    FOREIGN KEY (id_room) REFERENCES rooms(id_room),
    FOREIGN KEY (id_user) REFERENCES users(id_user)
);

INSERT INTO rooms VALUES ( 1,'Clasica', 1, 1500, 1);
INSERT INTO rooms VALUES ( 2, 'Estandar', 2, 2000, 2);
INSERT INTO rooms VALUES ( 3, 'Casual', 2, 3500, 3);
INSERT INTO rooms VALUES ( 4, 'Premium', 3, 5000, 4);
INSERT INTO rooms VALUES ( 5, 'Ejecutiva', 4, 8000, 5);
INSERT INTO rooms VALUES ( 6 ,'Presidencial', 6, 12500, 6);

INSERT INTO users (name, password, email, admin) VALUES 
('Alice Smith', 'password1', 'alice@example.com', 0),
('Bob Johnson', 'password2', 'bob@example.com', 1),
('Charlie Brown', 'password3', 'charlie@example.com', 0),
('Diana Prince', 'password4', 'diana@example.com', 1),
('Evan Davis', 'password5', 'evan@example.com', 0);


