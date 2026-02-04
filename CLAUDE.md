# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains a suite of four CI/CD skills for operating system projects:

1. **version-query** - Queries project version information from various sources (config files, Git tags, build metadata)
2. **version-compare** - Compares differences between two versions of a project
3. **build-status** - Checks CI build status for projects using various CI systems
4. **release-assist** - Assists with automated version release processes

## Code Architecture and Structure

The repository follows a modular structure with each skill in its own directory. Each skill directory contains:
- Implementation code for the specific skill
- A README.md file documenting the skill's functionality, interface, and implementation details
- Skill-specific dependencies and configuration

The skills are designed to be independent but complementary, supporting the full CI/CD lifecycle of operating system projects from version querying and comparison to build status checking and release assistance.

## Common Development Commands

Each skill follows a similar pattern for development and testing. Refer to each skill's README.md for specific commands, but general patterns include:

```
/version-query [options]
/version-compare <version1> <version2> [options]
/build-status [task-id] [options]
/release-assist <version> [options]
```

## Development Guidelines

- Each skill should handle authentication and permissions appropriately for its specific CI/CD system integrations
- Error handling should be comprehensive, covering network issues, authentication failures, and invalid inputs
- Skills should support multiple output formats (JSON, text) where appropriate
- Git operations should be performed safely with proper error handling
- Results should be cached where appropriate to improve performance