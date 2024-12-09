# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders import Identity
from itemloaders.processors import TakeFirst, Join, MapCompose, Compose


def parse_salary(text):
    salary = {}
    if len(text) == 1:
        return salary
    if text[0] in ('от','до'):
        salary['currency'] = text[-1][-1]
    if text[0] == 'от':
        salary['min'] = str_to_int(text[-1][:-1])
    elif text[0] == 'до':
        salary['max'] = str_to_int(text[-1][:-1])
    else :
        salary['min'] = str_to_int(text[0])
        salary['currency'] = text[-1]
        if len(text) != 3:
            salary['max'] = str_to_int(text[4])
        else:
            salary['max'] = str_to_int(text[0])
    return salary

def str_to_int(s):
    return int(s.replace('\xa0', ''))

class SuperjobItem(scrapy.Item):
    title = scrapy.Field(
        output_processor = TakeFirst()
    )
    url = scrapy.Field()
    address = scrapy.Field(
        output_processor = Join()
    )
    company = scrapy.Field(
        output_processor = TakeFirst()
    )
    salary = scrapy.Field(
        input_processor = Compose(parse_salary),
        output_processor = TakeFirst()
    )
    description = scrapy.Field(
        output_processor = Join()
    )
