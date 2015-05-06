from __future__ import print_function
import json
import os
import sys


entrypoint_information = {
    'performanceplatform.collector.ga': {
        'credentials': 'credentials/ga.json',
        'repeat': 'daily',
    },
    'performanceplatform.collector.webtrends.nhs-choices.reports': {
        'credentials': {
            u'nhs-choices': 'credentials/'
            'webtrends_nhs_choices.json'},
        'repeat': 'daily',
    },
    'performanceplatform.collector.webtrends.nhs-choices.keymetrics': {
        'credentials': {
            u'nhs-choices': 'credentials/'
            'webtrends_nhs_choices.json'},
        'repeat': 'hourly',
    },
    'performanceplatform.collector.webtrends.reports': {
        'credentials': {
            u'nas-applications': 'credentials/'
            'webtrends_national_apprenticeship_scheme.json'},
        'repeat': 'daily',
    },
    'performanceplatform.collector.webtrends.keymetrics': {
        'credentials': {
            u'nas-applications': 'credentials/'
            'webtrends_national_apprenticeship_scheme.json'},
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
    for index, (query, credentials, token) in enumerate(jobs):
        hour, minute = divmod(index, 60)
        entries.append(
            '{0} {1} * * *,{2},{3},{4},performanceplatform.json'
            .format(minute, hour, query, credentials, token))
    return entries


def hourly(jobs):
    entries = ['#', '# Hourly jobs', '#', '']
    for index, (query, credentials, token) in enumerate(jobs):
        minute = index % 60
        entries.append(
            '{0} * * * *,{1},{2},{3},performanceplatform.json'
            .format(minute, query, credentials, token))
    return entries


def two_minute(jobs):
    entries = ['#', '# Run every two minutes', '#', '']
    for index, (query, credentials, token) in enumerate(jobs):
        entries.append(
            '1-59/2 * * * *,{0},{1},{2},performanceplatform.json'
            .format(query, credentials, token))
    return entries


def setup_time_data_set(
        query_info,
        query,
        token_file,
        data_group):

    """Using default repeat
    >>> token_file = 'abc.txt'
    >>> query = {"some": 'query'}
    >>> query_info = {
    ... 'credentials': 'credentials/ga.json',
    ... 'repeat': 'daily',
    ... }
    >>> setup_time_data_set(query_info, query, token_file, None)
    ({'some': 'query'}, 'credentials/ga.json', 'abc.txt')
    >>> query_info = {
    ... 'credentials': {'nas':'credentials/ga.json'},
    ... 'repeat': 'daily',
    ... }
    >>> setup_time_data_set(query_info, query, token_file, 'nas')
    ({'some': 'query'}, 'credentials/ga.json', 'abc.txt')

    """
    credentials_file = query_info['credentials']
    if type(credentials_file) == dict:
        credentials_file = credentials_file[data_group]

    return (query, credentials_file, token_file)


def setup_time_data_sets(queries, entrypoint_information):
    """Testing returns correct time grouped data sets
    >>> entrypoint_information = {
    ...   'performanceplatform.collector.pingdom': {
    ...     'credentials': 'credentials/ga.json',
    ...     'repeat': 'daily'
    ...   }
    ... }
    >>> queries = ['queries/bis-payment-of-patent-renewal-fee-f12/monitoring.json']  # noqa
    >>> setup_time_data_sets(queries, entrypoint_information)
    {'daily': [('queries/bis-payment-of-patent-renewal-fee-f12/monitoring.json', 'credentials/ga.json', 'tokens/pingdom.json')]}
    >>> entrypoint_information = {
    ...   'performanceplatform.collector.pingdom': {
    ...     'credentials': 'credentials/ga.json',
    ...     'repeat': 'daily'
    ...   }
    ... }
    >>> queries = ['test/fixtures/query_with_repeat.json']
    >>> setup_time_data_sets(queries, entrypoint_information)
    {u'hourly': [('test/fixtures/query_with_repeat.json', 'credentials/ga.json', 'tokens/pingdom.json')]}
    """
    time_data_sets = {}
    for query in queries:
        with open(query) as query_fd:
            try:
                query_json = json.load(query_fd)
            except ValueError:
                raise ValueError("Invalid JSON in {}".format(query))
            entrypoint = query_json['entrypoint']
            token_file = "tokens/{0}.json".format(query_json['token'])

        query_info = entrypoint_information.get(entrypoint, None)

        if query_info is None:
            raise ValueError(
                "No entrypoint {0} from {1}".format(entrypoint, query))

        repeat = query_json.get('repeat', query_info['repeat'])

        if repeat not in time_data_sets:
            time_data_sets[repeat] = []

        time_data_sets[repeat].append(setup_time_data_set(
            query_info,
            query,
            token_file,
            query_json['data-set']['data-group']))

    return time_data_sets


def main():
    try:
        queries = [
            os.path.join(dp, f) for dp, dn, filenames
            in os.walk('queries') for f in filenames
            if os.path.splitext(f)[1] == '.json']
        time_data_sets = setup_time_data_sets(queries, entrypoint_information)

        daily_jobs = daily(time_data_sets['daily'])
        hourly_jobs = hourly(time_data_sets['hourly'])
        two_minute_jobs = two_minute(time_data_sets['2minute'])

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
