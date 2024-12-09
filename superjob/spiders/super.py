import scrapy
from itemloaders import ItemLoader

from superjob.items import SuperjobItem


class SuperSpider(scrapy.Spider):
    name = "super"
    allowed_domains = ["superjob.ru"]

    def __init__(self, **kwargs):
        super().__init__()
        self.start_urls = [
            f'https://nsk.superjob.ru/vacancy/search/?keywords={kwargs.get('search')}',
            f'https://spb.superjob.ru/vacancy/search/?keywords={kwargs.get('search')}'
        ]

    def parse(self, response):
        links = response.xpath('//div[@class="f-test-search-result-item"]//a[contains(@href, "vakansii")]')
        for link in links:
            yield response.follow(
                url = link.xpath('./@href').get(),
                callback=self.__parse_vacancy
            )

    def __parse_vacancy(self, selector):
        loader = ItemLoader(
            item=SuperjobItem(),
            selector=selector
        )

        loader.add_css(
            field_name='title',
            css='h1::text'
        )
        loader.add_css(
            field_name='salary',
            css = 'div h1 + span span:nth-of-type(1)::text'
        )
        loader.add_css(
            field_name='company',
            css = '._2rWHL._38Lv-._2A9ce._3L1uo::text'
        )
        loader.add_css(
            field_name='description',
            css = '.mrLsm.z4SA9._38Lv-._2A9ce._3L1uo._2h7Xb span *::text'
        )
        loader.add_value(
            field_name='url',
            value=selector.xpath('./@href').get()
        )

        yield loader.load_item()


