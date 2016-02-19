# store 10 (running)
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

# store12 (running)
for file in store12.02  store12.03 store12.04 store12.05 store12.06 store12.07 store12.08;
do
    in=/antelink/store0/tmp-compute-checksums/store12/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store12/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store13 (running)
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

# store4 (running)
for file in store4.02 store4.03 store4.04 store4.05 store4.06 store4.07 store4.08 store4.09 store4.10 store4.11 store4.12 store4.13 store4.14 store4.15 store4.16 store4.17 store4.18 store4.19 store4.20 store4.21 store4.22 store4.23 store4.24 store4.25 store4.26 store4.27 store4.28 store4.29;
do
    in=/antelink/store0/tmp-compute-checksums/store4/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store4/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store5 (running)
for file in store5.02 store5.03 store5.04 store5.05 store5.06 store5.07 store5.08 store5.09 store5.10 store5.11 store5.12 store5.13 store5.14 store5.15 store5.16 store5.17 store5.18 store5.19 store5.20 store5.21 store5.22 store5.23 store5.24 store5.25 store5.26 store5.27 store5.28 store5.29;
do
    in=/antelink/store0/tmp-compute-checksums/store5/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store5/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store6 (running)
for file in store6.01 store6.02 store6.03 store6.04 store6.05 store6.06 store6.07 store6.08 store6.09 store6.10 store6.11 store6.12 store6.13 store6.14 store6.15 store6.16 store6.17 store6.18 store6.19 store6.20 store6.21 store6.22 store6.23 store6.24 store6.25 store6.26 store6.27 store6.28 store6.29 store6.30 store6.31 store6.32 store6.33;
do
    in=/antelink/store0/tmp-compute-checksums/store6/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store6/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store7 (running)
for file in store7.01 store7.02 store7.03 store7.04 store7.05 store7.06 store7.07 store7.08 store7.09 store7.10 store7.11 store7.12 store7.13 store7.14 store7.15 store7.16 store7.17 store7.18 store7.19 store7.20 store7.21 store7.22 store7.23 store7.24 store7.25 store7.26 store7.27 store7.28 store7.29 store7.30 store7.31 store7.32 store7.33;
do
    in=/antelink/store0/tmp-compute-checksums/store7/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store7/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store8 (running)
for file in store8.01 store8.02 store8.03 store8.04 store8.05 store8.06 store8.07 store8.08 store8.09 store8.10 store8.11 store8.12 store8.13 store8.14 store8.15 store8.16 store8.17 store8.18 store8.19 store8.20 store8.21 store8.22 store8.23 store8.24 store8.25 store8.26 store8.27 store8.28 store8.29 store8.30 store8.31 store8.32 store8.33;
do
    in=/antelink/store0/tmp-compute-checksums/store8/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store8/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store9 (running)
for file in store9.01 store9.02 store9.03 store9.04 store9.05 store9.06 store9.07;
do
    in=/antelink/store0/tmp-compute-checksums/store9/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store9/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done
