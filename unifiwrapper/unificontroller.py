#!/usr/bin/env python3
import json

import requests

from unifiwrapper import TrafficRule


class UnifiController():

    def __init__(self, host: str, username: str, password: str) -> None:
        self._host = host
        self._username = username
        self._password = password

        self._session = requests.Session()
        self._token = self._login()

        self._trafficrules = None
        self._sites = None

    def _login(self):
        path = f'https://{self._host}/api/auth/login'

        logindict = dict()
        logindict["username"] = self._username
        logindict["password"] = self._password
        headersdict = dict()
        #headersdict["content-type"] = "application/json"
        #headersdict["Content-Type"] = "application/json"
        headersdict["accept"] = "application/json"
        headersdict["Accept"] = "application/json"
        headersdict["dataType"] = "json"
        # setting headers of session before post
        self._session.headers.update(headersdict)
        dataload = json.dumps(logindict)
        response = self._session.post(url=path,
                                      json=logindict,
                                      headers=headersdict,
                                      verify=False)
        responseheaders = response.headers
        if 'x-csrf-token' not in responseheaders.keys():
            return None
        else:
            return responseheaders['x-csrf-token']

    @property
    def token(self):
        return self._token

    @property
    def sites(self):
        if self._sites is None:
            self._get_sites()
        return self._sites

    def _get_sites(self):
        path = f'https://{self._host}/proxy/network/api/self/sites'
        headersdict = dict()
        headersdict["X-CSRF-Token"] = self._token
        headersdict["accept"] = "application/json"
        headersdict["Accept"] = "application/json"
        headersdict["dataType"] = "json"
        headersdict["Content-Type"] = "application/json"
        response = self._session.get(url=path,
                                     headers=headersdict,
                                     verify=False)
        json =  response.json()
        self._sites = list()
        for item in json["data"]:
            self._sites.append(item["desc"])
    @property
    def trafficrules(self):
        if self._trafficrules is None:
            self._get_trafficrules()
        return self._trafficrules

    def _get_trafficrules(self):
        path = f'https://{self._host}/proxy/network/v2/api/site/default/trafficrules'
        headersdict = dict()
        headersdict["X-CSRF-Token"] = self._token
        headersdict["accept"] = "application/json"
        headersdict["Accept"] = "application/json"
        headersdict["dataType"] = "json"
        headersdict["Content-Type"] = "application/json"
        response = self._session.get(url=path,
                                     headers=headersdict,
                                     verify=False)
        json =  response.json()
        self._trafficrules = list()
        for item in json:
            self._trafficrules.append(TrafficRule(item,self))
