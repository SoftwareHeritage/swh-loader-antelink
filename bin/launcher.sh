# store 10
for file in store10.02 store10.03 store10.04 store10.05 store10.06 store10.07 store10.08 store10.09 store10.10 store10.11;
do
    in=/antelink/store0/tmp-compute-checksums/store10/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store10/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    echo $in $out $logfile
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store 11
for file in store11.02 store11.03 store11.04;
do
    in=/antelink/store0/tmp-compute-checksums/store11/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store11/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store12
for file in store12.02  store12.03 store12.04 store12.05 store12.06 store12.07 store12.08;
do
    in=/antelink/store0/tmp-compute-checksums/store12/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store12/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store13
for file in store13.02 store13.03 store13.04 store13.05 store13.06 store13.07
do
    in=/antelink/store0/tmp-compute-checksums/store13/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store13/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store14
for file in store14.02 store14.03 store14.04 store14.05
do
    in=/antelink/store0/tmp-compute-checksums/store14/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store14/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store15
for file in store15.02 store15.03 store15.04 store15.05 store15.06 store15.07;
do
    in=/antelink/store0/tmp-compute-checksums/store15/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store15/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store16
for file in store16.02 store16.03 store16.04;
do
    in=/antelink/store0/tmp-compute-checksums/store16/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store16/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done
