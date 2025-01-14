.. _frontier-middlewares:

===========
Middlewares
===========

Frontier :class:`Middleware <new_frontera.core.components.Middleware>` sits between
:class:`FrontierManager <new_frontera.core.manager.FrontierManager>` and
:class:`Backend <new_frontera.core.components.Backend>` objects, using hooks for
:class:`Request <new_frontera.core.models.Request>`
and :class:`Response <new_frontera.core.models.Response>` processing according to
:ref:`frontier data flow <frontier-data-flow>`.

It’s a light, low-level system for filtering and altering Frontier’s requests and responses.

.. _frontier-activating-middleware:

Activating a middleware
=======================

To activate a :class:`Middleware <new_frontera.core.components.Middleware>` component, add it to the
:setting:`MIDDLEWARES` setting, which is a list whose values can be class paths or instances of
:class:`Middleware <new_frontera.core.components.Middleware>` objects.

Here’s an example::

    MIDDLEWARES = [
        'new_frontera.contrib.middlewares.domain.DomainMiddleware',
    ]

Middlewares are called in the same order they've been defined in the list, to decide which order to assign to your
middleware pick a value according to where you want to insert it. The order does matter because each middleware
performs a different action and your middleware could depend on some previous (or subsequent) middleware being applied.

Finally, keep in mind that some middlewares may need to be enabled through a particular setting. See
:ref:`each middleware documentation <frontier-built-in-middleware>` for more info.

.. _frontier-writing-middleware:

Writing your own middleware
===========================


Writing your own frontier middleware is easy. Each :class:`Middleware <new_frontera.core.components.Middleware>`
component is a single Python class inherited from :class:`Component <new_frontera.core.components.Component>`.


:class:`FrontierManager <new_frontera.core.manager.FrontierManager>` will communicate with all active middlewares
through the methods described below.

.. autoclass:: new_frontera.core.components.Middleware

    **Methods**

    .. automethod:: new_frontera.core.components.Middleware.frontier_start
    .. automethod:: new_frontera.core.components.Middleware.frontier_stop
    .. automethod:: new_frontera.core.components.Middleware.add_seeds

        :return: :class:`Request <new_frontera.core.models.Request>` object list or ``None``

        Should either return ``None`` or a list of :class:`Request <new_frontera.core.models.Request>` objects.

        If it returns ``None``, :class:`FrontierManager <new_frontera.core.manager.FrontierManager>` won't continue
        processing any other middleware and seed will never reach the
        :class:`Backend <new_frontera.core.components.Backend>`.

        If it returns a list of :class:`Request <new_frontera.core.models.Request>` objects, this will be passed to
        next middleware. This process will repeat for all active middlewares until result is finally passed to the
        :class:`Backend <new_frontera.core.components.Backend>`.

        If you want to filter any seed, just don't include it in the returned object list.

    .. automethod:: new_frontera.core.components.Middleware.page_crawled

        :return: :class:`Response <new_frontera.core.models.Response>` or ``None``

        Should either return ``None`` or a :class:`Response <new_frontera.core.models.Response>` object.

        If it returns ``None``, :class:`FrontierManager <new_frontera.core.manager.FrontierManager>` won't continue
        processing any other middleware and :class:`Backend <new_frontera.core.components.Backend>` will never be
        notified.

        If it returns a :class:`Response <new_frontera.core.models.Response>` object, this will be passed to
        next middleware. This process will repeat for all active middlewares until result is finally passed to the
        :class:`Backend <new_frontera.core.components.Backend>`.

        If you want to filter a page, just return None.

    .. automethod:: new_frontera.core.components.Middleware.request_error


        :return: :class:`Request <new_frontera.core.models.Request>` or ``None``

        Should either return ``None`` or a :class:`Request <new_frontera.core.models.Request>` object.

        If it returns ``None``, :class:`FrontierManager <new_frontera.core.manager.FrontierManager>` won't continue
        processing any other middleware and :class:`Backend <new_frontera.core.components.Backend>` will never be
        notified.

        If it returns a :class:`Response <new_frontera.core.models.Request>` object, this will be passed to
        next middleware. This process will repeat for all active middlewares until result is finally passed to the
        :class:`Backend <new_frontera.core.components.Backend>`.

        If you want to filter a page error, just return None.

    **Class Methods**

    .. automethod:: new_frontera.core.components.Middleware.from_manager



.. _frontier-built-in-middleware:

Built-in middleware reference
=============================

This page describes all :class:`Middleware <new_frontera.core.components.Middleware>` components that come with new_frontera.
For information on how to use them and how to write your own middleware, see the
:ref:`middleware usage guide. <frontier-writing-middleware>`.

For a list of the components enabled by default (and their orders) see the :setting:`MIDDLEWARES` setting.


.. _frontier-domain-middleware:

DomainMiddleware
----------------

.. autoclass:: new_frontera.contrib.middlewares.domain.DomainMiddleware()


.. _frontier-url-fingerprint-middleware:

UrlFingerprintMiddleware
------------------------

.. autoclass:: new_frontera.contrib.middlewares.fingerprint.UrlFingerprintMiddleware()
.. autofunction:: new_frontera.utils.fingerprint.hostname_local_fingerprint



.. _frontier-domain-fingerprint-middleware:

DomainFingerprintMiddleware
---------------------------

.. autoclass:: new_frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware()
