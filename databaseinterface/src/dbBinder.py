"""
    Author: Xingyu (Alfred) Liu 
    Email: xingyu.alfred.liu@gmail.com
    Description:
        This class serves as the database interface

        Functions:
            - read in database with given path
            data has to be in the JSON format
            - wirte properties with give key path
            - list out the key path available
            - overwrite data (dangerous, backup?)
"""

import os
import json


