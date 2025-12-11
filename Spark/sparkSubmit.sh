#!/bin/sh
#SPARK_PATH=/apps/spark-2.2.0-bin-hadoop2.7
SPARK_PATH=/apps/monitoring_script/spark
JAR_LOC=/home/spark/test.jar
PATH=$PATH:$SPARK_PATH/bin
MASTER_HOST=localhost
MASTER_URL=spark://$MASTER_HOST:7077
#MASTER_WEB_URL=http://$MASTER_HOST:8080
MASTER_WEB_URL=https://$MASTER_HOST:8480
appname=streamprocess_wmx
#secret_file=/home/spark/spark-secret
# See how we were called.
case "$1" in
  start)
        # Start daemon.
        echo "Starting SparkSubmit Job"
        # $SPARK_PATH/bin/spark-submit  --driver-java-options "-Dlog4j.configuration=file:$SPARK_PATH/conf/StreamProcessLogDriverWMx.properties" --conf "spark.executor.extraJavaOptions=-XX:+UseG1GC -Dlog4j.configuration=file:$SPARK_PATH/conf/StreamProcessLogExecutorWMx.properties -Dspark.authenticate=true -Dspark.authenticate.secret=file:$secret_file" --executor-memory 1g   --driver-memory 1g --total-executor-cores 6   --deploy-mode client --supervise  --master $MASTER_URL  --jars $JAR_LOC  --class com.xpo.bi.StreamProcess /apps/spark/custom/test.jar &
        # /apps/monitoring_script/spark/latest/bin/spark-submit --master spark://localhost:7077 /apps/monitoring_script/spark/utils/hello-spark.py
        $SPARK_PATH/latest/bin/spark-submit --master spark://$MASTER_HOST:7077 $SPARK_PATH/utils/hello-spark.py
        ;;
  stop)
        # Stop daemons.
        echo "Shutting down SparkSubmit WMX"
        #cmd="curl -s $MASTER_WEB_URL/json/ "
        cmd="curl -s $MASTER_WEB_URL/json/ --insecure"
        json=`$cmd | jq . > $appname.json`
        activeApps=`jq .activeapps[]  $appname.json`
        currentApp=`echo $activeApps  | jq 'select(.name=="PysparkCount")' >  $appname.json`
        currentAppId=`jq -r .id  $appname.json`
        echo $currentAppId
        contentTypeJson="Content-Type:application/json"
        params="{\"id\": $currentAppId, \"terminate\": \"true\"}"
        #killCmd="curl -X POST  $MASTER_WEB_URL/app/kill/  -d id=$currentAppId&terminate=true "
        killCmd="curl -X POST  $MASTER_WEB_URL/app/kill/  -d id=$currentAppId&terminate=true --insecure"
        status=`$killCmd`
        echo $status
        ;;
  restart)
        $0 stop
        sleep 2
        $0 start
        ;;
  status)
        #cmd="curl -s $MASTER_WEB_URL/json/"
        cmd="curl -s $MASTER_WEB_URL/json/ --insecure"
        json=`$cmd | jq . > $appname.json`
        activeApps=`jq .activeapps[]  $appname.json `
        currentApp=`echo $activeApps  | jq 'select(.name=="PysparkCount")' >  $appname.json`
        currentAppStatus=`jq '.name  + " with Id " + .id + " is  " + .state' $appname.json`
        echo $currentAppStatus
        ;;
  *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
esac

exit 0
