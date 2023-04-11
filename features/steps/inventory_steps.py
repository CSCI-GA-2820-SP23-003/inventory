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
    rest_endpoint = f"{context.BASE_URL}/inventory"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for inventory in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{inventory['id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new items
    for row in context.table:
        payload = {
            "id": row['id'],
            "name": row['name'],
            "condition": row['condition'],
            "quantity": row['quantity'],
            "restock_level": row['restock_level'],
            "created_at": row['created_at'],
            "updated_at": row['updated_at']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)
