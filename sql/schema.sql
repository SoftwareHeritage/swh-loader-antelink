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
create table content_s3
(
    sha1 sha1 primary key,
    path text not null,
    length bigint not null
);

-- alter table content_s3 alter column sha1 set data type sha1;

create table content_sesi_all
(
    origin_sha1 sha1 not null,
    sha1        sha1 not null,
    sha1_git    sha1_git not null,
    sha256      sha256 not null,
    length      bigint not null,
    path text   not null,
    corrupted   boolean not null,
    primary key (origin_sha1, path)
);

-- alter table content_sesi_all drop constraint content_sesi_all_pkey;
-- alter table content_sesi_all add primary key(origin_sha1, path);


-- Create content present on s3 and not on sesi (could be present in
-- swh though)...
create materialized view content_s3_not_in_sesi
as select sha1, path
    from content_s3 as s3
    where not exists
      (select 1 from content_sesi as sesi where s3.sha1 = sesi.sha1);

create materialized view content_s3_not_in_sesi_nor_in_swh
as select sha1, path
from content_s3_not_in_sesi as s3
where not exists
(select 1 from content as swh where s3.sha1 = swh.sha1);

-- after copy from swh the content table
-- create unique index on content(sha1_git);

create materialized view content_sesi_not_in_swh
as select sha1
from content_sesi as sesi
where not exists
(select 1 from content as swh where sesi.sha1 = swh.sha1);
