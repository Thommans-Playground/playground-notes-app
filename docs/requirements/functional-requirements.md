# Functional Requirements: Note Management

**Status:** Draft  
**Bounded Context:** Note Management  
**Language:** UL-NOTE-001

Downstream artifacts refer to a requirement by its ID. This document does not list them.

Non-functional requirements are in non-functional-requirements.md.

## Scope

The scope below applies to functional and non-functional requirements.

In scope:
- A single User managing their own Notes.

Out of scope:
- Ownership, tags, and sharing.

## Functional Requirements

### REQ-FR-NOTE-001: Create Note

**Priority:** Must have

**Need:** A User needs to create a Note so that they can keep written information.

**Requirement:** The system shall allow a User to create a Note with a Title and, optionally, Content.

**Rationale:** Creating a Note is the entry point to every other capability. Without it, no Note exists to retrieve, rename, archive, or delete.

**Acceptance Criteria**

```gherkin
Feature: Create Note

  @REQ-FR-NOTE-001/AC-001
  # ONT-RULE-NOTE-002, ONT-RULE-NOTE-006
  Scenario: Create a Note with Content
    Given the Title "Shopping list"
    And the Content "Milk, eggs, bread"
    When the User creates a Note
    Then the Note is created with that Title and Content

  @REQ-FR-NOTE-001/AC-002
  # ONT-RULE-NOTE-002, ONT-RULE-NOTE-006
  Scenario: Create a Note without Content
    Given the Title "Shopping list"
    And no Content
    When the User creates a Note
    Then the Note is created with that Title and no Content

  @REQ-FR-NOTE-001/AC-003
  # ONT-RULE-NOTE-001, ONT-RULE-NOTE-002
  Scenario: A new Note is identifiable
    Given the Title "Shopping list"
    When the User creates a Note
    Then the User receives the Note Identifier of the new Note

  @REQ-FR-NOTE-001/AC-004
  # ONT-RULE-NOTE-002, ONT-RULE-NOTE-003, ONT-RULE-NOTE-004
  Scenario: A new Note is Active
    Given the Title "Shopping list"
    When the User creates a Note
    Then the new Note is Active

  @REQ-FR-NOTE-001/AC-005
  # ONT-RULE-NOTE-002
  Scenario Outline: A Title with no visible characters is rejected
    Given the Title <title>
    When the User creates a Note
    Then no Note is created
    And the User is told the Title is not valid

    Examples:
      | title   |
      | ""      |
      | "   "   |

  @REQ-FR-NOTE-001/AC-006
  # ONT-RULE-NOTE-002
  Scenario: A failure to keep the Note is reported
    Given the Title "Shopping list"
    And the system cannot keep Notes
    When the User creates a Note
    Then no Note is created
    And the User is told that creation failed

  @REQ-FR-NOTE-001/AC-007
  # ONT-RULE-NOTE-002
  Scenario: Whitespace around a Title is removed
    Given the Title "  Shopping list  "
    When the User creates a Note
    Then the Note is created with the Title "Shopping list"
```
