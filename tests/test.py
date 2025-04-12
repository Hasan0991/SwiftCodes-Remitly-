import pytest
from app import app
import json

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_create_swift_code(client):

    payload = {
        "swiftCode": "XYZ1341211",
        "bankName": "Test Bank",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "123 Test St.",
        "isHeadquarter": True
    }
    response = client.post('/v1/swift_codes', json=payload)
    assert response.status_code == 201
    assert response.json['message'] == "SWIFT code XYZ1341211 added successfully."
    client.delete('/v1/swift_codes/XYZ1341211')

def test_create_swift_code_for_invalid_data(client):

    payload = {
        "swiftCode": "XYZ1236",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "123 Test St.",
        "isHeadquarter": True
    }
    response = client.post('/v1/swift_codes', json=payload)
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

    client.post('/v1/swift_codes', json=payload)


    response = client.post('/v1/swift_codes', json=payload)
    assert response.status_code == 409
    assert response.json['message'] == "SWIFT code XYZ1234 already exists."


def test_get_swift_codes(client):
    response = client.get('/v1/swift_codes')

    assert response.status_code == 200


    assert isinstance(response.json, list)

def test_delete_swift_code(client):
    payload = {
        "swiftCode": "XYZ12342",
        "bankName": "Test Bank",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "123 Test St.",
        "isHeadquarter": True
    }
    response = client.post('/v1/swift_codes', json=payload)
    assert response.status_code == 201
    response = client.get(f'/v1/swift_codes/{payload["swiftCode"]}')
    assert response.status_code == 200
    response = client.delete(f'/v1/swift_codes/{payload["swiftCode"]}')
    assert response.status_code == 200
    assert f"SWIFT code {payload["swiftCode"]} deleted successfully" in response.json['message']

def test_delete_swift_code_not_exist(client):
    payload = {
        "swiftCode": "XYZ1212342",
        "bankName": "Test Bank",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "123 Test St.",
        "isHeadquarter": True
    }

    response = client.delete(f'/v1/swift_codes/{payload["swiftCode"]}')
    assert response.status_code == 404
    assert f"SWIFT code {payload["swiftCode"]} not found" in response.json['message']
def test_update_swift_code(client):
    payload = {
        "swiftCode": "XYZ123401",
        "bankName": "Test Bank",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "123 Test St.",
        "isHeadquarter": True
    }
    payload2 = {
        "swiftCode": "XYZ123401",
        "bankName": "Test Bank",
        "countryISO2": "US",
        "countryName": "United States",
        "address": "Latif Imanov365.",
        "isHeadquarter": True
    }
    response = client.post('/v1/swift_codes', json=payload)
    assert response.status_code == 201
    response = client.put(f'/v1/swift_codes/{payload["swiftCode"]}',json=payload2)
    assert response.status_code == 200
    assert f"SWIFT code updated" in response.json['message']
    get_response = client.get(f'/v1/swift_codes/{payload["swiftCode"]}')
    assert get_response.status_code == 200
    assert get_response.json['address'] == "Latif Imanov365."
    client.delete("/v1/swift_codes/XYZ123401")
