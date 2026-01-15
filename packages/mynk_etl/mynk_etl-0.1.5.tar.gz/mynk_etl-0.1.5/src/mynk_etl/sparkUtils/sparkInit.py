from pyspark import SparkConf
from pyspark.sql import SparkSession

from mynk_etl.utils.common.constants import Constants
from mynk_etl.utils.logger.logDecor import inOutLog
from mynk_etl.sparkUtils.sparkComfunc import s3aSparkConfig


@inOutLog
def sparkIcebergKafka(key: str) -> SparkSession:

    appName = Constants.INFRA_CFG.value[key.split('.')[0]]['appName'] + "-" + key.split('.')[1] + "-" + str(Constants.RUN_ID.value) 
    # jarsHdfsPath = fetch_conf()['SparkParam']['common']['jarsHdfsPath']
    # jars_list = fetch_conf()['SparkParam']['kafkaIcebergNessie']['jars']
    # jars = ",".join([jarsHdfsPath + jar for jar in jars_list])

    conf = (
            SparkConf()
            .setMaster(Constants.SPARK_MASTER.value['master'])
            .setAppName(appName)
            .set("spark.executor.memory", "4g")
            .set("spark.executor.cores", "2")
            .set("spark.cores.max", "4")
            .set("spark.driver.memory", "2g")
            .set("spark.driver.cores", "1")
            .set('spark.jars.packages', 'org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.9.0,org.apache.hadoop:hadoop-aws:3.3.4,software.amazon.awssdk:bundle:2.30.38,software.amazon.awssdk:url-connection-client:2.30.38,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.5,org.apache.kafka:kafka-clients:3.6.2,org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.5.5,org.apache.spark:spark-avro_2.12:3.5.5')
            .set('spark.sql.extensions', 'org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions')
            .set('spark.sql.catalog.nessie', 'org.apache.iceberg.spark.SparkCatalog')
            .set("spark.sql.catalog.nessie.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")
            .set('spark.sql.catalog.nessie.uri', Constants.NESSIE.value['url'])
            .set('spark.sql.catalog.nessie.warehouse', Constants.NESSIE.value['warehouse'])
            .set("spark.sql.catalog.nessie.type", "rest")
            .set('spark.streaming.stopGracefullyOnShutdown', 'true')
            .set('spark.sql.streaming.schemaInference', 'true')
            .set("spark.sql.session.timeZone", "Asia/Kolkata")
            .set("spark.sql.shuffle.partitions", "9")
        )

    spark = SparkSession.builder.config(conf=conf).getOrCreate() # type: ignore

    s3aSparkConfig(spark)

    return spark

