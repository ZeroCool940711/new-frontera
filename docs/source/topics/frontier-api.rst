============
new_frontera API
============

This section documents the new_frontera core API, and is intended for developers of middlewares and backends.

new_frontera API / Manager
======================

The main entry point to new_frontera API is the :class:`FrontierManager <new_frontera.core.manager.FrontierManager>`
object, passed to middlewares and backend through the from_manager class method. This object provides access to all
new_frontera core components, and is the only way for middlewares and backend to access them and hook their
functionality into new_frontera.

The :class:`FrontierManager <new_frontera.core.manager.FrontierManager>` is responsible for loading the installed
middlewares and backend, as well as for managing the data flow around the whole frontier.

.. _frontier-loading-from-settings:

Loading from settings
=====================

Although :class:`FrontierManager <new_frontera.core.manager.FrontierManager>` can be initialized using parameters the most
common way of doing this is using :doc:`new_frontera Settings <new_frontera-settings>`.

This can be done through the :attr:`from_settings <new_frontera.core.manager.FrontierManager.from_settings>`
class method, using either a string path::

    >>> from new_frontera import FrontierManager
    >>> frontier = FrontierManager.from_settings('my_project.frontier.settings')

or a :class:`BaseSettings <new_frontera.settings.BaseSettings>` object instance::

    >>> from new_frontera import FrontierManager, Settings
    >>> settings = Settings()
    >>> settings.MAX_PAGES = 0
    >>> frontier = FrontierManager.from_settings(settings)

It can also be initialized without parameters, in this case the frontier will use the
:ref:`default settings <frontier-default-settings>`::

    >>> from new_frontera import FrontierManager, Settings
    >>> frontier = FrontierManager.from_settings()


Frontier Manager
================


.. autoclass:: new_frontera.core.manager.FrontierManager

    **Attributes**

    .. autoattribute:: new_frontera.core.manager.FrontierManager.request_model
    .. autoattribute:: new_frontera.core.manager.FrontierManager.response_model
    .. autoattribute:: new_frontera.core.manager.FrontierManager.backend
    .. autoattribute:: new_frontera.core.manager.FrontierManager.middlewares
    .. autoattribute:: new_frontera.core.manager.FrontierManager.test_mode
    .. autoattribute:: new_frontera.core.manager.FrontierManager.max_requests
    .. autoattribute:: new_frontera.core.manager.FrontierManager.max_next_requests
    .. autoattribute:: new_frontera.core.manager.FrontierManager.auto_start
    .. autoattribute:: new_frontera.core.manager.FrontierManager.settings
    .. autoattribute:: new_frontera.core.manager.FrontierManager.iteration
    .. autoattribute:: new_frontera.core.manager.FrontierManager.n_requests
    .. autoattribute:: new_frontera.core.manager.FrontierManager.finished

    **API Methods**

    .. automethod:: new_frontera.core.manager.FrontierManager.start
    .. automethod:: new_frontera.core.manager.FrontierManager.stop
    .. automethod:: new_frontera.core.manager.FrontierManager.add_seeds
    .. automethod:: new_frontera.core.manager.FrontierManager.get_next_requests
    .. automethod:: new_frontera.core.manager.FrontierManager.page_crawled
    .. automethod:: new_frontera.core.manager.FrontierManager.request_error

    **Class Methods**

    .. automethod:: new_frontera.core.manager.FrontierManager.from_settings


.. _frontier-start-stop:

Starting/Stopping the frontier
==============================

Sometimes, frontier components need to perform initialization and finalization operations. The frontier mechanism to
notify the different components of the frontier start and stop is done by the
:attr:`start() <new_frontera.core.manager.FrontierManager.start>` and
:attr:`stop() <new_frontera.core.manager.FrontierManager.stop>` methods respectively.

By default :attr:`auto_start <new_frontera.core.manager.FrontierManager.auto_start>` frontier value is activated,
this means that components will be notified once the
:class:`FrontierManager <new_frontera.core.manager.FrontierManager>` object is created.
If you need to have more fine control of when different components are initialized, deactivate
:attr:`auto_start <new_frontera.core.manager.FrontierManager.auto_start>` and manually call frontier API
:attr:`start() <new_frontera.core.manager.FrontierManager.start>` and
:attr:`stop() <new_frontera.core.manager.FrontierManager.stop>` methods.

.. note::
    Frontier :attr:`stop() <new_frontera.core.manager.FrontierManager.stop>` method is not automatically called
    when :attr:`auto_start <new_frontera.core.manager.FrontierManager.auto_start>` is active (because frontier is
    not aware of the crawling state). If you need to notify components of frontier end you should call the method
    manually.


.. _frontier-iterations:

Frontier iterations
===================

Once frontier is running, the usual process is the one described in the :ref:`data flow <frontier-data-flow>` section.

Crawler asks the frontier for next pages using the
:attr:`get_next_requests() <new_frontera.core.manager.FrontierManager.get_next_requests>` method.
Each time the frontier returns a non empty list of pages (data available), is what we call a frontier iteration.

Current frontier iteration can be accessed using the
:attr:`iteration <new_frontera.core.manager.FrontierManager.iteration>` attribute.


.. _frontier-finish:

Finishing the frontier
======================

Crawl can be finished either by the Crawler or by the new_frontera. new_frontera will finish when a maximum number
of pages is returned. This limit is controlled by the
:attr:`max_requests <new_frontera.core.manager.FrontierManager.max_requests>` attribute
(:setting:`MAX_REQUESTS` setting).

If :attr:`max_requests <new_frontera.core.manager.FrontierManager.max_requests>` has a value of 0 (default value)
the frontier will continue indefinitely.

Once the frontier is finished, no more pages will be returned by the
:attr:`get_next_requests <new_frontera.core.manager.FrontierManager.get_next_requests>` method and
:attr:`finished <new_frontera.core.manager.FrontierManager.finished>` attribute will be True.

.. _frontier-test-mode:

Component objects
=================

.. autoclass:: new_frontera.core.components.Component

    **Attributes**

    .. autoattribute:: new_frontera.core.components.Component.name

    **Abstract methods**

    .. automethod:: new_frontera.core.components.Component.frontier_start
    .. automethod:: new_frontera.core.components.Component.frontier_stop
    .. automethod:: new_frontera.core.components.Component.add_seeds
    .. automethod:: new_frontera.core.components.Component.page_crawled
    .. automethod:: new_frontera.core.components.Component.request_error

    **Class Methods**

    .. automethod:: new_frontera.core.components.Component.from_manager


Test mode
=========

In some cases while testing, frontier components need to act in a different way than they usually do (for instance
:ref:`domain middleware <frontier-domain-middleware>` accepts non valid URLs like ``'A1'`` or ``'B1'`` when parsing
domain urls in test mode).

Components can know if the frontier is in test mode via the boolean
:attr:`test_mode <new_frontera.core.manager.FrontierManager.test_mode>` attribute.

.. _frontier-another-ways:

Other ways of using the frontier
==================================

Communication with the frontier can also be done through other mechanisms such as an HTTP API or a queue system. These
functionalities are not available for the time being, but hopefully will be included in future versions.

