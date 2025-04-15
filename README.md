# Swift Code API

This project is a RESTful API developed using Flask that provides CRUD operations for managing SWIFT codes. It uses MySQL as the database backend and is containerized using Docker for easy deployment.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [GET /v1/swift_codes](#get-v1swift_codes)
  - [GET /v1/swift_codes/<swift_code>](#get-v1swift_codesswift_code)
  - [GET /v1/swift_codes/country/<countryISO2code>](#get-v1swift_codescountrycountryiso2code)
  - [POST /v1/swift_codes](#post-v1swift_codes)
  - [PUT /v1/swift_codes/<swift_code>](#put-v1swift_codesswift_code)
  - [DELETE /v1/swift_codes/<swift_code>](#delete-v1swift_codesswift_code)
- [Testing](#testing)
- [Docker Setup](#docker-setup)

## Features

- **CRUD operations**: Create, Read, Update, and Delete SWIFT codes.
- **Validation**: Ensures all fields for SWIFT codes are valid before adding or updating.
- **Error Handling**: Clear and informative error messages for edge cases.
- **Database**: Uses MySQL as the backend to store SWIFT codes.
- **Containerization**: The application and database are both containerized using Docker.

## Installation


### 1. Clone the repository

```bash
git clone https://github.com/yourusername/swift-code-api.git
cd swift-code-api

Set up environment variables (you can create a .env file or set them manually):

    DB_HOST=db
    DB_PORT=3306
    DB_USER=root
    DB_PASSWORD=hasan099
    DB_NAME=swift

Install dependencies (If you're running without Docker, install Flask and MySQL connector):

pip install -r requirements.txt

## API Endpoints



## GET /v1/swift_codes

Retrieve a list of all SWIFT codes in the database.

Response:

[
  {
    "address": "1234 Bank St.",
    "bankName": "Bank A",
    "countryISO2": "US",
    "countryName": "United States",
    "isHeadquarter": true,
    "swiftCode": "US123456"
  },
  ...
]

## GET /v1/swift_codes/<swift_code>

Retrieve details of a specific SWIFT code.

Example Request:

## GET /v1/swift_codes/US123456

Response:

{
  "address": "1234 Bank St.",
  "bankName": "Bank A",
  "countryISO2": "US",
  "countryName": "United States",
  "isHeadquarter": true,
  "swiftCode": "US123456",
  "branches": [
    {
      "address": "5678 Branch St.",
      "bankName": "Bank A",
      "countryISO2": "US",
      "isHeadquarter": false,
      "swiftCode": "US123457"
    }
  ]
}

## POST /v1/swift_codes

Create a new SWIFT code.

Request Body:

{
  "swiftCode": "US123458",
  "bankName": "Bank A",
  "countryISO2": "US",
  "countryName": "United States",
  "address": "1234 Bank St.",
  "isHeadquarter": true
}

Response:

{
  "message": "SWIFT code US123458 added successfully."
}

## PUT /v1/swift_codes/<swift_code>

Update an existing SWIFT code.

Request Body:

{
  "swiftCode": "US123458",
  "bankName": "Bank B",
  "countryISO2": "US",
  "countryName": "United States",
  "address": "9876 New Bank St.",
  "isHeadquarter": true
}

Response:

{
  "message": "SWIFT code US123458 updated successfully."
}

## DELETE /v1/swift_codes/<swift_code>

Delete a specific SWIFT code.

Response:

{
  "message": "SWIFT code US123458 deleted successfully."
}

## GET /v1/swift_codes/country/<countryISO2code>

Retrieve all SWIFT codes for a specific country.

Example Request:

## GET /v1/swift_codes/country/US

Response:

{
  "countryISO2": "US",
  "countryName": "United States",
  "swiftCodes": [
    {
      "swiftCode": "US123456",
      "bankName": "Bank A",
      "address": "1234 Bank St.",
      "isHeadquarter": true
    },
    ...
  ]
}

## Testing

To run tests for the application, you can use pytest to verify that all your endpoints work as expected:

Install pytest:

    pip install pytest

Run tests:

    pytest tests/

## Docker Setup

This project is containerized with Docker to run both the Flask application and MySQL database in isolated environments.
Build the Docker containers:

    docker-compose build

Run the containers:

    docker-compose up

This will start both the Flask app (on port 8080) and the MySQL database (on port 3307).