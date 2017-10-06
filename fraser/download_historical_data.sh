
rm temp/*

cur_date=`date +%Y-%m`
echo "current date = $cur_date"
for year in `seq $2 $3`; do
    for month in `seq -w 1 12`; do
        wget -O temp/$1-${year}-${month}.csv "http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=$1&Year=${year}&Month=${month}&Day=14&timeframe=1&submit= Download+Data" ;
        echo "year=$year, month=$month"
        if [ $cur_date == $year-$month ]; then
            break 2
        fi
    done
done

i=1
for f in temp/*.csv; do
    if [ "$i" == "1" ]; then
        cat $f > $1-$2-to-$3-combined.csv
        i=$(( $i + 1 ))
    else
        sed -n '18,$ p' $f >> $1-$2-to-$3-combined.csv
    fi
    echo $f
done

