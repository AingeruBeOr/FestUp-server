-- Adminer 4.8.1 PostgreSQL 16.3 (Debian 16.3-1.pgdg120+1) dump

\connect "festup";

DROP TABLE IF EXISTS "cuadrilla";
CREATE TABLE "public"."cuadrilla" (
    "nombre" character varying(50) NOT NULL,
    "descripcion" text NOT NULL,
    "lugar" character varying(50) NOT NULL,
    "accessToken" character varying(300),
    CONSTRAINT "cuadrilla_nombre" PRIMARY KEY ("nombre")
) WITH (oids = false);


DROP TABLE IF EXISTS "cuadrillaAsistente";
CREATE TABLE "public"."cuadrillaAsistente" (
    "nombre" character varying(50) NOT NULL,
    "id" uuid NOT NULL,
    CONSTRAINT "CudarillaAsistente_nombre_id" PRIMARY KEY ("nombre", "id")
) WITH (oids = false);


DROP TABLE IF EXISTS "evento";
CREATE TABLE "public"."evento" (
    "nombre" character varying(75) NOT NULL,
    "fecha" date NOT NULL,
    "descripcion" text NOT NULL,
    "localizacion" character varying(50) NOT NULL,
    "id" uuid DEFAULT gen_random_uuid() NOT NULL,
    CONSTRAINT "evento_id" PRIMARY KEY ("id")
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
    "telefono" character varying(20) DEFAULT '0',
    CONSTRAINT "usuario_username" PRIMARY KEY ("username")
) WITH (oids = false);


DROP TABLE IF EXISTS "usuarioAsistente";
CREATE TABLE "public"."usuarioAsistente" (
    "username" character varying(50) NOT NULL,
    "id" uuid NOT NULL,
    CONSTRAINT "usuarioAsistente_username_id" PRIMARY KEY ("username", "id")
) WITH (oids = false);


ALTER TABLE ONLY "public"."cuadrillaAsistente" ADD CONSTRAINT "CudarillaAsistente_id_fkey" FOREIGN KEY (id) REFERENCES evento(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."cuadrillaAsistente" ADD CONSTRAINT "CudarillaAsistente_nombre_fkey" FOREIGN KEY (nombre) REFERENCES cuadrilla(nombre) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."integrante" ADD CONSTRAINT "integrante_nombre_fkey" FOREIGN KEY (nombre) REFERENCES cuadrilla(nombre) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."integrante" ADD CONSTRAINT "integrante_username_fkey" FOREIGN KEY (username) REFERENCES usuario(username) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."seguidores" ADD CONSTRAINT "followers_followed_fkey" FOREIGN KEY (seguido) REFERENCES usuario(username) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."seguidores" ADD CONSTRAINT "followers_following_fkey" FOREIGN KEY (siguiendo) REFERENCES usuario(username) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

ALTER TABLE ONLY "public"."usuarioAsistente" ADD CONSTRAINT "usuarioAsistente_id_fkey" FOREIGN KEY (id) REFERENCES evento(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."usuarioAsistente" ADD CONSTRAINT "usuarioAsistente_username_fkey" FOREIGN KEY (username) REFERENCES usuario(username) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

-- 2024-05-14 07:58:59.938152+00