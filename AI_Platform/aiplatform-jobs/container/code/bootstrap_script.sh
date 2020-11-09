echo 'Running script as start up...'
$(basename $0) && exit

# Parse arguments
for i
    do
        case $i in
            -e=*|--entry_point=*)
                ENTRY_POINT="${i#*=}";
                shift;;
            -p=*|--r_package_path=*)
                R_PACKAGE_PATH="${i#*=}";
                shift;;
            # ... Other options ...
            -*) 
                echo "$0: Unrecognized option $i" >&2
                exit 2;;
            *) 
                echo 'In the Break statement'
                break ;;
        esac
    done

echo $ENTRY_POINT
echo $R_PACKAGE_PATH

echo 'here are the list of files...'
ls -l

echo 'Downloading the files from the bucket...'
# Download the R Package from bucket
gsutil cp $R_PACKAGE_PATH .

echo 'here are the list of files after downloading...'
ls -l

# Execute the function
Rscript $ENTRY_POINT

echo 'R script is executed and here are the list of files...'
ls -l
