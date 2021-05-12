--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

-- Started on 2021-05-11 20:07:39 AWST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 3278 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 204 (class 1259 OID 16417)
-- Name: categories; Type: TABLE; Schema: public; Owner: curator
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(255)
);


ALTER TABLE public.categories OWNER TO curator;

--
-- TOC entry 203 (class 1259 OID 16413)
-- Name: deleted; Type: TABLE; Schema: public; Owner: curator
--

CREATE TABLE public.deleted (
);


ALTER TABLE public.deleted OWNER TO curator;

--
-- TOC entry 3279 (class 0 OID 0)
-- Dependencies: 203
-- Name: TABLE deleted; Type: COMMENT; Schema: public; Owner: curator
--

COMMENT ON TABLE public.deleted IS 'Releases which have been deleted or moderated.';


--
-- TOC entry 202 (class 1259 OID 16410)
-- Name: relations; Type: TABLE; Schema: public; Owner: curator
--

CREATE TABLE public.relations (
);


ALTER TABLE public.relations OWNER TO curator;

--
-- TOC entry 200 (class 1259 OID 16396)
-- Name: releases; Type: TABLE; Schema: public; Owner: curator
--

CREATE TABLE public.releases (
    id bigint NOT NULL,
    name character varying(2500) NOT NULL,
    creator character varying(2500),
    publication_date date,
    category character varying(400),
    type character varying(120),
    resolution character varying(120),
    uploader character varying(120),
    featured boolean,
    created_at timestamp(0) without time zone,
    updated_at timestamp(0) without time zone,
    tags text,
    cover character varying(128),
    licence character varying(400),
    subtitles boolean,
    subtitles_file character varying(400),
    description text,
    mediainfo text,
    slug character varying(255),
    ipfs_hash character varying NOT NULL,
    moderated boolean
);


ALTER TABLE public.releases OWNER TO curator;

--
-- TOC entry 3280 (class 0 OID 0)
-- Dependencies: 200
-- Name: COLUMN releases.id; Type: COMMENT; Schema: public; Owner: curator
--

COMMENT ON COLUMN public.releases.id IS 'The unique identifier of each release.';


--
-- TOC entry 3281 (class 0 OID 0)
-- Dependencies: 200
-- Name: COLUMN releases.name; Type: COMMENT; Schema: public; Owner: curator
--

COMMENT ON COLUMN public.releases.name IS 'The name of the release.';


--
-- TOC entry 3282 (class 0 OID 0)
-- Dependencies: 200
-- Name: COLUMN releases.ipfs_hash; Type: COMMENT; Schema: public; Owner: curator
--

COMMENT ON COLUMN public.releases.ipfs_hash IS 'The IPFS hash used to locate and seed the content.';


--
-- TOC entry 201 (class 1259 OID 16405)
-- Name: tags; Type: TABLE; Schema: public; Owner: curator
--

CREATE TABLE public.tags (
    id integer NOT NULL
);


ALTER TABLE public.tags OWNER TO curator;

--
-- TOC entry 3272 (class 0 OID 16417)
-- Dependencies: 204
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: curator
--



--
-- TOC entry 3271 (class 0 OID 16413)
-- Dependencies: 203
-- Data for Name: deleted; Type: TABLE DATA; Schema: public; Owner: curator
--



--
-- TOC entry 3270 (class 0 OID 16410)
-- Dependencies: 202
-- Data for Name: relations; Type: TABLE DATA; Schema: public; Owner: curator
--



--
-- TOC entry 3268 (class 0 OID 16396)
-- Dependencies: 200
-- Data for Name: releases; Type: TABLE DATA; Schema: public; Owner: curator
--



--
-- TOC entry 3269 (class 0 OID 16405)
-- Dependencies: 201
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: curator
--



--
-- TOC entry 3134 (class 2606 OID 16400)
-- Name: releases releases_unique; Type: CONSTRAINT; Schema: public; Owner: curator
--

ALTER TABLE ONLY public.releases
    ADD CONSTRAINT releases_unique PRIMARY KEY (id);


--
-- TOC entry 3136 (class 2606 OID 16409)
-- Name: tags tags_unique; Type: CONSTRAINT; Schema: public; Owner: curator
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_unique PRIMARY KEY (id);


--
-- TOC entry 3137 (class 1259 OID 16420)
-- Name: categories_id_unique; Type: INDEX; Schema: public; Owner: curator
--

CREATE UNIQUE INDEX categories_id_unique ON public.categories USING btree (id);


--
-- TOC entry 3130 (class 1259 OID 16401)
-- Name: releases_id_idx; Type: INDEX; Schema: public; Owner: curator
--

CREATE UNIQUE INDEX releases_id_idx ON public.releases USING btree (id);


--
-- TOC entry 3131 (class 1259 OID 16421)
-- Name: releases_ipfs_hash_idx; Type: INDEX; Schema: public; Owner: curator
--

CREATE UNIQUE INDEX releases_ipfs_hash_idx ON public.releases USING btree (ipfs_hash);


--
-- TOC entry 3132 (class 1259 OID 16416)
-- Name: releases_slug_idx; Type: INDEX; Schema: public; Owner: curator
--

CREATE UNIQUE INDEX releases_slug_idx ON public.releases USING btree (slug);


-- Completed on 2021-05-11 20:07:39 AWST

--
-- PostgreSQL database dump complete
--
