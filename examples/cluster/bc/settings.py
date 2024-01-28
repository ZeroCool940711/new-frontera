# -*- coding: utf-8 -*-
new_frontera_SETTINGS = "bc.config.spider"

SCHEDULER = "new_frontera.contrib.scrapy.schedulers.frontier.new_fronteraScheduler"
SPIDER_MIDDLEWARES = {
    "new_frontera.contrib.scrapy.middlewares.schedulers.SchedulerSpiderMiddleware": 999,
    "new_frontera.contrib.scrapy.middlewares.seeds.file.FileSeedLoader": 1,
}
DOWNLOADER_MIDDLEWARES = {
    "new_frontera.contrib.scrapy.middlewares.schedulers.SchedulerDownloaderMiddleware": 999,
}

BOT_NAME = "bc"

SPIDER_MODULES = ["bc.spiders"]
NEWSPIDER_MODULE = "bc.spiders"

CONCURRENT_REQUESTS = 256
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DOWNLOAD_DELAY = 0.0
DOWNLOAD_TIMEOUT = 180
RANDOMIZE_DOWNLOAD_DELAY = False

REACTOR_THREADPOOL_MAXSIZE = 30
DNS_TIMEOUT = 120

COOKIES_ENABLED = False
RETRY_ENABLED = False
REDIRECT_ENABLED = True
AJAXCRAWL_ENABLED = False

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.01
AUTOTHROTTLE_MAX_DELAY = 3.0
AUTOTHROTTLE_DEBUG = False

LOG_LEVEL = "INFO"
