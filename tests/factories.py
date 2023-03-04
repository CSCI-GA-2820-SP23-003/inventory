"""
Test Factory to make fake objects for testing
"""

import csv
import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from service.models import Inventory, Condition

MIN_NAME_LENGTH = 1
MAX_NAME_LENGTH = 63

INVENTORY_ITEM_NAMES = []

with open('tests/fixtures/inventory_item_names.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        item_name = row["PRODUCT_NAME"]
        if MIN_NAME_LENGTH <= len(item_name) <= MAX_NAME_LENGTH:
            INVENTORY_ITEM_NAMES.append(item_name)

class InventoryFactory(factory.Factory):
    """Creates fake pets that you don't have to feed"""

    class Meta: # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Inventory

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=INVENTORY_ITEM_NAMES)
    condition = FuzzyChoice(choices=[Condition.NEW, Condition.OPEN_BOX, Condition.USED])
    quantity = FuzzyInteger(10000)
    restock_level = FuzzyInteger(10)