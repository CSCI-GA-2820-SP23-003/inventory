"""
Inventory Service

Service is used to manage products in the inventory.
"""

from flask import Flask, jsonify, request, url_for, make_response, abort
from service.common import status  # HTTP Status Codes
from service.models import Inventory

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
#  R E S T   A P I   E N D P O I N T S
######################################################################


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

    return item.serialize(), status.HTTP_200_OK
