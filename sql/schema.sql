---
--- Software Heritage - Antelink Data Model
---

-- scan of sesi-pv-lc2 data, antelink's backup fresh from 2 years
alter table content rename to content_sesi_ante_drama;

-- a SHA1 checksum (not necessarily originating from Git)
create domain sha1 as bytea check (length(value) = 20);

-- a Git object ID, i.e., a SHA1 checksum
create domain sha1_git as bytea check (length(value) = 20);

-- a SHA256 checksum
create domain sha256 as bytea check (length(value) = 32);

create type content_status as enum ('absent', 'visible', 'hidden');

-- scan of antelink's data from s3 (fresher than content_sesi_ante_drama)
create table content_s3
(
    sha1 sha1 primary key,
    path text not null,
    length bigint not null
);

-- alter table content_s3 alter column sha1 set data type sha1;

create table content_sesi
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

-- create unique index on content_sesi (sha1);
create index on content_sesi (sha1)
where not corrupted;

-- alter table content_sesi_all drop constraint content_sesi_all_pkey;
-- alter table content_sesi_all add primary key(origin_sha1, path);

-- consider all s3 sha1 that are not already in sesi (if not corrupted)
create materialized view content_s3_not_in_sesi
as select sha1
   from content_s3 as s3
   where not exists (select 1
                     from content_sesi as sesi
                     where s3.sha1 = sesi.sha1
                     and not corrupted);
-- 16609944

create unique index on content_s3_not_in_sesi(sha1);

-- consider from that all sha1 not already in swh
create materialized view content_s3_not_in_sesi_nor_in_swh
as select sha1
   from content_s3_not_in_sesi as s3
   where not exists (select 1
                     from content as swh
                     where s3.sha1 = swh.sha1);
-- 12637533

-- consider only not corrupted sha1 in sesi not already present in swh
create materialized view content_sesi_not_in_swh
as select sha1
   from content_sesi as sesi
    where not corrupted
    and not exists (select 1
                    from content as swh
                    where sesi.sha1 = swh.sha1);
-- 190139056

SELECT sum(s3.length)
FROM content_s3_not_in_sesi_nor_in_swh s3_not
INNER JOIN content_s3 s3
on s3_not.sha1 = s3.sha1;
-- 13594449732809 -> ~12.364080005508185 Tib

-- estimates of files with size >= 100Mib
select sum(length)
from content_sesi
where not corrupted
and length >= 104857600;
-- 12490817718209 b = 11.360332535522502 Tib

-- Find the maximal length on content_sesi
select max(length)
from content_sesi;
-- 5659069799 b = 5.2704194551333785 Gib

--
-- First computation
--

create materialized view content_sesi_old_not_in_s3
as select sha1
   from content_sesi_ante_drama sesi
   where not exists (select 1
                     from content_s3 s3
                     where sesi.sha1 = s3.sha1);
--

-- Create content present on s3 and not on sesi (could be present in
-- swh though)...
create materialized view content_s3_not_in_sesi_old
as select sha1, path
    from content_s3 as s3
    where not exists (select 1
                      from content_sesi_ante_drama as sesi
                      where s3.sha1 = sesi.sha1);
-- 741797

create materialized view content_s3_not_in_sesi_nor_in_swh_old
as select sha1, path
    from content_s3_not_in_sesi_old as s3
    where not exists (select 1
                      from content as swh
                      where s3.sha1 = swh.sha1);
-- 46

create materialized view content_sesi_not_in_swh_old
as select sha1
    from content_sesi_ante_drama as sesi
    where not exists (select 1
                      from content as swh
                      where sesi.sha1 = swh.sha1);
-- 207095510
