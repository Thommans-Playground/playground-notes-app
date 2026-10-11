# UL-NOTE-001: Note Ubiquitous Language

**Status:** Draft  
**Bounded Context:** Note Management  
**Ontology:** docs/ontology/ont-note.ttl  
**Related Domain Model:** DES-NOTE-001

## 1. Purpose

This is how we talk about notes.

Everyone who works on this context uses these words in the same way: in requirements, use cases, conversations, models, and code. When the way we talk changes, this document changes first.

It captures the language and nothing else. Rules, structure, and behavior are owned by other artifacts and are referred to by ID.

## 2. How We Talk About Notes

A **User** writes a **Note**.

A Note has a **Title**. It may also have **Content**.

The User **creates** a Note by giving it a Title and, if they wish, some Content.

Once created, a Note is **Active**. The User can **retrieve** it by its **Note Identifier**.

The User can **rename** a Note to give it a new Title.

When the User no longer needs a Note in front of them but wants to keep it, they **archive** it. An **Archived** Note can be **restored**, and then it is Active again.

When the User does not want a Note any more, they **delete** it. A **Deleted** Note is gone from the User's point of view.

## 3. Phrases With Specific Meaning

The formal meaning of each term is defined in the ontology.

| We say | We mean |
|---|---|
| Create a Note | Bring a new Note into existence (UC-NOTE-001) |
| Retrieve a Note | Get one Note back by its Note Identifier (UC-NOTE-002) |
| Rename a Note | Give an existing Note a new Title (UC-NOTE-003) |
| Archive a Note | Set a Note aside but keep it (UC-NOTE-004) |
| Restore a Note | Bring an Archived Note back to Active (UC-NOTE-005) |
| Delete a Note | Remove a Note (UC-NOTE-006) |

## 4. Words We Do Not Use

| Instead of | We say |
|---|---|
| memo, document, entry | Note |
| name, subject, heading | Title |
| body, text, description | Content |
| state, flag | Status |
| add, new | Create |
| fetch, load, read | Retrieve |
| destroy, trash, remove | Delete |

In the model and code, Note Identifier is written NoteId and Status is written NoteStatus.

## 5. Not Yet Part of the Language

We do not talk about owners, tags, or sharing in this version.
