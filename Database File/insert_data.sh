#!/bin/bash

PSQL="psql -X --username=narawishing --dbname=thailand_recommendations --no-align --tuples-only -c"
echo $($PSQL "TRUNCATE recommendations_place;")
cat Places.csv | while IFS="," read PLACE LAT LONG
do
	if [[ $Place != Place ]]
	then
	
	#Insert
	INSERT_PLACES_RESULTS=$($PSQL "INSERT INTO recommendations_place(name,province,latitude,longitude) VALUES('$PLACE', 'Khon Kaen', $LAT, $LONG);")

	if [[ INSERT_PLACES_RESULTS == "INSERT 0 1" ]]
	then 
		echo Inserted places $PLACE
	fi
fi
done
