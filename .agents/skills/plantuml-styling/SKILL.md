---
name: plantuml-styling
description: Guidelines and design system for authoring modern, unique, and elegant PlantUML diagrams (sequence, DDD class/aggregate, hexagonal architecture, context maps, and activity diagrams). Use whenever creating or restyling PlantUML diagrams.
---

# PlantUML Styling & Diagram Craft

Transform standard PlantUML diagrams from the default 1990s yellow-and-red palette into modern, publication-grade architectural visuals. This skill defines a distinctive **"Nordic Slate"** visual design system, semantic stereotypes, and diagramming rules for the project.

---

## 1. Visual Design System: "Nordic Slate"

The design language uses clean typography, soft neutral surfaces, precise borders, and purposeful semantic accents.

### Color Tokens

| Token | Hex | Role | Usage |
|---|---|---|---|
| **Base Surface** | `#FFFFFF` | Background of elements | Class boxes, participants, nodes |
| **Canvas** | `#FAFAFA` | Diagram canvas | Transparent or ultra-light gray |
| **Dark Slate** | `#0F172A` | Primary text & headers | Titles, class names, message labels |
| **Muted Slate** | `#475569` | Secondary text | Types, stereo notes, rule citations |
| **Border Slate** | `#94A3B8` | Structural strokes | Element boundaries, lifelines (1.0px) |
| **Muted Border** | `#CBD5E1` | Subtle dividers | Group boxes, package outlines |
| **Indigo Accent** | `#4F46E5` / `#EEF2FF` | Aggregate Root / Driving Ports | Primary architectural anchors |
| **Teal Accent** | `#0D9488` / `#F0FDFA` | Entities / Adapters | Core stateful components |
| **Amber Accent** | `#D97706` / `#FFFBEB` | Value Objects / Invariants | Immutable values, domain constraints |
| **Slate Gray** | `#64748B` / `#F8FAFC` | Enums / Driven Ports | Types, peripheral infrastructure |
| **Rose Accent** | `#E11D48` / `#FFF1F2` | Failure flows / Alt branches | Negative branches, error returns |

---

## 2. Global Theme Definition

Include or embed the following global theme block at the top of every diagram:

```plantuml
' === NORDIC SLATE THEME ===
skinparam monochrome false
skinparam shadowing false
skinparam roundcorner 8
skinparam defaultFontName "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
skinparam defaultFontSize 12
skinparam defaultFontColor #0F172A
skinparam ArrowColor #475569
skinparam ArrowThickness 1.2
skinparam BoxPadding 10
skinparam ParticipantPadding 12

' Canvas & borders
skinparam BackgroundColor #FAFAFA
skinparam PackageBorderColor #94A3B8
skinparam PackageBackgroundColor #FFFFFF
skinparam PackageFontSize 13
skinparam PackageFontStyle bold
skinparam PackageFontColor #0F172A

' Notes & Annotations
skinparam NoteBackgroundColor #FFFBEB
skinparam NoteBorderColor #D97706
skinparam NoteFontColor #92400E
skinparam NoteFontSize 11
skinparam NoteTextAlignment left
```

---

## 3. Diagram-Specific Styling Patterns

### A. Sequence Diagrams (Analysis & Use Cases)

**Rules:**
1. Actors are clean silhouettes or simple rounded boxes.
2. Lifelines are slim, muted slate (`#94A3B8`).
3. Return messages use dashed arrows (`-->`) with concise descriptions.
4. `alt` and `opt` frames have soft borders and clear headings citing Acceptance Criteria / Rule IDs.
5. Notes cite ontology rules (`(ONT-RULE-...)`).

```plantuml
' Sequence Diagram Skinparams
skinparam SequenceLifeLineBorderColor #94A3B8
skinparam SequenceLifeLineBackgroundColor #F1F5F9
skinparam ParticipantBackgroundColor #FFFFFF
skinparam ParticipantBorderColor #475569
skinparam ParticipantBorderThickness 1.2
skinparam ParticipantFontSize 13
skinparam ParticipantFontStyle bold

skinparam ActorBackgroundColor #FFFFFF
skinparam ActorBorderColor #475569
skinparam ActorFontSize 13
skinparam ActorFontStyle bold

skinparam SequenceGroupBackgroundColor #F8FAFC
skinparam SequenceGroupBorderColor #94A3B8
skinparam SequenceGroupHeaderFontColor #0F172A
skinparam SequenceGroupFontSize 11
skinparam SequenceGroupFontStyle bold
```

**Example Structure:**
```plantuml
@startuml
!include ../architecture/theme.puml
title UC-NOTE-001 - Create Note - Sequence

actor User
participant "Note Management" as System

User -> System : Create Note (Title, Content)
activate System #EEF2FF

System -> System : Normalize and validate Title\n<color:#4F46E5>ONT-RULE-NOTE-002</color>

alt #FFF1F2 Title not valid (AF-001, AC-005)
    System --> User : Title is not valid
else #F0FDF4 Title valid
    System -> System : Assign Note Identifier (ONT-RULE-NOTE-001)
    System -> System : Create Note as Active (ONT-RULE-NOTE-003)
    System --> User : Note Identifier
end

deactivate System
@enduml
```

---

### B. DDD Class & Aggregate Diagrams

**Rules:**
1. Turn off default letter badges (`skinparam classAttributeIconSize 0`).
2. Style DDD stereotypes with distinct, recognizable visual tones:
   - `<<Aggregate Root>>`: Indigo header tint (`#EEF2FF`), solid border (`#4F46E5`).
   - `<<Entity>>`: Teal tint (`#F0FDFA`), border (`#0D9488`).
   - `<<Value Object>>`: Warm amber tint (`#FFFBEB`), border (`#D97706`).
   - `<<Enum>>`: Slate tint (`#F8FAFC`), border (`#64748B`).
3. Attribute types: show exact type and ontology realization (`ONT-REL-...`).
4. Relationships: Use strong composition (`*--`) for value objects owned exclusively by the aggregate.

```plantuml
' DDD Class Skinparams
skinparam classAttributeIconSize 0
skinparam ClassBackgroundColor #FFFFFF
skinparam ClassBorderColor #94A3B8
skinparam ClassBorderThickness 1.2
skinparam ClassFontSize 12
skinparam ClassHeaderBackgroundColor #F8FAFC

skinparam ClassStereotypeFontSize 10
skinparam ClassStereotypeFontColor #475569

skinparam class<<Aggregate Root>> {
  HeaderBackgroundColor #EEF2FF
  BorderColor #4F46E5
  BorderThickness 1.5
}

skinparam class<<Entity>> {
  HeaderBackgroundColor #F0FDFA
  BorderColor #0D9488
}

skinparam class<<Value Object>> {
  HeaderBackgroundColor #FFFBEB
  BorderColor #D97706
}

skinparam class<<Enum>> {
  HeaderBackgroundColor #F8FAFC
  BorderColor #64748B
}
```

---

### C. Hexagonal Architecture & Ports/Adapters

**Rules:**
1. Use nested packages or frames to represent the **Onion Layers**:
   - `Domain` (center, highlighted).
   - `Application` & `Ports` (middle).
   - `Adapters` (outer boundary).
2. Color code driving adapters (inbound / client-facing) separately from driven adapters (outbound / persistence).
3. Dependency arrows point **strictly inward** (Adapters -> Ports -> Domain).

```plantuml
skinparam package<<Domain>> {
  BackgroundColor #EEF2FF
  BorderColor #4F46E5
}

skinparam package<<Application>> {
  BackgroundColor #F8FAFC
  BorderColor #64748B
}

skinparam package<<Adapters>> {
  BackgroundColor #FFFFFF
  BorderColor #94A3B8
}

skinparam interface<<Driving Port>> {
  BorderColor #4F46E5
}

skinparam interface<<Driven Port>> {
  BorderColor #0D9488
}
```

---

## 4. Reusable Theme File Location

All shared styling lives in:
```text
docs/architecture/theme.puml
```

Individual diagram files can include it cleanly at the top:
```plantuml
@startuml
!include ../architecture/theme.puml
' or !include theme.puml when in the same directory
...
@enduml
```

---

## 5. Checklist for Every Diagram

- [ ] Does the diagram start with `!include ...theme.puml` (or the inline Nordic Slate skinparams)?
- [ ] Are default PlantUML yellow boxes and gradient artifacts eliminated?
- [ ] Are fonts crisp, consistent, and readable (`Inter` / system sans-serif)?
- [ ] Do stereotypes (`<<Aggregate Root>>`, `<<Value Object>>`, `<<Driving Port>>`) have intentional, semantic colors?
- [ ] Do all rule references use exact IDs (`ONT-RULE-...`, `AC-...`) without restating rule bodies?
- [ ] Are lines clean, non-crossing where possible, with unambiguous arrows?

---

## 6. Do Not

- Do not use default unstyled PlantUML.
- Do not use high-saturation neon colors or dark, unreadable background fills.
- Do not let relationship lines create tangled rat nests; use directional hints (`-right->`, `-down->`, `*--`).
- Do not write verbose implementation pseudocode inside sequence or class diagrams. Cite IDs.
