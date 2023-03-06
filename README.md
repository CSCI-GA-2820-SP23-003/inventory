# NYU DevOps Inventory Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

## Overview

This repository contains the code for Inventory service. This project helps keep track of the assets in the inventory and allows you to effortlessly monitor your inventory with ease.

## Setup the Inventory Service

To run the inventory service:
* git clone the repo
    ```https://github.com/CSCI-GA-2820-SP23-003/inventory```
* Start the service
    ```hocho start```
* Run unit tests
    ```nosetests```


## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## Inventory APIs

The following segment details out the Inventory Service's CRUD APIs with sample URLs, Request Body, and Responses.

### POST /inventory

Example: `Create – POST  http://localhost:8000/inventory`

Request body:

```json
{
    "name": "TEST_ABC",
    "condition":"NEW",
    "quantity": 69,
    "restock_level": 34
}
```

Response body:

```json
{
    "condition": "NEW",
    "id": 270,
    "name": "TEST_ABC",
    "quantity": 69,
    "restock_level": 34
}
```

### PUT /inventory/[id]

Example: `Update – PUT  http://localhost:8000/inventory/270`

Request body:

```json
{
    "name": "TEST_ABC",
    "condition":"NEW",
    "quantity": 17,
    "restock_level": 34
}
```

Response body:

```json
{
    "condition": "NEW",
    "id": 270,
    "name": "TEST_ABC",
    "quantity": 17,
    "restock_level": 34
}
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
