.. image:: https://landscape.io/github/alphagov/performanceplatform-collector-config/master/landscape.png
   :target: https://landscape.io/github/alphagov/performanceplatform-collector-config/master
   :alt: Code Health

This repository holds all of the configuration for our_ instance of performanceplatform-collector_.

.. _our: https://www.gov.uk
.. _performanceplatform-collector: https://github.com/alphagov/performanceplatform-collector

.. contents:: :local:

Creating a new query
====================

Add a new config file in :code:`/queries`.


Query Reference
===============

performanceplatform.collector.ga
~~~~~~~~~~~~~~~~~~~~~

performanceplatform.collector.ga.trending
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

performanceplatform.collector.ga.realtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

performanceplatform.collector.pingdom
~~~~~~~~~~~~~~~~~~~~~~~~~~

performanceplatform.collector.webtrends.keymetrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Valid options:

- dataType
- additionalfields
- mappings
- idMapping
- plugins

After building up the basic data like so:

::
  
  {
    dataType: "the dataType in options if present,
               the data-type in data-set if not",
    _timestamp: "the period start datetime",
    ...
    and any 'measures' from the data...
  }

The options will be applied in order:

1. additionalfields will be added.

2. mappings will change keys at this point.

3. idMappings will generate a human and encoded id from the values of the keys in the given array.

4. plugins will run against the data at this point.


**Notes:**

You need to find out what keymetrics is calling unique visitors and then add this to mapping. In the following example "Visits" is used but this may be incorrect. 

::

  {
    "data-set": {
      "data-group": "national-appointments-scheme", 
      # Currently we don't pass the schema of realtime because they are returning 
      # floats instead of ints.
      # This means we need to use a type other than realtime.
      "data-type": "keymetrics"
    }, 
    "entrypoint": "performanceplatform.collector.webtrends.keymetrics", 
    "options": {
      "additionalFields": {
        "stage": "whoop",
        # This is required to pass the realtime schema.
        # It may not be necessary if we don't use this.
        "for_url": "boop"
      },
      "idMapping": ["dataType", "_timestamp", "stage"],
      # We need to specify all of these as something in backdrop is finding the original 
      # field names invalid. 
      # This may just be a realtime schema problem again though. 
      "mappings": {
       "Avg. Time on Site": "avg_time_on_site",
       "Page Views": "page_views",
       "Bounce Rate": "page_views",
       "Visits": "unique_visitors",
       "New Visitors": "new_visitors",
       "Page Views per Visit": "page_views_per_visit",
       "Avg. Visitors per Day": "avg_visitors_per_day"
      }
    }, 
    # Nothing is needed for query as all key metrics should be identical.
    "query": {
    }, 
    "token": "webtrends"
  }


performanceplatform.collector.webtrends.reports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Valid options:

- row_type_name
- dataType
- additionalfields
- mappings
- idMapping
- plugins

After building up the basic data like so:

::
  
  {
    <row_type_name_value>: "row dimension data",
    dataType: "the dataType in options if present,
               the data-type in data-set if not",
    _timestamp: "the period start datetime",
    ...
    and any 'measures' from the data...
  }

The options will be applied in order:

1. additionalfields will be added.

2. mappings will change keys at this point.

3. idMappings will generate a human and encoded id from the values of the keys in the given array.

4. plugins will run against the data at this point.

**Notes:**

**Version**

The default API version used is version 2 and the collector will work with no further config for anything with 'v2_0' in the reports or keymetrics url in the credentials file. For things with 'v3' in these urls you must add "api_version": "v3" to the credentials file in order for the version 3 urls to work.

**Measures**

Due to the nature of reports - the fields are defined by the service pushing data - you must inspect the response to find the measures available and choose from these. e.g. for:

::

  {
    "data":{  
      "10/29/2014-10/29/2014":{  
        "measures":{  
          "Visits":17.0
        },
        "SubRows":{  
          ...
        }
      }
    }
  }

In this case the measure available is "Visits". All measures are collected by default under their original title. If you need to change any of these then use the mappings option.

**row_type_name**

::

  "data": {
    "10/14/2014-10/15/2014": {
      "SubRows": {
        "Mozilla": {
          "Attributes": null,
          "SubRows": null,
          "measures": {
            "Visits": 1.0
          }
        },
        "Google Chrome": {
          "Attributes": null, 
          "SubRows": null, 
          "measures": {
            "Visits": 18.0
          }
        }
      }, 
      "measures": {
        "Visits": 19.0
      }
    }
  }

In the above data part of the response you can see that measures are grouped by browser name. "row_type_name" is a non optional argument which will tell the collector what call the data in this key for each row. In this case row type name is going to be "browser". This will result in data like the following:

::
  
  {
      "Visits": 5.0, 
      ...
      "browser": "Mozilla", 
  }

**Doing completion**

If the start and end stages of the service are in separate reports that you can specify two collectors collecting into a single data set and use the additionalfields parameter to distinguish one as start and one as end.

**Report id**

The reports config needs a report_id specified in query as below. This is unique to a service and report.

::

  {
    "data-set": {
      "data-group": "national-appointments-scheme", 
      "data-type": "browsers"
    }, 
    "entrypoint": "performanceplatform.collector.webtrends.reports", 
    "options": {
      "additionalFields": {
        "stage": "start"
      },
      "row_type_name": "browser",
      "idMapping": ["dataType", "_timestamp", "browser"],
      "mappings": {"old_key": "new_key"},
      "dataType": "govuk_visitors",
      "plugins": [
        # see performanceplatform-collector repo for all options
        "Comment('department computed from filtersets by collect-content-dashboard-table.py')", 
        "ComputeIdFrom('_timestamp', 'timeSpan', 'dataType', 'department', )"
      ]
    }, 
    "query": {
      # This is required and must be the valid report id.
      "report_id": "def"
    }, 
    "token": "webtrends"
  }

Testing locally:
~~~~~~~~~~~~~~~~

- Copy the credentials to the location of the current dummy credentials file.

- Copy the token to the location of the dummy token file.

- Change performanceplatform.json to reflect the real data endpoint locally (generally http://localhost:3039/data/).

- In the vm go to :code:`/var/apps/pp-puppet/development`.

- :code:`bowl stagecraft`

- :code:`bowl backdrop_read`

- Create a data set with the token, group and type on your local stagecraft.

- From the vm run:

::

  venv/bin/python /var/apps/performanceplatform-collector/venv/bin/pp-collector \
  -q /var/apps/performanceplatform-collector-config/queries/<path_to_query_file> \
  -c /var/apps/performanceplatform-collector-config/credentials/<path_to_credentials_json> \
  -t /var/apps/performanceplatform-collector-config/tokens/<path_to_token_json> \
  -b /var/apps/performanceplatform-collector-config/performanceplatform.json \
  --console-logging \
  --start=2014-10-29 --end=2014-10-30

- To check the result from the vm:

::  

  curl http://localhost:3038/data/<data_group>/<data_type>.
