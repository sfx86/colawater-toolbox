# Changelog
## [4.0.0](https://github.com/sfx86/colawater-toolbox/compare/v3.6.0..v4.0.0) - 2023-12-11

### Documentation

- Fetch info from pyproject.toml
- Re-pin astroid version
- Update tooltips

### Features

- Optionally filter mains with null values
- Dump to csv tool

### Miscellaneous Tasks

- Clean up imports
- Remove errata
- Bump version
- Add git-cliff config
- Update dev requirements to include git-cliff
- Configure release.ps1 and git-cliff
- Uncomment git tagging and commit portion
- Revert version number

### Refactor

- Change toolshed defaults and add docstring
- Generalize fallible decorator and slim api surface
- Convert deferred list constructors into listcomps
- Reduce tool output

## [3.6.0](https://github.com/sfx86/colawater-toolbox/compare/v3.5.0..v3.6.0) - 2023-09-28

### Bug Fixes

- Add LayerKind.Casing to layer.kind()

### Documentation

- New module level examples

### Miscellaneous Tasks

- Add docs path trigger
- Pin astroid version to resolve autoapi upstream failure
- Update dev deps
- Add mypy to lint
- New names for clarity
- Fix yaml error
- Rename workflow

## [3.5.0](https://github.com/sfx86/colawater-toolbox/compare/v3.4.0..v3.5.0) - 2023-09-26

### Bug Fixes

- Ensure fullmatch gets a str

### Documentation

- Bump version
- Better example
- Update xml

### Features

- Default date to previous sunday
- Kind function to discern water layer types

### Miscellaneous Tasks

- Clean imports
- Clean up comments
- Create release action
- Remove docs dir push trigger
- Filter tests dir
- Move mypy into pyproject.toml
- Fix archive path
- Fix archive path
- Fix archive directory and path
- Fix artifact path
- Add workflow_run trigger

### Refactor

- Remove get_ prefix on function names
- Clean up
- Clean up implementation with layer.kind() and LayerKind
- Remove logging module
- Make halt function more usable
- Slim up progressor api and add decorator
- Move module
- Clarify function names
- Clarify function names in mains
- Clarify progressor message
- Restructure project
- Valid package name and Tool class
- Restructure module layout and nightmare type factory

### Release

- 3.4.0
- V3.5.0

### Templates

- Changelog
- Changelog
- Change question mark placeholders to named

## [3.4.0](https://github.com/sfx86/colawater-toolbox/compare/v3.3.0..v3.4.0) - 2023-09-07

### Documentation

- Bump version

### Features

- Halt method in error
- Error checking on append to art
- Halt logs message
- Default date to previous sunday

## [3.3.0](https://github.com/sfx86/colawater-toolbox/compare/v3.2.0..v3.3.0) - 2023-08-21

### Bug Fixes

- Remove invalid characters from scratch layer path
- Bugs in boilerplate
- Sql error when running on cypress

### Documentation

- Update tooltips
- Bump version
- Update module docstrings for checks
- Update tool descriptions
- Update docstrings
- Update docstrings
- Update runtime error message for clarity and conciseness
- Update xml
- Update xml
- Update docstrings
- Add logo and favicon
- Update xml
- Clarify installation instructions
- Update releases link
- Update xml
- Update tooltips

### Features

- Tool constructor in toolbox file
- Add categories to type factory and enforce required methods
- Limit warning output per checks
- Get_name function for layers
- Fid_calculator feature layer is multivalue and auto-detects used layers

### Miscellaneous Tasks

- Update mypy config
- Make ignore comments more specific
- Remove 'raises' for functions not decorated with fallible
- Satisfy mypy

### Refactor

- Use layer object for dup fids
- Use rfind for get_workspace
- Improve conciseness of append_to_art
- Reduce progressor type changes
- Clean up types, listcomps, no more walrus operators
- Make progressor type checking condition clearer
- Conditionally add items and notes for all checks
- Conditionally add items and notes for all checks (include extra)
- Clean up boilerplate
- Clean up types

### Readme

- Update roadmap
- Update tool description
- Add logo
- Remove toc
- Add horizontal rule
- Update roadmap
- Update versioning
- Update releases link
- Update badges releases link

### Templates

- Update docstrings

## [3.2.0](https://github.com/sfx86/colawater-toolbox/compare/v3.1.1..v3.2.0) - 2023-08-11

### Bug Fixes

- Add explicit str constructors
- Index oids properly
- Proper length of tuple updating row
- Workspace generated correctly
- Remove syntax error in sql query

### Features

- Quality control check for duplicate fids
- Don't add any items if iterable has no elements
- Make attr.process more general
- Add_items adds no items if contents is empty

### Miscellaneous Tasks

- Fix mypy error
- Clean imports

### Refactor

- Use any in exists
- Simplify checks implementation and move to new module
- Add map partial idioms to reduce verbosity
- Remove groupby and fix type annotations
- Update error message and include more exceptions

### Readme

- Update roadmap

### Release

- 3.2.0

## [3.1.1](https://github.com/sfx86/colawater-toolbox/compare/v3.1.0..v3.1.1) - 2023-08-10

### Bug Fixes

- Remove parenthesized context manager
- Summary content cleared after posting
- Csv message only printed when results exist

### Documentation

- Bump version
- Bump version

## [3.1.0](https://github.com/sfx86/colawater-toolbox/compare/v3.0.0..v3.1.0) - 2023-08-10

### Bug Fixes

- Api exposed properly
- Catch appropriate exception
- Remove parenthesized context manager
- Let arcpy process args in set_progressor
- Use displayName for layer omitted message
- Lowercased to colawater
- Readd parenthesized context manager

### Documentation

- Autoapi options and update xml
- Update xml
- Update name
- Update name
- Fix title overline
- Remove autoapi options
- Autoapi options
- Update docs and conf options
- Update name to colawater-toolbox
- Fix name error
- Edit for clarity and conciseness
- Update docstrings
- Update xml

### Features

- Update error message to include more context
- Add progressor type checking
- Add initial inference to fid calculator
- Add_items function

### Miscellaneous Tasks

- Type hints and clean up imports
- Clean up imports

### Refactor

- Too many changes to list, sorry future me
- Conciseness
- Use set_progressor

### Styling

- Format with black

### Readme

- Fix badges
- Clarity
- Add append to art to toc
- Use details for tool descriptions

### Release

- 3.1.0

### Templates

- Update idioms and placeholder definitions
- Update toolbox

## [3.0.0](https://github.com/sfx86/colawater-toolbox/compare/v2.3.0..v3.0.0) - 2023-08-01

### Documentation

- Bump version
- Clean up sphinx conf
- Clean up formatting
- Add art tool
- Add doc comments

### Features

- Append to art tool

### Miscellaneous Tasks

- Add sphinx trigger, rename to black
- Restrict scope of black lint
- Add globs to paths
- Reformat

### Release

- 3.0.0

### Templates

- Trim content

## [2.3.0](https://github.com/sfx86/colawater-toolbox/compare/v2.2.0..v2.3.0) - 2023-07-26

### "readme

- Convert back to markdown"

### Bug Fixes

- Sphinx build
- Sphinx build
- Sphinx build
- Typo in html_title
- Calling str too early
- Fit __init__.py files
- Remove duplicate note mention from csv processing message

### Documentation

- Add doc comments
- Initial commit
- Update tooltips

### Features

- New methods on SummaryBuilder
- New qualifier option on add_header()

### Miscellaneous Tasks

- Sphinx build
- Black action
- Change to build docs only on published releases

### Refactor

- Use result api

### Styling

- Format with black
- Apply isort to imports
- Format with black

### Readme

- Convert to rst
- Update docs badge
- Reorder badges

### Release

- 2.3.0

### Requirements

- Initial commit

### Templates

- Added doc comments
- Docs
- Style isort

## [2.2.0](https://github.com/sfx86/colawater-toolbox/compare/v2.1.0..v2.2.0) - 2023-07-20

### Documentation

- Tooltips and descriptions
- Update tooltips

### Features

- SCAN_DIR constant
- Output dumped indication
- New functions and constants
- Water main data source check
- Add null attr processing to fid format qc
- Less dynamic api for SummaryContainer

### Miscellaneous Tasks

- Black format, mypy, restructure properly
- Type annotations

### Refactor

- Reorganize into status and summary modules
- Rename variable to be clearer
- Rename process_nullable_attr to process_attr

### Styling

- Format with black

### Gitignore

- Remove .xml

### Release

- 2.1.0
- 2.2.0

## [2.1.0](https://github.com/sfx86/colawater-toolbox/compare/v2.0.0..v2.1.0) - 2023-07-18

### Bug Fixes

- Non-existant field no longer specified

## [2.0.0](https://github.com/sfx86/colawater-toolbox/compare/v1.2.1..v2.0.0) - 2023-07-18

### Features

- Changes to apis and new modules

### Release

- 2.0.0

### Templates

- Trim down toolbox template
- Remove unused argument

## [1.2.1](https://github.com/sfx86/colawater-toolbox/compare/v1.2.0..v1.2.1) - 2023-07-14

### Patch

- Remove importlib

## [1.2.0](https://github.com/sfx86/colawater-toolbox/compare/v1.1.0..v1.2.0) - 2023-07-13

### Release

- 1.2.0

### Templates

- Initial commit

## [1.1.0](https://github.com/sfx86/colawater-toolbox/compare/v1.0.1..v1.1.0) - 2023-07-11

### Bug Fixes

- Uncaught old function signature

### Styling

- Format with black

### Release

- 1.1.0

## [1.0.1](https://github.com/sfx86/colawater-toolbox/compare/v1.0.0..v1.0.1) - 2023-07-06

### Bug Fixes

- Correct arcgis documentation link in comment

<!-- generated by git-cliff -->
