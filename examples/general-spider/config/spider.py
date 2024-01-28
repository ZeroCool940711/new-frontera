# -*- coding: utf-8 -*-
from __future__ import absolute_import
from new_frontera.settings.default_settings import MIDDLEWARES
from config import *

MAX_NEXT_REQUESTS = 256
DELAY_ON_EMPTY = 5.0

MIDDLEWARES.extend(
    [
        "new_frontera.contrib.middlewares.domain.DomainMiddleware",
        "new_frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware",
    ]
)

# --------------------------------------------------------
# Crawl frontier backend
# --------------------------------------------------------
BACKEND = "new_frontera.contrib.backends.remote.messagebus.MessageBusBackend"
