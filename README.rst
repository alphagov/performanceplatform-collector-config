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

Update the cronjobs: :code:`python tools/cronjobs.py > cronjobs`.

Reference
=========

Queries
-------

performanceplatform.collector.ga
~~~~~~~~~~~~~~~~~~~~~

performanceplatform.collector.ga.trending
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

performanceplatform.collector.ga.realtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

performanceplatform.collector.pingdom
~~~~~~~~~~~~~~~~~~~~~~~~~~

Credentials
-----------

Google Analytics
~~~~~~~~~~~~~~~~

Pingdom
~~~~~~~
