#! /bin/bash

# This is a really simple client for testing the package server.
# by FSD, 10/9/10

echo "------------------------------------ CONNECTING TO SERVER --------------------";
wget -O tmp.txt --header="Accept: application/json" 127.0.0.1:8000/testing/;
#wget -O tmp.txt --header="Accept: text/html" 127.0.0.1:8000/;
#wget -O tmp.txt --header="Accept: application/json" 127.0.0.1:8000/;
#wget -O tmp.txt --header="Accept: application/json" 127.0.0.1:8000/twitter-conn;
echo "------------------------------------- RESULTS --------------------------------";
cat tmp.txt;
echo "------------------------------------------------------------------------------";
rm tmp.txt;
