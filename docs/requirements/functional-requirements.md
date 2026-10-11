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
  Scenario: Create a Note with Content
    Given a valid Title (ONT-RULE-NOTE-002)
    And some Content
    When the User creates a Note
    Then the Note is created with that Title and Content

  @REQ-FR-NOTE-001/AC-002
  Scenario: Create a Note without Content
    Given a valid Title (ONT-RULE-NOTE-002)
    And no Content
    When the User creates a Note
    Then the Note is created with that Title and no Content

  @REQ-FR-NOTE-001/AC-003
  Scenario: A new Note is identifiable
    Given a valid Title (ONT-RULE-NOTE-002)
    When the User creates a Note
    Then the User receives the Note Identifier of the new Note (ONT-RULE-NOTE-001)

  @REQ-FR-NOTE-001/AC-004
  Scenario: A new Note is Active
    Given a valid Title (ONT-RULE-NOTE-002)
    When the User creates a Note
    Then the new Note is Active (ONT-RULE-NOTE-003)

  @REQ-FR-NOTE-001/AC-005
  Scenario: An invalid Title is rejected
    Given a Title that is not valid (ONT-RULE-NOTE-002)
    When the User creates a Note
    Then no Note is created
    And the User is told the Title is not valid

  @REQ-FR-NOTE-001/AC-006
  Scenario: A failure to keep the Note is reported
    Given a valid Title (ONT-RULE-NOTE-002)
    And the system cannot keep Notes
    When the User creates a Note
    Then no Note is created
    And the User is told that creation failed
```
