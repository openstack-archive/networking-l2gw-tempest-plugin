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

from tempest import clients
from tempest import config
from tempest.lib.services.identity.v2 import tenants_client
from tempest.lib.services.identity.v3 import projects_client

from networking_l2gw_tempest_plugin.services.l2gw import \
    l2_gateway_connections_client
from networking_l2gw_tempest_plugin.services.l2gw import l2_gateways_client

CONF = config.CONF


class Manager(clients.Manager):
    """Top level manager for OpenStack tempest clients"""
    default_params = {
        'disable_ssl_certificate_validation':
            CONF.identity.disable_ssl_certificate_validation,
        'ca_certs': CONF.identity.ca_certificates_file,
        'trace_requests': CONF.debug.trace_requests,
        'proxy_url': CONF.service_clients.proxy_url
    }

    # NOTE: Tempest uses timeout values of compute API if project specific
    # timeout values don't exist.
    default_params_with_timeout_values = {
        'build_interval': CONF.compute.build_interval,
        'build_timeout': CONF.compute.build_timeout
    }
    default_params_with_timeout_values.update(default_params)

    def __init__(self, credentials=None, service=None):
        super(Manager, self).__init__(credentials=credentials)

        self._set_identity_clients()

        self.l2gw_client = l2_gateways_client.L2GatewaysClient(
            self.auth_provider,
            CONF.network.catalog_type,
            CONF.network.region or CONF.identity.region,
            endpoint_type=CONF.network.endpoint_type,
            build_interval=CONF.network.build_interval,
            build_timeout=CONF.network.build_timeout,
            **self.default_params
        )
        self.l2gw_connection_client = \
            l2_gateway_connections_client.L2GatewayConnectionsClient(
                self.auth_provider,
                CONF.network.catalog_type,
                CONF.network.region or CONF.identity.region,
                endpoint_type=CONF.network.endpoint_type,
                build_interval=CONF.network.build_interval,
                build_timeout=CONF.network.build_timeout,
                **self.default_params
            )

        params = {
            'service': CONF.compute.catalog_type,
            'region': CONF.compute.region or CONF.identity.region,
            'endpoint_type': CONF.compute.endpoint_type,
            'build_interval': CONF.compute.build_interval,
            'build_timeout': CONF.compute.build_timeout
        }
        params.update(self.default_params)

    def _set_identity_clients(self):
        params = {
            'service': CONF.identity.catalog_type,
            'region': CONF.identity.region
        }
        params.update(self.default_params_with_timeout_values)
        params_v2_admin = params.copy()
        params_v2_admin['endpoint_type'] = CONF.identity.v2_admin_endpoint_type
        # Client uses admin endpoint type of Keystone API v2
        self.tenants_client = tenants_client.TenantsClient(self.auth_provider,
                                                           **params_v2_admin)
        # Client uses admin endpoint type of Keystone API v3
        self.projects_client = projects_client.ProjectsClient(
            self.auth_provider, **params_v2_admin)
