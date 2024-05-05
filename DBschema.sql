-- Adminer 4.8.1 PostgreSQL 16.2 (Debian 16.2-1.pgdg120+2) dump

\connect "festup";

DROP TABLE IF EXISTS "cuadrilla";
CREATE TABLE "public"."cuadrilla" (
    "nombre" character varying(50) NOT NULL,
    "descripcion" text NOT NULL,
    "lugar" character varying(50) NOT NULL,
    "accessToken" character varying(300),
    CONSTRAINT "cuadrilla_nombre" PRIMARY KEY ("nombre")
) WITH (oids = false);


DROP TABLE IF EXISTS "cudarillaAsistente";
CREATE TABLE "public"."cudarillaAsistente" (
    "nombre" character varying(50) NOT NULL,
    "id" integer NOT NULL,
    CONSTRAINT "CudarillaAsistente_nombre_id" PRIMARY KEY ("nombre", "id")
) WITH (oids = false);


DROP TABLE IF EXISTS "evento";
DROP SEQUENCE IF EXISTS evento_id_seq;
CREATE SEQUENCE evento_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."evento" (
    "id" integer DEFAULT nextval('evento_id_seq') NOT NULL,
    "nombre" character varying(75) NOT NULL,
    "fecha" date NOT NULL,
    "numeroAsistentes" integer,
    "descripcion" text NOT NULL,
    "localizacion" character varying(50) NOT NULL,
    CONSTRAINT "evento_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


DROP TABLE IF EXISTS "integrante";
CREATE TABLE "public"."integrante" (
    "username" character varying(50) NOT NULL,
    "nombre" character varying(50) NOT NULL,
    CONSTRAINT "integrante_username_nombre" PRIMARY KEY ("username", "nombre")
) WITH (oids = false);


DROP TABLE IF EXISTS "seguidores";
CREATE TABLE "public"."seguidores" (
    "siguiendo" character varying(50) NOT NULL,
    "seguido" character varying(50) NOT NULL,
    CONSTRAINT "followers_following_followed" PRIMARY KEY ("siguiendo", "seguido")
) WITH (oids = false);


DROP TABLE IF EXISTS "usuario";
CREATE TABLE "public"."usuario" (
    "username" character varying(50) NOT NULL,
    "password" bytea NOT NULL,
    "email" character varying(50) NOT NULL,
    "nombre" character varying(50) NOT NULL,
    "fechaNacimiento" date,
    CONSTRAINT "usuario_username" PRIMARY KEY ("username")
) WITH (oids = false);


DROP TABLE IF EXISTS "usuarioAsistente";
CREATE TABLE "public"."usuarioAsistente" (
    "username" character varying(50) NOT NULL,
    "id" integer NOT NULL,
    CONSTRAINT "usuarioAsistente_username_id" PRIMARY KEY ("username", "id")
) WITH (oids = false);


ALTER TABLE ONLY "public"."cudarillaAsistente" ADD CONSTRAINT "CudarillaAsistente_id_fkey" FOREIGN KEY (id) REFERENCES evento(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."cudarillaAsistente" ADD CONSTRAINT "CudarillaAsistente_nombre_fkey" FOREIGN KEY (nombre) REFERENCES cuadrilla(nombre) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."integrante" ADD CONSTRAINT "integrante_nombre_fkey" FOREIGN KEY (nombre) REFERENCES cuadrilla(nombre) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."integrante" ADD CONSTRAINT "integrante_username_fkey" FOREIGN KEY (username) REFERENCES usuario(username) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."seguidores" ADD CONSTRAINT "followers_followed_fkey" FOREIGN KEY (seguido) REFERENCES usuario(username) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."seguidores" ADD CONSTRAINT "followers_following_fkey" FOREIGN KEY (siguiendo) REFERENCES usuario(username) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."usuarioAsistente" ADD CONSTRAINT "usuarioAsistente_id_fkey" FOREIGN KEY (id) REFERENCES evento(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."usuarioAsistente" ADD CONSTRAINT "usuarioAsistente_username_fkey" FOREIGN KEY (username) REFERENCES usuario(username) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

-- 2024-05-04 14:30:36.479895+00
