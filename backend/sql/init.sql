CREATE TABLE rooms (
    id_room INT AUTO_INCREMENT,
    room_name VARCHAR(50) NOT NULL,
    capacity INT NOT NULL,
    price DECIMAL(20,2) NOT NULL,
    stars INT NOT NULL,
    description TEXT DEFAULT NULL,
    url_imagen VARCHAR(256) DEFAULT NULL,
    PRIMARY KEY (id_room)
);

CREATE TABLE users (
    id_user INT AUTO_INCREMENT,
    user_name VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    admin TINYINT(1) NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    url_imagen VARCHAR(256) DEFAULT NULL,
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
    amount DECIMAL(20,2) DEFAULT 0.00 NOT NULL,
    PRIMARY KEY (id_reserve),
    FOREIGN KEY (id_room) REFERENCES rooms(id_room),
    FOREIGN KEY (id_user) REFERENCES users(id_user)
);

CREATE TABLE promotions (
    id_promotion INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    first_date DATE,
    discount INT NOT NULL,
    last_date DATE
);

INSERT INTO rooms (room_name, description, stars, capacity, price) VALUES 
( 'Habitación Básica','La Habitación Básica está diseñada para quienes buscan una estancia práctica y funcional. Con una superficie de 15 a 20 metros cuadrados, esta habitación es perfecta para estadías cortas o viajes de negocios. Encontrarás una cama individual o matrimonial que ofrece el confort esencial, junto con un escritorio pequeño y una silla, ideales para trabajar o estudiar. Entre los servicios y comodidades disponibles, destaca el Wi-Fi gratuito, que te mantendrá conectado en todo momento. También tendrás acceso a una televisión por cable para tu entretenimiento y aire acondicionado para asegurar una temperatura agradable durante toda tu estancia. El baño privado cuenta con una ducha y está equipado con artículos de aseo básicos como jabón y champú, además de toallas y un secador de pelo para tu conveniencia. La decoración de la Habitación Básica es sencilla y funcional, con colores neutros que promueven la relajación y el descanso. Como extras, recibirás una botella de agua gratuita y podrás disfrutar de un servicio de limpieza diario que mantendrá tu habitación impecable. Un pequeño armario o perchas están a tu disposición para organizar tu ropa de manera práctica.', 1, 2, 1500),
( 'Confort Estándar', 'La Habitación Confort Estándar ofrece una experiencia más amplia y cómoda, con una superficie de 20 a 25 metros cuadrados. Puedes elegir entre una cama matrimonial o dos camas individuales, adaptándose a tus necesidades. Además, cuenta con una zona de estar con silla o sillón, proporcionando un espacio adicional para relajarte. \n Esta habitación está equipada con Wi-Fi gratuito de alta velocidad, ideal tanto para el trabajo como para el entretenimiento sin interrupciones. La televisión de pantalla plana ofrece una excelente calidad de imagen para disfrutar de tus programas favoritos. El aire acondicionado y la calefacción garantizan una estancia confortable en cualquier época del año. \n El baño privado puede incluir una ducha o una bañera, y está provisto de artículos de aseo de mejor calidad, toallas de mayor grosor y un secador de pelo. La decoración es moderna y confortable, con colores cálidos y detalles decorativos que crean un ambiente acogedor. \n Entre los extras, encontrarás un mini bar con una selección de bebidas y snacks, así como un servicio de limpieza diario y servicio a la habitación. También dispones de una caja fuerte para guardar tus objetos de valor con total seguridad.',2, 3, 2000),
( 'Habitación Superior', 'La Habitación Superior se distingue por su amplitud y elegancia, con una superficie de 25 a 30 metros cuadrados. Ofrece una cama king size o dos camas queen, junto con una zona de estar con mesa y sillas, proporcionando un espacio adicional para trabajar o relajarte. \n El Wi-Fi gratuito de alta velocidad y la televisión de pantalla plana de mayor tamaño aseguran una conexión y entretenimiento de alta calidad. La habitación cuenta con aire acondicionado, calefacción y un purificador de aire para mantener un ambiente saludable y confortable. \n El baño privado incluye una bañera y está equipado con artículos de aseo de lujo, así como albornoces y zapatillas para una experiencia más refinada. La decoración es elegante y moderna, con colores sofisticados y obras de arte que añaden un toque de distinción. \n Además, dispones de una máquina de café/té para preparar tus bebidas favoritas en cualquier momento. El servicio de limpieza y el servicio a la habitación están disponibles las 24 horas para tu comodidad. También puedes solicitar un periódico diario para mantenerte informado.', 2, 3, 3500),
( 'Premium','La Habitación Premium es la opción perfecta para aquellos que buscan un nivel superior de comodidad y lujo. Con una superficie de 25 a 30 metros cuadrados, esta habitación ofrece una cama king size o dos camas queen, junto con una zona de estar con mesa y sillas para mayor comodidad. \n El Wi-Fi gratuito de alta velocidad y la televisión de pantalla plana de mayor tamaño garantizan una conexión y entretenimiento de alta calidad. La habitación está equipada con aire acondicionado, calefacción y un purificador de aire para mantener un ambiente saludable y confortable durante toda tu estancia. \n El baño privado cuenta con una bañera y está equipado con artículos de aseo de lujo, albornoces y zapatillas para una experiencia más refinada. La decoración de la Habitación Premium es elegante y moderna, con colores sofisticados y detalles decorativos que añaden un toque de distinción. \n Además, podrás disfrutar de una máquina de café/té en la habitación para preparar tus bebidas favoritas en cualquier momento. El servicio de limpieza y el servicio a la habitación están disponibles las 24 horas para tu comodidad. También puedes solicitar un periódico diario para mantenerte informado.', 3, 4, 5000),
( 'Suite Ejecutiva','La Suite Ejecutiva ofrece un lujo superior con una superficie de 35 a 45 metros cuadrados. Incluye una cama king size y una sala de estar separada con sofá y escritorio, proporcionando un amplio espacio para relajarte y trabajar. \n El Wi-Fi gratuito de alta velocidad y las televisiones de pantalla plana en el dormitorio y la sala de estar aseguran entretenimiento y conectividad sin interrupciones. La suite está equipada con aire acondicionado, calefacción y un sistema de sonido para una experiencia auditiva excepcional. \n El baño privado cuenta con una bañera y una ducha separada, así como artículos de aseo premium, albornoces, zapatillas y un espejo de aumento. La decoración es lujosa y moderna, con colores sofisticados y acabados de alta calidad que crean un ambiente exclusivo. \n Entre los extras, encontrarás un mini bar con una selección de bebidas premium y un servicio de limpieza y servicio a la habitación disponibles las 24 horas. Además, tendrás acceso a una sala ejecutiva con servicios adicionales, ideal para reuniones y eventos privados.', 4, 2, 7500),
( 'Suite Presidencial','La Suite Presidencial es la cúspide del lujo, con una superficie de 50 a 70 metros cuadrados. Esta suite incluye un dormitorio principal con cama king size, una sala de estar y un comedor independientes, ofreciendo un espacio opulento y privado. \n El Wi-Fi gratuito de alta velocidad y los televisores de pantalla plana en todas las habitaciones aseguran una excelente conectividad y entretenimiento. La suite está equipada con aire acondicionado, calefacción y un sistema de sonido envolvente para una experiencia auditiva inigualable. \n El baño privado incluye una bañera de hidromasaje y una ducha separada, además de artículos de aseo de lujo y amenities exclusivas. Albornoces, zapatillas y toallas de alta calidad están disponibles para tu comodidad. La decoración es opulenta y sofisticada, con mobiliario de diseño y obras de arte exclusivas que reflejan un gusto refinado. \n Además, dispones de un bar privado y un servicio de limpieza y mayordomo disponibles las 24 horas para atender todas tus necesidades. Tendrás acceso a una sala ejecutiva y otros servicios VIP que aseguran una estancia de primera clase.', 6, 4, 12500),
( 'Residencia Real','La Residencia Real redefine el lujo con una superficie de 100 a 150 metros cuadrados. Incluye múltiples habitaciones, como un dormitorio principal y habitaciones adicionales, así como una sala de estar, un comedor, una cocina y un estudio independientes.\n El Wi-Fi gratuito de alta velocidad y los televisores de pantalla plana en todas las habitaciones aseguran una conectividad y entretenimiento excepcionales. La residencia está equipada con aire acondicionado, calefacción y un sistema de sonido envolvente para una experiencia inigualable.\n Los baños privados cuentan con bañeras de hidromasaje y duchas separadas, además de artículos de aseo de lujo y amenities exclusivas. Albornoces, zapatillas y toallas de alta calidad están disponibles para tu confort. La decoración es extremadamente lujosa y personalizada, con mobiliario de diseño, antigüedades y obras de arte exclusivas que crean un ambiente único.\n Además, dispones de una cocina completamente equipada, ideal para estancias prolongadas. El servicio de limpieza y mayordomo están disponibles las 24 horas, y tendrás acceso a todos los servicios VIP del hotel, incluyendo transporte privado y actividades exclusivas, asegurando una estancia verdaderamente inolvidable.', 7, 8, 20000);

INSERT INTO users (user_name, password, email, admin, url_imagen) VALUES 
('Alice Smith', 'password1', 'alice@example.com', 0,"https://i.pinimg.com/564x/c6/f3/df/c6f3dfae6b76fcea17c975fda36586d0.jpg"),
('Bob Johnson', 'password2', 'bob@example.com', 1,"https://i.pinimg.com/564x/a9/fd/3d/a9fd3d91b5fb4b66c8afc9a7c8d2af48.jpg"),
('Charlie Brown', 'password3', 'charlie@example.com', 0,"https://i.pinimg.com/564x/d8/bf/4a/d8bf4a1465fcf805f838f8c26fbe46b4.jpg"),
('Diana Prince', 'password4', 'diana@example.com', 1,"https://i.pinimg.com/564x/be/73/31/be73315b54a89d2c0425c5c9b398d884.jpg"),
('Evan Davis', 'password5', 'evan@example.com', 0, "https://i.pinimg.com/564x/33/7a/5f/337a5fef9e8c54a791bf0b8a4e88411a.jpg");

-- Inserción de Promociones en la tabla `promotions`

INSERT INTO promotions (title, description, first_date, last_date, discount) VALUES 
('Winter Wonderland', 'Enjoy our winter wonderland promotion with special discounts on all rooms!', '2024-06-21', '2025-09-20', 40),
('Spring Fling', 'Celebrate spring with our exclusive offers on select rooms!', '2024-09-21', '2024-12-20', 20),
('Summer Escape', 'Escape the heat with our summer discounts and special packages!', '2024-12-21', '2025-03-20', 10),
('Autumn Adventure', 'Experience the beauty of autumn with our seasonal deals!', '2025-03-21', '2025-06-21', 30);


-- Reservas de ejemplo
INSERT INTO reserves (id_room, id_user, start_date, end_date) VALUES
(2, 1, '2022-02-01', '2022-02-02'),
(3, 2, '2022-03-01', '2022-03-02'),
(4, 2, '2022-04-01', '2022-04-02'),
(1, 3, '2022-05-01', '2022-05-02');

-- Instruccion para traer la relacion entre promotions y months
-- SELECT p.title, p.description, p.start_date, p.end_date, m.month_name
-- FROM promotions p
-- JOIN months m ON p.id_promotion = m.id_promotion
-- ORDER BY p.id_promotion, m.id_month;

-- AGREGAR PROCENTAJE DE DESCUENTO EN LAS PROMOCIONES
