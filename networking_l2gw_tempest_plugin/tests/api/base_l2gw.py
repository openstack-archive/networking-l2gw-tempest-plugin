# Copyright 2015 Hewlett-Packard Development Company, L.P.
# Copyright 2015 OpenStack Foundation
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from tempest.api.network import base
from tempest.common import utils
from tempest import config

from networking_l2gw_tempest_plugin.tests.api import clients

CONF = config.CONF

SEGMENTATION_ID_DELIMITER = "#"
INTERFACE_SEG_ID_DELIMITER = "|"
DEVICE_INTERFACE_DELIMITER = "::"
DEVICE_DELIMITER = ","
INTERFACE_DELIMITER = ";"
"""
  Sample for providing input for gateway creation in config is noted below
  Options provide flexibility to user to create l2gateway
  For single device ,single interface with single vlan
    l2gw_switch = device_name1::int_name1|vlan1
  For single device multiple interfaces with single or multiple vlans
    l2gw_switch = device_name1::int_name1|vlan1#vlan2;int_name2|vlan3
  For multiple devices with mutiple interfaces having single or mutiple vlan
    l2gw_switch = device_name1::int_name1|vlan1,device_name2::int_name2|vlan2
"""


def get_interface(interfaces):
    interface_dict = []
    for interface in interfaces:
        if INTERFACE_SEG_ID_DELIMITER in interface:
            int_name = interface.split(INTERFACE_SEG_ID_DELIMITER)[0]
            segid = interface.split(INTERFACE_SEG_ID_DELIMITER)[1]
            if SEGMENTATION_ID_DELIMITER in segid:
                segid = segid.split(SEGMENTATION_ID_DELIMITER)
            else:
                segid = [segid]
            interface_detail = {'name': int_name, 'segmentation_id': segid}
        else:
            interface_detail = {'name': interface}
        interface_dict.append(interface_detail)
    return interface_dict


def get_l2gw_body(l2gw_conf):
    device_dict = []
    devices = l2gw_conf.split(DEVICE_DELIMITER)
    for device in devices:
        if DEVICE_INTERFACE_DELIMITER in device:
            device_name = device.split(DEVICE_INTERFACE_DELIMITER)[0]
            interface = device.split(DEVICE_INTERFACE_DELIMITER)[1]
            if INTERFACE_DELIMITER in interface:
                interface_dict = interface.split(INTERFACE_DELIMITER)
                interfaces = get_interface(interface_dict)
            else:
                interfaces = get_interface([interface])
        device = {'device_name': device_name,
                  'interfaces': interfaces}
        device_dict.append(device)
    body = {'devices': device_dict}
    return body


def form_dict_devices(devices):
    seg_ids = []
    devices1 = dict()
    int_seg = []
    for device in devices:
        device_name = device['device_name']
        interfaces = device['interfaces']
        for interface in interfaces:
            interface_name = interface['name']
            int_seg.append(interface_name)
            seg_id = interface['segmentation_id']
            if type(seg_id) is list:
                for segid in seg_id:
                    seg_ids.append(segid)
            else:
                seg_ids.append(seg_id)
            int_seg.append(seg_id)
            devices1.setdefault(device_name, []).append(int_seg)
            int_seg = []
    return devices1


class BaseL2GatewayTest(base.BaseNetworkTest):
    force_tenant_isolation = False
    credentials = ['primary']

    @classmethod
    def setup_clients(cls):
        super(BaseL2GatewayTest, cls).setup_clients()
        cls.l2gws_client = cls.os.l2gw_client
        cls.l2gw_conns_client = cls.os.l2gw_connection_client

    @classmethod
    def resource_setup(cls):
        super(BaseL2GatewayTest, cls).resource_setup()
        # At least one switch detail should be provided to run the tests
        if (len(CONF.l2gw.l2gw_switch) <= 0):
            msg = ('At least one switch detail must be defined.')
            raise cls.skipException(msg)
        if not utils.is_extension_enabled('l2-gateway', 'network'):
            msg = "L2Gateway Extension not enabled."
            raise cls.skipException(msg)

    @classmethod
    def get_client_manager(cls, credential_type=None, roles=None,
                           force_new=None):
        manager = super(BaseL2GatewayTest, cls).get_client_manager(
            credential_type=credential_type,
            roles=roles,
            force_new=force_new
        )
        # Neutron uses a different clients manager than the one in the Tempest
        # save the original in case mixed tests need it
        if credential_type == 'primary':
            cls.os_tempest = manager
        return clients.Manager(manager.credentials)


class BaseAdminL2GatewayTest(BaseL2GatewayTest):

    credentials = ['primary', 'admin']

    @classmethod
    def setup_clients(cls):
        super(BaseAdminL2GatewayTest, cls).setup_clients()
        cls.admin_networks_client = cls.os_admin.networks_client
        cls.admin_l2gws_client = cls.os_admin.l2gw_client
        cls.admin_l2gw_conns_client = cls.os_admin.l2gw_connection_client
