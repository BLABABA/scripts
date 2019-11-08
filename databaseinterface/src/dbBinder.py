"""
    Author: Xingyu (Alfred) Liu 
    Email: xingyu.alfred.liu@gmail.com
    Description:
        This class serves as the database interface

        Functions:
            - load data from JSON path
            - write/overwrite data 
            - output JSONs
            - delete key-val pairs
            
"""

import os
import json
import collections
import six
import math

# python 3.8+ compatibility
try:
    collectionsAbc = collections.abc
except:
    collectionsAbc = collections
# this part is taken from:
# https://stackoverflow.com/questions/3232943/update
#-value-of-a-nested-dictionary-of-varying-depth
def update(dictionary, newdict):
    for key, val in six.iteritems(newdict):
        dv = dictionary.get(key, {})
        if not isinstance(dv, collectionsAbc.Mapping):
            if val == math.inf:
                dictionary.pop(key)
            else:
                dictionary[key] = val
        elif isinstance(val, collectionsAbc.Mapping):
            if val == math.inf:
                dictionary.pop(key)
            else:
                dictionary[key] = update(dv, val)
        else:
            if val == math.inf:
                dictionary.pop(key)
            else:
                dictionary[key] = val
    return dictionary

class dbcontrol(object):
    def __init__(self, dbpath):
        """
        dbpath: string
        this is the path point to the folder where 
        all JSONs are stored
        """

        # clean up dbpath in case there are something else
        self.dbpath = dbpath
        namelist = os.listdir(self.dbpath)
        for val in namelist[:]:
            if not val.endswith("json"):
                namelist.remove(val)
        self.namelist = namelist

    def loaddb(self):
        """
        namelist: list of strings
            - namelist is a list of strings, each of the string is the
            ID of each JSON file, which is the name except the last
            ".json" part
            - we don't necessarily need to load all data everytime
            because everytime load and write, only part of them are
            needed
            - the default is all the files inside self.dbpath
        
        self.db: a list of dictionaries
            - each dictionary has the information in each JSON, the
            highest level key is the ID, of course, each dictionary has 
            a key-val pair indicating the ID, which is struct_id
        """

        # in case the namelist is only indicated with ID without the suffix
        for i, val in enumerate(self.namelist):
            if not val.endswith(".json"):
                self.namelist[i] = val+".json"
        # load in the data into a dictionary with each key, val as a dict
        self.db = dict()
        for name in self.namelist:
            with open(os.path.join(self.dbpath, name), "r") as f:
                data = json.load(f)
            self.db[name[:-5]] = data

    def writedata(self, val):
        """
        val: a list of dict
            - the val is passed to the database by a list of dictionaries
            for each of the dict, it should look like:
                val[i] = {'ABECAL': 
                                {'dft': 
                                        {
                                            'bandgap': 1.11, 
                                            'VBdisp': 2.22
                                        }
                                }
            as shown above, each of the element in val is a dictionary,
            with the highest level key as the ID, here the example is "ABECAL";
            and then following the standard JSON format designed for storing
            the data for this project.
            The reason for this design is that everytime, there might be multiple
            values under this ID to be passed and stored into the db. As long as 
            the each val element follows the standard the format, the values will be 
            written correctly. 
        """
        for newval in val:
            if list(newval.keys())[0] in list(self.db.keys()):
                self.db = update(self.db, newval)
                print(list(newval.keys())[0])
            else:
                print('Warning: Struct %s is not in the current database!' %(list(newval.keys())[0]))
        
    def delkey(self, val):
        """
        val: a list of dict
            - similar as that in writedata(self, val), val is a list of dictionaries,
            with its "ID" provided at top. The difference is, the value is math.inf
            provided this time. For example:
                val[i] = {'ABECAL': 
                                {'dft': 
                                        {
                                            'bandgap': math.inf, 
                                            'VBdisp': math.inf
                                        }
                                }
            It's designed in this way just to be consistent with former function.
            If math.inf is detected, the key for this value will be popped out.
        """
        print("Warning!!! You are about to delete some values from db!!!")
        for newval in val:
            if list(newval.keys())[0] in list(self.db.keys()):
                self.db = update(self.db, newval)
            else:
                print('Warning: Struct %s is not in the current database!' %(list(newval.keys())[0]))

    def writedb(self, outpath):
        """
        outpath:
            dir where you want to output your data
        """
        for key, val in self.db.items():
            with open(os.path.join(outpath, key+".json"), "w") as f:
                f.write(json.dumps(val, indent=4))

