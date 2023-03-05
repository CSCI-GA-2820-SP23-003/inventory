"""
TestInventory API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import db, init_db, Inventory, Condition
from tests.factories import InventoryFactory
from service.common import status  # HTTP Status Codes

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/inventory"

######################################################################
#  T E S T   C A S E S
######################################################################
class TestInventoryServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()
        self.client = app.test_client()
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_items(self, count):
        """Factory method to create inventory items in bulk"""
        items = []
        for _ in range(count):
            test_item = InventoryFactory()
            response = self.client.post(BASE_URL, json=test_item.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test item"
            )
            new_item = response.get_json()
            test_item.id = new_item["id"]
            items.append(test_item)
        return items

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_create_item(self):
        """It should Create a new item"""
        test_item = InventoryFactory()
        logging.debug("Test Item: %s", test_item.serialize())
        response = self.client.post(BASE_URL, json=test_item.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the data is correct
        new_item = response.get_json()
        self.assertEqual(new_item["name"], test_item.name)
        self.assertEqual(new_item["condition"], test_item.condition.name)
        self.assertEqual(new_item["quantity"], test_item.quantity)
        self.assertEqual(new_item["restock_level"], test_item.restock_level)

    ######################################################################
    #  T E S T   S A D   P A T H S
    ######################################################################

    def test_create_item_no_data(self):
        """It should not Create an item with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_item_no_content_type(self):
        """It should not Create an item with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_item_wrong_content_type(self):
        """It should not Create an item with wrong content type"""
        response = self.client.post(BASE_URL, content_type = "text/html")
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_create_item_bad_restock_level(self):
        """It should not Create an item with bad restock_level data"""
        test_item = InventoryFactory()
        logging.debug(test_item)
        # change restock_level to an unknown value
        test_item.restock_level = "true"
        response = self.client.post(BASE_URL, json=test_item.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_inventory_bad_quantity(self):
        """It should not Create an item with bad quantity data"""
        item = InventoryFactory()
        logging.debug(item)
        # change quantity to a bad string
        test_item = item.serialize()
        test_item["quantity"] = "male"    # wrong case
        response = self.client.post(BASE_URL, json=test_item)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)