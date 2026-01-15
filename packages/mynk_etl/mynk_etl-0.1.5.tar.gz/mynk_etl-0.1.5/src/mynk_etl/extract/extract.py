from abc import ABC, abstractmethod
from pyspark.sql import DataFrame

class Extract(ABC):

    @abstractmethod
    def extractSparkStreamData(self, topic: str) -> DataFrame:
        ...

    @abstractmethod
    def extractSparkData(self, topic: str) -> DataFrame:
        ...