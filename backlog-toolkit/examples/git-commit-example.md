# Git Commit Message Example

This is an example of a properly formatted git commit message using the template.

## Example 1: Feature Implementation

```
FR-042: Add user authentication feature

Implemented secure user login and registration functionality to enable personalized user experiences and protect user data. This feature is critical for MVP launch as it enables access to protected features and builds user trust.

Technical changes for developers:
- Added AuthService class with login(), register(), and logout() methods
- Implemented bcrypt password hashing with cost factor 12
- Created session management using secure HTTP-only cookies
- Added AuthenticationMiddleware for protected routes
- Updated database schema with users and sessions tables
- Added unit tests for AuthService methods
- Added integration tests for authentication flow
- Created login and registration UI components

Refs FR-042
```

## Example 2: Bug Fix

```
BF-015: Fix email validation rejecting valid addresses

Email addresses containing plus signs are now correctly accepted during registration and profile updates. This fixes an issue affecting approximately 15% of users who use email addresses with plus signs for filtering.

Technical changes for developers:
- Updated email regex pattern in UserService.validateEmail() to include '+' character
- Fixed regex pattern: changed [a-z0-9._%+-] to properly escape plus sign
- Added unit tests for email validation with plus signs
- Added integration tests for registration with plus sign emails
- Updated validation error messages

Refs BF-015
```

## Example 3: Small Change

```
FR-044: Improve error message clarity

Updated error messages to be more user-friendly and actionable. Users will now see clearer guidance when validation fails.

Technical changes for developers:
- Refactored error message generation in ValidationService
- Updated error message templates with user-friendly language
- Added context to error messages (e.g., "Email must be valid format" instead of "Invalid input")

Refs FR-044
```

## Example 4: Refactoring

```
FR-042: Refactor authentication service for better testability

Restructured authentication code to improve testability and maintainability. This change makes it easier to add new authentication methods in the future.

Technical changes for developers:
- Extracted password hashing logic into PasswordHasher class
- Separated session management into SessionManager class
- Updated AuthService to use dependency injection
- Refactored unit tests to use mocks
- Updated integration tests to match new structure

Refs FR-042
```

## Example 5: Documentation Update

```
FR-042: Update API documentation with authentication endpoints

Added comprehensive documentation for new authentication endpoints to help developers integrate with the API.

Technical changes for developers:
- Added API documentation for POST /api/v1/auth/login
- Added API documentation for POST /api/v1/auth/register
- Added API documentation for POST /api/v1/auth/logout
- Included request/response examples
- Added error code documentation

Refs FR-042
```

---

## Key Points Demonstrated

1. **Task number in title**: Each commit title starts with `FR-XXX:` or `BF-XXX:` to link to backlog items
2. **Business-first**: Each commit starts with what the change does for users/business
3. **Technical details**: Bullet points provide specific technical information
4. **Backlog references**: Links commits to backlog items (in title and optional Refs line)
5. **Appropriate detail**: Level of detail matches the scope of the change
6. **Clear structure**: Easy to scan and understand

---

**Last Updated**: 2025-01-27

