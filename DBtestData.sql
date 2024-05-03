-- Adminer 4.8.1 PostgreSQL 16.2 (Debian 16.2-1.pgdg120+2) dump

\connect "festup";

INSERT INTO "usuario" ("username", "password", "email", "nombre", "fechaNacimiento", "profileImagePath") VALUES
('ikersobron',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'iker.sobron@ehu.eus',	'Iker Sobrón',	NULL,	'api/userProfileImages/no-user.png'),
('aingerubellido',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'abellido008@ikasle.ehu.eus',	'Aingeru Bellido',	'2002-03-05',	'api/userProfileImages/no-user.png'),
('nagoregomez',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'ngomez067@ikasle.ehu.eus',	'Nagore Gómez',	'2002-12-04',	'api/userProfileImages/no-user.png'),
('maitaneurruela',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'murruela002@ikasle.ehu.eus',	'Maitane Urruela',	'2002-09-27',	'api/userProfileImages/no-user.png'),
('sergiomartin',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'smartin128@ikasle.ehu.eus',	'Sergio Martín',	'2002-05-23',	'api/userProfileImages/no-user.png');

INSERT INTO "cuadrilla" ("nombre", "descripcion", "lugar", "profileImagePath", "accessToken") VALUES
('PIKITO',	'Somos la cuadrilla PIKITO. Nos conocimos en la carrera de Informática de la UPV/EHU.',	'Bilbao','api/cuadrillaProfileImages/no-cuadrilla.png',	'12345678'),
('HITZ',	'HITZ taldeko kideak',	'Bilbao y alrededores','api/cuadrillaProfileImages/no-cuadrilla.png',	'12345678'),
('IXA',	'IXA taldeko kideak',	'Bilbao','api/cuadrillaProfileImages/no-cuadrilla.png',	'12345678');

INSERT INTO "evento" ("id", "nombre", "fecha", "numeroAsistentes", "descripcion", "localizacion", "eventoImagePath") VALUES
(1,	'San Jorge',	'2024-04-28',	1,	'Fiestas de San Jorge, Santurtzi.',	'Santurtzi', 'api/eventoImages/no-image.png'),
(2,	'San Roque',	'2024-08-14',	5,	'Fiestas de Portugalete',	'Portugalete',	'api/eventoImages/no-image.png');

INSERT INTO "cudarillaAsistente" ("nombre", "id") VALUES
('PIKITO',	1),
('HITZ',	1);


INSERT INTO "integrante" ("username", "nombre") VALUES
('aingerubellido',	'PIKITO'),
('maitaneurruela',	'PIKITO'),
('sergiomartin',	'PIKITO'),
('nagoregomez',	'PIKITO'),
('ikersobron',	'IXA');

INSERT INTO "seguidores" ("siguiendo", "seguido") VALUES
('aingerubellido',	'maitaneurruela'),
('nagoregomez',	'sergiomartin'),
('aingerubellido',	'nagoregomez'),
('aingerubellido',	'sergiomartin');


INSERT INTO "usuarioAsistente" ("username", "id") VALUES
('ikersobron',	1);

-- 2024-05-01 09:19:24.890559+00