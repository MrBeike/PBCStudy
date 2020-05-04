'''
----------------------------------------------------------------------------------------------
                    Some Functions for the Main Scripts  
----------------------------------------------------------------------------------------------
'''
# FIXME 怎么让修改不返回就能生效 update?
def dictPicker(storeDict, originDict,*keys): 
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

