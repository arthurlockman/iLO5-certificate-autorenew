 # Copyright 2020 Hewlett Packard Enterprise Development LP
 #
 # Licensed under the Apache License, Version 2.0 (the "License"); you may
 # not use this file except in compliance with the License. You may obtain
 # a copy of the License at
 #
 #      http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 # License for the specific language governing permissions and limitations
 # under the License.

# -*- coding: utf-8 -*-
"""
An example of importing an SSL certificate for HPE iLO systems
"""

import sys
import json
from redfish import RedfishClient
from redfish.rest.v1 import ServerDownOrUnreachableError

from get_resource_directory import get_resource_directory

def import_ssl(_redfishobj, ssl_cert, disable_resource_dir=False):

    https_cert_uri = None
    body = dict()

    resource_instances = get_resource_directory(_redfishobj)
    if disable_resource_dir or not resource_instances:
        #if we do not have a resource directory or want to force it's non use to find the
        #relevant URI
        managers_uri = _redfishobj.root.obj['Managers']['@odata.id']
        managers_response = _redfishobj.get(managers_uri)
        managers_members_uri = next(iter(managers_response.obj['Members']))['@odata.id']
        managers_members_response = _redfishobj.get(managers_members_uri)
        security_service_uri = managers_members_response.obj.Oem.Hpe.Links['SecurityService']\
                                                                                    ['@odata.id']
        security_service_response = _redfishobj.get(security_service_uri)
        https_cert_uri = security_service_response.obj.Links['HttpsCert']['@odata.id']
    else:
        for instance in resource_instances:
            #Use Resource directory to find the relevant URI
            if '#HpeHttpsCert.' in instance['@odata.type']:
                https_cert_uri = instance['@odata.id']
                break

    if https_cert_uri:
        https_cert_import_uri = _redfishobj.get(https_cert_uri).obj['Actions']\
                                                ['#HpeHttpsCert.ImportCertificate']['target']
        body = dict()
        body["Action"] = "HpeHttpsCert.ImportCertificate"
        body["Certificate"] = ssl_cert
        resp = _redfishobj.post(https_cert_import_uri, body)
        #If iLO responds with soemthing outside of 200 or 201 then lets check the iLO extended info
        #error message to see what went wrong
        if resp.status == 400:
            try:
                print(json.dumps(resp.obj['error']['@Message.ExtendedInfo'], indent=4, \
                                                                                sort_keys=True))
            except Exception as excp:
                sys.stderr.write("A response error occurred, unable to access iLO Extended "\
                                 "Message Info...")
        elif resp.status != 200:
            sys.stderr.write("An http response of \'%s\' was returned.\n" % resp.status)
        else:
            print("Success!\n")
            print(json.dumps(resp.dict, indent=4, sort_keys=True))
            print("\nImporting SSL Certificate may take a few minutes...\n "\
                  "iLO will reset with new changes.\n")
