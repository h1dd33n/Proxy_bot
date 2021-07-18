import requests_mock
import pytest
from requests import request
from ..spiders import ProxyBot


@pytest.fixture()
def spider():
    return ProxyBot()


@pytest.mark.parametrize()
def test_parse(spider, url , response, status):
    result = next(spider.parse(response))
    assert result.status == status

# def test_response():
#     with requests_mock.Mocker(real_http=True) as m:
#         m.request('GET', 'https://www.sslproxies.org/', status_code=200)
#         request('GET', 'https://www.sslproxies.org/').status_code
