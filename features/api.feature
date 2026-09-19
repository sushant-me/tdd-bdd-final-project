# ---------------------------------------------------------------------------
# API-level acceptance tests -- these ARE what CI runs.
#
# They are not a substitute for the @ui scenario in products.feature, which
# remains excluded (see the comment there).  These scenarios exercise the
# service over real HTTP through the same REST endpoints a client would use,
# so a change that breaks the API breaks CI.
# ---------------------------------------------------------------------------
@api
Feature: Product API
    As a client of the service
    I want a working product REST API
    So that I can manage the product catalog

    Background:
        Given the following products:
            | name   | category | available | description     | price |
            | Fedora | CLOTHS   | True      | A real nice hat | 25.0  |
            | Jeans  | CLOTHS   | False     | Blue denim      | 40.0  |

    Scenario: List the products
        When I request the list of all products
        Then the response status should be 200
        And the response should contain 2 products
        And the response should contain a product named "Fedora"
        And the response should contain a product named "Jeans"

    Scenario: Filter the products by name
        When I request the products with name "Fedora"
        Then the response status should be 200
        And the response should contain 1 products
        And the response should contain a product named "Fedora"

    Scenario: Filter the products by category
        When I request the products in category "CLOTHS"
        Then the response status should be 200
        And the response should contain 2 products

    Scenario: Filter the products by availability
        When I request the products that are available
        Then the response status should be 200
        And the response should contain 1 products
        And the response should contain a product named "Fedora"

    Scenario: Retrieve a single product by id
        When I request the product named "Fedora" by id
        Then the response status should be 200
        And the response should contain a product named "Fedora"
