# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- `plutus insert` to safely and quickly add new items
- A new lint warning to identify negative income / refunds and positive expenses

### Fixed

- Add missing `\n` when `plutus edit --sort` writes the file
- Ignore empty new lines in your profile to avoid throwing a parse error
- Demo data had incorrect positive amounts for certain personal expenses

### Changed

- Switch diff labels to be more human friendly for `plutus edit --sort`

## [0.1.0] - 2025-02-07

### Added

- Everything!

[Unreleased]: https://github.com/nickjj/plutus/compare/0.1.0...HEAD
[0.1.0]: https://github.com/nickjj/plutus/releases/tag/0.1.0
