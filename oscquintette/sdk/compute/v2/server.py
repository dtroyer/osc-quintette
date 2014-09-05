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

"""Server v2 API library"""


RESOURCE_KEY = 'server'
RESOURCES_KEY = 'servers'
BASE_PATH = '/servers'


def list(
    session,
    endpoint,
    long=False,
    all_data=False,
    marker=None,
    limit=None,
    end_marker=None,
    **params
):

    if all_data:
        data = listing = list(
            session,
            endpoint,
            long=long,
            marker=marker,
            limit=limit,
            end_marker=end_marker,
            **params
        )
        while listing:
            # TODO(dtroyer): How can we use name here instead?
            marker = listing[-1]['id']
            listing = list(
                session,
                endpoint,
                long=long,
                marker=marker,
                limit=limit,
                end_marker=end_marker,
                **params
            )
            if listing:
                data.extend(listing)
        return data

    # NOTE(dtroyer): If we settle on not validating input these can be
    #                passed in **params
    if marker:
        params['marker'] = marker
    if limit:
        params['limit'] = limit
    if end_marker:
        params['end_marker'] = end_marker

    # is endpoint or service catalog in session?

    url = endpoint + BASE_PATH
    if long:
        url += "/detail"

    return session.get(url, params=params).json()[RESOURCES_KEY]
