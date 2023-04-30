"""
Inventory Service

Service is used to manage products in the inventory.
"""

# pylint: disable=cyclic-import, import-error
from flask import request, abort
# pylint: disable=unused-import
from flask_restx import Resource, fields, reqparse  # noqa: F401
from service.common import status  # HTTP Status Codes
from service.models import Inventory, Condition

# Import Flask application
from . import app, api


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
    return app.send_static_file("index.html")


# Define the model so that the docs reflect what can be sent
# pylint: disable=protected-access
create_model = api.model('Inventory', {
    'name': fields.String(required=True,
                          description='The name of the inventory item'),
    'condition': fields.String(required=True, enum=Condition._member_names_,
                               description='The condition of inventory (NEW, OPEN_BOX, USED)'),
    'quantity': fields.Integer(required=True,
                               description='The quantity of an inventory item'),
    'restock_level': fields.Integer(required=True,
                                    description='The restock level of an inventory item'),
})

inventory_model = api.inherit(
    'InventoryModel',
    create_model,
    {
        'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)

# query string arguments
inventory_args = reqparse.RequestParser()
inventory_args.add_argument('name', type=str, location='args', required=False,
                            help='List Inventory Items by Name')
inventory_args.add_argument('condition', type=str, location='args', required=False,
                            help='List Inventory Items by Condition')
inventory_args.add_argument('restock', type=str, location='args', required=False,
                            help='List Inventory Items by Restock Level')
inventory_args.add_argument('quantity', type=str, location='args', required=False,
                            help='List Inventory Items by Quantity')

######################################################################
#  R E S T   A P I   E N D P O I N T S
######################################################################


######################################################################
#  PATH: /inventory/{inventory_id}
######################################################################
@api.route('/inventory/<inventory_id>')
@api.param('inventory_id', 'The Inventory identifier')
class InventoryResource(Resource):
    """
    InventoryResource class

    Allows the manipulation of a single Inventory Item
    GET /inventory/{inventory_id} - Returns an Item with the inventory_id
    PUT /inventory/{inventory_id} - Update an Item with the inventory_id
    DELETE /inventory/{inventory_id} -  Deletes an Item with the inventory_id
    """

    ######################################################################
    # RETRIEVE AN INVENTORY ITEM
    ######################################################################
    @api.doc('get_inventory_items')
    @api.response(404, 'Inventory Item not found')
    @api.marshal_with(inventory_model)
    def get(self, inventory_id):
        """
        Retrieve a single Inventory

        This endpoint will return an Inventory item based on it's id
        """
        app.logger.info("Request for item with id: %s", inventory_id)
        inventory = Inventory.find(inventory_id)
        if not inventory:
            abort(status.HTTP_404_NOT_FOUND, f"Inventory with id '{inventory_id}' was not found.")

        app.logger.info("Returning item: %s", inventory.name)
        return inventory.serialize(), status.HTTP_200_OK

    ######################################################################
    #  UPDATE AN INVENTORY ITEM
    ######################################################################

    @api.doc('update_inventory_items')
    @api.response(404, 'Inventory item not found')
    @api.response(400, 'The posted Item data was not valid')
    @api.expect(inventory_model)
    @api.marshal_with(inventory_model)
    def put(self, inventory_id):
        """
        Updating an inventory item

        This endpoint will update an item based on the data in the body that is posted
        """

        app.logger.info("Request to update an inventory item with inventory_id:%s", inventory_id)
        item = Inventory.find(inventory_id)
        if not item:
            abort(status.HTTP_404_NOT_FOUND, f"Item with inventory_id: {inventory_id} not found")
        item.deserialize(request.get_json())
        item.id = inventory_id
        item.update()
        return item.serialize(), status.HTTP_200_OK

    ######################################################################
    # DELETE AN INVENTORY ITEM
    ######################################################################

    @api.doc('delete_inventory_items')
    @api.response(204, 'Inventory Item deleted')
    def delete(self, inventory_id):
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

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /inventory
######################################################################
@api.route('/inventory', strict_slashes=False)
class InventoryCollection(Resource):
    """ Handles all interactions with collections of Inventory """
    ######################################################################
    # ADD A NEW INVENTORY ITEM
    ######################################################################
    @api.doc('create_inventory')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(inventory_model, code=201)
    def post(self):
        """
        Creates an inventory item
        This endpoint will create an item based on the data in the body that is posted
        """
        app.logger.info("Request to create an inventory item")
        item = Inventory()
        item.deserialize(api.payload)
        item.create()
        location_url = api.url_for(InventoryResource, inventory_id=item.id, _external=True)
        app.logger.info("Inventory item named [%s] with ID [%s] created.", item.name, item.id)
        return item.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

    ######################################################################
    # LIST ALL INVENTORY ITEMS
    ######################################################################
    @api.doc('list_inventory_items')
    @api.expect(inventory_args, validate=True)
    @api.marshal_list_with(inventory_model)
    def get(self):
        """
        List all inventory items

        This endpoint will list all inventory items in the database
        """
        app.logger.info("Request to list all inventory items")
        items = []
        args = inventory_args.parse_args()
        condition = args["condition"]
        restock = args["restock"]
        quantity = args["quantity"]
        name = args["name"]
        if condition:
            items = Inventory.find_by_condition(condition)
        elif restock:
            items = Inventory.find_by_restock_level(restock)
        elif quantity:
            items = Inventory.find_by_quantity(quantity)
        elif name:
            items = Inventory.find_by_name(name)
        else:
            items = Inventory.all()
        results = [item.serialize() for item in items]
        app.logger.info("Returning %d inventory items", len(results))
        return results, status.HTTP_200_OK

######################################################################
#  PATH: /inventory/{inventory_id}/restock
######################################################################


@api.route('/inventory/<inventory_id>/restock')
@api.param('inventory_id', 'The Inventory Item identifier')
class RestockResource(Resource):
    """ Restock Action on an Inventory Item"""
    ######################################################################
    # RESTOCK AN INVENTORY ITEM
    ######################################################################
    @api.doc('restock_item')
    @api.response(404, 'Inventory Item not found')
    @api.response(409, 'The item quantity is above restock level')
    def put(self, inventory_id):
        """
        Restock an existing inventory item

        This is an Action as URL that will restock an existing
        inventory item in the database
        """
        app.logger.info("Request to restock an inventory item with inventory_id:%s", inventory_id)
        item = Inventory.find(inventory_id)
        if not item:
            abort(status.HTTP_404_NOT_FOUND,
                  f"Item with inventory_id: {inventory_id} was not found")
        if item.quantity > item.restock_level:
            abort(
                status.HTTP_409_CONFLICT,
                f"Item with inventory_id: {inventory_id} is already above the restock level"
            )
        else:
            item.quantity = item.restock_level + 1
            item.id = inventory_id
            item.update()

        return item.serialize(), status.HTTP_200_OK
