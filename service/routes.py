"""
Inventory Service

Service is used to manage products in the inventory.
"""

# pylint: disable=cyclic-import, import-error
from flask import jsonify, request, url_for, abort
from service.common import status  # HTTP Status Codes
from service.models import Inventory, DataValidationError

# Import Flask application
from . import app


############################################################
# Health Endpoint
############################################################
@app.route("/health", methods=["GET"])
def health():
    """Health Status"""
    app.logger.info("Request to check health of Kubernetes cluster")
    return {"status": 'OK'}, status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    path = url_for('create_inventory_item', _external=True)
    return (
        jsonify(
            name="Inventory REST API Service",
            version="1.0",
            paths=path,
            endpoints={
                "DELETE /inventory/<id>": "Delete an inventory by <id>",
                "POST   /inventory     ": "Create an inventory",
                "PUT    /inventory/<id>": "Update an inventory by <id>",
                "GET    /inventory/<id>": "Read an inventory by <id>",
                "GET    /inventory     ": "List entire inventory",
            },
            usage=f"<endpoints> {path}[/id]"
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################

######################################################################
# ADD A NEW INVENTORY ITEM
######################################################################
@app.route("/inventory", methods=["POST"])
def create_inventory_item():  # Replace entry with item
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
    location_url = url_for("get_inventory", inventory_id=item.id, _external=True)

    app.logger.info("Inventory item named [%s] with ID [%s] created.", item.name, item.id)
    return jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}


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
#  UPDATE AN INVENTORY ITEM
######################################################################

@app.route("/inventory/<int:inventory_id>", methods=["PUT"])
def update_inventory(inventory_id):
    """
    Updating an inventory item

    This endpoint will update an item based on the data in the body that is posted
    """

    app.logger.info("Request to update an inventory item with inventory_id:%s", inventory_id)
    check_content_type("application/json")
    item = Inventory.find(inventory_id)
    if not item:
        abort(status.HTTP_404_NOT_FOUND, "Item with inventory_id:%s not found", inventory_id)
    try:
        item.deserialize(request.get_json())
        item.id = inventory_id
        item.update()
    except DataValidationError:
        abort(status.HTTP_400_BAD_REQUEST, "Malformed request")

    return jsonify(item.serialize()), status.HTTP_200_OK


######################################################################
# DELETE AN INVENTORY ITEM
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

    else:
        app.logger.info("Inventory with ID [%s] does not exist", inventory_id)

    return "", status.HTTP_204_NO_CONTENT


######################################################################
# LIST ALL INVENTORY ITEMS
######################################################################
@app.route("/inventory", methods=["GET"])
def list_inventory_items():
    """
    List all inventory items

    This endpoint will list all inventory items in the database
    """
    app.logger.info("Request to list all inventory items")
    items = []
    condition = request.args.get("condition")
    restock = request.args.get("restock")
    quantity = request.args.get("quantity")
    if condition:
        items = Inventory.find_by_condition(condition)
    elif restock:
        items = Inventory.find_by_restock_level(restock)
    elif quantity is not None: 
        # The case where quantity query is an empty string is handled in models.py
        items = Inventory.find_by_quantity(quantity)
    else:
        items = Inventory.all()
    results = [item.serialize() for item in items]
    app.logger.info("Returning %d inventory items", len(results))
    return jsonify(results), status.HTTP_200_OK


######################################################################
# RESTOCK AN INVENTORY ITEM
######################################################################

@app.route("/inventory/<int:inventory_id>/restock", methods=["PUT"])
def restock_inventory(inventory_id):
    """
    Restock an existing inventory item

    This is an Action as URL that will perform an restock to an existing
    inventory item in the database
    """
    app.logger.info("Request to restock an inventory item with inventory_id:%s", inventory_id)
    item = Inventory.find(inventory_id)
    if not item:
        abort(status.HTTP_404_NOT_FOUND, "Item with inventory_id:%s was not found", inventory_id)
    if item.quantity > item.restock_level:
        abort(
            status.HTTP_409_CONFLICT,
            "Item with inventory_id:%s is already above the restock level",
            inventory_id
        )
    else:
        item.quantity = item.restock_level + 1
        item.id = inventory_id
        item.update()

    return jsonify(item.serialize()), status.HTTP_200_OK


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
