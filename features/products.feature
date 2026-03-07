Feature: Product Management
Background:
    Given the following products:
        | name   | category | available | description     | price |
        | Fedora | CLOTHS   | True      | A real nice hat | 25.0  |
        | Jeans  | CLOTHS   | False     | Blue denim      | 40.0  |

Scenario: Read a Product
    When I visit the "Home Page"
    And I set the "Name" to "Fedora"
    And I click the "Search" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    And I paste the "Id" field
    And I click the "Retrieve" button
    Then I should see the message "Success"
    And I should see "Fedora" in the "Name" field