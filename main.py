from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from superjob.spiders.super import SuperSpider

if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    query = input('Введите запрос\n')

    runner.crawl(SuperSpider, search = query)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
