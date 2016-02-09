---
--- Software Heritage - Antelink Data Model
---

create table content_s3
(
  sha1 bytea primary key,
  path text not null
);
