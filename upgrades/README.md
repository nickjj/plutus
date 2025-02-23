# Plutus: CLI for income and expense tracking

This documentation is specific to upgrading to new versions where the Plutus
profile structure changes such as adding, modifying or removing a CSV header.
Most new versions won't do this. You'll know when because the changelog for
that release will be marked with 🧬 and link here.

## ⭐️ Philosophy

All of the upgrade scripts try to follow these philosophies:

- Your Plutus profile is a sacred file and should never be directly modified
- Provide a number of outputs to help you understand what changed

## ⚡️ Installation

The only rule is you must upgrade in steps. For example:

1. You have version 0.9
2. The latest version is 2.0
3. There are upgrade scripts for 0.x to 1.0 and 1.0 to 2.0
4. First run the 0.x. to 1.0 script
5. Then run the 1.0 to 2.0 script

You cannot skip step 4 because you need to run them incrementally in order.

All of the scripts are installed in the same way. Replace the `VERSION` number
with the version you're upgrading to.

```sh
# Install it on a well known system path that will work on most systems, feel
# free to adjust this path if you want.
export VERSION="0.x-to-0.7" && sudo curl \
  -L "https://raw.githubusercontent.com/nickjj/plutus/main/upgrades/${VERSION}" \
  -o "/usr/local/bin/${VERSION}" && sudo chmod +x "/usr/local/bin/${VERSION}"
```

*Once the upgrade is complete you can delete this script.*

## 🧾 Changes

Each script has built-in documentation and more details about the change.

### [0.x to 0.7](./0.x-to-0.7)

A new `Description` field was added before `Notes`. The script's main purpose
is to shift your existing notes over 1 field to the right so you don't lose
anything. This makes room for importing and using descriptions.
