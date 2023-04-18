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
