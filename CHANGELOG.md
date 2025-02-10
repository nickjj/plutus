# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- `plutus info` command to display information (`--categories`, `--items`, `--lint-rules`)

### Changed

- Moved `plutus demo --categories` to `plutus info --categories`
- Moved `plutus demo --items` to `plutus info --items`
- Moved `plutus lint --rules` to `plutus info --lint-rules`

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

[Unreleased]: https://github.com/nickjj/plutus/compare/0.3.0...HEAD
[0.3.0]: https://github.com/nickjj/plutus/compare/0.2.5...0.3.0
[0.2.5]: https://github.com/nickjj/plutus/compare/0.2.4...0.2.5
[0.2.4]: https://github.com/nickjj/plutus/compare/0.2.3...0.2.4
[0.2.3]: https://github.com/nickjj/plutus/compare/0.2.2...0.2.3
[0.2.2]: https://github.com/nickjj/plutus/compare/0.2.1..0.2.2
[0.2.1]: https://github.com/nickjj/plutus/compare/0.2.0..0.2.1
[0.2.0]: https://github.com/nickjj/plutus/compare/0.1.0..0.2.0
[0.1.0]: https://github.com/nickjj/plutus/releases/tag/0.1.0
