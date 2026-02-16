# Workflow Diagrams Example

This document demonstrates the Mermaid.js workflow diagrams used to visualize the backlog management process. These diagrams help team members understand how feature requests and bug fixes flow through the system.

## Feature Request Workflow

This flowchart shows the complete lifecycle of a feature request from initial creation through backlog management to sprint planning and completion.

```mermaid
flowchart TD
    A[Create Feature Request] --> B[Use Feature Request Template]
    B --> C[Assign Unique ID FR-XXX]
    C --> D[Fill Required Fields]
    D --> E[Document Dependencies]
    E --> F[Save to features/FR-XXX-name.md]
    F --> G[Add to Product Backlog Table]
    G --> H[Set Status: Not Started]
    H --> I[Assign Priority]
    I --> J[Estimate Story Points]
    J --> K{Backlog Refinement}
    K -->|Clarify Requirements| L[Update Feature Request]
    L --> K
    K -->|Identify Dependencies| M[Review All Dependencies]
    M --> N[Sort Backlog by Dependency Order]
    N --> O{Ready for Sprint?}
    O -->|No| K
    O -->|Yes| P[Select for Sprint Planning]
    P --> Q{All Dependencies Resolved?}
    Q -->|No| R[Include Dependencies in Sprint]
    Q -->|Yes| S[Add to Sprint Planning Document]
    R --> S
    S --> T[Break Down into Tasks]
    T --> U[Update Status: In Progress]
    U --> V[Work on Feature]
    V --> W[Complete Feature]
    W --> X[Update Status: Completed]
    X --> Y[Mark Acceptance Criteria Complete]
    Y --> Z[Conduct Retro Session]
```

**Key Steps**:
1. Create feature request using template and document dependencies
2. Add to product backlog with initial status
3. Go through backlog refinement including dependency identification
4. Sort backlog by dependency order
5. Select for sprint planning (ensuring dependencies are resolved)
6. Break down into tasks and work on feature
7. Complete and mark as done
8. Conduct sprint retrospective (retro session)

## Bug Fix Workflow

This flowchart shows the complete lifecycle of a bug fix, including decision points for critical bugs that require immediate attention.

```mermaid
flowchart TD
    A[Create Bug Fix] --> B[Use Bug Fix Template]
    B --> C[Assign Unique ID BF-XXX]
    C --> D[Fill Required Fields]
    D --> E[Document Steps to Reproduce]
    E --> F[Save to bugs/BF-XXX-description.md]
    F --> G[Add to Product Backlog Table]
    G --> H[Set Status: Not Started]
    H --> I[Assign Priority]
    I --> J{Is Critical?}
    J -->|Yes| K[Immediate Action Required]
    K --> L[Add to Current Sprint]
    J -->|No| M[Estimate Story Points]
    M --> N{High Priority?}
    N -->|Yes| O[Address in Next Sprint]
    N -->|No| P[Wait for Sprint Planning]
    O --> Q[Add to Sprint Planning]
    P --> Q
    L --> Q
    Q --> R[Break Down into Tasks]
    R --> S[Update Status: In Progress]
    S --> T[Work on Bug Fix]
    T --> U[Complete Bug Fix]
    U --> V[Update Status: Completed]
    V --> W[Verify Fix]
    W --> X[Conduct Retro Session]
```

**Key Decision Points**:
- **Critical Bugs**: Require immediate action and are added to current sprint
- **High Priority Bugs**: Should be addressed in next sprint
- **Medium/Low Priority Bugs**: Can wait for regular sprint planning

## Status Lifecycle

This state diagram shows the status transitions for backlog items throughout their lifecycle.

```mermaid
stateDiagram-v2
    [*] --> NotStarted: Item Created
    NotStarted --> InProgress: Work Begins
    InProgress --> Completed: Work Finished
    InProgress --> NotStarted: Work Paused/Cancelled
    Completed --> [*]
    
    note right of NotStarted
        Item in backlog
        Not assigned to sprint
    end note
    
    note right of InProgress
        Item assigned to sprint
        Currently being worked on
    end note
    
    note right of Completed
        Item finished
        Tested and verified
    end note
```

**Status Definitions**:
- **⭕ Not Started**: Item is in backlog, not yet assigned to a sprint or started
- **⏳ In Progress**: Item is currently being worked on (assigned to active sprint)
- **✅ Completed**: Item is finished, tested, and verified

## How to Use These Diagrams

1. **Reference During Process**: Use these diagrams as quick reference when working with backlog items
2. **Onboarding**: Share with new team members to help them understand the workflow
3. **Process Improvement**: Use as a basis for discussing process improvements
4. **Documentation**: Include in process documentation to provide visual context

## Integration

These diagrams are integrated into:
- `backlog-toolkit/processes/backlog-management-process.md` - Main process documentation
- Feature request template examples
- Sprint planning documentation

## Notes

- Diagrams use Mermaid.js syntax and render in most modern markdown viewers
- Diagrams should be updated if the process changes
- For best rendering, use markdown viewers that support Mermaid.js (GitHub, GitLab, VS Code with extensions, etc.)

