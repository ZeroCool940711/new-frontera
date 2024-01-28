========
Backends
========

A :class:`DistributedBackend <new_frontera.core.components.DistributedBackend>` is used to separate higher level code
of :term:`crawling strategy` from low level storage API. :class:`Queue <new_frontera.core.components.Queue>`,
:class:`Metadata <new_frontera.core.components.Metadata>`, :class:`States <new_frontera.core.components.States>` and
 :class:`DomainMetadata <new_frontera.core.components.DomainMetadata>` are inner components of the DistributedBackend.
The latter is meant to instantiate and hold the references to the objects of above mentioned classes. new_frontera is
bundled with database and in-memory implementations of Queue, Metadata, States and DomainMetadata which can be combined
in your custom backends or used standalone by directly instantiating specific variant of
:class:`FrontierManager <new_frontera.core.manager.FrontierManager>`.

DistributedBackend methods are called by the FrontierManager after
:class:`Middleware <new_frontera.core.components.Middleware>`, using hooks for
:class:`Request <new_frontera.core.models.Request>` and :class:`Response <new_frontera.core.models.Response>` processing
according to :ref:`frontier data flow <frontier-data-flow>`.

Unlike Middleware, that can have many different instances activated, only one DistributedBackend can be used per
frontier.


.. _frontier-activating-backend:

Activating a backend
====================

To activate the specific backend, set it through the :setting:`BACKEND` setting.

Here’s an example::

    BACKEND = 'new_frontera.contrib.backends.memory.MemoryDistributedBackend'

Keep in mind that some backends may need to be additionally configured through a particular setting. See
:ref:`backends documentation <frontier-built-in-backend>` for more info.

.. _frontier-writing-backend:

Writing your own backend
========================

Each backend component is a single Python class inherited from
:class:`DistributedBackend <new_frontera.core.components.DistributedBackend>` and using one or all of
:class:`Queue`, :class:`Metadata`, :class:`States` and :class:`DomainMetadata`.

:class:`FrontierManager` will communicate with active backend through the methods described below.


.. autoclass:: new_frontera.core.components.Backend

    **Methods**

    .. automethod:: new_frontera.core.components.Backend.frontier_start

        :return: None.

    .. automethod:: new_frontera.core.components.Backend.frontier_stop

        :return: None.

    .. automethod:: new_frontera.core.components.Backend.finished

    .. automethod:: new_frontera.core.components.Backend.add_seeds

        :return: None.

    .. automethod:: new_frontera.core.components.Backend.page_crawled

        :return: None.

    .. automethod:: new_frontera.core.components.Backend.request_error

        :return: None.

    .. automethod:: new_frontera.core.components.Backend.get_next_requests

    **Class Methods**

    .. automethod:: new_frontera.core.components.Backend.from_manager

    **Properties**

    .. autoattribute:: new_frontera.core.components.Backend.queue

    .. autoattribute:: new_frontera.core.components.Backend.states

    .. autoattribute:: new_frontera.core.components.Backend.metadata


.. autoclass:: new_frontera.core.components.DistributedBackend

Inherits all methods of Backend, and has two more class methods, which are called during strategy and db worker
instantiation.

    .. automethod:: new_frontera.core.components.DistributedBackend.strategy_worker
    .. automethod:: new_frontera.core.components.DistributedBackend.db_worker

Backend should communicate with low-level storage by means of these classes:

Metadata
^^^^^^^^

Is used to store the contents of the crawl.

.. autoclass:: new_frontera.core.components.Metadata

    **Methods**

    .. automethod:: new_frontera.core.components.Metadata.add_seeds

    .. automethod:: new_frontera.core.components.Metadata.request_error

    .. automethod:: new_frontera.core.components.Metadata.page_crawled


Known implementations are: :class:`MemoryMetadata` and :class:`sqlalchemy.components.Metadata`.

Queue
^^^^^

Is a priority queue and used to persist requests scheduled for crawling.

.. autoclass:: new_frontera.core.components.Queue

    **Methods**

    .. automethod:: new_frontera.core.components.Queue.get_next_requests

    .. automethod:: new_frontera.core.components.Queue.schedule

    .. automethod:: new_frontera.core.components.Queue.count

Known implementations are: :class:`MemoryQueue` and :class:`sqlalchemy.components.Queue`.

States
^^^^^^

Is a storage used for checking and storing the link states. Where state is a short integer of one of states descibed in
:class:`new_frontera.core.components.States`.

.. autoclass:: new_frontera.core.components.States

    **Methods**

    .. automethod:: new_frontera.core.components.States.update_cache

    .. automethod:: new_frontera.core.components.States.set_states

    .. automethod:: new_frontera.core.components.States.flush

    .. automethod:: new_frontera.core.components.States.fetch


Known implementations are: :class:`MemoryStates` and :class:`sqlalchemy.components.States`.

DomainMetadata
^^^^^^^^^^^^^^

Is used to store per-domain flags, counters or even robots.txt contents to help :term:`crawling strategy` maintain
features like per-domain number of crawled pages limit or automatic banning.

.. autoclass:: new_frontera.core.components.DomainMetadata

    **Methods**

    .. automethod:: new_frontera.core.components.DomainMetadata.__setitem__

    .. automethod:: new_frontera.core.components.DomainMetadata.__getitem__

    .. automethod:: new_frontera.core.components.DomainMetadata.__delitem__

    .. automethod:: new_frontera.core.components.DomainMetadata.__contains__


Known implementations are: native dict and :class:`sqlalchemy.components.DomainMetadata`.


.. _frontier-built-in-backend:

Built-in backend reference
==========================

This article describes all backend components that come bundled with new_frontera.


.. _frontier-backends-memory:

Memory backend
^^^^^^^^^^^^^^

This implementation is using `heapq`_ module to store the requests queue and native dicts for other purposes and is
meant to be used for educational or testing purposes only.

.. autoclass:: new_frontera.contrib.backends.memory.MemoryDistributedBackend


.. _frontier-backends-sqlalchemy:

SQLAlchemy backends
^^^^^^^^^^^^^^^^^^^

This implementations is using RDBMS storage with `SQLAlchemy`_ library.

By default it uses an in-memory SQLite database as a storage engine, but `any databases supported by SQLAlchemy`_ can
be used.

If you need to use your own `declarative sqlalchemy models`_, you can do it by using the
:setting:`SQLALCHEMYBACKEND_MODELS` setting.

For a complete list of all settings used for SQLAlchemy backends check the :doc:`settings <new_frontera-settings>` section.

.. autoclass:: new_frontera.contrib.backends.sqlalchemy.Distributed


HBase backend
^^^^^^^^^^^^^

.. autoclass:: new_frontera.contrib.backends.hbase.HBaseBackend

Is more suitable for large scale web crawlers. Settings reference can be found here :ref:`hbase-settings`. Consider
tunning a block cache to fit states within one block for average size website. To achieve this it's recommended to use
:attr:`hostname_local_fingerprint <new_frontera.utils.fingerprint.hostname_local_fingerprint>` to achieve documents
closeness within the same host. This function can be selected with :setting:`URL_FINGERPRINT_FUNCTION` setting.


Redis backend
^^^^^^^^^^^^^

.. autoclass:: new_frontera.contrib.backends.redis_backend.RedisBackend

This is similar to the HBase backend. It is suitable for large scale crawlers that still has a limited scope. It is
recommended to ensure Redis is allowed to use enough memory to store all data the crawler needs. In case of Redis
running out of memory, the crawler will log this and continue. When the crawler is unable to write metadata or queue
items to the database; that metadata or queue items are lost.

In case of connection errors; the crawler will attempt to reconnect three times. If the third attempt at connecting
to Redis fails, the worker will skip that Redis operation and continue operating.


.. _OrderedDict: https://docs.python.org/2/library/collections.html#collections.OrderedDict
.. _heapq: https://docs.python.org/2/library/heapq.html
.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _any databases supported by SQLAlchemy: http://docs.sqlalchemy.org/en/latest/dialects/index.html
.. _declarative sqlalchemy models: http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/index.html

