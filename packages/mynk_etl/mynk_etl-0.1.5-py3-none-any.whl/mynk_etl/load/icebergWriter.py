import logging

from typing import Any
from attrs import define, field

from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from mynk_etl.load.load import Load
from mynk_etl.sparkUtils.sparkComfunc import writerConfig


logger = logging.getLogger(__name__)


@define(kw_only=True)
class IcebergWriter(Load):
    df: DataFrame
    key: str = field(eq=str)

    
    def streamWriter(self, param_dct: dict[str, Any]) -> None:

        table = self.key.split('.')[1].lower()
        
        logger.info(f"Writing Table : {param_dct['dbName']}.{table}")

        x = self.df.writeStream.trigger(processingTime=param_dct['triggering'])

        for k, v in param_dct['Opts'].items():
            if k != 'path':
                x = x.option(k, v)

        if param_dct['partition']:
            x.toTable(f"nessie.{param_dct['dbName']}.{table}", format="iceberg", outputMode=param_dct['mode'], partitionBy=param_dct['partcols'].split(','), checkpointLocation=param_dct['checkpointLocation']).awaitTermination(timeout=int(param_dct['timeout']))
        else:
            x.toTable(f"nessie.{param_dct['dbName']}.{table}", format="iceberg", outputMode=param_dct['mode'], checkpointLocation=param_dct['checkpointLocation']).awaitTermination(timeout=int(param_dct['timeout']))
        

    def nonStreamWriter(self, param_dct: dict[str, Any]) -> None:

        table = self.key.split('.')[1].lower()
        
        logger.info(f"Writing Table : {param_dct['dbName']}.{table}")
        
        x = self.df.writeTo(f"nessie.{param_dct['dbName']}.{table}").using("iceberg")
        
        if param_dct['partition']:
            x = x.partitionedBy(*[col(x) for x in param_dct['partcols'].split(",")])
        
        __OPS_TYPE = {
            "create" : x.createOrReplace(),
            "append" : x.append(),
            "overwrite" : x.overwritePartitions()
        }

        __OPS_TYPE[param_dct['mode']]
            
          

    def multiSinkWriter(self, param_dct: dict[str, Any]) -> None:
        
        table = self.key.split('.')[1].lower()

        logger.info(f"Writing Table : {param_dct['dbName']}.{table}")

        x = self.df.writeTo(f"nessie.{param_dct['dbName']}.{table}").using("iceberg")
        
        if param_dct['partition'] == 'Y':
            x = x.partitionedBy(*[col(x) for x in param_dct['partcols'].split(",")])

        x.append()


    __writerType = {
        "NonStream": nonStreamWriter,
        "Streaming": streamWriter,
        "MultiSink": multiSinkWriter
    }

    def writer(self) -> None:

        wrt_dct = writerConfig(self.key)
        logger.info(wrt_dct)

        return self.__writerType[wrt_dct['type']](self, wrt_dct)