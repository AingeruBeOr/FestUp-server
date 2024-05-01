-- Adminer 4.8.1 PostgreSQL 16.2 (Debian 16.2-1.pgdg120+2) dump

\connect "festup";

INSERT INTO "usuario" ("username", "password", "email", "nombre", "fechaNacimiento", "profileImagePath") VALUES
('ikersobron',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'iker.sobron@ehu.eus',	'Iker Sobrón',	NULL,	NULL),
('aingerubellido',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'abellido008@ikasle.ehu.eus',	'Aingeru Bellido',	'2002-03-05',	NULL),
('nagoregomez',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'ngomez067@ikasle.ehu.eus',	'Nagore Gómez',	'2002-12-04',	NULL),
('maitaneurruela',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'murruela002@ikasle.ehu.eus',	'Maitane Urruela',	'2002-09-27',	NULL),
('sergiomartin',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'smartin128@ikasle.ehu.eus',	'Sergio Martín',	'2002-05-23',	NULL);

INSERT INTO "cuadrilla" ("nombre", "descripcion", "lugar", "profileImagePath", "accessToken") VALUES
('PIKITO',	'Somos la cuadrilla PIKITO. Nos conocimos en la carrera de Informática de la UPV/EHU.',	'Bilbao',	NULL,	NULL),
('HITZ',	'HITZ taldeko kideak',	'Bilbao y alrededores',	NULL,	NULL),
('IXA',	'IXA taldeko kideak',	'Bilbao',	NULL,	NULL);

INSERT INTO "evento" ("id", "nombre", "fecha", "numeroAsistentes", "descripcion", "localizacion", "eventoImagePath") VALUES
(1,	'San Jorge',	'2024-04-28',	1,	'Fiestas de San Jorge, Santurtzi.',	'Santurtzi',	NULL),
(2,	'San Roque',	'2024-08-14',	5,	'Fiestas de Portugalete',	'Portugalete',	NULL);

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