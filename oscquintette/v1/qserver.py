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

"""QServer action implementations"""

import logging

from openstackclient.common import exceptions as osc_exceptions
from openstackclient.compute.v2 import server
from oscquintette.v1 import find


class CreateQServer(server.CreateServer):
    """Create a new qserver"""

    log = logging.getLogger(__name__ + '.CreateQServer')

    def get_parser(self, prog_name):
        parser = super(self.__class__, self).get_parser(prog_name)

        # TODO(dtroyer): break into superclass parser and make
        #                --flavor optional, or mutex with the flavor
        #                constraint options below
        parser.add_argument(
            "--ram",
            type=int,
            metavar="<size-mb>",
            help="Minimum memory size in MB",
        )
        parser.add_argument(
            "--disk",
            type=int,
            metavar="<size-gb>",
            help="Minimum disk size in GB",
        )
        parser.add_argument(
            "--vcpus",
            type=int,
            metavar="<vcpus>",
            help="Minimum number of vcpus",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        compute_client = self.app.client_manager.compute
        pa = vars(parsed_args)

        # Just munge the passed args
        flair = {}
        for i in ['ram', 'disk', 'vcpus']:
            if i in parsed_args:
                flair[i] = pa.pop(i)

        all_flavors = compute_client.flavors.list(),
        flavors = find.find_flair(
            all_flavors,
            'ram',
            **flair
        )

        if len(flavors) > 1 and flavors[0] is not None:
            parsed_args.flavor = flavors[0].id
            self.log.info('selected flavor %s', flavors[0].name)
        elif parsed_args.flavor is not None:
            f_name = find.findbyattr(all_flavors, 'name', parsed_args.flavor)
            if len(f_name) > 0:
                parsed_args.flavor = f_name[0]
            else:
                f_id = find.findbyattr(all_flavors, 'id', parsed_args.flavor)
                if len(f_id) > 0:
                    parsed_args.flavor = f_id[0]
                else:
                    parsed_args.flavor = None
        if parsed_args.flavor is None:
            msg = 'No suitable flavor found'
            raise osc_exceptions.CommandError(msg)

        return super(self.__class__, self).take_action(parsed_args)
