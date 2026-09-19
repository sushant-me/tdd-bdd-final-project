# ---------------------------------------------------------------------------
# Browser-driven acceptance test -- EXCLUDED FROM CI.
#
# This feature is tagged @ui so the CI job can skip it explicitly with
# `behave --tags="not @ui"`:
#
#   * the repository ships no front-end (there is no `templates/` or `static/`
#     directory), so the "Home Page" the scenario visits does not exist and
#     none of the element ids it uses (`name`, `search-btn`, `flash_message`,
#     ...) can be found; and
#   * CI installs neither a browser nor a WebDriver.
#
# It therefore cannot pass until a UI is added; it is kept (not deleted and
# not silenced with `|| true`) so the gap stays visible.  Everything CI does
# exercise is covered by features/api.feature, which drives the very same
# service over real HTTP.
#
# To run it locally once a front-end exists, install a browser + chromedriver
# and use: behave --tags=@ui
# ---------------------------------------------------------------------------
@ui
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
