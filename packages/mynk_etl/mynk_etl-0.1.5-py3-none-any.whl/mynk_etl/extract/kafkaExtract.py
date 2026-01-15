from attrs import define, field

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import col, expr
from pyspark.sql.types import StringType


from mynk_etl.extract.extract import Extract
from mynk_etl.utils.common.constants import Constants
from mynk_etl.utils.common.genUtils import param_init
from mynk_etl.utils.common.kUtils import get_schema_str
from mynk_etl.utils.common.marketUtils import marketCheck
from mynk_etl.utils.logger.logDecor import logtimer, inOutLog


@define(kw_only=True)
class KafkaExtract(Extract):
    spark: SparkSession
    key: str = field(eq=str)

    @logtimer
    def extractSparkStreamData(self, topic: str) -> DataFrame:
        """_summary_

        Args:
            topic (str): Kafka topic to subscribe.

        Returns:
            DataFrame: Return dataframe using 'spark.readStream' on the topic.
        """
        kafka_df=(self.spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", Constants.KAFKA_BROKERS.value['bootstrap.servers'])
        .option("subscribe", topic)
        .option("startingOffsets","earliest")
        .option("kafka.compression.type", "snappy")
        # .option("failOnDataLoss", "false")
        # .option("minPartitions", "10")
        # .option("mode", "PERMISSIVE")
        # .option("truncate", False)
        # .option("newRows", 1000)
        .load())

        schema = get_schema_str(topic)
        
        kafka_val_df = kafka_df.withColumn('fixedValue', expr("substring(value, 6, length(value)-5)"))
        kafka_val_df = kafka_val_df.select(col("key").cast(StringType()).alias("symbol"), from_avro(col("fixedValue"), schema.schema_str, {"mode": "PERMISSIVE"}).alias("parsed_value"))
        kafka_val_df = kafka_val_df.select("symbol","parsed_value.*")


        return kafka_val_df


    @logtimer    
    def extractSparkData(self, topic: str) -> DataFrame:
        """_summary_

        Args:
            topic (str): Kafka topic to subscribe.

        Returns:
            DataFrame: Return dataframe using 'spark.read' on the topic.
        """

        kafka_df=(self.spark.read.format("kafka")
            .option("kafka.bootstrap.servers", Constants.KAFKA_BROKERS.value['bootstrap.servers'])
            .option("subscribe", topic)
            .option("startingOffsets","earliest")
            .option("kafka.compression.type", "snappy")
            .load())
        
        schema = get_schema_str(topic)

        kafka_val_df = kafka_df.withColumn('fixedValue', expr("substring(value, 6, length(value)-5)"))
        kafka_val_df = kafka_val_df.select(col("key").cast(StringType()).alias("symbol"), from_avro(col("fixedValue"), schema.schema_str, {"mode": "PERMISSIVE"}).alias("parsed_value"))
        kafka_val_df = kafka_val_df.select("symbol","parsed_value.*")

        return kafka_val_df

    
    __extractType = {
        "NonStream": extractSparkData,
        "Streaming": extractSparkStreamData
    }


    @inOutLog
    def getData(self) -> DataFrame:

        prop_key, conf_dict, prop_dict = param_init(self.key)

        if not marketCheck():
            prop_dict['type'] = 'NonStream'

        self.spark.sql(f"CREATE SCHEMA IF NOT EXISTS nessie.{conf_dict['dbName']}").show()
        
        return self.__extractType[prop_dict['type']](self, prop_key.lower())
