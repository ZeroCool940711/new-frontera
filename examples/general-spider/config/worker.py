# -*- coding: utf-8 -*-
from __future__ import absolute_import
from new_frontera.settings.default_settings import MIDDLEWARES
from config import *

MAX_NEXT_REQUESTS = 512

# --------------------------------------------------------
# Url storage
# --------------------------------------------------------

BACKEND = "new_frontera.contrib.backends.sqlalchemy.Distributed"


SQLALCHEMYBACKEND_ENGINE_ECHO = False
from datetime import timedelta

SQLALCHEMYBACKEND_REVISIT_INTERVAL = timedelta(days=3)


MIDDLEWARES.extend(
    [
        "new_frontera.contrib.middlewares.domain.DomainMiddleware",
        "new_frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware",
    ]
)

LOGGING_CONFIG = "logging.conf"
