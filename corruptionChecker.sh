#Directory corruption tester
#slightly better than 
#for dir in *; do cd $dir; echo Corruption test in $dir; for file in *; do zcat $file | head; zcat $file | tail; done; cd ..; done

cd  /usr/local/apache/htdocs-hgdownload/goldenPath/galGal6
test_corruption () {
    if [[ $1 == *".gz" ]]; then
        zcat $1 | head -n1;
    fi;
}

for dir in * ; do
    echo Going into $dir;
    cd $dir
    for file in *; do
        if [ "$file" == "README.txt" ]; then # -o $file = 
            echo Printing five lines of $dir / $file
            head -n5 $file
            continue;
        fi;
        if [ "$file" == "md5sum.txt" ]; then
            echo Skipping $dir/$file
            continue;
        fi;
        echo Reading from $dir/$file;
        if [ "$file" == "reciprocalBest" ]; then
            cd $file
            for rbfile in .; do
                if [ "$rbfile" == "axtRBestNet" ]; then
                    cd axtRBestNet;
                    for axfile in *.gz; do
                        test_corruption $axfile
                    done;
                    cd ..;
                fi
                test_corruption $rbfile
                cd ..;
                done;
        fi;
        test_corruption $file
    done;
    cd ..
 done