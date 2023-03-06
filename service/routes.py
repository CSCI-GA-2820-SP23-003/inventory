"""
Inventory Service

Service is used to manage products in the inventory.
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import Inventory, DataValidationError

# Import Flask application
from . import app


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
        status.HTTP_200_OK,
    )


######################################################################
# RETRIEVE AN INVENTORY ITEM
######################################################################
@app.route("/inventory/<int:inventory_id>", methods=["GET"])
def get_inventory(inventory_id):
    """
    Retrieve a single Inventory

    This endpoint will return a Inventory based on it's id
    """
    app.logger.info("Request for item with id: %s", inventory_id)
    inventory = Inventory.find(inventory_id)
    if not inventory:
        abort(status.HTTP_404_NOT_FOUND, f"Inventory with id '{inventory_id}' was not found.")

    app.logger.info("Returning item: %s", inventory.name)
    return jsonify(inventory.serialize()), status.HTTP_200_OK


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

######################################################################
# ADD A NEW INVENTORY ENTRY
######################################################################
@app.route("/inventory", methods=["POST"])
def create_inventory_item():#Replace entry with item
    """
    Creates an inventory item
    This endpoint will create an item based on the data in the body that is posted
    """
    app.logger.info("Request to create an inventory item")
    check_content_type("application/json")
    item = Inventory()
    item.deserialize(request.get_json())
    item.create()
    message = item.serialize()

    app.logger.info("Inventory item named [%s] with ID [%s] created.", item.name, item.id)
    return jsonify(message), status.HTTP_201_CREATED

######################################################################
#  UPDATE AN INVENTORY ITEM
######################################################################

@app.route("/inventory/<int:id>", methods=["PUT"])
def update_inventory(id):
    """
    Updating an inventory item
    This endpoint will update an item based on the data in the body that is posted
    """

    app.logger.info("Requesr to update an inventory item with id:%s", id)
    check_content_type("application/json")
    item = Inventory.find(id)
    if not item:
        abort(status.HTTP_404_NOT_FOUND, "Item with id:%s not found", id)
    try:
        item.deserialize(request.get_json())
        item.id = id
        item.update()
    except DataValidationError as err:
        abort(status.HTTP_400_BAD_REQUEST, "Malformed request")

    return jsonify(item.serialize()), status.HTTP_200_OK
# DELETE AN INVENTORY ENTRY
######################################################################
@app.route("/inventory/<int:inventory_id>", methods=["DELETE"])
def delete_inventory(inventory_id):
    """
    Delete an inventory

    This endpoint will delete an inventory item based the id specified in the path
    """
    app.logger.info("Request to delete inventory with id: %s", inventory_id)
    inventory = Inventory.find(inventory_id)
    if inventory:
        inventory.delete()

    app.logger.info("Inventory with ID [%s] delete complete.", inventory_id)
    return "", status.HTTP_204_NO_CONTENT

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(content_type):
    """Checks that the media type is correct"""
    if "Content-Type" not in request.headers:
        app.logger.error("No Content-Type specified.")
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {content_type}",
        )

    if request.headers["Content-Type"] == content_type:
        return

    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {content_type}",
    )
