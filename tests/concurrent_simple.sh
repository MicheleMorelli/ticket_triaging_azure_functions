#! /bin/bash

# simple script to test the system against multiple
# concurrent requests
for i in {1..100};
do
    bash az_performance_tests.sh &
done

