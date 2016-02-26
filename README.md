swh-loader-antelink
===================

# Goal

The goal of this repository is to retrieve data from antelink's
storage that swh does not already store.

This, in order to reduce the actual cloud service cost of storing
antelink's data (s3).

Out of scope for now:
- The check/deletion of the replicated data from s3 (when the loading
  will be done)
- The metadata information relative to content will be retrieved
  later.

# Workflow

- [X] Compute and inject all hashes from sesi contents (~289M)
- [X] Compute existing data information in s3 (~271M)
- [X] Filter s3 data not in sesi nor in swh (~12.6M)
- [ ] Load the s3 files downloads and store in swh disks
- [ ] Delete the s3 storage contents regarding those files
- [ ] Inject s3 contents in swh
- [ ] Retrieve and inject data from sesi in swh

# data?

All the data up to now are stored in the antelink db.
