# -*- coding: utf-8 -*-
BOT_NAME = "general"

SPIDER_MODULES = ["general.spiders"]
NEWSPIDER_MODULE = "general.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = (
    "new_frontera-based example bot (+https://github.com/scrapinghub/new_frontera)"
)

SPIDER_MIDDLEWARES = {
    "new_frontera.contrib.scrapy.middlewares.schedulers.SchedulerSpiderMiddleware": 1000,
    "scrapy.spidermiddleware.depth.DepthMiddleware": None,
    "scrapy.spidermiddleware.offsite.OffsiteMiddleware": None,
    "scrapy.spidermiddleware.referer.RefererMiddleware": None,
    "scrapy.spidermiddleware.urllength.UrlLengthMiddleware": None,
}

DOWNLOADER_MIDDLEWARES = {
    "new_frontera.contrib.scrapy.middlewares.schedulers.SchedulerDownloaderMiddleware": 1000,
}

SCHEDULER = "new_frontera.contrib.scrapy.schedulers.frontier.new_fronteraScheduler"


HTTPCACHE_ENABLED = False
REDIRECT_ENABLED = True
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 240
RETRY_ENABLED = False
DOWNLOAD_MAXSIZE = 1 * 1024 * 1024

# auto throttling
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False
AUTOTHROTTLE_MAX_DELAY = 3.0
AUTOTHROTTLE_START_DELAY = 0.25
RANDOMIZE_DOWNLOAD_DELAY = False

# concurrency
CONCURRENT_REQUESTS = 64
CONCURRENT_REQUESTS_PER_DOMAIN = 10
DOWNLOAD_DELAY = 0.0

LOG_LEVEL = "INFO"

REACTOR_THREADPOOL_MAXSIZE = 32
DNS_TIMEOUT = 180
new_frontera_SETTINGS = "config.spider"
HTTPERROR_ALLOW_ALL = True
