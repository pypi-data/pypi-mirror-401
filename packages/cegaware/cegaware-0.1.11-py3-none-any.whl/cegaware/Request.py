###################################################################################
# Copyright © 2025 Matthieu Charrier. All rights reserved. ########################
# This file is the exclusive intellectual property of Matthieu Charrier. ##########
# No reproduction, modification, distribution, or use is permitted without ########
# prior written authorization. A separate licensing agreement may grant ###########
# Cegaware limited rights of use. Absent such agreement, no rights are granted. ###
###################################################################################

# std.
import json
import requests as rq

# cegaware.
from cegaware.Struct import *
from cegaware.Enum import *

def SetValue(Dict, Keys, Value):
    if(len(Keys) == 1):
        Dict[Keys[0]] = Value
    else:
        if(Keys[0] not in Dict):
            Dict[Keys[0]] = dict()
        SetValue(Dict[Keys[0]], Keys[1:], Value)

def GetValue(Dict, Keys):
    if(len(Keys) == 0):
        return Dict
    elif(len(Keys) == 1):
        if Keys[0] in Dict:
            return Dict[Keys[0]]
        else:
            return None
    else:
        if Keys[0] in Dict:
            return GetValue(Dict[Keys[0]], Keys[1:])
        else:
            return None

def Request(pPath, pArgs, pLogger, pAPIToken='', pVerbose=False):

    # prepare request.
    RequestDict = {}
    for ArgNames, ArgStruct in pArgs:
        if(len(ArgNames) == 0):
            RequestDict.update(ArgStruct.serialize())
        else:
            SetValue(RequestDict, ArgNames, ArgStruct.serialize())
    ResponseStr = ""
    
    # set URL.
    url = 'https://api.cegaware.com{}'.format(pPath)

    # get response.
    try:
        Response = rq.post(url, json=RequestDict, headers={ 'X-API-Token': pAPIToken, 'Content-Type': 'application/json' })
        Response.raise_for_status()
        ResponseStr = Response.text
        Success = True
    except rq.exceptions.HTTPError as error:
        print(error)
        return False
    except rq.ConnectionError as error:
        print(error)
        return False

    # set results.
    if ResponseStr != '':
        try:
            ResponseDict = json.loads(ResponseStr)
            if pVerbose:
                print(json.dumps(ResponseDict, indent=4, ensure_ascii=False))
            pLogger.deserialize(ResponseDict['Logs'])
            if Success:
                for ArgNames, ArgStruct in pArgs:
                    Value = GetValue(ResponseDict, ArgNames)
                    if Value is not None:
                        ArgStruct.deserialize(Value)
                return True
            else:
                return False
        except json.decoder.JSONDecodeError:
            print('[ERROR] Cannot decode JSON response')
            return False
    else:
        print('[ERROR] Cannot read response')
        return False