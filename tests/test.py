import pytest
from app import app
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_create_swift_code(client):

    payload = {
        "swiftCode": "XYZ1234",
        "bankName": "Test Bank",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "123 Test St.",
        "isHeadquarter": True
    }
    response = client.post('/api/swift_codes', json=payload)
    assert response.status_code == 201
    assert response.json['message'] == "SWIFT code XYZ1234 added successfully."


def test_create_swift_code_for_invalid_data(client):

    payload = {
        "swiftCode": "XYZ1236",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "123 Test St.",
        "isHeadquarter": True
    }
    response = client.post('/api/swift_codes', json=payload)
    assert response.status_code == 400
    assert 'error' in response.json


def test_create_swift_code_already_exist(client):
    payload = {
        "swiftCode": "XYZ1234",
        "bankName": "Test Bank",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "123 Test St.",
        "isHeadquarter": True
    }

    client.post('/api/swift_codes', json=payload)


    response = client.post('/api/swift_codes', json=payload)
    assert response.status_code == 409
    assert response.json['message'] == "SWIFT code XYZ1234 already exists."


def test_get_swift_codes(client):
    response = client.get('/api/swift_codes')

    assert response.status_code == 200


    assert isinstance(response.json, list)

def test_delete_swift_code(client):
    payload = {
        "swiftCode": "XYZ1234",
        "bankName": "Test Bank",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "123 Test St.",
        "isHeadquarter": True
    }
    response = client.get(f'/api/swift_codes/{payload["swiftCode"]}')
    assert response.status_code == 200
    response = client.delete(f'/api/swift_codes/{payload["swiftCode"]}')
    assert response.status_code == 200
    assert f"SWIFT code {payload['swiftCode']} deleted successfully" in response.json['message']

def test_update_swift_code(client):
    payload = {
        "swiftCode": "XYZ1234",
        "bankName": "Test Bank",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "123 Test St.",
        "isHeadquarter": True
    }
    payload2 = {
        "swiftCode": "XYZ1234",
        "bankName": "Test Bank",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "Latif Imanov365.",
        "isHeadquarter": True
    }
    response = client.put(f'/api/swift_codes/{payload["swiftCode"]}',json=payload2)
    assert response.status_code == 200
    assert f"SWIFT code updated" in response.json['message']
    get_response = client.get(f'/api/swift_codes/{payload["swiftCode"]}')
    assert get_response.status_code == 200
    assert get_response.json['address'] == "Latif Imanov365."
