-- Adminer 4.8.1 PostgreSQL 16.2 (Debian 16.2-1.pgdg120+2) dump

\connect "festup";

INSERT INTO "usuario" ("username", "password", "email", "nombre", "fechaNacimiento") VALUES
('ikersobron',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'iker.sobron@ehu.eus',	'Iker Sobrón',	'2000-01-01'),
('aingerubellido',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'abellido008@ikasle.ehu.eus',	'Aingeru Bellido',	'2002-03-05'),
('nagoregomez',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'ngomez067@ikasle.ehu.eus',	'Nagore Gómez',	'2002-12-04'),
('maitaneurruela',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'murruela002@ikasle.ehu.eus',	'Maitane Urruela',	'2002-09-27'),
('sergiomartin',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'smartin128@ikasle.ehu.eus',	'Sergio Martín',	'2002-05-23');

INSERT INTO "cuadrilla" ("nombre", "descripcion", "lugar", "accessToken") VALUES
('PIKITO',	'Somos la cuadrilla PIKITO. Nos conocimos en la carrera de Informática de la UPV/EHU.',	'Bilbao', '12345678'),
('HITZ',	'HITZ taldeko kideak',	'Bilbao y alrededores',	'12345678'),
('IXA',	'IXA taldeko kideak',	'Bilbao',	'12345678');

INSERT INTO "evento" ("id", "nombre", "fecha", "numeroAsistentes", "descripcion", "localizacion") VALUES
(1,	'San Jorge',	'2024-04-28',	1,	'Fiestas de San Jorge, Santurtzi.',	'Santurtzi'),
(2,	'San Roque',	'2024-08-14',	5,	'Fiestas de Portugalete',	'Portugalete');

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
