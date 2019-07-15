# -*- coding: utf-8 -*-
import pytest

from short_url.core import encode


def test_encode():
    assert encode(0) == '0'
    assert encode(63) == '11'


@pytest.mark.parametrize("data", ({'url': 'http://www.baidu.com?id1234&name=张三&title=多吃水果有益健康'},))
def test_main(test_app, client, data):
    response = client.post('/shorten', json=data)

    assert response.status_code == 200
    assert response.json != ''

    response_1 = client.post('/expand', json={'url': response.json})

    assert response_1.status_code == 200
    assert response_1.json == data['url']
