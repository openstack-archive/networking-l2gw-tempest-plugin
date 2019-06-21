# Copyright (c) 2019 Ericsson
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

from tempest.lib.services.network import base


class L2GatewaysClient(base.BaseNetworkClient):

    def create_l2_gateway(self, **kwargs):
        """Creates an l2gw.

        :param kwargs: dict of l2gw in the form
                       {'name': 'foo', 'devices': [{'device_name': 'foo',
                        'interfaces': [{'name': 'bar', 'segmentation_id': 4}]}]
                       }
        :return: tempest.lib.common.rest_client.ResponseBody
        """
        uri = '/l2-gateways'
        post_data = {'l2_gateway': kwargs}
        return self.create_resource(uri, post_data)

    def update_l2_gateway(self, l2gw_id, **kwargs):
        """Updates an l2gw.

        :param l2gw_id: The uuid of the l2gw
        :param kwargs: dict of l2gw to be updated.

        :return: tempest.lib.common.rest_client.ResponseBody
        """
        uri = '/l2-gateways/%s' % l2gw_id
        post_data = {'l2_gateway': kwargs}
        return self.update_resource(uri, post_data)

    def show_l2_gateway(self, l2gw_id, **fields):
        """Show details of an l2gw.

        :param l2gw_id: The uuid of the l2gw.
        :param fields: a dict with key fields and a list of fields name

        :return: tempest.lib.common.rest_client.ResponseBody
        """
        uri = '/l2-gateways/%s' % l2gw_id
        return self.show_resource(uri, **fields)

    def delete_l2_gateway(self, l2gw_id):
        """Deletes and l2gw.

        :param l2gw_id: The uuid of the l2gw.

        :return: tempest.lib.common.rest_client.ResponseBody
        """
        uri = '/l2-gateways/%s' % l2gw_id
        return self.delete_resource(uri)

    def list_l2_gateways(self, **filters):
        """Lists l2gws.

        :return: tempest.lib.common.rest_client.ResponseBody
        """
        uri = '/l2-gateways'
        return self.list_resources(uri, **filters)
