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

"""OpenStackClient Plugin interface"""

import logging

from openstackclient.common import utils


LOG = logging.getLogger(__name__)

DEFAULT_OSCQUINTETTE_API_VERSION = '1'

# Required by the OSC plugin interface
API_NAME = 'oscquintette'
API_VERSION_OPTION = 'os_oscquintette_api_version'
API_VERSIONS = {
    '1': 'oscquintette.plugin.EmptyClient',
}


# Required by the OSC quintette interface
def make_client(instance):
    """Returns a client to the ClientManager

    Called to instantiate the requested client version.  instance has
    any available auth info that may be required to prepare the client.

    :param ClientManager instance: The ClientManager that owns the new client
    """
    plugin_client = utils.get_client_class(
        API_NAME,
        instance._api_version[API_NAME],
        API_VERSIONS)
    LOG.debug('Instantiating plugin client: %s' % plugin_client)

    client = plugin_client()
    return client


# Required by the OSC plugin interface
def build_option_parser(parser):
    """Hook to add global options

    Called from openstackclient.shell.OpenStackShell.__init__()
    after the builtin parser has been initialized.  This is
    where a plugin can add global options such as an API version setting.

    :param argparse.ArgumentParser parser: The parser object that has been
        initialized by OpenStackShell.
    """
    parser.add_argument(
        '--os-oscquintette-api-version',
        metavar='<oscquintette-api-version>',
        default=utils.env(
            'OS_OSCQUINTETTE_API_VERSION',
            default=DEFAULT_OSCQUINTETTE_API_VERSION),
        help='OSC Quintette API version, default=' +
             DEFAULT_OSCQUINTETTE_API_VERSION +
             ' (Env: OS_OSCQUINTETTE_API_VERSION)')
    return parser

class EmptyClient(object):
    pass
