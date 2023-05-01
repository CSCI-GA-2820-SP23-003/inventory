"""
Inventory Steps

Steps file for inventory.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given
from compare import expect


@given('the following inventory items')
def step_impl(context):
    """ Delete all items and load new ones """
    # List all of the items and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/api/inventory"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for inventory in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{inventory['id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new items
    for row in context.table:
        payload = {
            "name": row['name'],
            "condition": row['condition'],
            "quantity": int(row['quantity']),
            "restock_level": int(row['restock_level'])
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)
