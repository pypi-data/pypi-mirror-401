# Changelog

All notable changes to the bclearer-interop-services package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2026-01-14

### Added
- SQLite support for `bclearer_interop_services` package
  - New `SqliteFacade` class implementing the `DatabaseFacade` interface
  - SQLite support in `DatabaseFactory` for creating SQLite database connections
  - Full API compatibility with PostgreSQL facade for seamless switching
  - Support for in-memory databases using `:memory:` parameter
  - Automatic creation of parent directories for database files
  - Foreign key constraint enforcement enabled by default
  - Comprehensive unit tests for all SQLite functionality
  - Support for DataFrame storage and retrieval
  - Schema validation for existing tables

### Changed
- Updated `DatabaseFactory.get_database()` method signature to make all parameters optional except `db_type`
- Enhanced error messages to list supported database types

### Notes
- SQLite uses the `database` parameter as a file path, while other parameters (host, user, password, port) are ignored
- SQLite stores JSON data as TEXT (as opposed to PostgreSQL's JSONB)
- SQLite uses `?` placeholders for parameters (DatabaseFacade handles this automatically)
- Use SQLite for local development, testing, or deployments without PostgreSQL access
- Use PostgreSQL for production deployments requiring advanced features like concurrent writes, complex queries, or large datasets

## [0.5.0] - Previous Release

### Previous Changes
- Initial release with PostgreSQL support
- Core interop services for data integration
