-- Adminer 4.8.1 PostgreSQL 16.3 (Debian 16.3-1.pgdg120+1) dump

\connect "festup";

INSERT INTO "cuadrilla" ("nombre", "descripcion", "lugar", "accessToken") VALUES
('PIKITO',	'Somos la cuadrilla PIKITO. Nos conocimos en la carrera de Informática de la UPV/EHU.',	'Bilbao',	'12345678'),
('HITZ',	'HITZ taldeko kideak',	'Bilbao y alrededores',	'12345679'),
('IXA',	'IXA taldeko kideak',	'Bilbao',	'12345677');

INSERT INTO "evento" ("nombre", "fecha", "descripcion", "localizacion", "id") VALUES
('San Roque',	'2024-08-14',	'Fiestas de Portugalete',	'Portugalete',	'474f6028-2b24-4195-8be6-6160f72e24d5'),
('Fiestas de la Trinidad',	'2024-05-26',	'Fiestas patronales de Las Carreras. La Trinidad 2024.',	'Las Carreras',	'd1b7aa41-f786-44a7-b744-a6600570e66c'),
('San Juan',	'2024-06-24',	'Fiestas patronales de Muskiz.',	'Muskiz',	'2848f872-2055-4618-b128-43379b857b6b'),
('Virgen del Carmen',	'2024-07-16',	'Fiestas patronales de Barakaldo',	'Barakaldo',	'38788436-7c31-4065-b005-251d353bc130'),
('Transfiguración del Señor',	'2024-08-06',	'Fiestas patronales de Trapagaran.',	'Trapagaran',	'19d4055a-1db6-4d1d-88cd-9feecf1ec3f3');

INSERT INTO "usuario" ("username", "password", "email", "nombre", "fechaNacimiento", "telefono") VALUES
('ikersobron',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'iker.sobron@ehu.eus',	'Iker Sobrón',	'2000-01-01',	'0'),
('aingerubellido',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'abellido008@ikasle.ehu.eus',	'Aingeru Bellido',	'2002-03-05',	'644311712'),
('sergiomartin',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'smartin128@ikasle.ehu.eus',	'Sergio Martín',	'2002-05-23',	'661748789'),
('nagoregomez',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'ngomez067@ikasle.ehu.eus',	'Nagore Gómez',	'2002-12-04',	'638258837'),
('maitaneurruela',	'\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969',	'murruela002@ikasle.ehu.eus',	'Maitane Urruela',	'2002-09-27',	'674825543'),
('aitziberatutxa',	'\x24326224313224394157556f64324f5167646d4a335556525231486b4f3078345934506d33516a4a4333414454547743734f636f74344b36724d6332',	'aitziber.atutxa@gmail.com',	'Aitziber',	'2000-01-01',	'000000000'),
('koldogojenola',	'\x243262243132242e384a387245544266766b6c724f525977477566644f50526c682f74334834714a586b61465a6739645a39654f3452416a3250714b',	'koldo.gojenola@ehu.eus',	'Koldo',	'2000-01-01',	'000000000');

INSERT INTO "cuadrillaAsistente" ("nombre", "id") VALUES
('PIKITO',	'2848f872-2055-4618-b128-43379b857b6b');

INSERT INTO "integrante" ("username", "nombre") VALUES
('aingerubellido',	'PIKITO'),
('maitaneurruela',	'PIKITO'),
('sergiomartin',	'PIKITO'),
('nagoregomez',	'PIKITO'),
('ikersobron',	'IXA');

INSERT INTO "seguidores" ("siguiendo", "seguido") VALUES
('aingerubellido',	'maitaneurruela'),
('aingerubellido',	'nagoregomez'),
('aingerubellido',	'sergiomartin');

INSERT INTO "usuarioAsistente" ("username", "id") VALUES
('aingerubellido',	'2848f872-2055-4618-b128-43379b857b6b'),
('sergiomartin',	'19d4055a-1db6-4d1d-88cd-9feecf1ec3f3'),
('aingerubellido',	'474f6028-2b24-4195-8be6-6160f72e24d5');

-- 2024-05-17 13:34:21.366808+00