import pytest
import requests
import json
from requests.exceptions import HTTPError

@pytest.fixture(scope='module')
def fxtr_currency_rates():
    mb_url = "http://localhost:2525"
    imposter_port = 4545
    
    # Удаляю старый импостер, если он существует
    try:
        requests.delete(f"{mb_url}/imposters/{imposter_port}")
    except:
        pass
    
    # Создаю новый импостер
    with open("imposter.json") as f:
        imposter_cfg = json.load(f)

    requests.post(f"{mb_url}/imposters",
                  json=imposter_cfg,
                  headers={"Content-Type": "application/json"})

    yield
    
    # Удаляю импостер после завершения тестов
    try:
        requests.delete(f"{mb_url}/imposters/{imposter_port}")
    except:
        pass

def get_exchange_rate(base_url, from_currency, to_currency):
    response = requests.get(f"{base_url}/rate", params={
        "from": from_currency,
        "to": to_currency
    })
    response.raise_for_status()
    return response.json()["rate"]

@pytest.mark.usefixtures("fxtr_currency_rates")
@pytest.mark.parametrize("from_curr,to_curr,expected_rate", [
    ("USD", "EUR", 0.91),
    ("EUR", "USD", 1.10),
    ("EUR", "RUB", 95.04),
    ("USD", "RUB", 86.17),
    ("RUB", "EUR", 0.01),
    ("RUB", "USD", 0.012),
    ("EUR", "CHF", 0.93),
    ("CHF", "EUR", 1.08),
])

def test_currency_rat(from_curr, to_curr, expected_rate):
    rate = get_exchange_rate("http://localhost:4545", from_curr, to_curr)
    assert rate == expected_rate


def test_invalid_currency():
    with pytest.raises(HTTPError) as ex:
        get_exchange_rate("http://localhost:4545", "XYZ", "ABC")

    response = ex.value.response
    assert 400 <= response.status_code < 500

