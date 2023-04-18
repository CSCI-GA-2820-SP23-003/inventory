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
    Then I should see the message "409 Conflict"
