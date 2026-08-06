# Table Design

This document defines the logical structure of the database tables used in the NexusAI platform.

Each table represents a core business entity identified during the analysis phase. The table definitions provided in this document serve as the foundation for the database implementation.

## 1. Organization

### Purpose

Represents an organization that subscribes to the NexusAI platform.

The Organization entity serves as the primary tenant within the system, ensuring logical isolation of users, documents, AI conversations, and organizational resources.

### Planned Columns

| Column | Data Type | Description |
|---------|----------|-------------|
| id | UUID | Unique identifier of the organization |
| name | VARCHAR | Organization name |
| slug | VARCHAR | Unique organization identifier used in URLs |
| description | TEXT | Organization description |
| status | ENUM | Organization status (ACTIVE, INACTIVE, SUSPENDED) |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | User who created the organization |
| updated_by | UUID | User who last updated the organization |

### Relationships

- One Organization can have multiple Users.
- One Organization can have multiple Documents.
- One Organization can have multiple Conversations.
- One Organization can have multiple Audit Logs.

### Business Rules

- Every organization shall have a unique identifier.
- Organization names shall be unique across the platform.
- Organization slugs shall be unique across the platform.
- Every user must belong to one organization.
- Every uploaded document must belong to one organization.
- Organizations shall only access their own data.
- Suspended organizations shall not be permitted to access platform resources.

### Future Enhancements

Future versions may support:

- Organization Logo
- Organization Website
- Organization Contact Information
- Subscription Plans
- Storage Quotas
- User Limits
- Custom Branding
- Time Zone Configuration
- Organization Settings

---

## 2. Role

### Purpose

Represents the authorization level assigned to users within the platform.

Roles define the actions and resources that users are permitted to access using the Role-Based Access Control (RBAC) model.

### Planned Columns

| Column | Data Type | Description |
|---------|----------|-------------|
| id | UUID | Unique role identifier |
| name | VARCHAR | Role name |
| description | TEXT | Role description |
| is_system_role | BOOLEAN | Indicates whether the role is predefined by the system |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### Relationships

- One Role can be assigned to multiple Users.

### Business Rules

- Every role shall have a unique name.
- The platform shall provide the following default roles:
  - Platform Admin
  - Organization Admin
  - Employee
- Every user shall be assigned exactly one role.
- User permissions shall be determined by the assigned role.
- System-defined roles cannot be deleted.
- Platform authorization shall follow the Role-Based Access Control (RBAC) model.

### Future Enhancements

Future versions may support:

- Custom Roles
- Fine-Grained Permissions
- Permission Groups
- Role Hierarchies
- Temporary Role Assignment
- Department-Based Roles
- Dynamic Permission Management

---

## 3. User

### Purpose

Represents an authenticated user belonging to an organization.

The User entity stores authentication details, profile information, organizational association, and account status for every user accessing the NexusAI platform.

### Planned Columns

| Column | Data Type | Description |
|---------|----------|-------------|
| id | UUID | Unique user identifier |
| organization_id | UUID | Associated organization |
| role_id | UUID | Assigned role |
| full_name | VARCHAR | User's full name |
| email | VARCHAR | User's email address |
| password_hash | VARCHAR | Encrypted password |
| email_verified | BOOLEAN | Indicates whether the user's email has been verified |
| failed_login_attempts | INTEGER | Number of consecutive failed login attempts |
| account_locked_until | TIMESTAMP | Timestamp until which the account remains locked |
| last_login | TIMESTAMP | Timestamp of the user's last successful login |
| status | ENUM | User status (ACTIVE, INACTIVE, LOCKED) |
| password_updated_at | TIMESTAMP | Timestamp of the last password update |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |
| created_by | UUID | User who created this account |
| updated_by | UUID | User who last updated this account |

### Relationships

- A User belongs to one Organization.
- A User is assigned one Role.
- A User can upload multiple Documents.
- A User can create multiple Conversations.
- A User can generate multiple Audit Logs.

### Business Rules

- Every user shall belong to exactly one organization.
- Every user shall be assigned exactly one role.
- Email addresses shall be unique within an organization.
- Users shall verify their email address before accessing protected resources.
- Consecutive failed login attempts shall be tracked.
- User accounts may be temporarily locked after exceeding the maximum allowed failed login attempts.
- The `last_login` field shall be updated after every successful authentication.
- Passwords shall always be stored in encrypted form.

### Future Enhancements

Future versions may support:

- Multi-Factor Authentication (MFA)
- Single Sign-On (SSO)
- Password Expiration Policies
- Profile Pictures
- Phone Number Verification
- External Identity Provider Integration (OAuth, Azure AD, Google Workspace)

## 4. Document

### Purpose

Represents an enterprise document uploaded to the NexusAI platform.

The Document entity stores metadata about uploaded files and manages the complete lifecycle of document processing, including upload, OCR, indexing, and AI-powered knowledge retrieval.

### Planned Columns

| Column | Data Type | Description |
|---------|----------|-------------|
| id | UUID | Unique document identifier |
| organization_id | UUID | Organization that owns the document |
| uploaded_by | UUID | User who uploaded the document |
| file_name | VARCHAR | System-generated unique file name |
| original_file_name | VARCHAR | Original file name uploaded by the user |
| file_type | ENUM | Document type (PDF, DOCX, IMAGE, XLSX) |
| mime_type | VARCHAR | MIME type of the uploaded file |
| file_size | BIGINT | File size in bytes |
| storage_path | VARCHAR | Storage location of the file |
| processing_status | ENUM | Processing status (UPLOADING, PROCESSING, READY, FAILED, ARCHIVED) |
| ocr_status | ENUM | OCR status (PENDING, PROCESSING, COMPLETED, FAILED, NOT_REQUIRED) |
| total_pages | INTEGER | Total number of pages in the document |
| extracted_text | TEXT | Extracted text from the document (optional for small files) |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### Relationships

- A Document belongs to one Organization.
- A Document is uploaded by one User.
- A Document contains multiple Document Chunks.
- A Document can be referenced by multiple Citations.

### Business Rules

- Every document shall belong to exactly one organization.
- Every document shall be uploaded by an authenticated user.
- Organizations shall only access their own documents.
- Supported file types shall be validated before upload.
- Documents shall pass through the processing pipeline before becoming searchable.
- AI responses shall only use successfully processed documents.
- Failed document processing shall not make documents available for AI retrieval.

### Future Enhancements

Future versions may support:

- Document Versioning
- Document Tags
- Automatic Document Classification
- Duplicate Document Detection
- Virus Scanning
- Document Expiration Policies
- Custom Metadata
- Document Sharing
- SharePoint Integration
- OneDrive Integration

## 5. Document Chunk
### Purpose

Represents a searchable segment of a processed document.

After a document is processed, its unified textual representation is divided into smaller chunks. Each chunk is converted into an embedding and stored for semantic search and Retrieval-Augmented Generation (RAG).

### Planned Columns

| Column | Data Type | Description |
|---------|----------|-------------|
| id | UUID | Unique chunk identifier |
| document_id | UUID | Associated document |
| chunk_index | INTEGER | Sequential chunk number within the document |
| page_number | INTEGER | Original page number (if applicable) |
| chunk_text | TEXT | Text content of the chunk |
| embedding_id | VARCHAR | Reference to the embedding stored in the vector database |
| metadata | JSONB | Additional metadata associated with the chunk |
| created_at | TIMESTAMP | Record creation timestamp |

### Relationships

- A Document Chunk belongs to one Document.
- A Document Chunk can be referenced by multiple Citations.

### Business Rules

- Every chunk shall belong to exactly one document.
- Chunks shall be generated only after successful document processing.
- Chunk ordering shall be preserved using the chunk index.
- Every chunk shall have exactly one embedding representation.
- Chunks shall retain metadata required for accurate retrieval and citation generation.

### Future Enhancements

Future versions may support:

- Parent-Child Chunking
- Semantic Chunking
- Adaptive Chunk Sizes
- Multi-Vector Embeddings
- Keyword Indexing
- Chunk Quality Scoring
- Incremental Re-indexing

## 6. Conversation
### Purpose

Represents an AI conversation session between a user and the NexusAI assistant.

A conversation groups multiple messages exchanged during a chat session and preserves the context required for AI-powered interactions. Each conversation belongs to a single organization and is owned by a specific user.

### Planned Columns

| Column | Data Type | Description |
|---------|----------|-------------|
| id | UUID | Unique conversation identifier |
| organization_id | UUID | Organization that owns the conversation |
| user_id | UUID | User who initiated the conversation |
| title | VARCHAR | User-defined or AI-generated conversation title |
| status | ENUM | Conversation status (ACTIVE, ARCHIVED, DELETED) |
| last_message_at | TIMESTAMP | Timestamp of the most recent message |
| created_at | TIMESTAMP | Record creation timestamp |
| updated_at | TIMESTAMP | Last update timestamp |

### Relationships

- A Conversation belongs to one Organization.
- A Conversation belongs to one User.
- A Conversation contains multiple Messages.

### Business Rules

- Every conversation shall belong to exactly one organization.
- Every conversation shall be associated with exactly one user.
- Users shall only access conversations belonging to their organization.
- A conversation may contain multiple user and assistant messages.
- Conversation history shall be preserved to maintain AI context.
- The conversation title may be automatically generated from the initial user messages.
- The `last_message_at` field shall be updated whenever a new message is added.
- Archived conversations shall remain accessible in read-only mode.
- Deleted conversations shall not be visible to end users.

### Future Enhancements

Future versions may support:

- AI-Generated Conversation Titles
- AI-Generated Conversation Summaries
- Conversation Sharing
- Conversation Pinning
- Favorite Conversations
- Conversation Search
- Folder-Based Organization
- Conversation Export
- Conversation Templates
- Conversation Restore

## 7. Message
### Purpose

Represents an individual message exchanged between a user and the NexusAI assistant.

The Message entity stores the complete conversation history, including user queries and AI-generated responses. It also records AI model information, token usage, response metrics, and additional metadata required for monitoring, debugging, and future enhancements.

### Planned Columns

| Column | Data Type | Description |
|---------|----------|-------------|
| id | UUID | Unique message identifier |
| conversation_id | UUID | Associated conversation |
| role | ENUM | Message sender (USER, ASSISTANT, SYSTEM) |
| message_type | ENUM | Message type (TEXT, IMAGE, FILE) |
| message_text | TEXT | Content of the message |
| model_name | VARCHAR | AI model used to generate the response (nullable for user messages) |
| prompt_tokens | INTEGER | Number of prompt tokens consumed |
| completion_tokens | INTEGER | Number of completion tokens generated |
| total_tokens | INTEGER | Total tokens consumed |
| response_time_ms | INTEGER | AI response generation time in milliseconds |
| metadata | JSONB | Additional message metadata |
| created_at | TIMESTAMP | Record creation timestamp |

### Relationships

- A Message belongs to one Conversation.
- An Assistant Message may reference multiple Citations.

### Business Rules

- Every message shall belong to exactly one conversation.
- Messages shall be stored in chronological order.
- The `role` field shall identify whether the message was generated by the User, Assistant, or System.
- User messages shall not contain AI model information.
- AI-generated messages shall record model usage and token statistics.
- Token usage shall be tracked for monitoring, analytics, and cost estimation.
- Additional processing information may be stored within the metadata field.
- Messages shall not be permanently deleted unless explicitly removed by system administrators.

### Future Enhancements

Future versions may support:

- Streaming Responses
- Message Editing
- Message Regeneration
- Voice Messages
- Image Responses
- File Attachments
- Tool Calling History
- AI Reasoning Metadata
- User Feedback and Ratings
- Message Reactions
- Message Search
- Message Translation

## 8. Citation
### Purpose

Represents the source references used by the AI assistant while generating a response.

Each citation links an AI-generated answer to the corresponding document and document chunk, allowing users to verify the origin of the information and improving transparency and trust in AI-generated responses.

### Planned Columns

| Column | Data Type | Description |
|---------|----------|-------------|
| id | UUID | Unique citation identifier |
| message_id | UUID | Associated assistant message |
| document_id | UUID | Source document |
| document_chunk_id | UUID | Source document chunk |
| page_number | INTEGER | Original page number within the document |
| chunk_index | INTEGER | Chunk sequence number within the document |
| relevance_score | DECIMAL | Similarity score returned by the retrieval system |
| created_at | TIMESTAMP | Record creation timestamp |

### Relationships

- A Citation belongs to one Message.
- A Citation references one Document.
- A Citation references one Document Chunk.

### Business Rules

- Every citation shall reference exactly one document chunk.
- An AI-generated message may contain multiple citations.
- Citations shall only reference successfully indexed documents.
- Users shall only access citations belonging to documents within their organization.
- Citation information shall remain available for answer verification.
- Citation references shall be preserved even if multiple chunks from the same document are used during retrieval.

### Future Enhancements

Future versions may support:

- Clickable Document Preview
- Highlighted Source Text
- Confidence Indicators
- Citation Groups
- Multi-Document Citations
- AI Explanation for Citation Selection
- Section and Paragraph References
- Citation Export
- Source Comparison View

## 9. Audit Log
### Purpose

Records significant user and system activities performed within the NexusAI platform.

Audit logs provide traceability, accountability, security monitoring, compliance support, and troubleshooting capabilities by maintaining an immutable history of important events.

### Planned Columns

| Column | Data Type | Description |
|---------|----------|-------------|
| id | UUID | Unique audit log identifier |
| organization_id | UUID | Organization associated with the event |
| user_id | UUID | User who performed the action (nullable for system events) |
| action | ENUM | Action performed by the user or system |
| resource_type | ENUM | Type of resource affected |
| resource_id | UUID | Identifier of the affected resource |
| status | ENUM | Result of the action (SUCCESS, FAILED) |
| ip_address | VARCHAR | IP address from which the action originated |
| user_agent | TEXT | Client or browser information |
| details | JSONB | Additional event details and metadata |
| created_at | TIMESTAMP | Event timestamp |

### Relationships

- An Audit Log belongs to one Organization.
- An Audit Log may belong to one User.

### Business Rules

- All security-sensitive operations shall be recorded.
- Audit logs shall be immutable after creation.
- Audit logs shall only be accessible by authorized administrators.
- System-generated events shall be recorded even when no user is associated with the action.
- Audit logs shall never contain sensitive information such as passwords or authentication tokens.
- Audit records shall include sufficient information to support troubleshooting, security investigations, and compliance reporting.

### Example Actions

- User Login
- User Logout
- Failed Login Attempt
- Password Reset
- User Created
- User Updated
- User Deleted
- Organization Created
- Organization Updated
- Document Uploaded
- Document Updated
- Document Deleted
- Document Processing Started
- Document Processing Completed
- Document Processing Failed
- Conversation Created
- AI Response Generated
- Role Assigned
- Permission Updated

### Future Enhancements

Future versions may support:

- Security Alerts
- Risk Scoring
- SIEM Integration
- Audit Log Export
- Compliance Reports
- Device Tracking
- Geo-location Tracking
- Session Tracking
- Anomaly Detection
- Log Retention Policies