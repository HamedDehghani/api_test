CREATE SEQUENCE public.pk_identity_seq INCREMENT 1 START 4 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1;
ALTER SEQUENCE public.pk_identity_seq OWNER TO postgres;

CREATE TABLE public.features (
    id bigint DEFAULT nextval('public.pk_identity_seq'::regclass) NOT NULL,
    name character varying NOT NULL,
    value character varying,
    active boolean,
    updated_at timestamp with time zone
);

insert into features (name, active, updated_at) values ('price_change', true, '2020-01-23 15:35:00+03:30');
select * from features;
