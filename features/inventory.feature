Feature: The inventory service back-end
    As an Inventory Manager
    I need a RESTful catalog service
    So that I can keep track of all my items

Background:
    Given the following inventory items
        | name         | condition | quantity | restock_level  |
        | cheetos      | NEW       | 12       | 23             |
        | lays         | OPEN_BOX  | 24       | 12             |
        | doritos      | USED      | 12       | 11             |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Inventory RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create an Inventory Item
    When I visit the "home page"
    And I set the "Name" to "TestCreate"
    And I select "New" in the "Condition" dropdown
    And I set the "Quantity" to "10"
    And I set the "Restock Level" to "20"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Quantity" field should be empty
    And the "Restock Level" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "TestCreate" in the "Name" field
    And I should see "New" in the "Condition" dropdown
    And I should see "10" in the "Quantity" field
    And I should see "20" in the "Restock Level" field

Scenario: List all inventory items
    When I visit the "home page"
    And I press the "search" button
    Then I should see the message "Success"
    And I should see "cheetos" in the results
    And I should see "NEW" in the results
    And I should see "lays" in the results
    And I should see "OPEN_BOX" in the results
    And I should see "doritos" in the results
    And I should see "USED" in the results

Scenario: Do not List inventory items which are not present
    When I visit the "home page"
    And I press the "search" button
    Then I should see the message "Success"
    And I should not see "cheezeit" in the results

Scenario: Update an Inventory Item
    When I visit the "home page"
    And I set the "Name" to "cheetos"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "cheetos" in the "Name" field
    And I should see "NEW" in the "Condition" field
    When I change "Name" to "pringles"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "pringles" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "pringles" in the results
    And I should not see "cheetos" in the results

Scenario: Restock an Inventory Item
    When I visit the "home page"
    And I set the "Name" to "TestCreate"
    And I select "New" in the "Condition" dropdown
    And I set the "Quantity" to "10"
    And I set the "Restock Level" to "20"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Quantity" field should be empty
    And the "Restock Level" field should be empty
    When I paste the "Id" field
    And I press the "Restock" button
    Then I should see the message "Success"
    And I should see "TestCreate" in the "Name" field
    And I should see "New" in the "Condition" dropdown
    And I should see "21" in the "Quantity" field
    And I should see "20" in the "Restock Level" field

Scenario: Do not Restock an Inventory Item which is above the restock level
    When I visit the "home page"
    And I set the "Name" to "TestCreate"
    And I select "New" in the "Condition" dropdown
    And I set the "Quantity" to "10"
    And I set the "Restock Level" to "9"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Quantity" field should be empty
    And the "Restock Level" field should be empty
    When I paste the "Id" field
    And I press the "Restock" button
    Then I should not see "Success"
    And I should see the message "already above the restock level"

Scenario: Search for inventory items by Name
    When I visit the "home page"
    And I set the "Name" to "lays"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "lays" in the results
    And I should not see "cheetos" in the results
    And I should not see "doritos" in the results

Scenario: Search for inventory items by Condition
    When I visit the "home page"
    And I select "New" in the "Condition" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "cheetos" in the results
    And I should not see "lays" in the results
    And I should not see "doritos" in the results
    When I press the "Clear" button
    And I select "Open Box" in the "Condition" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "lays" in the results
    And I should not see "cheetos" in the results
    And I should not see "doritos" in the results
    When I press the "Clear" button
    And I select "Used" in the "Condition" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "doritos" in the results
    And I should not see "cheetos" in the results
    And I should not see "lays" in the results

Scenario: Search for inventory items by Quantity
    When I visit the "home page"
    And I set the "Quantity" to "12"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "cheetos" in the results
    And I should see "doritos" in the results
    And I should not see "lays" in the results
    When I press the "Clear" button
    And I set the "Quantity" to "24"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "lays" in the results
    And I should not see "cheetos" in the results
    And I should not see "doritos" in the results

Scenario: Search for inventory items by Restock Level
    When I visit the "home page"
    And I set the "Restock Level" to "true"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "cheetos" in the results
    And I should not see "doritos" in the results
    And I should not see "lays" in the results
    When I press the "Clear" button
    And I set the "Restock Level" to "false"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "lays" in the results
    And I should see "doritos" in the results
    And I should not see "cheetos" in the results
    When I press the "Clear" button
    And I set the "Restock Level" to "True"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "cheetos" in the results
    And I should not see "doritos" in the results
    And I should not see "lays" in the results
    When I press the "Clear" button
    And I set the "Restock Level" to "False"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "lays" in the results
    And I should see "doritos" in the results
    And I should not see "cheetos" in the results

Scenario: No item found of search for inventory items by Name
    When I visit the "home page"
    And I set the "Name" to "non-existent"
    And I press the "Search" button
    Then I should see the message "No items found"

Scenario: No item found of search for inventory items by Condition
    When I visit the "home page"
    And I select "New" in the "Condition" dropdown
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "cheetos" in the results
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Quantity" field should be empty
    And the "Restock Level" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Item has been Deleted!"
    When I press the "Clear" button
    And I select "New" in the "Condition" dropdown
    And I press the "Search" button
    Then I should see the message "No items found"
    And I should not see "cheetos" in the results

Scenario: No item found of search for inventory items by Quantity
    When I visit the "home page"
    And I set the "Quantity" to "999999"
    And I press the "Search" button
    Then I should see the message "No items found"

Scenario: No item found of search for inventory items by Restock Level
    When I visit the "home page"
    And I set the "Restock Level" to "true"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "cheetos" in the results
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Quantity" field should be empty
    And the "Restock Level" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Item has been Deleted!"
    When I press the "Clear" button
    And I set the "Restock Level" to "true"
    And I press the "Search" button
    Then I should see the message "No items found"

Scenario: Invalid query for Search by Restock Level
    When I visit the "home page"
    And I set the "Restock Level" to "12"
    And I press the "Search" button
    Then I should see the message "Invalid restock query string"

Scenario: Invalid query for Search by Quantity
    When I visit the "home page"
    And I set the "Quantity" to "awesome"
    And I press the "Search" button
    Then I should see the message "Invalid quantity in query"
    When I press the "Clear" button
    And I set the "Quantity" to "-100"
    And I press the "Search" button
    Then I should see the message "Invalid quantity in query"

Scenario: Delete an Inventory Item
    When I visit the "home page"
    And I set the "Name" to "TestCreate"
    And I select "New" in the "Condition" dropdown
    And I set the "Quantity" to "10"
    And I set the "Restock Level" to "20"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Quantity" field should be empty
    And the "Restock Level" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Item has been Deleted!"
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should not see "Success"
    And I should see the message "was not found"

Scenario: The swagger API docs is running
    When I visit the "home page"
    And I press the "API" button
    Then I should see "NYU-DevOps Inventory REST API Service" in the title
