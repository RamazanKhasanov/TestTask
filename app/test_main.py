from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_calc_deposit():
    response = client.post('/deposit',
                           json={"date": "29.01.2021",
                                 "periods": 3,
                                 "amount": 10000,
                                 "rate": 6}
                           )
    assert response.status_code == 200
    assert response.json() == {
        "29.01.2021": 10050,
        "28.02.2021": 10100.25,
        "29.03.2021": 10150.75
    }


def test_calc_deposit_end_month():
    response = client.post('/deposit',
                           json={"date": "31.10.2022",
                                 "periods": 6,
                                 "amount": 250000,
                                 "rate": 8}
                           )
    assert response.status_code == 200
    assert response.json() == {
        "31.10.2022": 251666.67,
        "30.11.2022": 253344.44,
        "31.12.2022": 255033.41,
        "31.01.2023": 256733.63,
        "28.02.2023": 258445.19,
        "31.03.2023": 260168.16
    }


def test_validation_data_date():
    response = client.post('/deposit',
                           json={"date": 123456,
                                 "periods": 3,
                                 "amount": 10000,
                                 "rate": 6}
                           )
    assert response.status_code == 400
    assert response.json() == {
        "error": "Неверно введенная дата заявки"
    }


def test_validation_data_periods():
    response = client.post('/deposit',
                           json={"date": "29.01.2021",
                                 "periods": 5000,
                                 "amount": 10000,
                                 "rate": 6}
                           )
    assert response.status_code == 400
    assert response.json() == {
        "error": "Неверно введенные данные"
    }


def test_validation_data_amount():
    response = client.post('/deposit',
                           json={"date": "29.01.2021",
                                 "periods": 3,
                                 "amount": 50000000,
                                 "rate": 6}
                           )
    assert response.status_code == 400
    assert response.json() == {
        "error": "Неверно введенные данные"
    }


def test_validation_data_rate():
    response = client.post('/deposit',
                           json={"date": "29.01.2021",
                                 "periods": 3,
                                 "amount": 10000,
                                 "rate": 3000}
                           )
    assert response.status_code == 400
    assert response.json() == {
        "error": "Неверно введенные данные"
    }
