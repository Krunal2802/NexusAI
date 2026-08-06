# Entity Relationship Diagram (ER Diagram)

## Purpose

This document describes the relationships between the core entities of the NexusAI platform.

The ER Diagram provides a high-level representation of the database structure and illustrates how different entities interact with each other. It serves as a reference for database implementation, backend development, and future system enhancements.

# Relationship Overview

The NexusAI platform follows a multi-tenant architecture where every organization owns its users, documents, conversations, and audit logs. Users interact with the AI assistant through conversations, while uploaded documents are processed into document chunks that form the enterprise knowledge base.

AI-generated responses include citations that reference the original document chunks used to generate the answer.

# Entity Relationships

## Organization

Organization is the primary entity of the system.

Relationships:

- One Organization can have multiple Users.
- One Organization can have multiple Documents.
- One Organization can have multiple Conversations.
- One Organization can have multiple Audit Logs.

Relationship Type:

```
Organization (1) -------- (*) User

Organization (1) -------- (*) Document

Organization (1) -------- (*) Conversation

Organization (1) -------- (*) Audit Log
```

## Role

Each role can be assigned to multiple users.

Relationship Type:

```
Role (1) -------- (*) User
```

## User

Each user belongs to one organization and is assigned one role.

Users can upload documents and create AI conversations.

Relationship Type:

```
Organization (1) -------- (*) User

Role (1) -------- (*) User

User (1) -------- (*) Document

User (1) -------- (*) Conversation
```

## Document

Each uploaded document belongs to one organization and one user.

After processing, every document is divided into multiple chunks.

Relationship Type:

```
Organization (1) -------- (*) Document

User (1) -------- (*) Document

Document (1) -------- (*) Document Chunk
```

## Document Chunk

Each document chunk belongs to exactly one document.

Chunks are indexed in the vector database and may be referenced by AI-generated citations.

Relationship Type:

```
Document (1) -------- (*) Document Chunk

Document Chunk (1) -------- (*) Citation
```

## Conversation

Each conversation belongs to one organization and one user.

A conversation contains multiple messages exchanged between the user and the AI assistant.

Relationship Type:

```
Organization (1) -------- (*) Conversation

User (1) -------- (*) Conversation

Conversation (1) -------- (*) Message
```

## Message

Each message belongs to one conversation.

AI-generated messages may reference multiple citations.

Relationship Type:

```
Conversation (1) -------- (*) Message

Message (1) -------- (*) Citation
```

## Citation

Each citation references one document and one document chunk used during AI response generation.

Relationship Type:

```
Message (1) -------- (*) Citation

Document (1) -------- (*) Citation

Document Chunk (1) -------- (*) Citation
```

## Audit Log

Audit logs record user and system activities within an organization.

Relationship Type:

```
Organization (1) -------- (*) Audit Log

User (1) -------- (*) Audit Log
```

# Database Relationship Summary

| Parent Entity | Child Entity | Relationship |
|---------------|-------------|--------------|
| Organization | User | One-to-Many |
| Organization | Document | One-to-Many |
| Organization | Conversation | One-to-Many |
| Organization | Audit Log | One-to-Many |
| Role | User | One-to-Many |
| User | Document | One-to-Many |
| User | Conversation | One-to-Many |
| Document | Document Chunk | One-to-Many |
| Conversation | Message | One-to-Many |
| Message | Citation | One-to-Many |
| Document | Citation | One-to-Many |
| Document Chunk | Citation | One-to-Many |

# Notes

- Every table uses a UUID as its primary key.
- Foreign key relationships enforce referential integrity.
- All business entities are logically isolated by Organization to support multi-tenancy.
- Soft deletion is preferred for business-critical entities where applicable.
- AI-generated responses maintain traceability through document citations.