import typing

import pandas as pd

import src.elements.s3_parameters as s3p
import src.elements.service as sr
import src.s3.unload


class References:

    def __init__(self, service: sr.Service, s3_parameters: s3p.S3Parameters):
        """

        :param service:
        :param s3_parameters:
        """

        self.__service: sr.Service = service
        self.__s3_parameters: s3p.S3Parameters = s3_parameters

        # S3 Unload Instance
        self.__unload = src.s3.unload.Unload(service=self.__service, s3_parameters=self.__s3_parameters)

    def __read(self, filename: str) -> pd.DataFrame:
        """

        :param filename:
        :return:
        """

        key_name = f'{self.__s3_parameters.references_}{filename}'
        buffer = self.__unload.exc(key_name=key_name)

        try:
            return pd.read_csv(filepath_or_buffer=buffer, header=0, encoding='utf-8')
        except ImportError as err:
            raise Exception(err) from err

    @staticmethod
    def __integrate(registry: pd.DataFrame, stations: pd.DataFrame, substances: pd.DataFrame) -> pd.DataFrame:
        """
        Integrates the frames such that each record has the details of each distinct
        sequence identification code.

        :param registry:
        :param stations:
        :param substances:
        :return:
        """

        frame = registry.merge(stations, how='left', on='station_id')
        frame = frame.copy().merge(
            substances.copy()[['pollutant_id', 'substance', 'notation']], how='left', on='pollutant_id')

        return frame

    def exc(self) -> pd.DataFrame:
        """

        :return:
          registry: DataFrame
          stations: DataFrame
          substances: DataFrame
        """

        registry = self.__read(filename='registry.csv')
        stations = self.__read(filename='stations.csv')
        substances = self.__read(filename='substances.csv')

        data = self.__integrate(registry=registry, stations=stations, substances=substances)

        return data
