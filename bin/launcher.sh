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

# store4 (running)
for file in store4.26 store4.27;
do
    in=/antelink/store0/tmp-compute-checksums/store4/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store4/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

for file in store4.25.02 store4.28 store4.29;
do
    in=/antelink/store0/tmp-compute-checksums/store4/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store4/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store5 (running)
for file in store5.22.02 store5.23 store5.24;
do
    in=/antelink/store0/tmp-compute-checksums/store5/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store5/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

for file in store5.26.02 store5.27 store5.28 store5.29;
do
    in=/antelink/store0/tmp-compute-checksums/store5/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store5/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store6 (running)
for file in store6.23.02 store6.24;
do
    in=/antelink/store0/tmp-compute-checksums/store6/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store6/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

for file in store6.25;
do
    in=/antelink/store0/tmp-compute-checksums/store6/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store6/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

for file in store6.30.02 store6.31;
do
    in=/antelink/store0/tmp-compute-checksums/store6/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store6/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

for file in store6.32;
do
    in=/antelink/store0/tmp-compute-checksums/store6/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store6/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

for file in store6.33;
do
    in=/antelink/store0/tmp-compute-checksums/store6/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store6/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store7 (running)
for file in store7.30.02 store7.31 store7.32 store7.33 ;
do
    in=/antelink/store0/tmp-compute-checksums/store7/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store7/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

for file in store7.24.02 store7.25 store7.26 store7.27;
do
    in=/antelink/store0/tmp-compute-checksums/store7/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store7/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store8 (running)
for file in store8.23.02 store8.24 store8.25 store8.26 store8.27;
do
    in=/antelink/store0/tmp-compute-checksums/store8/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store8/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

for file in store8.29.02 store8.30 store8.31 store8.32 store8.33;
do
    in=/antelink/store0/tmp-compute-checksums/store8/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store8/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store9
for file in store9.01 store9.02 store9.03 store9.04 store9.05 store9.06 store9.07;
do
    in=/antelink/store0/tmp-compute-checksums/store9/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/store9/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

# store huge
for n in 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22;
do
    file=huge.$n
    in=/antelink/store0/tmp-compute-checksums/huge-files/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/huge-files/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done

for n in 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38;
do
    file=huge.$n
    in=/antelink/store0/tmp-compute-checksums/huge-files/file-$file.csv
    out=/antelink/store0/tmp-compute-checksums/huge-files/checksums-$file.csv
    logfile=/home/andumont/compute-checksums-$file.log
    cat $in | PYTHONPATH=$PYTHONPATH:/home/andumont/swh-core:/home/andumont/swh-loader-antelink python3 -m swh.loader.antelink.compute_checksums $logfile > $out
done
