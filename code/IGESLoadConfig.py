# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 18:06:24 2013
@author: Rod Persky
Licensed under the Academic Free License ("AFL") v. 3.0
"""

def IGESTreeWalk(object, level=0, levelname=""):
    """Walk IGES Class Tree"""
    
    branch = list()
    
    for item in object.__dict__: #Get keys for this level
        if "IGES" in str(type(object.__dict__[item])): #There is another level down
            branch.extend(IGESTreeWalk(object.__dict__[item], level+1, "".join((levelname,item,"."))))
        elif "_" not in item:
            branch.append("".join((levelname,item)))
    return branch
    
def IGESetKey(object,key,value): #Otherwise known as reverse tree walk
    IGESKey = key.split(".")   
    if  IGESKey[0] in object.__dict__:
        try:
            if 1 < len(IGESKey):
                IGESetKey(object.__dict__[IGESKey[0]],IGESKey[1:][0],value)
            else:
                if type(object.__dict__[IGESKey[0]]) == list:
                    #Because multline items are assumed to always be parameters, we
                    #  need to convert this to format [[line1],[line2],...[lineN],]
                    #  note subversion info is automatically added unless you spicify
                    #  where it can go with an @subversion on a line by itself
                    IGESItem = list()
                    if "@subversion" not in value:
                        value = ''.join((value,"\n@subversion"))
                    for line in value.split("\n"):
                        if "@subversion" in line: #The automatically updates from subversion, ignore it
                            IGESItem.extend([["| Subversion Information:"],    
                                            ["| Last Revised $Date: 2013-04-21 00:26:27 +1000 (Sun, 21 Apr 2013) $"],    
                                            ["| Last HEAD $Rev: 46 $"],
                                            ["| Last $Author: rodney $"],["|"]] )
                        else: IGESItem.append([line])
                    object.__dict__[IGESKey[0]] = IGESItem
                elif type(object.__dict__[IGESKey[0]]) == str:
                    object.__dict__[IGESKey[0]] = value
                elif 8 < len(value): raise ResourceWarning(''.join((key," (",value,") cannot have a length longer than 8 characters")))
                elif type(object.__dict__[IGESKey[0]]) == int:
                    object.__dict__[IGESKey[0]] = int(value) #We assume that the hard coded types are correct!
                elif type(object.__dict__[IGESKey[0]]) == float:
                    object.__dict__[IGESKey[0]] = float(value)
                else:
                    raise NotImplementedError(''.join((value," connects to an unhandled type: ",
                                                       str(type(object.__dict__[IGESKey[0]])))))
        except:
            raise ValueError("Traceback to value:",key)

def IGESConfigFromFile(object,filename='IGESUserSettings.ini'):
    """Configure IGES settings from a file"""
    
    import configparser
    config = configparser.ConfigParser()
    config.read(filename)
              
    IGESTree = IGESTreeWalk(object)

    for IGESitem in IGESTree:
        section = IGESitem.split(".")
        if len(section) < 2: raise NotImplementedError("TODO: Fix for single value items")
        keyLen = len(section)-1
        if section[keyLen-1] in config.sections():
            if section[keyLen] in config[section[keyLen-1]]:
                IGESetKey(object,IGESitem,config[section[keyLen-1]][section[keyLen]])
        #    else:
        #        print("{} not in {}".format(section[keyLen],config[section[keyLen-1]]))
        #else:
        #    print("{} not in {}".format(section[keyLen-1],config.sections()))
            
