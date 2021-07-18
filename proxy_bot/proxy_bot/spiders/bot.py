from scrapy.spiders import CrawlSpider
from scrapy import Request
from scrapy.utils.project import get_project_settings
from ..items import ProxyBotItem

class ProxyBot(CrawlSpider):
    name = 'hunter'

    # start_urls = ['https://www.sslproxies.org/']

    def __init__(self):
        self.filepath = get_project_settings().get('FILE_PATH')

    def start_requests(self):
        self.logger.info('----------------------------------------------')
        return [Request('https://www.sslproxies.org/', callback=self.parse)]

    def parse(self, response, **kwargs):
        self.logger.info('+++++++++++++++++++++++++++++++++++++++++++++++++')
        table = response.css('table#proxylisttable>tbody')
        for tr in table.css('tr'):
            item = ProxyBotItem()
            item['ip'] = tr.css('td:nth-child(1)::text').get()
            item['port'] = tr.css('td:nth-child(2)::text').get()
            yield item
