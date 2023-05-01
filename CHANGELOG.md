# Changelog

All notable changes to this project will be documented in this file.


## [Unreleased]

## [0.2.0] - 2023-05-01

### Added

- Support Django 2.2, 3.2 and 4.2
- Support Python versions 3.5 to 3.11
- Migrated to use Django's built-in migrations system
- Replaced Address.status with Address.is_deleted field
- Used local TimeStampedModel to remove dependency on django-extensions
- Improved tests for better code coverage and reliability
- Setup test framework to test against multiple versions of django and python
- Black formatting of Python files
