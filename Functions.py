'''
----------------------------------------------------------------------------------------------
                    Some Functions for the Main Scripts  
----------------------------------------------------------------------------------------------
'''
import json
import requests

# FIXME 怎么让修改不返回就能生效 update?


def dictPicker(storeDict, originDict, *keys):
    '''
    Pick useful key-value to a new dict.Kind like a temp store.
    params: storeDict: dict, the dict which store the picked key-value. 
    params: originDict: dict, the original dict to be Pick.
    params: keys: str/*tuple/*list, the keyname to be picked.
    '''
    storeDict = {}
    for key in keys:
        storeDict[key] = originDict[key]
    return storeDict


def getJson(url, data=data, method='GET', status_code=200, encode='UTF-8', session=None):
    '''
    get response from the specify url and parse the response to dict.
    (assume {Content-Type: application/json;charset=UTF-8})
    params: url: str, Uniform Resource Locator :).
    params: method: str, Http method.
    params: status_code: int, response status_code.
    params: encode: str, the codec of the response content.
    params: session: requests.session(), emmm...
    return: json_dict: dict, the parsed Json. 
    '''
    if session == None:
        s = requests.Session()
    else:
        s = session
    try:
        req = requests.Request(method, url, data=data,json=json)
        prepped = req.prepare()

        # # do something with prepped.body
        # prepped.body = 'No, I want exactly this as the body.'
        # # do something with prepped.headers
        # del prepped.headers['Content-Type']

        resp = s.send(prepped, stream=False, verify=True, proxies={}, cert=None) 
        if resp.status_code == status_code:
            json = resp.content.decode(encode)
            dict = json.loads(json)
        else:
            dict = False
        return dict