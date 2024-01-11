#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 17:21:54 2022

@author: singla
"""

import json
import requests


class Singla:
    def __init__(self, ip, vers, port=80):
        self.ip_ = ip
        self.version_ = vers
        self.port_ = port
        self.status = "na"



    def set_config(self, param, value, iface='detector'):
        """
        SINGLA configuration
        'iface' can be detector, filewriter, stream,
        Generic configuration command
        """
        url = 'http://%s:%s/%s/api/%s/config/%s' % (self.ip_, self.port_, iface, self.version_, param)
        self._request("PUT", url, data=json.dumps({'value': value}))

    def get_config(self, param, iface):
        url = 'http://%s:%s/%s/api/%s/config/%s' % (self.ip_, self.port_, iface, self.version_, param)
        reply = self._request("GET", url)
        val = reply['value']
        return val

    def get_status(self, param, iface="detector"):
        url = 'http://%s:%s/%s/api/%s/status/%s' % (self.ip_, self.port_, iface, self.version_, param)
        reply = self._request("GET", url)
        val = reply['value']
        return val




    def send_command(self, command):
        """
        SINGLA Commands:
            arm, trigger,disarm, cancel, initialize
        """
        url = 'http://%s:%s/detector/api/%s/command/%s' % (self.ip_, self.port_, self.version_, command)
        json_reply = self._request("PUT", url)
        return json_reply

    def get_url(self):
        return "http://%s:%s" % (self.ip_, self.port_)

    def _request(self, method, url, data={}, headers={}):
        reply = {'value': -1}
        # https://python-forum.io/thread-27907.html
        try:
            response = requests.request(method, url, data=data, headers=headers)
            response.raise_for_status()
            self.response_status = response.reason
            reply = response.json()

        except json.decoder.JSONDecodeError:
            self.response_status = "Error: Invalid JSON response"
        except requests.exceptions.HTTPError as errh:
            self.response_status = "Http Error: " + str(response.status_code)
        except requests.exceptions.ConnectionError as errc:
            self.response_status = "Error Connecting"
        except requests.exceptions.Timeout as errt:
            self.response_status = "Timeout Error"
        except requests.exceptions.RequestException as err:
            self.response_status = "Error" + str(err)
        except Exception as exc:  #:
            self.response_status = str(exc)
        return reply

        # return reply.json()


if __name__ == '__main__':
    # univie = Singla(SIP, SPORT, SVERS)
    print("error: Singla should be importet and not run individually\n")
    exit(1)
