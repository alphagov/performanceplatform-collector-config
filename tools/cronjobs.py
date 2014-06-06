
import json
import os


entrypoint_information = {
    'performanceplatform.collector.ga': {
        'credentials': 'credentials/ga.json',
        'repeat': 'daily',
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
    'performanceplatform.collector.gcloud': {
        'credentials': '',
        'repeat': 'daily',
    },
}


def daily(jobs):
    entries = ['#', '# Daily jobs', '#', '']
    for index, (query, credentials, token) in enumerate(jobs):
        hour, minute = divmod(index, 60)
        entries.append('{0} {1} * * *,{2},{3},{4},performanceplatform.json'.format(minute, hour, query, credentials, token))
    return entries


def hourly(jobs):
    entries = ['#', '# Hourly jobs', '#', '']
    for index, (query, credentials, token) in enumerate(jobs):
        minute = index % 60
        entries.append('{0} * * * *,{1},{2},{3},performanceplatform.json'.format(minute, query, credentials, token))
    return entries


def two_minute(jobs):
    entries = ['#', '# Run every two minutes', '#', '']
    for index, (query, credentials, token) in enumerate(jobs):
        entries.append('1-59/2 * * * *,{0},{1},{2},performanceplatform.json'.format(query, credentials, token))
    return entries


def main():
    queries = [os.path.join(dp, f) for dp, dn, filenames in os.walk('queries') for f in filenames if os.path.splitext(f)[1] == '.json']
    time_data_sets = {}

    for query in queries:
        with open(query) as query_fd:
            query_json = json.load(query_fd)
            entrypoint = query_json['entrypoint']
            token_file = "tokens/{0}.json".format(query_json['token'])

        query_info = entrypoint_information.get(entrypoint, None)

        if query_info is None:
            print "No entrypoint {0} from {1}".format(entrypoint, query)
        else:
            if query_info['repeat'] not in time_data_sets:
                time_data_sets[query_info['repeat']] = []

            time_data_sets[query_info['repeat']].append((query, query_info['credentials'], token_file))

    daily_jobs = daily(time_data_sets['daily'])
    hourly_jobs = hourly(time_data_sets['hourly'])
    two_minute_jobs = two_minute(time_data_sets['2minute'])

    spacer = ['', '']
    cronjobs_content = [
        '#',
        '# This file was generated by cronjobs.py',
        '#',
    ] + spacer + daily_jobs + spacer + hourly_jobs + spacer + two_minute_jobs

    print '\n'.join(cronjobs_content)


if __name__ == '__main__':
    main()
