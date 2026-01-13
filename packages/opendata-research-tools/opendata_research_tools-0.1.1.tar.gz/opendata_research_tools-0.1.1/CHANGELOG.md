# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Clinical Trials search tool
- News search tool  
- Patent search tool
- Advanced filtering options
- Batch query support
- Async/await support
- GraphQL API interface

## [0.1.0] - 2026-01-11

### Added
- **Core Search Tools**
  - PubMed search tool for scientific literature
  - NCBI Gene search tool for gene information
  - UniProt search tool for protein data
  - ChEMBL search tool for bioactive molecules
  - PubChem search tool for chemical compounds
  - Protein Structure search tool (PDB + AlphaFold)
  - WikiData search tool for structured knowledge

- **Utilities**
  - HTTP caching utility for performance optimization
  - Gene symbol resolver for cross-database gene name resolution
  - Standardized output format across all tools

- **Documentation**
  - Comprehensive README with philosophy and quick start
  - API reference documentation
  - Quick start guide
  - Example usage scripts

- **Testing**
  - Unit tests for all search tools
  - Integration tests with real APIs
  - Mock tests for offline development
  - Test coverage > 85%

- **Project Infrastructure**
  - MIT License
  - PyPI-ready package configuration
  - Development dependencies (pytest, black, ruff, mypy)
  - Documentation generation setup (mkdocs)
  - Continuous integration configuration

### Design Principles
- **Minimal Dependencies**: Only `requests` required
- **Standardized Output**: All tools return consistent dictionary formats
- **Zero Configuration**: Works out of the box with sensible defaults
- **Focus on Search**: No data management or opinionated workflows
- **HTTP Caching**: Optional caching to reduce API calls

### Breaking Changes
- None (initial release)

### Known Issues
- WikiData queries may timeout for very broad searches
- Some APIs have rate limits (handled with exponential backoff)
- AlphaFold structure search limited to UniProt IDs
