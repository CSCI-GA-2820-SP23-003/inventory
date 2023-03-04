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


######################################################################
#  T E S T   C A S E S   F O R   I N V E N T O R Y   S E R V I C E
######################################################################
class TestInventoryServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """

    ######################################################################
    # T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_item(self):
        """It should Update an existing item"""
        # Create an inventory item
        test_item = InventoryFactory()
        logging.debug("Test Inventory Item: %s", test_item.serialize())
        response = self.client.post(BASE_URL, json=test_item.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update an inventory item
        new_item = response.get_json()
        logging.debug("Received Test Inventory Item: %s", new_item)
        new_item["quantity"] = 10005
        response = self.client.put(f"{BASE_URL}/{new_item['id']}", json=new_item)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_item = response.get_json()
        self.assertEqual(new_item["quantity"], updated_item["quantity"])



    ######################################################################
    #  T E S T   S A D   P A T H S
    ######################################################################

    def test_update_inventory_no_id(self):
        """It should return a 404 Not Found Error if the id does not exist on updating inventory"""
        # No new inventory item has been created
        test_item = {'id': 34}
        logging.debug(test_item)
        response = self.client.put(f"{BASE_URL}/{test_item['id']}", json=test_item)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)