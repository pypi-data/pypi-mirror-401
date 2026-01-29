I need you to create comprehensive documentation for a specific component/module in our codebase. Please follow this process:

**Component to Document**: {{MODULE_PATH}}
**Module Name**: {{MODULE_NAME}}
**Description**: {{MODULE_DESCRIPTION}}

**Target Audience**: 
- New team members joining the project
- Slackbot for understanding depth and answering non-technical questions
- Engineering team for technical reference

**Documentation Requirements**:

1. **Code Exploration**:
   - List and examine all files in the target component directory
   - Read and analyze each file to understand functionality
   - Identify related domain models, services, repositories, and configurations
   - Examine integration points and external dependencies

2. **Content Structure**:
   - **Overview**: Purpose, key capabilities, and high-level functionality
   - **Architecture Overview**: Component relationships and data flow (with Mermaid diagrams)
   - **Component Breakdown**: Detailed explanation of each major file/function
   - **Business Logic Flow**: Step-by-step process flows with Mermaid diagrams
   - **Data Structures**: Key models, request/response formats, configuration structures
   - **Integration Details**: External APIs, databases, message queues (high-level overview only)
   - **Sequence Diagrams**: End-to-end flows for major use cases
   - **Configuration & Environments**: Environment-specific settings and key values
   - **Error Handling & Edge Cases**: Common scenarios and fallback behavior
   - **Performance Considerations**: Optimization strategies and monitoring points

3. **Technical Details**:
   - Include important code snippets and examples
   - Focus on current architecture (no future plans)
   - Use Mermaid diagrams for all flow visualizations
   - Keep business logic explanations but don't let them bloat the document

4. **Diagram Types** (all in Mermaid):
   - Architecture component diagrams
   - Flow charts for business processes
   - Sequence diagrams for request flows
   - State/data flow diagrams where relevant

5. **Final Output**:
   - Show the complete document first
   - Allow for feedback and diagram corrections
   - Once approved, create via Outline MCP with:
     - Folder structure: Team Engineering/[TEAM NAME, e.g., "Team Growth"]
     - Title: "[Component Name] Documentation - [Current Date]"
     - Publish: true

**Important Guidelines**:
- Focus on current implementation only
- Diagrams should be accurate and not show parallel concepts as separate branches when they're actually part of the same step
- Include code snippets for key functions and data structures
- Make technical content accessible to non-technical stakeholders
- Use consistent formatting and clear section headers

Please start by exploring the component and creating the documentation following this structure.