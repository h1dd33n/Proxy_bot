import requests
import os
from itertools import chain


class ProxyBotPipeline:
    # Check if proxy is valid
    proxy_list = set()

    def _chech_proxy(self, item):
        try:
            ip_port = item['ip'] + ':' + item['port']
            proxy = {'https://': ip_port}
            req = requests.request('GET', 'https://google.com', proxies=proxy,
                                   timeout=(10, 10))
            if req.status_code == 200:
                print(f'{proxy} STATUS_CODE == 200')
                req.close()
                return proxy
            else:
                return False

        except Exception as e:
            print(e)
            return False

    def process_item(self, item, spider):
        spider.logger.info('----------------In Process item----------------')
        proxy = self._chech_proxy(item)
        if proxy:
            proxy = 'https://' + proxy['https://']
            spider.logger.info(f'{proxy}')
            self.proxy_list.add(proxy)
        return proxy

    def close_spider(self, spider):
        spider.logger.info('Spider finishing Job')
        spider.logger.info(f'Converting {len(self.proxy_list)} proxies')
        if os.path.isfile(spider.filepath):
            proxy_list = set(open(spider.filepath))
            new_list = chain(proxy_list, self.proxy_list)
            os.remove(spider.filepath)
            with open(spider.filepath, 'a') as f:
                for i in new_list:
                    spider.logger.info(f'{i}')
                    f.write(i + '\n')
                f.close()
        else:
            with open(spider.filepath, 'a') as f:
                for i in self.proxy_list:
                    f.write(i + '\n')
                f.close()
