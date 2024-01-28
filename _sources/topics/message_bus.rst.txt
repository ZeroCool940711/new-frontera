===========
Message bus
===========

Message bus is the transport layer abstraction mechanism. new_frontera provides interface and several implementations.
Only one message bus can be used in crawler at the time, and it's selected with :setting:`MESSAGE_BUS` setting.

Spiders process can use

.. autoclass:: new_frontera.contrib.backends.remote.messagebus.MessageBusBackend

to communicate using message bus.


Built-in message bus reference
==============================

ZeroMQ
------
It's the default option, implemented using lightweight `ZeroMQ`_ library in

.. autoclass:: new_frontera.contrib.messagebus.zeromq.MessageBus

and can be configured using :ref:`zeromq-settings`.

ZeroMQ message bus requires installed ZeroMQ library and running broker process, see :ref:`running_zeromq_broker`.

Overall ZeroMQ message bus is designed to get a working PoC quickly and smaller deployments. Mainly because it's prone
to message loss when data flow of components isn't properly adjusted or during startup. Here's the recommended order of
components startup to avoid message loss:

#. :term:`db worker`
#. :term:`strategy worker`
#. :term:`spider`s

Unfortunately, it's not possible to avoid message loss when stopping running crawler with unfinished crawl. We recommend
 to use Kafka message bus if your crawler application is sensitive to small message loss.

.. pull-quote::
    WARNING! ZeroMQ message bus doesn't support yet multiple SW and DB workers, only one instance of each worker
    type is allowed.

Kafka
-----
Can be selected with

.. autoclass:: new_frontera.contrib.messagebus.kafkabus.MessageBus

and configured using :ref:`kafka-settings`.

Requires running `Kafka`_ service and more suitable for large-scale web crawling.

.. _Kafka: http://kafka.apache.org/
.. _ZeroMQ: http://zeromq.org/


.. _message_bus_protocol:

Protocol
========

Depending on stream new_frontera is using several message types to code it's messages. Every message is a python native
object serialized using `msgpack`_ or JSON. The codec module can be selected using :setting:`MESSAGE_BUS_CODEC`, and
it's required to export ``Encoder`` and ``Decoder`` classes.

Here are the classes needed to subclass to implement own codec:

.. autoclass:: new_frontera.core.codec.BaseEncoder

    .. automethod:: new_frontera.core.codec.BaseEncoder.encode_add_seeds
    .. automethod:: new_frontera.core.codec.BaseEncoder.encode_page_crawled
    .. automethod:: new_frontera.core.codec.BaseEncoder.encode_request_error
    .. automethod:: new_frontera.core.codec.BaseEncoder.encode_request
    .. automethod:: new_frontera.core.codec.BaseEncoder.encode_update_score
    .. automethod:: new_frontera.core.codec.BaseEncoder.encode_new_job_id
    .. automethod:: new_frontera.core.codec.BaseEncoder.encode_offset

.. autoclass:: new_frontera.core.codec.BaseDecoder

    .. automethod:: new_frontera.core.codec.BaseDecoder.decode
    .. automethod:: new_frontera.core.codec.BaseDecoder.decode_request


Available codecs
================

MsgPack
-------
.. automodule:: new_frontera.contrib.backends.remote.codecs.msgpack

Module: new_frontera.contrib.backends.remote.codecs.msgpack

JSON
----
.. automodule:: new_frontera.contrib.backends.remote.codecs.json

Module: new_frontera.contrib.backends.remote.codecs.json


.. _msgpack: http://msgpack.org/index.html
