# -*- coding: utf-8 -*-
from new_frontera.settings.default_settings import MIDDLEWARES

MAX_NEXT_REQUESTS = 512
SPIDER_FEED_PARTITIONS = 1
SPIDER_LOG_PARTITIONS = 1
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
QUEUE_HOSTNAME_PARTITIONING = True
URL_FINGERPRINT_FUNCTION = "new_frontera.utils.fingerprint.hostname_local_fingerprint"

# MESSAGE_BUS='new_frontera.contrib.messagebus.kafkabus.MessageBus'
# KAFKA_LOCATION = 'localhost:9092'
# SCORING_GROUP = 'scrapy-scoring'
# SCORING_TOPIC = 'frontier-score'
