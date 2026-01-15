from mynk_etl.extract.kafkaExtract import KafkaExtract
from mynk_etl.load.icebergWriter import IcebergWriter
from mynk_etl.sparkUtils.sparkInit import sparkIcebergKafka   


def writeYfData(key: str) -> None:
    """_summary_

    Args:
        key (str): Writes fetched data from Jugaad-Data package via kafka stream to Iceberg table.
    """

    spark = sparkIcebergKafka(key)
    
    df = KafkaExtract(spark=spark, key=key).getData()
    df.show(10, False)
    IcebergWriter(df=df, key=key).writer()

    spark.stop()