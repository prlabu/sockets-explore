#!/bin/bash
my_array=(1 2 3 5 6 7 8 9 10 13 15 17 19 21 28 30 33 35 40 45 50 55 60 70 80 90 100)
for index in "${my_array[@]}"; do python httpClient-keepAlive.py "$index"; done