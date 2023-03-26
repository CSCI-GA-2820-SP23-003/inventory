"""
Models for Inventory

All of the models are stored in this module

Models
------
Inventory - An Inventory item used in the Inventory

Attributes:
-----------
name (string) - the name of the Inventory item
condition (string) - the condition of the Inventory item
quantity (number) - the quantity of the Inventory item
restock_level (number) - the restock level of the Inventory item

"""
import logging
from enum import Enum
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """ Initializes the SQLAlchemy app """
    Inventory.init_db(app)


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """


class Condition(Enum):
    """Enumeration of valid Inventory item conditions"""

    NEW = 0
    OPEN_BOX = 1
    USED = 2


def updated_at_default(context):
    """ Initializes the created_at time """
    return context.get_current_parameters()["created_at"]


class Inventory(db.Model):
    """
    Class that represents a Inventory
    """

    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    condition = db.Column(db.Enum(Condition), nullable=False, server_default=(Condition.NEW.name))
    quantity = db.Column(db.Integer, nullable=False)
    restock_level = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=updated_at_default, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Inventory item: id={self.id}, name={self.name}, condition={self.condition}>"

    def create(self):
        """
        Creates an Inventory item to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        # Disregard created_at and updated_at if provided
        self.created_at = None
        self.updated_at = None
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates an Inventory item in the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        """ Removes an Inventory item from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes an Inventory item into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "condition": self.condition.name,
            "quantity": self.quantity,
            "restock_level": self.restock_level
            }

    def deserialize(self, data):
        """
        Deserializes an Inventory item from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.condition = getattr(Condition, data["condition"])
            if isinstance(data["quantity"], int):
                self.quantity = data["quantity"]
            else:
                raise DataValidationError(
                    "Invalid type for int [quantity]: "
                    + str(type(data["quantity"]))
                )
            if isinstance(data["restock_level"], int):
                self.restock_level = data["restock_level"]
            else:
                raise DataValidationError(
                    "Invalid type for int [restock_level]: "
                    + str(type(data["restock_level"]))
                )

        except AttributeError as error:
            raise DataValidationError(
                "Invalid attribute: " + error.args[0]
            ) from error
        except KeyError as error:
            raise DataValidationError(
                "Invalid Inventory item: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid Inventory item: body of request contained bad or no data - "
                "Error message: " + str(error)
            ) from error
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Inventory items in the database """
        logger.info("Processing all Inventory items")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds an Inventory item by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all Inventory items with the given name

        Args:
            name (string): the name of the Inventory item you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)
