#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

"""Server v2 action implementations"""


import logging

from cliff import lister

from openstackclient.common import utils

from oscquintette.sdk.compute.v2 import server as server_lib


def _format_addresses(addresses):
    """Return a formatted string of networks and IP addresses

    :param addresses: a dict of network IP addresses
    :rtype: a string of semi-colon separated networks and IP addresses
    """

    if not addresses:
        return ""

    output = []
    for (network, addr_list) in addresses.items():
        if not addr_list:
            continue
        addresses_csv = ', '.join(
            [addr['addr'] for addr in addr_list]
        )
        group = "%s=%s" % (network, addresses_csv)
        output.append(group)
    return '; '.join(sorted(output))


class ServerList(lister.Lister):
    """List servers"""

    log = logging.getLogger(__name__ + '.ServerList')

    def get_parser(self, prog_name):
        parser = super(ServerList, self).get_parser(prog_name)
        parser.add_argument(
            '--name',
            metavar='<name>',
            help='Filter by server names (regular expression)',
        )
        parser.add_argument(
            '--status',
            metavar='<status>',
            # FIXME(dhellmann): Add choices?
            help='Filter by server status (ACTIVE, etc)',
        )
        parser.add_argument(
            '--flavor',
            metavar='<flavor-id>',
            help='Search by flavor ID',
        )
        parser.add_argument(
            '--image',
            metavar='<image-id>',
            help='Search by image ID',
        )
        parser.add_argument(
            "--marker",
            metavar="<server-id>",
            help="Start anchor for paging",
        )
        parser.add_argument(
            "--end-marker",
            metavar="<server-id>",
            help="End anchor for paging",
        )
        parser.add_argument(
            "--limit",
            metavar="<num>",
            type=int,
            help="Limit the number of servers returned",
        )
        parser.add_argument(
            '--long',
            action='store_true',
            default=False,
            help='List additional fields in output',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            default=False,
            help='List all servers (default is 10000)',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        qc = self.app.client_manager.oscquintette

        kwargs = {}
        if parsed_args.name:
            kwargs['name'] = parsed_args.name
        if parsed_args.status:
            kwargs['status'] = parsed_args.status
        if parsed_args.flavor:
            kwargs['flavor'] = parsed_args.flavor
        if parsed_args.image:
            kwargs['image'] = parsed_args.image
        if parsed_args.marker:
            kwargs['marker'] = parsed_args.marker
        if parsed_args.end_marker:
            kwargs['end_marker'] = parsed_args.end_marker
        if parsed_args.limit:
            kwargs['limit'] = parsed_args.limit
        if parsed_args.long:
            kwargs['long'] = True
        if parsed_args.all:
            kwargs['all_data'] = True

        endpoint = self.app.client_manager.get_endpoint_for_service_type(
            "compute",
        )
        data = server_lib.list(
            self.app.client_manager.session,
            endpoint,
            **kwargs
        )
        print "data: %s" % data

        if parsed_args.long:
            columns = (
                'id',
                'name',
                'status',
                'addresses',
                'OS-EXT-AZ:availability_zone',
                'OS-EXT-SRV-ATTR:host',
                'metadata',
            )
            column_headers = (
                'ID',
                'Name',
                'Status',
                'Networks',
                'Availability Zone',
                'Host',
                'Properties',
            )
            mixed_case_fields = [
                'OS-EXT-AZ:availability_zone',
                'OS-EXT-SRV-ATTR:host',
            ]
        else:
            columns = ('ID', 'Name')
            column_headers = columns
            mixed_case_fields = []

        return (
            column_headers,
            (utils.get_dict_properties(
                s, columns,
                mixed_case_fields=mixed_case_fields,
                formatters={
                    'addresses': _format_addresses,
                    'metadata': utils.format_dict,
                },
            ) for s in data))
