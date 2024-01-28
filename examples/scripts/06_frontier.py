"""
Frontier from parameters example
"""
from new_frontera import FrontierManager, graphs, Request, Response

if __name__ == "__main__":
    # Create graph
    graph = graphs.Manager("sqlite:///data/graph.db")

    # Create frontier
    frontier = FrontierManager(
        request_model="new_frontera.core.models.Request",
        response_model="new_frontera.core.models.Response",
        backend="new_frontera.contrib.backends.memory.FIFO",
        logger="new_frontera.logger.FrontierLogger",
        event_log_manager="new_frontera.logger.events.EventLogManager",
        middlewares=[
            "new_frontera.contrib.middlewares.domain.DomainMiddleware",
            "new_frontera.contrib.middlewares.fingerprint.UrlFingerprintMiddleware",
            "new_frontera.contrib.middlewares.fingerprint.DomainFingerprintMiddleware",
        ],
        test_mode=True,
    )

    # Add seeds
    frontier.add_seeds([Request(seed.url) for seed in graph.seeds])

    # Get next requests
    next_requests = frontier.get_next_requests()

    # Crawl pages
    for request in next_requests:
        # Fake page crawling
        crawled_page = graph.get_page(request.url)

        # Create response
        response = Response(
            url=request.url, status_code=crawled_page.status, request=request
        )
        # Create page links
        page_links = [Request(link.url) for link in crawled_page.links]

        # Update Page
        frontier.page_crawled(response=response, links=page_links)
