#!/bin/bash

while true
do
  #date

  # clear input.csv file
  if [ -e input.csv ]; then
	rm input.csv
  fi

  # check SMS message
  python sms2_run.py > input.csv

  # update Google SpreadSheet
  if [ -s input.csv ]; then
	python update_oauth.py input.csv
  fi

  # sleep
  sleep 5
done

