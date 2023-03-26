
# https://dev.to/mvillarrealb/creating-a-spark-standalone-cluster-with-docker-and-docker-compose-2021-update-6l4

Environment	Description
SPARK_MASTER	Spark master url
SPARK_WORKER_CORES	Number of cpu cores allocated for the worker
SPARK_WORKER_MEMORY	Amount of ram allocated for the worker
SPARK_DRIVER_MEMORY	Amount of ram allocated for the driver programs
SPARK_EXECUTOR_MEMORY	Amount of ram allocated for the executor programs
SPARK_WORKLOAD	The spark workload to run(can be any of master, worker, submit)


# docker build -t cluster-apache-spark:3.0.2 .

docker build -t cluster-apache-spark:3.3.2 .
docker-compose up -d

psql -U postgres -h 0.0.0.0 -p 5432
# It will ask for your password defined in the compose file

/opt/spark/bin/spark-submit --master spark://spark-master:7077 \
--jars /opt/spark-apps/postgresql-42.2.22.jar \
--driver-memory 1G \
--executor-memory 1G \
/opt/spark-apps/main.py