# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.3] - 2025-01-13

### Fixed
- **CRITICAL: Transaction Rollback Error**: Fixed SQLAlchemy error "Can't reconnect until invalid transaction is rolled back" that occurred on EVERY access resolution request
  - **Root Cause**: When `scalar_one_or_none()` raised an exception (e.g., "Multiple rows found"), the error handler attempted to execute a debug query within the same invalid transaction
  - **Impact**: All async access resolution requests were failing with transaction errors, making the system unusable
  - **Symptom**: Error message "Failed to resolve user access: Can't reconnect until invalid transaction is rolled back. Please rollback() fully before proceeding (Background on this error at: https://sqlalche.me/e/20/8s2b)"
  - **Fix**: Removed debug queries from exception handlers that were executing within invalid transaction states
  - **Files Changed**:
    - `medha_one_access/core/resolver.py`:
      - Line 1205-1219: `AsyncBODMASResolver.resolve_user_access()` - User lookup error handler
      - Line 1299-1314: `AsyncBODMASResolver.resolve_user_access()` - Artifact lookup error handler
      - Line 1383-1398: `AsyncBODMASResolver.resolve_resource_access()` - Resource lookup error handler
    - `medha_one_access/core/controller.py`:
      - Line 17: Added SQLAlchemy exception imports (`InvalidRequestError`, `PendingRollbackError`, `DBAPIError`)
      - Line 604-620: Added specific error handling for transaction and database errors with helpful diagnostics

### Changed
- **Error Handling**: Exception handlers no longer attempt to query the database when transaction is in invalid state
- **Error Messages**: Improved error messages to provide clearer guidance without requiring additional database queries
- **Transaction Safety**: All async database operations now properly respect transaction boundaries

### Technical Details
- **Before**: `scalar_one_or_none()` exception → catch → execute debug query → "Can't reconnect" error
- **After**: `scalar_one_or_none()` exception → catch → raise helpful error message → transaction rolls back cleanly
- **Why It Failed Always**: The v0.3.2 fix added database queries to group detection methods, increasing query frequency and making this bug trigger on every request instead of intermittently
- **Session Management**: The `AsyncDatabaseManager.session_scope()` context manager properly handles rollback, but only if no queries are attempted after initial failure

### Migration Notes
- **No Breaking Changes**: This fix only improves error handling without changing API behavior
- **Performance Impact**: None - actually improved by removing unnecessary debug queries
- **Recommended Action**: Update to this version immediately if experiencing transaction errors

## [0.3.2] - 2025-01-12

### Fixed
- **CRITICAL: Artifact Group Access Resolution Bug**: Fixed major bug in `_involves_resource_groups()` and `_involves_user_groups()` methods that prevented proper access resolution for groups
  - **Root Cause**: Heuristic check only detected groups if their IDs contained keywords like "group", "cluster", "team", etc.
  - **Impact**: Resource/user groups without these keywords were incorrectly treated as individual entities, causing incomplete BODMAS resolution
  - **Symptom**: New user access wasn't fully resolved for artifact groups until those groups were modified in the UI
  - **Fix**: Replaced keyword-based heuristic with proper database queries to check entity types (RESOURCEGROUP, USERGROUP)
  - **Files Changed**:
    - `medha_one_access/core/resolver.py` (lines 967-989 for sync, 1978-2032 for async)

### Changed
- **Synchronous Resolver**: `_involves_user_groups()` and `_involves_resource_groups()` now query database to check actual entity types
- **Async Resolver**: Methods now process all expressions to avoid async/sync access issues, with actual filtering during expression resolution

### Technical Details
- **Before**: `return any(indicator in expression_lower for indicator in ["group", "cluster", ...])`
- **After (Sync)**: Database query to check `Artifact.type == "RESOURCEGROUP"` or `User.type == "USERGROUP"`
- **After (Async)**: Return True for all valid expressions to ensure comprehensive processing
- **Fallback**: If parsing fails, assumes group involvement to prevent skipping rules
- **BODMAS Steps Affected**: Steps 1 (UserGroup×ResourceGroup) and 3 (User×ResourceGroup) are now correctly executed

### Migration Notes
- **No Breaking Changes**: This fix improves access resolution accuracy without changing API
- **Performance Impact**: Minimal - adds lightweight database query for sync resolver
- **Recommended Action**: Update to this version immediately to fix access resolution issues

## [0.2.2] - 2025-08-26

### Fixed
- **Expression Validation**: Added support for additional common characters in entity names:
  - Colons `:` (e.g., `"Entity: Test"`)
  - Commas `,` (e.g., `"Entity, Demo"`) 
  - Apostrophes `'` (e.g., `"FD's Snapshot"`)
- **Character Validation**: Updated allowed character set for comprehensive entity name support

### Changed
- **Validation Regex**: Enhanced pattern to: `r"[^a-zA-Z0-9_+\-|.\s@&#\"():,']"`
- **Error Messages**: Updated to include colons, commas, and apostrophes in allowed characters list

## [0.2.1] - 2025-08-26

### Fixed
- **Expression Validation**: Added support for parentheses `()` in entity names (e.g., `"Manpower Budget (Input to Finance) FY26"`)
- **Character Validation**: Updated allowed character set to include parentheses for entity names with brackets

### Changed
- **Validation Regex**: Updated validation pattern to allow parentheses: `r'[^a-zA-Z0-9_+\-|.\s@&#"()]'`
- **Error Messages**: Updated validation error messages to include parentheses in allowed characters list

## [0.2.0] - 2025-08-26

### Added
- **Quoted Entity Support**: Added support for quoted entities in expressions to handle entity names with hyphens and special characters
- **Enhanced Expression Validation**: Added validation for properly matched quotes in expressions

### Fixed
- **Critical Expression Parsing Bug**: Fixed major bug where entity IDs containing hyphens (e.g., `user-service-api`) were incorrectly parsed as mathematical operations
- **Expression Validation**: Updated validation to allow quotes in expressions while maintaining security

### Changed
- **Expression Parser**: Updated core expression parsing regex to support quoted entities: `"entity-with-hyphens"`
- **Backward Compatibility**: Maintained 100% compatibility with existing unquoted expressions

### Technical Details
- Updated `ExpressionParser.parse_expression()` regex pattern to: `r'([+-]?)(".*?"|[^+-]+)'`
- Added automatic quote stripping in token processing
- Enhanced `validate_expression()` to check for unmatched quotes
- Updated allowed character validation to include quote characters

### Migration
- **No Breaking Changes**: All existing expressions continue to work unchanged
- **New Feature**: Entities with special characters can now be quoted for proper parsing
- **Examples**: 
  - Old (broken): `user-service-api+admin-panel` 
  - New (working): `"user-service-api"+"admin-panel"`
  - Still works: `simpleuser+basicgroup`

## [0.1.1] - 2025-08-25

### Fixed
- **Pagination Defaults**: Fixed hardcoded 100-record limits in all list methods (list_users, list_artifacts, list_access_rules)
- **User Group Resolution**: Fixed `get_usergroup_members` method to use correct `resolve_user_expression` method instead of non-existent `resolve_expression`
- **Query Optimization**: Updated all list methods to support optional limit parameter for unlimited record loading

### Changed
- **list_users()**: Changed limit parameter from `int = 100` to `Optional[int] = None`
- **list_artifacts()**: Changed limit parameter from `int = 100` to `Optional[int] = None` 
- **list_access_rules()**: Changed limit parameter from `int = 100` to `Optional[int] = None`
- **Query Logic**: Added conditional query execution to apply limit only when specified

## [0.1.0] - 2025-08-19

### Added
- Initial release of Access Control Library
- BODMAS-based access resolution engine with 4-step priority system
- Expression-based user and resource grouping with + (include) and - (exclude) operators
- Time-based access constraints (date ranges, time windows, day-of-week restrictions)
- Comprehensive audit trails for access decisions
- SQLAlchemy models and Pydantic schemas for all entities
- Database management with Alembic migrations
- AccessController class providing clean Python API
- CLI tools for database management, data import/export, and access checking
- FastAPI integration module for optional web APIs
- Complete test suite with fixtures and examples
- Type hints and py.typed marker for full typing support
- Support for PostgreSQL and SQLite databases
- Hierarchical organization structures
- Context managers for database sessions
- Expression validation and error handling

### Supported Features
- **User Management**: Create individual users and user groups with expressions
- **Resource Management**: Create individual resources and resource groups with expressions
- **Access Rules**: Define flexible access rules with user/resource expressions and permissions
- **Time Constraints**: Apply temporal restrictions to access rules
- **BODMAS Resolution**: Mathematical precedence-based access resolution
- **Audit Trails**: Detailed logging of access resolution steps
- **CLI Interface**: Command-line tools for all operations
- **REST API**: Optional FastAPI integration for web services
- **Database Support**: PostgreSQL (recommended) and SQLite
- **Migration Support**: Alembic-based database schema management

### Technical Specifications
- Python 3.8+ support
- SQLAlchemy 2.0+ with async support
- Pydantic v2 for data validation
- FastAPI for optional web API
- Click for CLI interface
- Comprehensive test coverage
- Type hints throughout
- Modern Python packaging (pyproject.toml)

## [Unreleased]

### Planned Features
- Redis caching for improved performance
- Webhook notifications for access events
- LDAP/Active Directory integration
- Role-based access control (RBAC) helpers
- Attribute-based access control (ABAC) extensions
- GraphQL API support
- Performance optimizations and query optimization
- Additional database backend support (MySQL, MongoDB)
- Docker containerization
- Kubernetes deployment examples