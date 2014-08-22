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

"""Plugin find action implementation"""

import logging

from cliff import lister

from openstackclient.common import utils


def findbyattr(d=None, a=None, v=None):
    """Search a list of resources by resource attribute"""

    def match(item):
        return getattr(item, a, None) == v

    if d is None or a is None:
        return []
    return filter(match, d)


def sortbyattr(d=None, a=None):
    """Sort a list of resources by resource attribute"""

    def getkey(item):
        return getattr(item, a, None)

    if d is None or a is None:
        return []
    return sorted(d, key=getkey)


def find_flair(items, sort_attr, **kwargs):
    """Find all resources meeting the given constraints"""

    def minimum_pieces_of_flair(item):
        """Find lowest value greater than the minumum"""

        result = True
        for k in kwargs:
            result = result and kwargs[k] <= getattr(item, k, 0)
        return result

    return sortbyattr(filter(minimum_pieces_of_flair, items), sort_attr)


class FindFlavor(lister.Lister):
    """Find matching flavor

    Find all flavors matching the specified minimum criteria
    """
    # TODO(dtroyer): This should eventually be merged into flavor.ListFlavor

    auth_required = True
    log = logging.getLogger(__name__ + ".FindFlavor")

    def get_parser(self, prog_name):
        parser = super(FindFlavor, self).get_parser(prog_name)
        parser.add_argument(
            "--ram",
            type=int,
            metavar="<size-mb>",
            default=256,
            help="Memory size in MB (default 256M)",
        )
        parser.add_argument(
            "--disk",
            type=int,
            metavar="<size-gb>",
            default=0,
            help="Disk size in GB (default 0G)",
        )
        parser.add_argument(
            "--vcpus",
            type=int,
            metavar="<vcpus>",
            default=1,
            help="Number of vcpus (default 1)",
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug("take_action(%s)" % parsed_args)
        compute_client = self.app.client_manager.compute

        columns = (
            "ID",
            "Name",
            "RAM",
            "Disk",
            "Ephemeral",
            "Swap",
            "VCPUs",
            "RXTX Factor",
            "Is Public",
            "Extra Specs"
        )

        flair = {}
        for i in ['ram', 'disk', 'vcpus']:
            if i in parsed_args:
                flair[i] = vars(parsed_args)[i]

        all_data = compute_client.flavors.list()

        # TODO(dtroyer): for now sort by RAM size, this should be generalized
        #                for all selection attributes
        data = find_flair(
            all_data,
            'ram',
            **flair
        )

        return (columns,
                (utils.get_item_properties(
                    s, columns,
                ) for s in data))
