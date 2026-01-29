# Functional Component Discovery

You are analyzing a codebase to identify **functional components** - groups of code that work together to deliver specific business functionality.

## Repository
Path: {{REPO_PATH}}

## Task

Discover functional components by analyzing **entry points** (APIs, Kafka consumers, SQS handlers, cron jobs, etc.) and grouping them by business functionality.

### Step 1: Find All Entry Points

Search the codebase for:

1. **HTTP/REST APIs**
   - Look in routes/, controllers/, handlers/
   - Find route definitions (express routes, fastify, etc.)
   - Note: HTTP method, path, handler function

2. **Kafka Consumers/Producers**
   - Look for kafka topic subscriptions
   - Find consumer handlers and producers
   - Note: topic name, handler function

3. **SQS/Queue Handlers**
   - Look for SQS queue listeners
   - Find message handlers
   - Note: queue name, handler function

4. **Scheduled Jobs/Cron**
   - Look for scheduled tasks
   - Find job definitions

5. **Event Handlers**
   - Internal event emitters/listeners
   - Webhooks

### Step 2: Trace the Flow

For each entry point:
1. What controller/handler receives it?
2. What service(s) does it call?
3. What repositories/data access does it use?
4. What external services does it call?

### Step 3: Group by Functionality

Group entry points that serve the same **business purpose**. Examples:
- "User Management" - APIs for user CRUD, profile updates
- "Class Management" - APIs/events for class creation, enrollment
- "Notifications" - Kafka consumers and services for sending notifications
- "Authentication" - Login, logout, token refresh APIs
- "Reporting" - APIs that generate reports

### Step 4: Output Format

Output a valid JSON object:

```json
{
  "repo_path": "{{REPO_PATH}}",
  "language": "detected language",
  "framework": "detected framework",
  "components": [
    {
      "name": "Component Name",
      "description": "What business functionality this component provides",
      "entry_points": [
        {
          "type": "api",
          "method": "POST",
          "path": "/api/v1/users",
          "handler": "UserController.create",
          "file": "src/controllers/user.controller.ts"
        },
        {
          "type": "kafka",
          "topic": "user.created",
          "handler": "UserEventHandler.onUserCreated",
          "file": "src/handlers/user-events.ts"
        }
      ],
      "services": ["UserService", "EmailService"],
      "repositories": ["UserRepository"],
      "files": [
        "src/controllers/user.controller.ts",
        "src/services/user.service.ts",
        "src/repository/user.repository.ts"
      ],
      "related_topics": ["user.created", "user.updated"],
      "external_dependencies": ["email-service", "auth-service"]
    }
  ],
  "summary": {
    "total_apis": 25,
    "total_kafka_topics": 10,
    "total_components": 8
  }
}
```

## Important Guidelines

1. **Focus on business logic** - Group by what the code DOES, not where files are located
2. **Trace dependencies** - Follow the call chain from entry point to data layer
3. **Be specific** - Include actual function names, file paths, topic names
4. **Include ALL entry points** - Don't miss APIs or event handlers
5. **Merge related functionality** - If multiple APIs serve the same feature, group them
6. **Note external calls** - Track calls to other services/APIs

## Example Groupings

Good grouping (by functionality):
- ✅ "Class Enrollment" - includes enroll API, enrollment service, enrollment events
- ✅ "User Authentication" - login, logout, token refresh, password reset

Bad grouping (by file structure):
- ❌ "Controllers" - just listing all controller files
- ❌ "Services" - just listing all service files

Now analyze the repository, find all entry points, and group them into functional components.
 