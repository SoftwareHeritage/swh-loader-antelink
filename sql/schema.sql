---
--- Software Heritage - Antelink Data Model
---

-- scan of sesi-pv-lc2 data, antelink's backup fresh from 2 years
alter table content rename to content_sesi;

-- a SHA1 checksum (not necessarily originating from Git)
create domain sha1 as bytea check (length(value) = 20);

-- a Git object ID, i.e., a SHA1 checksum
create domain sha1_git as bytea check (length(value) = 20);

-- a SHA256 checksum
create domain sha256 as bytea check (length(value) = 32);

create type content_status as enum ('absent', 'visible', 'hidden');

-- scan of antelink's data from s3 (fresher than content_sesi)
create table content_s3_2
(
    sha1 bytea primary key,
    path text not null,
    length bigint not null
);

-- alter table content_s3 alter column sha1 set data type sha1;

create table content_sesi_all
(
    sha1      sha1 primary key,
    sha1_git  sha1_git not null,
    sha256    sha256 not null,
    length    bigint not null,
    path text not null,
    corrupted boolean not null
);

-- Create content present on s3 and not on sesi (could be present in swh though)...
create materialized view if not exists content_s3_not_in_sesi
as select sha1, path
   from content_s3 as s3
   where not exists
     (select 1 from content_sesi as sesi where s3.sha1 = sesi.sha1)
with data;
