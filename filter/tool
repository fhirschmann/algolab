#!/bin/bash

case "$1" in
    drop)
        mongo osm-data --eval "db.dropDatabase();"
        ;;
    *)
        echo "Usage: tool {drop}"
        ;;
esac
