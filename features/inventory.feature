Feature: The inventory service back-end
    As an Inventory Manager
    I need a RESTful catalog service
    So that I can keep track of all my items

Background:
    Given the following inventory items
        | name         | condition | quantity | restock_level  |
        | cheetos      | NEW       | 12       | 23             |
        | testone      | OPEN_BOX  | 24       | 12             |
        | testtwo      | USED      | 12       | 11             |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Inventory RESTful Service" in the title
    And I should not see "404 Not Found"
