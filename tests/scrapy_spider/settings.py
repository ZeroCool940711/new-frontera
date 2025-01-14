# --------------------------------------------------------------------------
# Scrapy Settings
# --------------------------------------------------------------------------
BOT_NAME = "scrapy_spider"

SPIDER_MODULES = ["tests.scrapy_spider.spiders"]
NEWSPIDER_MODULE = "tests.scrapy_spider.spiders"

HTTPCACHE_ENABLED = False
REDIRECT_ENABLED = True
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 20
RETRY_ENABLED = False

CONCURRENT_REQUESTS = 10
CONCURRENT_REQUESTS_PER_DOMAIN = 2

LOGSTATS_INTERVAL = 10

# --------------------------------------------------------------------------
# Frontier Settings
# --------------------------------------------------------------------------
SPIDER_MIDDLEWARES = {
    "new_frontera.contrib.scrapy.middlewares.schedulers.SchedulerSpiderMiddleware": 999
}
DOWNLOADER_MIDDLEWARES = {
    "new_frontera.contrib.scrapy.middlewares.schedulers.SchedulerDownloaderMiddleware": 999
}
SCHEDULER = "new_frontera.contrib.scrapy.schedulers.frontier.new_fronteraScheduler"
new_frontera_SETTINGS = "tests.scrapy_spider.new_frontera.settings"


# --------------------------------------------------------------------------
# Testing
# --------------------------------------------------------------------------
# CLOSESPIDER_PAGECOUNT = 1
