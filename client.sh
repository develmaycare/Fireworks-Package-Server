#! /bin/bash

# This is a really simple client for testing the package server.
# by FSD, 10/9/10

# Connect to the server using `Accept: application/json`.
function json_connect()
{
    local url=$1;
    echo "------------------------------- CONNECTING TO SERVER ($url) --------------------";
    wget -O tmp.txt --header="Accept: application/json" 127.0.0.1:8000/$url;
    echo "------------------------------------- RESULTS --------------------------------";
    cat tmp.txt;
    echo "------------------------------------------------------------------------------";
    rm tmp.txt;
}

# Connect to the server using `Accept: text/html`.
function html_connect()
{
    local url=$1;
    echo "------------------------------- CONNECTING TO SERVER ($url) --------------------";
    wget -O tmp.txt --header="Accept: text/html" 127.0.0.1:8000/$url;
    echo "------------------------------------- RESULTS --------------------------------";
    cat tmp.txt;
    echo "------------------------------------------------------------------------------";
    rm tmp.txt;
}

clear;

json_connect "packages/";
json_connect "packages/wordpress";
