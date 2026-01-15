from typing import Any
from pyspark import SparkContext
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, year, month, dayofmonth, trim

from mynk_etl.utils.common.constants import Constants
from mynk_etl.utils.common.genUtils import param_init
from mynk_etl.utils.common.marketUtils import marketCheck
from mynk_etl.utils.logger.logDecor import logtimer

@logtimer
def colTrim(df: DataFrame) -> DataFrame:
    for i in df.columns:
        df = df.withColumn(i, trim(col(i)))

    return df


@logtimer
def defaultPartition(nonPartDF: DataFrame, datetimeCol: str) -> DataFrame:
    
    partDF = nonPartDF.withColumn("year", year(col(datetimeCol)))\
    .withColumn("month", month(col(datetimeCol)))\
    .withColumn("day", dayofmonth(col(datetimeCol)))

    return partDF


def writerConfig(key) -> dict[str, Any]:

    prop_key, conf_dict, prop_dict = param_init(key)

    if not marketCheck():
        prop_dict['type'] = 'NonStream'
    
    typeOfData = prop_dict['type']

    wrt_dct = {}
    wrt_dct['type'] = prop_dict['type']
    wrt_dct['partition'] = prop_dict['partition']
    if wrt_dct['partition']:
        wrt_dct['partcols'] = prop_dict['partcols']
    wrt_dct['dbName'] = conf_dict['dbName']

    # wrt_dct['hdfsPath'] = fetch_conf()['SparkParam']['common']['hdfsPath']   
    typeOfOps_dict = Constants.INFRA_CFG.value[typeOfData]['common']
    wrt_dct['mode'] = typeOfOps_dict['mode']
    wrt_dct['Opts'] = Constants.INFRA_CFG.value[typeOfData]['Opts']

    if typeOfData == 'Streaming':
        wrt_dct['triggering'] = typeOfOps_dict['triggering']
        wrt_dct['timeout'] = typeOfOps_dict['timeout']
        wrt_dct['checkpointLocation'] = "s3://" + typeOfOps_dict['checkpointLocation'] + prop_key

    return wrt_dct


def s3aSparkConfig(spark_context: SparkContext) -> None:

    spark_context._jsc.hadoopConfiguration().set("fs.s3a.access.key", Constants.MINIO.value["user"]) # type: ignore
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.secret.key", Constants.MINIO.value["pass"]) # type: ignore
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.endpoint", Constants.MINIO.value["endpoint"]) # type: ignore
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled", "false") # type: ignore
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true") # type: ignore
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.attempts.maximum", "1") # type: ignore
    spark_context._jsc.hadoopConfiguration().set("fs.s3a.connection.establish.timeout", "5000") # type: ignore