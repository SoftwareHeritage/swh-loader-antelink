swh-loader-antelink
===================

<!-- markdown-toc start - Don't edit this section. Run M-x markdown-toc-generate-toc again -->
**Table of Contents**

- [swh-loader-antelink](#swh-loader-antelink)
- [Goal](#goal)
- [Status](#status)
- [Notes](#notes)
- [Workflow overview](#workflow-overview)

<!-- markdown-toc end -->

# Goal

The goal of this repository is to retrieve data from antelink's
storage that swh does not already store.

This, in order to reduce the actual cloud service cost of storing
antelink's data.

Out of scope for now:
- The check/deletion of the replicated data from s3 (when the loading
  will be done)
- The metadata information relative to content will be retrieved
  later.


# Status


There exists:
- an old backup on the machine sesi-pv-lc2.inria.fr (sesi-pv-lc2) in
  `/antelink/`
- an `antelink` db on swh's side with one table 'content' with id
  (sha1 of the uncompressed file), path (referencing the path to the
  compressed content on the sesi-pv-lc2 machine).


# Notes


314 899 904 contents are referenced in the table 'content' (db
antelink).  This represents an ideal representation of the backup in
sesi-pv-lc2 but no longer the reality.


But:
- some data have been lost by inria admin back in october/november
  (bad manipulation). Those are to be considered missing.
- some other data may have been corrupted (checksums could no longer
  match)... Those are to be considered missing.

Also:
- the sesi-pv-lc2 is not complete in regards to s3 storage so an
  extract through `aws-cli s3 ls` has been done by Guillaume.
  This is to be used as input in conjunction with the antelink db.
- Bucket s3 contains gzipped contents.
- sesi-pv-lc2 contains gzipped contents.
- the size in the `aws-cli s3 ls` represents the size of the
  compressed data

Implementation detail change in storage:
- A new table `content_large` in swh-storage with the same structure
as content and content_missing will be created.  This table will be
used to store content metadata when the size is larger than our actual
threshold size.
- The antelink contents are to be injected as blob

# Workflow overview

![Worflow overview](./docs/workflow.png)


# db connection

Ask admin for credential access.

.pgpass:

``` apacheconf
****:****:antelink:guest:****
```

.pg_service.conf:

``` apacheconf
[antelink-swh]
dbname=antelink
host=****
port=****
user=guest
```


# Injection of ls in content_s3

- Name: xyz.ls with x,y,z in [1..f] (hex)
- Number of files: 4096

## round-1 through 6

Multiple issues in data (some uncompressed and duplicated files) thus
in the code, in environment (network failures -> code is run from my
machine) was discovered and fixed.

cf. stats/round-1 files (3% of files were rejected -> 123 files due to
uncompressed files).

Number of uncompressed files: 1 072 939 (without any .gz extension)
``` shell
# tony at corellia in ~/work/inria/repo/swh-environment/swh-loader-antelink on git:master x [10:41:13]
$ cat stats/round-1 | cut -d' ' -f1 | xargs grep -v '.gz' | wc -l
1072939
```

cf. stats/round-2 files containing all the failed files from round-1 reinjected.

Total number of .gz files in those 4096 files: 271 042 276

``` shell
# tony at corellia in ~/work/inria/repo/swh-environment/swh-loader-antelink on git:master x [10:43:35]
$ cat stats/round-1 | cut -d' ' -f1 | xargs cat | grep '.gz' | wc -l
271042276
```

Total number of lines in content_s3 after round-2: 261 380 000

``` sql
antelink=> select count(*) from content_s3;
   count
-----------
 261380000
(1 row)
```

Not every *.ls file were completely injected in db (bug in code).

Total number of files in 4096 files (one row represents one file): 272 115 215

``` shell
# tony at corellia in ~/work/inria/repo/swh-environment/swh-loader-antelink on git:master x [10:47:45]
$ cat stats/round-1 | cut -d' ' -f1 | xargs cat | wc -l
272115215
```

This includes the uncompressed ones.

Thus, total number of compressed ones: 271 042 276

``` newlisp
(- 272115215 1072939) ;; 271042276
```

## round-7 through 8

Fixed multiple problem from previous iteration.

All files in content_s3: 271 042 276

Content in db:
``` sql
antelink=> select count(*) from content_s3;
   count
-----------
 271042276
(1 row)
```

This match the number of compressed files in the 4096 files.
