# NexusAI Core Entities
This document identifies the core business entities used within the NexusAI platform. These entities represent the primary business objects that participate in the system and serve as the foundation for database design.

## 1. Organization
Represents an organization that subscribes to the NexusAI platform.

Responsibilities include:

- Managing organizational users
- Managing organizational documents
- Maintaining an isolated knowledge base
- Managing AI conversations
- Storing organization-specific audit logs

## 2. User
Represents an authenticated individual who belongs to an organization.

Responsibilities include:

- Logging into the platform
- Uploading documents
- Asking AI questions
- Viewing AI responses
- Managing organizational resources based on assigned permissions

## 3. Role
Represents the authorization level assigned to a user.

Example roles include:

- Platform Administrator
- Organization Administrator
- Employee

Roles determine which resources and operations a user is permitted to access.

## 4. Document
Represents an uploaded enterprise document that contributes to the organization's knowledge base.

Supported document types include:

- PDF
- Word Documents
- Excel Files
- Images

Documents are processed before becoming searchable by the AI system.

## 5. Document Chunk
- Represents a smaller logical section of a document.
- Document chunks enable efficient semantic search and AI knowledge retrieval.
- Each document may contain multiple document chunks.

## 6. Conversation
- Represents a chat session between a user and NexusAI.
- A conversation contains multiple user and AI messages.

## 7. Message
Represents an individual message exchanged during a conversation.

Message types include:
- User Message
- AI Response

Each message belongs to a single conversation.

## 8. Citation
- Represents the original source referenced while generating an AI response.
- A citation provides traceability by identifying the source document and relevant location.

## 9. Audit Log
Represents important activities performed within the platform.

Examples include:
- User Login
- Document Upload
- Document Deletion
- User Management
- Administrative Actions

Audit logs improve system monitoring, security, and compliance.