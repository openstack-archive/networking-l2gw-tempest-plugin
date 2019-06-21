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


class L2GatewayConnectionsClient(base.BaseNetworkClient):

    def create_l2_gateway_connection(self, **kwargs):
        """Creates an l2gw connection.

        :param kwargs: dict of l2gw in the form
                       {'l2_gateway_id': '1234', 'network_id': '4321',
                        'segmentation_id': '0'}
        :return: tempest.lib.common.rest_client.ResponseBody
        """
        uri = '/l2-gateway-connections'
        post_data = {'l2_gateway_connection': kwargs}
        return self.create_resource(uri, post_data)

    def show_l2_gateway_connection(self, l2gw_connection_id, **fields):
        """Show details of an l2gw connection.

        :param l2gw_id: The uuid of the l2gw connection.
        :param fields: a dict with key fields and a list of fields name

        :return: tempest.lib.common.rest_client.ResponseBody
        """
        uri = '/l2-gateway-connections/%s' % l2gw_connection_id
        return self.show_resource(uri, **fields)

    def delete_l2_gateway_connection(self, l2gw_id):
        """Deletes and l2gw connection.

        :param l2gw_id: The uuid of the l2gw connection.

        :return: tempest.lib.common.rest_client.ResponseBody
        """
        uri = '/l2-gateway-connections/%s' % l2gw_id
        return self.delete_resource(uri)

    def list_l2_gateway_connections(self, **filters):
        """Lists l2gw connections.

        :return: tempest.lib.common.rest_client.ResponseBody
        """
        uri = '/l2-gateway-connections'
        return self.list_resources(uri, **filters)
