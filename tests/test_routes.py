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
#  T E S T   C A S E S   F O R   I N V E N T O R Y   S E R V I C E
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
    # T E S T   C A S E S
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], "Inventory REST API Service")
        self.assertIn("version", data)
        self.assertIn("endpoints", data)
        self.assertIn("POST  ", data["endpoints"])
        self.assertIn("PUT   ", data["endpoints"])
        self.assertIn("GET   ", data["endpoints"])
        self.assertIn("DELETE", data["endpoints"])

    def test_create_item(self):
        """It should Create a new item"""
        test_item = InventoryFactory()
        logging.debug("Test Item: %s", test_item.serialize())
        response = self.client.post(BASE_URL, json=test_item.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_item = response.get_json()
        self.assertEqual(new_item["name"], test_item.name)
        self.assertEqual(new_item["condition"], test_item.condition.name)
        self.assertEqual(new_item["quantity"], test_item.quantity)
        self.assertEqual(new_item["restock_level"], test_item.restock_level)

    def test_get_item(self):
        """It should Get a single item"""
        # get the id of a inventory
        test_item = self._create_items(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_item.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_item.name)
        self.assertEqual(data["condition"], test_item.condition.name)
        self.assertEqual(data["quantity"], test_item.quantity)
        self.assertEqual(data["restock_level"], test_item.restock_level)
    
    def test_get_item_not_found(self):
        """It should not Get an item thats not found"""
        # get the id of a inventory
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])
        
    def test_delete_item(self):
        """It should Delete a inventory that is present in the database"""
        test_inventory = self._create_items(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        # make sure they are deleted
        response = self.client.get(f"{BASE_URL}/{test_inventory.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item_not_found(self):
        """ It should return a 204 on deleting an item that is not present in the database""" 
        # make sure item is not present in the database
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # Delete an item that is missing from the database
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(response.data), 0)
        logging.debug("Item with id %s does not exist. Delete returned 204 NO CONTENT")
        

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

    def test_update_inventory_no_id(self):
        """It should return a 404 Not Found Error if the id does not exist on updating inventory"""
        # No new inventory item has been created
        test_item = {'id': 34}
        logging.debug(test_item)
        response = self.client.put(f"{BASE_URL}/{test_item['id']}", json=test_item)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_inventory_malformed_request(self):
        """It should return a 400 Bad Request if the data is malformed"""
        # Inventory item has incorrect data
        # Create an inventory item
        test_item = InventoryFactory()
        logging.debug("Test Inventory Item: %s", test_item.serialize())
        response = self.client.post(BASE_URL, json=test_item.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Update an inventory item
        test_item = response.get_json()
        logging.debug("Received Test Inventory Item: %s", test_item)
        test_item["quantity"] = 10005
        # Removing the restock level which will create malformed request
        del test_item["restock_level"]
        response = self.client.put(f"{BASE_URL}/{test_item['id']}", json=test_item)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
