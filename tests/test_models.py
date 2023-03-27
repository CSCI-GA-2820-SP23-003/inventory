"""
Test cases for Inventory Model

"""
import os
import logging
import unittest
from datetime import datetime
from service.models import Inventory, Condition, DataValidationError, db
from service import app
from tests.factories import InventoryFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  YourResourceModel   M O D E L   T E S T   C A S E S
######################################################################
class TestInventoryModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Inventory.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Inventory).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_an_inventory_item(self):
        """It should Create an Inventory item and assert that it exists"""
        item = Inventory(
            name="Nike shoes", condition=Condition.NEW,
            quantity=5, restock_level=1
        )
        self.assertEqual(
            str(item), "<Inventory item: id=None, name=Nike shoes,"
            " condition=Condition.NEW>")
        self.assertTrue(item is not None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.name, "Nike shoes")
        self.assertEqual(item.condition, Condition.NEW)
        self.assertEqual(item.quantity, 5)
        self.assertEqual(item.restock_level, 1)

    def test_add_an_inventory_item(self):
        """It should Create an Inventory item and add it to the database"""
        curr_time = datetime.utcnow()
        items = Inventory.all()
        self.assertEqual(items, [])
        item = Inventory(
            name="Nike shoes", condition=Condition.NEW, quantity=5,
            restock_level=1, created_at=curr_time, updated_at=curr_time
        )
        self.assertTrue(item is not None)
        self.assertEqual(item.id, None)
        item.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(item.id)
        items = Inventory.all()
        self.assertEqual(len(items), 1)
        # Assert that the DB generates its own timestamps instead of taking input
        self.assertNotEqual(curr_time, items[0].created_at)
        self.assertNotEqual(curr_time, items[0].updated_at)
        self.assertEqual(items[0].created_at, items[0].updated_at)

    def test_add_an_inventory_item_default_values(self):
        """
        It should Create an Inventory item and add it to the database
        using default values wherever they are not provided
        """
        item = Inventory(name="Nike shoes", quantity=5, restock_level=1)
        self.assertTrue(item is not None)
        self.assertEqual(item.id, None)
        item.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(item.id)
        items = Inventory.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].condition, Condition.NEW)
        self.assertIsNotNone(items[0].created_at)
        self.assertIsNotNone(items[0].updated_at)
        self.assertEqual(items[0].created_at, items[0].updated_at)

    def test_read_an_inventory_item(self):
        """It should Read an Inventory item"""
        item = InventoryFactory()
        logging.debug(item)
        item.id = None
        item.create()
        self.assertIsNotNone(item.id)
        # Fetch it back
        found_item = Inventory.find(item.id)
        self.assertEqual(found_item.id, item.id)
        self.assertEqual(found_item.name, item.name)
        self.assertEqual(found_item.condition, item.condition)
        self.assertEqual(found_item.quantity, item.quantity)
        self.assertEqual(found_item.restock_level, item.restock_level)
        self.assertEqual(found_item.created_at, item.created_at)
        self.assertEqual(found_item.updated_at, item.updated_at)

    def test_update_an_inventory_item(self):
        """It should Update an Inventory item"""
        item = InventoryFactory()
        logging.debug(item)
        print(item.updated_at)
        item.id = None
        item.create()
        logging.debug(item)
        self.assertIsNotNone(item.id)
        # Change it an save it
        item.quantity = 25
        original_id = item.id
        item.update()
        self.assertEqual(item.id, original_id)
        self.assertEqual(item.quantity, 25)
        self.assertGreater(item.updated_at, item.created_at)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        items = Inventory.all()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].id, original_id)
        self.assertEqual(items[0].quantity, 25)
        self.assertGreater(items[0].updated_at, items[0].created_at)

    def test_update_no_id(self):
        """It should not Update an Inventory item with no id"""
        item = InventoryFactory()
        logging.debug(item)
        item.id = None
        self.assertRaises(DataValidationError, item.update)

    def test_update_field_updated_at(self):
        """It should not Update the updated_at field with the value given"""
        item = InventoryFactory()
        logging.debug(item)
        item.updated_at = datetime(2023, 1, 1, 0, 0, 1)
        item.update()
        self.assertNotEqual(item.updated_at, datetime(2023, 1, 1, 0, 0, 1))

    def test_delete_an_inventory_item(self):
        """It should Delete an Inventory item"""
        item = InventoryFactory()
        item.create()
        self.assertEqual(len(Inventory.all()), 1)
        # delete the Inventory item and make sure it isn't in the database
        item.delete()
        self.assertEqual(len(Inventory.all()), 0)

    def test_list_all_inventory_items(self):
        """It should List all Inventory items in the database"""
        items = Inventory.all()
        self.assertEqual(items, [])
        # Create 5 Inventory items
        for _ in range(5):
            item = InventoryFactory()
            item.create()
        # See if we get back 5 Inventory items
        items = Inventory.all()
        self.assertEqual(len(items), 5)

    def test_serialize_an_inventory_item(self):
        """It should serialize an Inventory item"""
        item = InventoryFactory()
        data = item.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], item.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], item.name)
        self.assertIn("condition", data)
        self.assertEqual(data["condition"], item.condition.name)
        self.assertIn("quantity", data)
        self.assertEqual(data["quantity"], item.quantity)
        self.assertIn("restock_level", data)
        self.assertEqual(data["restock_level"], item.restock_level)

    def test_deserialize_an_inventory_item(self):
        """It should de-serialize an Inventory item"""
        data = InventoryFactory().serialize()
        item = Inventory()
        item.deserialize(data)
        self.assertNotEqual(item, None)
        self.assertEqual(item.id, None)
        self.assertEqual(item.name, data["name"])
        self.assertEqual(item.condition.name, data["condition"])
        self.assertEqual(item.quantity, data["quantity"])
        self.assertEqual(item.restock_level, data["restock_level"])

    def test_deserialize_missing_data(self):
        """It should not deserialize an Inventory item with missing data"""
        data = {
            "id": 1, "name": "Adidas T-Shirt",
            "condition": Condition.OPEN_BOX,
            "quantity": 50
        }
        item = Inventory()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        item = Inventory()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_bad_value_type(self):
        """It should not deserialize a bad value type"""
        test_item = InventoryFactory()
        data = test_item.serialize()
        data["quantity"] = "100"
        item = Inventory()
        self.assertRaises(DataValidationError, item.deserialize, data)
        data["quantity"] = 100
        assert item.deserialize(data)
        data["restock_level"] = "5"
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_bad_condition(self):
        """It should not deserialize a bad condition attribute"""
        test_item = InventoryFactory()
        data = test_item.serialize()
        data["condition"] = "damaged"
        item = Inventory()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_find_inventory_item(self):
        """It should Find an Inventory item by ID"""
        items = InventoryFactory.create_batch(5)
        for item in items:
            item.create()
        logging.debug(items)
        # make sure they got saved
        self.assertEqual(len(Inventory.all()), 5)
        # find the 2nd Inventory item in the list
        item = Inventory.find(items[1].id)
        self.assertIsNot(item, None)
        self.assertEqual(item.id, items[1].id)
        self.assertEqual(item.name, items[1].name)
        self.assertEqual(item.condition, items[1].condition)
        self.assertEqual(item.quantity, items[1].quantity)
        self.assertEqual(item.restock_level, items[1].restock_level)
        self.assertEqual(item.created_at, items[1].created_at)
        self.assertEqual(item.updated_at, items[1].updated_at)

    def test_find_by_name(self):
        """It should Find Inventory items by name"""
        items = InventoryFactory.create_batch(10)
        for item in items:
            item.create()
        name = items[0].name
        count = len([item for item in items if item.name == name])
        found = Inventory.find_by_name(name)
        self.assertEqual(found.count(), count)
        for item in found:
            self.assertEqual(item.name, name)

    def test_find_by_condition(self):
        """It should find Inventory items by condition"""
        items = InventoryFactory.create_batch(10)
        for item in items:
            item.create()
        condition = items[0].condition
        count = len([item for item in items if item.condition == condition])
        found = Inventory.find_by_condition(condition)
        self.assertEqual(found.count(), count)
        for item in found:
            self.assertEqual(item.condition, condition)

    def test_find_by_bad_condition(self):
        """It should not query Inventory items by a bad condition"""
        items = InventoryFactory.create_batch(10)
        for item in items:
            item.create()
        condition = "damaged"
        self.assertRaises(DataValidationError, Inventory.find_by_condition, condition)
