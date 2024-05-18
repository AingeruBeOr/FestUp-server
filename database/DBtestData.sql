-- Adminer 4.8.1 PostgreSQL 16.3 (Debian 16.3-1.pgdg120+1) dump

\connect "festup";

-- Insertando en la tabla cuadrilla
INSERT INTO "cuadrilla" ("nombre", "descripcion", "lugar", "accessToken") VALUES
('PIKITO', 'Somos la cuadrilla PIKITO. Nos conocimos en la carrera de Informática de la UPV/EHU.', 'Bilbao', '12345678'),
('HITZ', 'HITZ taldeko kideak', 'Bilbao y alrededores', '12345679'),
('IXA', 'IXA taldeko kideak', 'Bilbao', '12345677');

INSERT INTO "evento" ("nombre", "fecha", "descripcion", "localizacion", "id") VALUES
('San Roque', '2024-08-14', 'Fiestas de Portugalete', 'Portugalete', '474f6028-2b24-4195-8be6-6160f72e24d5'),
('Fiestas de la Trinidad', '2024-05-26', 'Fiestas patronales de Las Carreras. La Trinidad 2024.', 'Las Carreras', 'd1b7aa41-f786-44a7-b744-a6600570e66c'),
('San Juan', '2024-06-24', 'Fiestas patronales de Muskiz.', 'Muskiz', '2848f872-2055-4618-b128-43379b857b6b'),
('Virgen del Carmen', '2024-07-16', 'Fiestas patronales de Barakaldo', 'Barakaldo', '38788436-7c31-4065-b005-251d353bc130'),
('Transfiguración del Señor', '2024-08-06', 'Fiestas patronales de Trapagaran.', 'Trapagaran', '19d4055a-1db6-4d1d-88cd-9feecf1ec3f3'),
('Fiestas de Vitoria', '2024-08-04', 'Fiestas patronales de Vitoria-Gasteiz', 'Vitoria-Gasteiz', 'b178c8b3-451e-498b-8332-f939ec5231a0'),
('Donostiko Aste Nagusia', '2024-08-10', 'Semana grande de San Sebastian, fiestas patronales del municipio de Donosti', 'San Sebastian, Donosti', '97244e3d-6310-4305-9600-035a68675b92'),
('Fiestas de Gernika', '2024-10-01', 'Fiestas de la villa de Gernika', 'Gernika', '60f33d53-2b8f-4973-bee3-47fb1bb7a0e5'),
('San Blas', '2024-02-03', 'Fiestas en honor a San Blas', 'Abadiño', 'd7db81be-54ad-431b-9d2a-c628eb51cc3b'),
('Santa Águeda', '2024-02-05', 'Fiestas de Santa Águeda', 'Zarautz', '8a224d32-239b-499c-bd8b-bd7f3f22c894'),
('Semana Grande de Bilbao', '2024-08-16', 'Fiestas de la Semana Grande de Bilbao', 'Bilbao', '460eb61d-f5ac-4648-b92b-4a07a669c96a'),
('Fiestas de San Fermín', '2024-07-07', 'Fiestas de San Fermín en Pamplona', 'Pamplona', 'aa17a9f4-6c66-4529-b65c-b2ea028a3077'),
('La Tomatina', '2024-08-28', 'Festival de La Tomatina en Buñol', 'Buñol', '95e7ce9b-52a2-4c9e-ba89-9c5bea86b62a'),
('Fallas de Valencia', '2024-03-19', 'Fiestas de las Fallas en Valencia', 'Valencia', '4b8bebea-8abe-44d2-acd3-e1722c7a0403'),
('Carnaval de Tenerife', '2024-02-12', 'Carnaval de Santa Cruz de Tenerife', 'Santa Cruz de Tenerife', 'a9f9e309-b958-499d-9a34-abd9d1dad08a'),
('Semana Santa de Sevilla', '2024-04-14', 'Procesiones de Semana Santa en Sevilla', 'Sevilla', '290fe5b0-1548-4f93-a9ac-4157550f8a2b'),
('San Isidro', '2024-05-15', 'Fiestas de San Isidro en Madrid', 'Madrid', 'e3992e27-7b7c-418a-a693-b97d1b65bbb5');

-- Insertando en la tabla usuario
INSERT INTO "usuario" ("username", "password", "email", "nombre", "fechaNacimiento", "telefono") VALUES
('ikersobron', '\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969', 'iker.sobron@ehu.eus', 'Iker Sobrón', '2000-01-01', '0'),
('aingerubellido', '\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969', 'abellido008@ikasle.ehu.eus', 'Aingeru Bellido', '2002-03-05', '644311712'),
('sergiomartin', '\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969', 'smartin128@ikasle.ehu.eus', 'Sergio Martín', '2002-05-23', '661748789'),
('nagoregomez', '\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969', 'ngomez067@ikasle.ehu.eus', 'Nagore Gómez', '2002-12-04', '638258837'),
('maitaneurruela', '\x24326224313224716d5257636e3436504a63774c477a7351735346722e416b4c497564636f364e5064695931774857612e7356766a5a566741747969', 'murruela002@ikasle.ehu.eus', 'Maitane Urruela', '2002-09-27', '674825543'),
('aitziberatutxa', '\x24326224313224394157556f64324f5167646d4a335556525231486b4f3078345934506d33516a4a4333414454547743734f636f74344b36724d6332', 'aitziber.atutxa@gmail.com', 'Aitziber', '2000-01-01', '000000000'),
('koldogojenola', '\x243262243132242e384a387245544266766b6c724f525977477566644f50526c682f74334834714a586b61465a6739645a39654f3452416a3250714b', 'koldo.gojenola@ehu.eus', 'Koldo', '2000-01-01', '000000000');

-- Insertando en la tabla cuadrillaAsistente
INSERT INTO "cuadrillaAsistente" ("nombre", "id") VALUES
('PIKITO', '2848f872-2055-4618-b128-43379b857b6b');

-- Insertando en la tabla integrante
INSERT INTO "integrante" ("username", "nombre") VALUES
('aingerubellido', 'PIKITO'),
('maitaneurruela', 'PIKITO'),
('sergiomartin', 'PIKITO'),
('nagoregomez', 'PIKITO'),
('ikersobron', 'IXA'),
('aitziberatutxa', 'IXA'),
('koldogojenola', 'IXA');

-- Insertando en la tabla seguidores
INSERT INTO "seguidores" ("siguiendo", "seguido") VALUES
('aingerubellido', 'maitaneurruela'),
('aingerubellido', 'nagoregomez'),
('aingerubellido', 'sergiomartin'),
('ikersobron', 'aingerubellido'),
('ikersobron', 'sergiomartin'),
('ikersobron', 'nagoregomez'),
('ikersobron', 'maitaneurruela');

-- Insertando en la tabla usuarioAsistente
INSERT INTO "usuarioAsistente" ("username", "id") VALUES
('aingerubellido', '2848f872-2055-4618-b128-43379b857b6b'),
('sergiomartin', '19d4055a-1db6-4d1d-88cd-9feecf1ec3f3'),
('aingerubellido', '474f6028-2b24-4195-8be6-6160f72e24d5'),
('ikersobron', '474f6028-2b24-4195-8be6-6160f72e24d5'),
('ikersobron', '2848f872-2055-4618-b128-43379b857b6b'),
('ikersobron', '460eb61d-f5ac-4648-b92b-4a07a669c96a'),
('nagoregomez', '38788436-7c31-4065-b005-251d353bc130'),
('maitaneurruela', 'b178c8b3-451e-498b-8332-f939ec5231a0'),
('maitaneurruela', '460eb61d-f5ac-4648-b92b-4a07a669c96a');

-- 2024-05-17 13:34:21.366808+00