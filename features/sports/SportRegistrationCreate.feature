Feature: Register for a sport
  As a user of the site,
  So that I can register for and associate my user account with different sports
  I want to be able to register for different sports and choose my desired roles for a sport

  Background: User account exists
    Given The following users exist
      | first_name | last_name | email           | password       |
      | John       | Doe       | user@ayrabo.com | myweakpassword |
    And The following team object exists
      | name                  | division        | league                            | sport      |
      | Green Machine IceCats | Midget Minor AA | Long Island Amateur Hockey League | Ice Hockey |
    And The following sport exists "Ice Hockey"
    And The following sport exists "Baseball"
    And The following sport exists "Basketball"
    And The following waffle switch exists
      | name                | active |
      | sport_registrations | True   |
    And I login with "user@ayrabo.com" and "myweakpassword"

  Scenario: Redirected to new sport registration page after userprofile created
    Given I go to the "home" page
    Then I should be on the "home" page

  Scenario: Redirected when trying to navigate to profile create page when no sport registrations
    Given I go to the "account_complete_registration" page
    Then I should be on the "home" page

  Scenario: Informative text displayed to user
    Given I am on the "sports:register" page
    Then I should see "Register for sports"
    And I should see "Registering for sports help us streamline your registration process."
    And I should see "Add form"

  Scenario: Submit one valid form
    Given I am on the "sports:register" page
    When I select "Ice Hockey" from "id_sportregistrations-0-sport"
    # Player
    And I press "id_sportregistrations-0-roles_1"
    # Coach
    And I press "id_sportregistrations-0-roles_2"
    # Scorekeeper
    And I press "id_sportregistrations-0-roles_5"
    And I press "sport_registration_next_step_btn"
    Then I should be on the "home" page
    And I should see "You have been registered for Ice Hockey."

  Scenario: Submit one invalid form
    Given I am on the "sports:register" page
    When I press "sport_registration_next_step_btn"
    Then I should be on the "sports:register" page
    And "This field is required." should show up 2 times

  Scenario: Add another sport registration
    Given I am on the "sports:register" page
    When I press "add_another_form_btn"
    Then "id_sportregistrations-TOTAL_FORMS" should have value "2"

  Scenario: Remove form
    Given I am on the "sports:register" page
    When I press "add_another_form_btn"
    And I press ".fa.fa-trash.fa-trash-red"
    And I wait for ".multiField" to be removed
    Then "id_sportregistrations-TOTAL_FORMS" should have value "1"

  Scenario: Add max amount of forms
    Given I am on the "sports:register" page
    When I press "add_another_form_btn"
    And I press "add_another_form_btn"
    Then "add_another_form_btn" should be disabled

  Scenario: Added forms optional when submitting, 3 invalid forms
    Given I am on the "sports:register" page
    When I press "add_another_form_btn"
    And I press "add_another_form_btn"
    And I press "sport_registration_next_step_btn"
    # as opposed to 6 times
    Then "This field is required." should show up 2 times
    And "add_another_form_btn" should be disabled

  Scenario: Submit 2 valid forms
    Given I am on the "sports:register" page
    And I press "add_another_form_btn"
    When I select "Ice Hockey" from "id_sportregistrations-0-sport"
    And I press "id_sportregistrations-0-roles_1"
    And I press "id_sportregistrations-0-roles_2"
    And I select "Baseball" from "id_sportregistrations-1-sport"
    And I press "id_sportregistrations-1-roles_2"
    And I press "sport_registration_next_step_btn"
    Then I should be on the "home" page
    And I should see "You have been registered for Ice Hockey, Baseball."

  Scenario: Already registered for all 3 sports
    Given "user@ayrabo.com" is completely registered for "Ice Hockey" with roles "Player, Coach"
    And "user@ayrabo.com" is completely registered for "Baseball" with roles "Player, Manager"
    And "user@ayrabo.com" is completely registered for "Basketball" with roles "Player, Referee"
    When I go to the "sports:register" page
    Then I should see "You have already registered for all available sports."
    And I should be on the "home" page

  Scenario: Selecting duplicate sports
    Given I am on the "sports:register" page
    And I press "add_another_form_btn"
    When I select "Ice Hockey" from "id_sportregistrations-0-sport"
    And I press "id_sportregistrations-0-roles_1"
    And I press "id_sportregistrations-0-roles_2"
    And I select "Ice Hockey" from "id_sportregistrations-1-sport"
    And I press "id_sportregistrations-1-roles_2"
    And I press "sport_registration_next_step_btn"
    Then I should see "Ice Hockey has already been selected. Choose another sport or remove this form."
    And I should be on the "sports:register" page

  Scenario: Already registered for ice hockey and baseball. They should not be options in select box
    Given "user@ayrabo.com" is completely registered for "Ice Hockey" with roles "Player, Coach"
    Given "user@ayrabo.com" is completely registered for "Baseball" with roles "Player, Coach"
    And I am on the "sports:register" page
    Then "add_another_form_btn" should be disabled
    And "id_sportregistrations-0-sport" should not have the option "Ice Hockey"
    And "id_sportregistrations-0-sport" should not have the option "Baseball"

  Scenario: Add form but don't fill it out
    Given I am on the "sports:register" page
    And I press "add_another_form_btn"
    When I select "Ice Hockey" from "id_sportregistrations-0-sport"
    And I press "id_sportregistrations-0-roles_1"
    And I press "id_sportregistrations-0-roles_2"
    And I press "sport_registration_next_step_btn"
    Then I should be on the "home" page
