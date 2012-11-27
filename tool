#!/bin/bash

# Path to the algorithm lab tools
ALGO_PATH=${ALGO_PATH:-./}

# Path to a map
ALGO_OSM_DATA=${ALGO_OSM_DATA:-${ALGO_PATH}/suedhessen.osm}

# Host/Port
ALGO_OSM_HOST=${ALGO_OSM_HOST:-127.0.0.1}
ALGO_OSM_PORT=${ALGO_OSM_PORT:-27017}


# Amount of memory to use
ALGO_MEM=${ALGO_MEM:-3000m}
ACTION=$1

JAVA="java -jar -Xms256m -Xmx${ALGO_MEM}"


case "$1" in
    dropdb)
        mongo osm-data --eval "db.dropDatabase();"
        ;;

    1)
        $JAVA 1_osm_railway_graph_import/osm_railway_graph_import.jar \
            $ALGO_OSM_DATA $ALGO_OSM_HOST $ALGO_OSM_PORT
        ;;

    2)
        cd 2_shortest_routes_finder
        $JAVA shortest_routes_finder.jar \
            railway_graph 16 $ALGO_OSM_HOST $ALGO_OSM_PORT
        ;;

    3)
        $JAVA 3_simple_routes_filter/simple_routes_filter.jar \
            $ALGO_OSM_HOST $ALGO_OSM_PORT
        ;;

    4)
        cd 4_railviz
        java -Xmx${ALGO_MEM} -classpath railviz_2.0.jar railViz/RailViz -p conf/config.xml -s -dr
        ;;
    4r)
        echo "Removing serialized data..."
        rm -rvf 4_railviz/data/november2/Optimized/serialized/
        $0 4
        ;;

    5)
        cd 5_web_frontend_motis_\(randm\)/code
        rails s
        ;;

    *)
        echo "Usage: tool {dropdb|1|2|3|4|4r|5}"
        ;;
esac
