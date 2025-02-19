# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- General purpose CSV import script for bank CSV exports, GnuCash and more!

### Changed

- For the `show` command, either `--summary` or `--summaey-with-items` can be set but not both
- Rename `Transportation` to `Travel` in the demo categories

### Removed

- GnuCash import script (the general purpose one replaces it)

## [0.5.2] - 2025-02-14

### Added

- `--help` output for each subcommand

## [0.5.1] - 2025-02-14

### Added

- `info --template` to store custom notes and checklists

## [0.5.0] - 2025-02-13

### Added

- `alias` command to quickly generate reports and run custom commands
- Support using `-v` and `--version` in addition to `version` to show the version
- Version the GnuCash import script in the same way as the main Plutus script

### Fixed

- Gracefully handle (with an exception) if too many valid fields exist in a CSV item
- Better handle the config file being partially invalid (ie. missing `[Settings]`)

### Changed

- Allow quarter helper filters (ie. `2025-q1`) to work with any regex pattern you supply

## [0.4.4] - 2025-02-12

### Changed

- Allow running the `version` command with an invalid config file
- For the `demo` command, enforce either `--init` or `--init-benchmarks` are set but not both
- Use `Decimal` instead of `float` when working with amounts

## [0.4.3] - 2025-02-11

### Fixed

- Show the latest 5 items as a preview when inserting new items (it listed the oldest 5)
- Ensure the locale fallback formatting includes 2 decimal places

### Changed

- Improve error message if `EDITOR` is unset so it shows your last run command

## [0.4.2] - 2025-02-11

### Changed

- Allow the `config` command to be run without validating the config so you can edit it

## [0.4.1] - 2025-02-11

### Fixed

- Improve locale fallback to resolve currency error if your locale is `C` or `C.UTF-8`

## [0.4.0] - 2025-02-10

### Added

- `plutus info` command to display information (`--categories`, `--items`, `--lint-rules`)

### Changed

- Moved `plutus demo --categories` to `plutus info --categories`
- Moved `plutus demo --items` to `plutus info --items`
- Moved `plutus lint --rules` to `plutus info --lint-rules`
- Rename `plutus demo --init-benchmark` to `plutus demo --init-benchmarks` (both technically work now)

## [0.3.0] - 2025-02-09

### Added

- Detect if your config file is missing settings (useful for upgrading)
- New config settings `lint_income_words` and `lint_expense_words` instead of hard coding English words

## [0.2.5] - 2025-02-09

### Fixed

- `plutus demo --init-benchmark` to run with any `plutus` binary path (really fixed)

## [0.2.4] - 2025-02-09

### Fixed

- `plutus demo --init-benchmark` to run with any `plutus` binary path

## [0.2.3] - 2025-02-08

### Added

- `plutus demo --init-benchmark` for setting up and running benchmarks

## [0.2.2] - 2025-02-08

### Fixed

- Display currency symbols correctly (they were always US based before)

## [0.2.1] - 2025-02-08

### Fixed

- Allow `config` and `version` commands to be run without needing a profile

## [0.2.0] - 2025-02-08

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

[Unreleased]: https://github.com/nickjj/plutus/compare/0.5.2...HEAD
[0.5.2]: https://github.com/nickjj/plutus/compare/0.5.1...0.5.2
[0.5.1]: https://github.com/nickjj/plutus/compare/0.5.0...0.5.1
[0.5.0]: https://github.com/nickjj/plutus/compare/0.4.4...0.5.0
[0.4.4]: https://github.com/nickjj/plutus/compare/0.4.3...0.4.4
[0.4.3]: https://github.com/nickjj/plutus/compare/0.4.2...0.4.3
[0.4.2]: https://github.com/nickjj/plutus/compare/0.4.1...0.4.2
[0.4.1]: https://github.com/nickjj/plutus/compare/0.4.0...0.4.1
[0.4.0]: https://github.com/nickjj/plutus/compare/0.3.0...0.4.0
[0.3.0]: https://github.com/nickjj/plutus/compare/0.2.5...0.3.0
[0.2.5]: https://github.com/nickjj/plutus/compare/0.2.4...0.2.5
[0.2.4]: https://github.com/nickjj/plutus/compare/0.2.3...0.2.4
[0.2.3]: https://github.com/nickjj/plutus/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/nickjj/plutus/compare/0.2.1..0.2.2
[0.2.1]: https://github.com/nickjj/plutus/compare/0.2.0..0.2.1
[0.2.0]: https://github.com/nickjj/plutus/compare/0.1.0..0.2.0
[0.1.0]: https://github.com/nickjj/plutus/releases/tag/0.1.0
