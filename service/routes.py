"""
My Service

Describe what your service does here
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
# RETRIEVE A PET
######################################################################
@app.route("/inventory/<int:inventory_id>", methods=["GET"])
def get_pets(inventory_id):
    """
    Retrieve a single Inventory

    This endpoint will return a Inventory based on it's id
    """
    app.logger.info("Request for pet with id: %s", inventory_id)
    inventory = Inventory.find(inventory_id)
    if not inventory:
        abort(status.HTTP_404_NOT_FOUND, f"Inventory with id '{inventory_id}' was not found.")

    app.logger.info("Returning pet: %s", inventory.name)
    return jsonify(inventory.serialize()), status.HTTP_200_OK


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

# Place your REST API code here ...
