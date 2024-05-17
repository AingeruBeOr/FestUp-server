-- Adminer 4.8.1 PostgreSQL 16.3 (Debian 16.3-1.pgdg120+1) dump

\connect "festup";

INSERT INTO "usuario" ("username", "password", "email", "nombre", "fechaNacimiento", "telefono") VALUES
('ikersobron',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'iker.sobron@ehu.eus',	'Iker Sobrón',	'2000-01-01',	'0'),
('aingerubellido',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'abellido008@ikasle.ehu.eus',	'Aingeru Bellido',	'2002-03-05',	'644311712'),
('sergiomartin',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'smartin128@ikasle.ehu.eus',	'Sergio Martín',	'2002-05-23',	'661748789'),
('nagoregomez',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'ngomez067@ikasle.ehu.eus',	'Nagore Gómez',	'2002-12-04',	'638258837'),
('maitaneurruela',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'murruela002@ikasle.ehu.eus',	'Maitane Urruela',	'2002-09-27',	'674825543');

INSERT INTO "cuadrilla" ("nombre", "descripcion", "lugar", "accessToken") VALUES
('PIKITO',	'Somos la cuadrilla PIKITO. Nos conocimos en la carrera de Informática de la UPV/EHU.',	'Bilbao',	'12345678'),
('HITZ',	'HITZ taldeko kideak',	'Bilbao y alrededores',	'12345679'),
('IXA',	'IXA taldeko kideak',	'Bilbao',	'12345677');


INSERT INTO "evento" ("nombre", "fecha", "descripcion", "localizacion", "id") VALUES
('San Jorge',	'2024-04-28',	'Fiestas de San Jorge, Santurtzi.',	'Santurtzi',	'c555c8f3-1fb9-4ca5-bc92-37778f2fe1d4'),
('San Roque',	'2024-08-14',	'Fiestas de Portugalete',	'Portugalete',	'474f6028-2b24-4195-8be6-6160f72e24d5');

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


-- 2024-05-14 11:12:38.07607+00