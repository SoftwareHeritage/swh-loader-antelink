---
--- Software Heritage - Antelink Data Model
---

-- scan of sesi-pv-lc2 data, antelink's backup fresh from 2 years
alter table content rename to content_sesi;

-- scan of antelink's data from s3 (fresher than content_sesi)
create table content_s3
(
  sha1 bytea primary key,
  path text not null
);


-- a SHA1 checksum (not necessarily originating from Git)
create domain sha1 as bytea check (length(value) = 20);

-- a Git object ID, i.e., a SHA1 checksum
create domain sha1_git as bytea check (length(value) = 20);

-- a SHA256 checksum
create domain sha256 as bytea check (length(value) = 32);

create type content_status as enum ('absent', 'visible', 'hidden');


create table content_sesi_all
(
    sha1      sha1 primary key,
    sha1_git  sha1_git not null,
    sha256    sha256 not null,
    length    bigint not null,
    path text not null,
    corrupted boolean not null
);
