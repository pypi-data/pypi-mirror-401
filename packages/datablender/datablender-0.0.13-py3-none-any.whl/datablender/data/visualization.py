"""
"""
from __future__ import annotations
from typing import Dict, Union, List, Callable, Tuple

import os
import copy
import json
import pandas
import subprocess

from datablender.base import (
    getFunction,
    Directory,
    Data,
    AsyncDataConfiguration,
    AsyncConnection,
    AsyncDataElement,
    AsyncRequest
)
from datablender.database import AsyncDatabase
from datablender.data.dataVersion import AsyncDataVersion
from datablender.base import DataSets

class Visualization(AsyncDataElement):
    """Extract, transform and load data within the database.

    The first step is to extract data from the database.
    Data can come from 3 places :
        1. Query
        2. Table
        3. View

    After the data selection, the data is transform. Transformations 
    can be applied to a specific data set, or all of them.

    Then the data is export to the tables.

    Attributes:
    ----------
        Attributes

    Methods:
    ----------
        Methods

    Examples:
    ----------
        >>> import datablender
        >>> data_process = datablender.DataProcess(
        >>>     datablender.Connection(),
        >>>     data_process_test,
        >>>     data = [
        >>>         'data_set'
        >>>     ] 
        >>> )

        >>> import datablender
        >>> data_process = datablender.DataProcess(
        >>>     datablender.Connection(),
        >>>     data_process_test,
        >>>     data = [
        >>>         'data_set'
        >>>     ] 
        >>> )
        

    """
    def __init__(
        self,
        connection:AsyncConnection,
        name:str,
        database:AsyncDatabase= None,
        data_configuration:AsyncDataConfiguration=None,
        acticvate_data_config:bool=False,
        status:str='developpement',
        event_server=None,
        id:int=None,
        content:dict = {
          "name": None,
          "description":None,
          "content_elements": []
        },
        database_name:str = None,
        sets:Dict = {},
        display_map:bool = False,
        columns:List[dict] = [] 
    ):
        super(Visualization,self).__init__(
            connection,
            name,
            'visualization',
            status,
            data_configuration,
            acticvate_data_config,
            id,
            content,
            event_server
        )

        self.sets = sets
        self.display_map = display_map  

        self.database,self.initiate_database = (database,False) if database else (AsyncDatabase(
            self.connection,
            name = database_name if database_name else self.connection.database_name,
            data_configuration=self.data_configuration,
            event_server=self.data_logging.event_server
        ),True)

        self.data_logging.element_configuration = self.configuration        
    
    async def initiate(self) -> Visualization:

        self.data_logging.setActionName(
            'initiate',
            self.element_type,
            self.configuration
        )
        await self.data_logging.manageTable()

        if self.initiate_database:
            await self.database.initiate()

        await self.database.manage(
            data_logging_action = self.data_logging.action
        )
            
        await self.manageAttributes()
        return self

    @property
    def configuration(self) -> dict:
        """Get configuration.

        Returns:
            dict: configuration.
        """
        return {
            'id':self.id,
            'name':self.name,
            'status':self.status,
            'content':self.content,
            'sets':self.sets,
            'display_map':self.display_map
        }
    
    @configuration.setter
    def configuration(self,new_config:dict):
        """Set the configuration.

        Args:
            new_config (dict): New configuration.

        Returns:
            Dict: configuration.
        """
        if new_config:
            [
                setattr(
                    self,
                    attribute_name,
                    new_config[attribute_name]
                    if attribute_name in new_config 
                    else getattr(self,attribute_name)
                )
                for attribute_name
                in [
                    'name',
                    'status',
                    'content',
                    'display_map'
                ]
            ]
            
        return new_config
  
    async def setConfiguration(
        self,
        new_config:dict
    ) -> None:
    
        self.configuration = copy.deepcopy(new_config)
        self.sets= new_config.get('sets')
        await self.manageAttributes()

    async def manage(
        self,
        manage_from='configuration',
        new_configuration:dict={}
    ) -> Visualization:
        """Manage the data process configuration in the data configuration.

        Args:
            manage_from (str, optional): Manage the data process from. Defaults to 'configuration'.
            new_configuration (dict, optional): New configuration to manage the data process. Defaults to {}.

        Returns:
            DataSource: self.
        """
        self.data_logging.setActionName(
            'manage',
            self.element_type,
            self.configuration
        )
            
        await self.data_configuration.getElements(self.element_type)
        # If there is a new configuration, set all data source attributes from the new config
        if new_configuration:
            await self.setConfiguration(new_configuration)
        
        # If data source exists in the data configuration,
        # manage the data source in the data config
        if self.data_configuration.active:
            # If there is a config element, it means that it exists in config
            if self.config_element:
                # If there's not a new config from the user,
                # the config in the data configuration is the right one.
                if not new_configuration and manage_from != 'values':
                    await self.setConfiguration(self.config_element)

                # If status is inexistant, then delete it
                if self.status =='inexistant':
                    await self.data_configuration.deleteElement(
                        self.id,
                        self.element_type
                    )
                
                # Else if one of the attributes is different from the data configuration,
                # edit the data source
                
                elif any([
                    self.config_element[attribute] != self.configuration[attribute]
                    for attribute in self.config_element
                ]) and (new_configuration or manage_from == 'values'):
                    await self.data_configuration.putElement(
                        self.id,
                        self.configuration,
                        self.element_type
                    )

            elif new_configuration and self.status !='inexistant':
                await self.data_configuration.postElement(
                    self.configuration,
                    self.element_type
                )
                
            # If it does not exists and there is no new config, but the name or id,
            # post it with the values of this object
            elif self.name or self.id:
                await self.data_configuration.postElement(
                    self.configuration,
                    self.element_type
                )

                
            # If data config is active, but there is no directory name or data source name
            # If data config is active, but there is no directory name or data source name
            else:
                self.name = 'data'
                await self.data_configuration.postElement(
                    self.configuration,
                    self.element_type
                )

        # If data config is not active and there is not a new configuration,
        elif not new_configuration and manage_from != 'values':
            self.name = 'data' if not self.name else self.name
        
        return self
