from __future__ import absolute_import
from new_frontera.contrib.scrapy.schedulers.frontier import new_fronteraScheduler
from tests.mocks.frontier_manager import FakeFrontierManager
from tests.mocks.crawler import FakeCrawler
from new_frontera.core.models import Request as FRequest
from new_frontera.core.models import Response as FResponse
from scrapy.http import Request, Response
from scrapy.spiders import Spider
from scrapy.settings import Settings
from six.moves import range


# test requests
r1 = Request("http://www.example.com")
r2 = Request("https://www.example.com/some/page")
r3 = Request("http://example1.com")


# test requests with redirects
rr1 = Request("http://www.example.com", meta={b"redirect_times": 1})
rr2 = Request("https://www.example.com/some/page", meta={b"redirect_times": 4})
rr3 = Request("http://example1.com", meta={b"redirect_times": 0})


# test frontier requests
fr1 = FRequest("http://www.example.com")
fr2 = Request("https://www.example.com/some/page")
fr3 = Request("http://example1.com")


class Testnew_fronteraScheduler(object):
    def test_redirect_disabled_enqueue_requests(self):
        settings = Settings()
        settings["REDIRECT_ENABLED"] = False
        crawler = FakeCrawler(settings)
        fs = new_fronteraScheduler(crawler, manager=FakeFrontierManager)
        fs.open(Spider)
        assert fs.enqueue_request(rr1) is False
        assert fs.enqueue_request(rr2) is False
        assert fs.enqueue_request(rr3) is False

    def test_redirect_enabled_enqueue_requests(self):
        settings = Settings()
        settings["REDIRECT_ENABLED"] = True
        crawler = FakeCrawler(settings)
        fs = new_fronteraScheduler(crawler, manager=FakeFrontierManager)
        fs.open(Spider)
        assert fs.enqueue_request(rr1) is True
        assert fs.enqueue_request(rr2) is True
        assert fs.enqueue_request(rr3) is True
        assert set([request.url for request in fs._pending_requests]) == set(
            [rr1.url, rr2.url, rr3.url]
        )

    def test_next_request(self):
        crawler = FakeCrawler()
        fs = new_fronteraScheduler(crawler, manager=FakeFrontierManager)
        fs.open(Spider)
        fs.frontier.manager.put_requests([fr1, fr2, fr3])
        requests = [fs.next_request() for _ in range(3)]
        assert set([request.url for request in requests]) == set(
            [fr1.url, fr2.url, fr3.url]
        )
        assert all([isinstance(request, Request) for request in requests])
        assert (
            fs.stats_manager.stats.get_value("new_frontera/returned_requests_count")
            == 3
        )

    def test_next_request_manager_finished(self):
        crawler = FakeCrawler()
        fs = new_fronteraScheduler(crawler, manager=FakeFrontierManager)
        fs.open(Spider)
        fs.frontier.manager.put_requests([fr1])
        fs.frontier.manager.finished = True
        assert fs.next_request() is None
        assert (
            fs.stats_manager.stats.get_value("new_frontera/returned_requests_count")
            is None
        )

    def test_next_request_overused_keys_info(self):
        settings = Settings()
        settings["CONCURRENT_REQUESTS_PER_DOMAIN"] = 0
        settings["CONCURRENT_REQUESTS_PER_IP"] = 5
        crawler = FakeCrawler(settings)
        # the keys in the slot_dict are ip's, the first value in the pair is the
        # slot.active list(only it's length is needed) and the second value is slot.concurrency.
        slot_dict = {
            "1.2.3": ([0] * 3, 1),
            "2.1.3": ([0] * 30, 2),
            "3.2.2": ([0] * 5, 1),
            "4.1.3": ([0] * 110, 20),
        }
        crawler.set_slots(slot_dict)
        fs = new_fronteraScheduler(crawler, manager=FakeFrontierManager)
        fs.open(Spider)
        fs.frontier.manager.put_requests([fr1])
        request = fs.next_request()
        assert request.url == fr1.url
        assert isinstance(request, Request)
        assert fs.frontier.manager.get_next_requests_kwargs[0]["key_type"] == "ip"
        assert set(
            fs.frontier.manager.get_next_requests_kwargs[0]["overused_keys"]
        ) == set(["2.1.3", "4.1.3"])
        assert (
            fs.stats_manager.stats.get_value("new_frontera/returned_requests_count")
            == 1
        )

    def test_process_spider_output(self):
        i1 = {"name": "item", "item": "i1"}
        i2 = {"name": "item", "item": "i2"}
        items = [i1, i2]
        requests = [r1, r2, r3]
        result = list(requests)
        result.extend(items)
        resp = Response(
            fr1.url, request=Request(fr1.url, meta={b"frontier_request": fr1})
        )
        crawler = FakeCrawler()
        fs = new_fronteraScheduler(crawler, manager=FakeFrontierManager)
        spider = Spider(name="testing")
        fs.open(spider)
        out_items = list(fs.process_spider_output(resp, result, spider))
        assert len(out_items) == len(items)
        assert set([r.url for r in fs.frontier.manager.links]) == set(
            [r.url for r in requests]
        )

        assert isinstance(fs.frontier.manager.responses[0], FResponse)
        assert fs.frontier.manager.responses[0].url == resp.url
        assert set([request.url for request in fs.frontier.manager.links]) == set(
            [r1.url, r2.url, r3.url]
        )
        assert all(
            [isinstance(request, FRequest) for request in fs.frontier.manager.links]
        )
        assert fs.stats_manager.stats.get_value("new_frontera/crawled_pages_count") == 1
        assert (
            fs.stats_manager.stats.get_value("new_frontera/crawled_pages_count/200")
            == 1
        )
        assert (
            fs.stats_manager.stats.get_value("new_frontera/links_extracted_count") == 3
        )

    def test_process_exception(self):
        exception = type("exception", (object,), {})
        crawler = FakeCrawler()
        fs = new_fronteraScheduler(crawler, manager=FakeFrontierManager)
        fs.open(Spider)
        fs.process_exception(r1, exception(), Spider)
        error = fs.frontier.manager.errors.pop()
        assert error[0].url == r1.url
        assert error[1] == "exception"
        assert (
            fs.stats_manager.stats.get_value("new_frontera/request_errors_count") == 1
        )
        assert (
            fs.stats_manager.stats.get_value(
                "new_frontera/request_errors_count/exception"
            )
            == 1
        )

    def test_close(self):
        crawler = FakeCrawler()
        fs = new_fronteraScheduler(crawler, manager=FakeFrontierManager)
        fs.open(Spider)
        fs.frontier.manager.put_requests([fr1, fr2, fr3])
        fs.next_request()
        fs.frontier.manager.iteration = 5
        fs.close("reason")
        assert fs.frontier.manager._stopped is True
        assert (
            fs.stats_manager.stats.get_value("new_frontera/pending_requests_count") == 2
        )
        assert fs.stats_manager.stats.get_value("new_frontera/iterations") == 5
