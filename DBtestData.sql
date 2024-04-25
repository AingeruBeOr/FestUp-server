-- Adminer 4.8.1 PostgreSQL 16.2 (Debian 16.2-1.pgdg120+2) dump

\connect "festup";

INSERT INTO "evento" ("id", "nombre", "fecha", "numeroAsistentes", "descripcion", "localizacion") VALUES
(1,	'San Jorge',	'2024-04-26',	1,	'Fiestas de San Jorge, Santurtzi.',	'Santurtzi');

INSERT INTO "cuadrilla" ("nombre", "descripcion", "lugar") VALUES
('PIKITO',	'Somos la cuadrilla PIKITO. Nos conocimos en la carrera de Informática de la UPV/EHU.',	'Bilbao');

INSERT INTO "usuario" ("username", "password", "email", "nombre") VALUES
('aingerubellido',	'abellido',	'abellido008@ikasle.ehu.eus',	'Aingeru Bellido'),
('nagoregomez',	'ngomez',	'ngomez067@ikasle.ehu.eus',	'Nagore Gómez'),
('sergiomartin',	'smartin',	'smartin128@ikasle.ehu.eus',	'Sergio Martín'),
('maitaneurruela',	'murruela',	'murruela002@ikasle.ehu.eus',	'Maitane Urruela'),
('ikersobron',	'isobron',	'iker.sobron@ehu.eus',	'Iker Sobrón');

INSERT INTO "cudarillaAsistente" ("nombre", "id") VALUES
('PIKITO',	1);


INSERT INTO "integrante" ("username", "nombre") VALUES
('aingerubellido',	'PIKITO'),
('maitaneurruela',	'PIKITO'),
('sergiomartin',	'PIKITO'),
('nagoregomez',	'PIKITO');

INSERT INTO "seguidores" ("siguiendo", "seguido") VALUES
('aingerubellido',	'maitaneurruela'),
('nagoregomez',	'sergiomartin'),
('aingerubellido',	'nagoregomez');

INSERT INTO "usuarioAsistente" ("username", "id") VALUES
('ikersobron',	1);

-- 2024-04-25 22:59:54.00203+00