import configparser
import logging


def config_fromstring(string: str) -> configparser.ConfigParser:
    try:
        logging.info("Received as config string: \n{}".format(string))
        config = configparser.ConfigParser()
        config.read_string(string)
        logging.info("Parsed config: \n{}".format(string))
        return config
    except:
        logging.info("Unable to parse config from input: \n".format(string))
        return configparser.ConfigParser()
