import datetime
import json
import os
import shutil
import sys

from pyspark import SparkConf, SparkContext
from pyspark.rdd import RDD
from pyspark.sql import Row, SparkSession
from pyspark.streaming import StreamingContext

some_file_path = 'meetup_spark.sql'
checkpoint_path = 'checkpoint_01'
stream_hostname = 'localhost'
stream_port = 301


def get_sql_query() -> str:
    """Getting the SQL Template
    """
    with open(some_file_path, 'r') as f:
        return f.read()



def get_spark_session_instance(spark_conf: SparkConf) -> SparkSession:
    """ Lazily instantiated global instance of SparkSession
    """
    if 'sparkSessionSingletonInstance' not in globals():
        globals()['sparkSessionSingletonInstance'] = SparkSession \
            .builder \
            .config(conf=spark_conf) \
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']


def process(time: datetime.datetime, rdd: RDD[str]) -> None:
    """Convert RDDs of the words DStream to DataFrame and run SQL query
    """
    print("===========-----> %s <-----===========" % str(time))

    try:
        spark = get_spark_session_instance(rdd.context.getConf())

        row_rdd = rdd.map(lambda w: Row(
            venue_name=w.get('venue_name'),
            venue_id=w.get('venue_id'),
            lon=w.get('lon'),
            lat=w.get('lat'),
            event_name=w.get('event_name'),
            event_id=w.get('event_id'),
            event_time=w.get('event_time'),
            event_url=w.get('event_url'),
            range=w.get('range'),
        ))

        test_data_frame = spark.createDataFrame(row_rdd)

        test_data_frame.createOrReplaceTempView("meetup_events")

        sql_query = get_sql_query()
        test_result_data_frame = spark.sql(sql_query)
        test_result_data_frame.show(n=5)

        # Insert into DB
        try:
            test_result_data_frame.write \
                .format("jdbc") \
                .mode("append") \
                .option("driver", 'org.postgresql.Driver') \
                .option("url", "jdbc:postgresql://localhost:5432/meetupDB") \
                .option("dbtable", "transaction_flow") \
                .option("user", "spark_user_2702") \
                .option("password", "K6IL@F5PW7RdqTiQdtAC") \
                .save()

        except Exception as e:
            print("--> Opps! It seems an Errrorrr with DB working!", e, file=sys.stderr)

    except Exception as e:
        print("--> Opps! Is seems an Error!!!", e, file=sys.stderr)


def create_context():
    """General function
    """
    sc = SparkContext(appName="PythonMeetupStreaming")
    sc.setLogLevel("ERROR")

    ssc = StreamingContext(sc, 2)

    try:
        lines = ssc.socketTextStream(hostname=stream_hostname, port=stream_port)
        parsed_lines = lines.map(lambda v: json.loads(v))

    except Exception as ex:
        print("Producer error:", ex, file=sys.stderr)
        raise ConnectionError()

    # RDD handling
    parsed_lines.foreachRDD(process)

    return ssc


def main():
    print("--> Creating new context")
    if os.path.exists(checkpoint_path):
        shutil.rmtree('outputPath')

    ssc = StreamingContext.getOrCreate(checkpoint_path, lambda: create_context())
    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    main()
