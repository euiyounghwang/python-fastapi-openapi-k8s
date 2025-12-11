#!/bin/sh
SPARK_EXPORT_PATH=/apps/monitoring_script/spark/latest
SERVICE_NAME=es-spark-workers-service

SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"


case "$1" in
  start)
        # Start daemon.
        echo "🦄 Starting $SERVICE_NAME";
        # nohup $SPARK_EXPORT_PATH/bin/spark-class org.apache.spark.deploy.worker.Worker spark://VM_Node_#1:7077 &> /dev/null &
        # $SPARK_EXPORT_PATH/bin/spark-class org.apache.spark.deploy.worker.Worker spark://VM_Node_#1:7077
        $SPARK_EXPORT_PATH/sbin/start-worker.sh spark://VM_Node_#1:7077
        ;;
  stop)
        # Stop daemons.
        echo "🦄 Shutting down $SERVICE_NAME";
        pid=`ps ax | grep -i 'org.apache.spark.deploy.worker.Worker' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          kill -9 $pid
         else
          echo "🦄 $SERVICE_NAME was not Running"
        fi
        ;;
  restart)
        $0 stop
        sleep 2
        $0 start
        ;;
  status)
        pid=`ps ax | grep -i 'org.apache.spark.deploy.worker.Worker' | grep -v grep | awk '{print $1}'`
        if [ -n "$pid" ]
          then
          echo "🦄 $SERVICE_NAME is Running as PID: $pid"
        else
          echo "🦄 $SERVICE_NAME is not Running"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
esac

