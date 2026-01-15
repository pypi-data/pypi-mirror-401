import logging

from os import getcwd
from json import load
from fastavro.schema import load_schema
from mynk_etl.utils.common.constants import Constants
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.error import SchemaRegistryError


logger = logging.getLogger(__name__)
schema_client = SchemaRegistryClient(Constants.KAFKA_SCHEMA_CLIENT.value)

    
def get_schema_str(schema_registry_subject):
    try:
        schema_version = schema_client.get_latest_version(schema_registry_subject)
        schema = schema_client.get_schema(schema_version.schema_id)
    except SchemaRegistryError as err:
        logger.warning("Schema does not exists : " + str(err))    

    return schema


def get_clientSchema(fl_nm: str, schema_type: str):

    path = Constants.INFRA_CFG.value["Kafka"]["schema"][schema_type.lower()]

    if schema_type == "JSON":
        fl_nm += ".json"
        with open(getcwd() + path + fl_nm) as fl:
            schema = load(fl)
    else:
        fl_nm += ".avsc"
        schema = load_schema(getcwd() + path + fl_nm)

    return schema

