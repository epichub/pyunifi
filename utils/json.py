import json


# from https://stackoverflow.com/questions/25851183/how-to-compare-two-json-objects-with-the-same-elements-in-a-different-order-equa
def myordered(obj):
    if isinstance(obj, dict):
        return sorted((k, myordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(myordered(x) for x in obj)
    else:
        return obj


# from https://stackoverflow.com/questions/31813111/how-to-convert-object-with-properties-to-json-without-in-python-3
class MyEncoder(json.JSONEncoder):

    def default(self, o:dict):
        return {k.lstrip('_'): v for k, v in o.items()}
