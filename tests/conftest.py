# -*- coding: utf-8 -*-
import pytest

from wsgi import app


@pytest.fixture(scope='function')
def test_app():

    yield app


@pytest.fixture(scope='function')
def client():
    testing_client = app.test_client()

    yield testing_client
