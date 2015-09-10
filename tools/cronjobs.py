from __future__ import print_function
import json
import os
import re
import sys


entrypoint_information = {
    'performanceplatform.collector.ga': {
        'credentials': 'credentials/ga.json',
        'repeat': 'daily',
    },
    'performanceplatform.collector.webtrends.reports': {
        'credentials': [
            ('^nas-applications$',
             'credentials/webtrends_national_apprenticeship_scheme.json'),
            ('^nhs-choices$',
             'credentials/webtrends_nhs_choices.json'),
        ],
        'repeat': 'daily',
    },
    'performanceplatform.collector.webtrends.keymetrics': {
        'credentials': [
            ('^nas-applications$',
             'credentials/webtrends_national_apprenticeship_scheme.json'),
            ('^nhs-choices$',
             'credentials/webtrends_nhs_choices.json'),
        ],
        'repeat': 'hourly',
    },
    'performanceplatform.collector.ga.trending': {
        'credentials': 'credentials/ga.json',
        'repeat': 'daily',
    },
    'performanceplatform.collector.ga.contrib.content.table': {
        'credentials': 'credentials/ga.json',
        'repeat': 'daily',
    },
    'performanceplatform.collector.ga.realtime': {
        'credentials': 'credentials/ga.json',
        'repeat': '2minute',
    },
    'performanceplatform.collector.pingdom': {
        'credentials': 'credentials/pingdom.json',
        'repeat': 'hourly',
    },
    'performanceplatform.collector.piwik.core': {
        'credentials': 'credentials/piwik_fco.json',
        'repeat': 'daily',
    },
    'performanceplatform.collector.piwik.realtime': {
        'credentials': 'credentials/piwik_fco.json',
        'repeat': '2minute',
    },
    'performanceplatform.collector.gcloud': {
        'credentials': 'credentials/gcloud.json',
        'repeat': 'hourly',
    },
}


def daily(jobs):
    entries = ['#', '# Daily jobs', '#', '']
    for index, (collector, credentials, token) in enumerate(jobs):
        hour, minute = divmod(index, 60)
        entries.append(
            '{0} {1} * * *,{2},{3},{4},performanceplatform.json'
            .format(minute, hour, collector['slug'], credentials, token))
    return entries


def hourly(jobs):
    entries = ['#', '# Hourly jobs', '#', '']
    for index, (collector, credentials, token) in enumerate(jobs):
        minute = index % 60
        entries.append(
            '{0} * * * *,{1},{2},{3},performanceplatform.json'
            .format(minute, collector['slug'], credentials, token))
    return entries


def two_minute(jobs):
    entries = ['#', '# Run every two minutes', '#', '']
    for index, (collector, credentials, token) in enumerate(jobs):
        entries.append(
            '1-59/2 * * * *,{0},{1},{2},performanceplatform.json'
            .format(collector['slug'], credentials, token))
    return entries


def setup_time_data_set(
        collector_info,
        collector,
        token_file,
        data_group):

    """Using default repeat
    >>> token_file = 'abc.txt'
    >>> collector = {"some": 'query', "entry_point": "entry.point"}
    >>> collector_info = {
    ... 'credentials': 'credentials/ga.json',
    ... 'repeat': 'daily',
    ... }
    >>> setup_time_data_set(collector_info, collector, token_file, None)
    ({'entry_point': 'entry.point', 'some': 'query'}, 'credentials/ga.json', 'abc.txt')
    >>> collector_info = {
    ... 'credentials': [('nas', 'credentials/ga.json')],
    ... 'repeat': 'daily',
    ... }
    >>> setup_time_data_set(collector_info, collector, token_file, 'nas')
    ({'entry_point': 'entry.point', 'some': 'query'}, 'credentials/ga.json', 'abc.txt')
    >>> collector_info = {
    ... 'credentials': [
    ...   ('blah', 'credentials/ga.json'),
    ...   ('.*', 'credentials/default.json'),
    ...  ],
    ... 'repeat': 'daily',
    ... }
    >>> setup_time_data_set(collector_info, collector, token_file, 'some-other')
    ({'entry_point': 'entry.point', 'some': 'query'}, 'credentials/default.json', 'abc.txt')

    """
    credentials_file = collector_info['credentials']
    if type(credentials_file) == list:
        for pattern, path in credentials_file:
            if re.search(pattern, data_group):
                credentials_file = path
                break

    return (collector, credentials_file, token_file)


def setup_time_data_sets(collectors, entrypoint_information):
    """Testing returns correct time grouped data sets
    >>> entrypoint_information = {
    ...   'performanceplatform.collector.pingdom': {
    ...     'credentials': 'credentials/ga.json',
    ...     'repeat': 'daily'
    ...   }
    ... }
    >>> collectors = [{
    ...   'slug': 'test-collector',
    ...   'entry_point': 'performanceplatform.collector.pingdom',
    ...   'type': {'slug': 'pingdom'},
    ...   'data_set': {'data_group': 'test_data_group'}
    ... }]  # noqa
    >>> setup_time_data_sets(collectors, entrypoint_information) #doctest: +NORMALIZE_WHITESPACE
    {'daily': [({'type': {'slug': 'pingdom'},
    'entry_point': 'performanceplatform.collector.pingdom',
    'slug': 'test-collector',
    'data_set': {'data_group': 'test_data_group'}},
    'credentials/ga.json',
    'tokens/pingdom.json')]}
    >>> entrypoint_information = {
    ...   'performanceplatform.collector.pingdom': {
    ...     'credentials': 'credentials/ga.json',
    ...     'repeat': 'hourly'
    ...   }
    ... }
    >>> collectors = [{
    ...   'slug': 'test-collector',
    ...   'entry_point': 'performanceplatform.collector.pingdom',
    ...   'type': {'slug': 'pingdom'},
    ...   'data_set': {'data_group': 'test_data_group'}
    ... }]
    >>> setup_time_data_sets(collectors, entrypoint_information) #doctest: +NORMALIZE_WHITESPACE
    {'hourly': [({'type': {'slug': 'pingdom'},
    'entry_point': 'performanceplatform.collector.pingdom',
    'slug': 'test-collector',
    'data_set': {'data_group': 'test_data_group'}},
    'credentials/ga.json',
    'tokens/pingdom.json')]}
    """
    time_data_sets = {}
    for collector in collectors:
        entrypoint = collector.get('entry_point')
        token_file = "tokens/{0}.json".format(
            collector.get('type').get('slug'))

        collector_info = entrypoint_information.get(entrypoint, None)

        if collector_info is None:
            raise ValueError(
                "No entrypoint {0} from {1}".format(entrypoint, collector))

        repeat = collector.get('repeat', collector_info['repeat'])

        if repeat not in time_data_sets:
            time_data_sets[repeat] = []

        time_data_sets[repeat].append(setup_time_data_set(
            collector_info,
            collector,
            token_file,
            collector['data_set']['data_group']))


    return time_data_sets


def main():
    with open('performanceplatform.json', 'r') as f:
        environment_config = json.load(f)

    stagecraft_url = environment_config['stagecraft_url'].replace(
        "http://","",1)

    from httplib import HTTPSConnection
    conn = HTTPSConnection(stagecraft_url)

    token = environment_config['omniscient_api_token']
    headers = {
        "Authorization": "Bearer {}".format(token)
    }
    conn.request("GET", "/collector", headers=headers)
    resp = conn.getresponse()
    data = resp.read()

    collectors = json.loads(data)

    try:
        time_data_sets = setup_time_data_sets(collectors,
                                              entrypoint_information)

        daily_jobs = daily(time_data_sets['daily']) \
            if 'daily' in time_data_sets else []
        hourly_jobs = hourly(time_data_sets['hourly']) \
            if 'hourly' in time_data_sets else []
        two_minute_jobs = two_minute(time_data_sets['2minute']) \
            if '2minute' in time_data_sets else []

        spacer = ['', '']
        cronjobs_content = [
            '#',
            '# This file was generated by cronjobs.py',
            '#',
        ] + spacer + \
            daily_jobs + \
            spacer + \
            hourly_jobs + \
            spacer + \
            two_minute_jobs

        print('\n'.join(cronjobs_content))
    except ValueError as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
