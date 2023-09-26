import copy
import json

from utils import MyEncoder


# examplejson = {
#     "_id": "REDACTED",
#     "action": "BLOCK",
#     "app_category_ids": [
#         24,
#         4,
#         8
#     ],
#     "app_ids": [],
#     "bandwidth_limit": {
#         "download_limit_kbps": 1024,
#         "enabled": false,
#         "upload_limit_kbps": 1024
#     },
#     "description": "Blokker tv",
#     "domains": [],
#     "enabled": false,
#     "ip_addresses": [],
#     "ip_ranges": [],
#     "matching_target": "APP_CATEGORY",
#     "network_ids": [],
#     "regions": [],
#     "schedule": {
#         "mode": "EVERY_DAY",
#         "repeat_on_days": [],
#         "time_all_day": false,
#         "time_range_end": "18:00",
#         "time_range_start": "07:00"
#     },
#     "target_devices": [
#         {
#             "client_mac": "00:00:00:00:00:00",
#             "type": "CLIENT"
#         },
#         {
#             "client_mac": "00:00:00:00:00:00",
#             "type": "CLIENT"
#         },
#         {
#             "client_mac": "00:00:00:00:00:00",
#             "type": "CLIENT"
#         }
#     ]
# }
class TrafficRule(object):
    # init based on json data from unifi controller
    def __init__(self, jsondata: str, unificontroller):
        self._jsondata = jsondata
        self._controller = unificontroller
        # _id, action, app_category_ids, app_ids, bandwidth_limit,
        # description, enaled, ip_addresses, ip_ranges, matching_target,
        # network_ids, regions, schedule (dict), target_devices (dict)
        self._id = jsondata["_id"]
        self._action = jsondata["action"]
        self._app_category_ids = jsondata["app_category_ids"]
        self._app_ids = jsondata["app_ids"]
        self._bandwidth_limit = jsondata["bandwidth_limit"]
        self._description = jsondata["description"]
        self._enabled = jsondata["enabled"]
        self._ip_addresses = jsondata["ip_addresses"]
        self._ip_ranges = jsondata["ip_ranges"]
        self._matching_target = jsondata["matching_target"]
        self._network_ids = jsondata["network_ids"]
        self._regions = jsondata["regions"]
        self._schedule = jsondata["schedule"]
        self._target_devices = jsondata["target_devices"]

    @property
    def id(self):
        return self._id

    @property
    def action(self):
        return self._action

    @property
    def app_category_ids(self):
        return self._app_category_ids

    @property
    def app_ids(self):
        return self._app_ids

    @property
    def bandwidth_limit(self):
        return self._bandwidth_limit

    @property
    def description(self):
        return self._description

    @property
    def enabled(self):
        return self._enabled

    @property
    def ip_addresses(self):
        return self._ip_addresses

    @property
    def ip_ranges(self):
        return self._ip_ranges

    @property
    def matching_target(self):
        return self._matching_target

    @property
    def network_ids(self):
        return self._network_ids

    @property
    def regions(self):
        return self._regions

    @property
    def schedule(self):
        return self._schedule

    def to_json(self):
        dictcopy = copy.deepcopy(self.__dict__)
        dictcopy.pop("_jsondata")
        dictcopy.pop("_controller")
        dictret = dict()
        for k, v in dictcopy.items():
            dictret[k.lstrip('_')] = v
        #dictret = json.dumps(self.__dict__)
        return dictret

    def enable(self):
        if not self._enabled:
            self._enabled = True
            self.send_enable()

    def disable(self):
        if self._enabled:
            self._enabled = False
            self.send_enable()

    testdict = {
        "_id":
        "6490a2c5e95f8d55e3dbe842",
        "action":
        "BLOCK",
        "app_category_ids": [24, 4, 8],
        "app_ids": [],
        "bandwidth_limit": {
            "download_limit_kbps": 1024,
            "enabled": False,
            "upload_limit_kbps": 1024
        },
        "description":
        "Blokker tv",
        "domains": [],
        "enabled":
        False,
        "ip_addresses": [],
        "ip_ranges": [],
        "matching_target":
        "APP_CATEGORY",
        "network_ids": [],
        "regions": [],
        "schedule": {
            "mode": "EVERY_DAY",
            "repeat_on_days": [],
            "time_all_day": False,
            "time_range_end": "18:00",
            "time_range_start": "07:00"
        },
        "target_devices": [{
            "client_mac": "38:8c:50:fe:b9:aa",
            "type": "CLIENT"
        }, {
            "client_mac": "74:e6:b8:08:23:ac",
            "type": "CLIENT"
        }, {
            "client_mac": "dc:56:e7:2f:87:6b",
            "type": "CLIENT"
        }],
        "isAllTab":
        True
    }

    def send_enable(self):
        path = f'https://{self._controller._host}/proxy/network/v2/api/site/default/trafficrules/{self._id}'
        headersdict = dict()
        headersdict["X-CSRF-Token"] = self._controller._token
        headersdict["accept"] = "application/json"
        headersdict["Accept"] = "application/json"
        headersdict["dataType"] = "json"
        headersdict["Content-Type"] = "application/json"
        data_dict = self.to_json()
        data = json.dumps(data_dict)
        response = self._controller._session.put(url=path,
                                                 headers=headersdict,
                                                 data=data,
                                                 verify=False)

        if response.status_code == 200:
            return True
