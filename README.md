# Plutus: CLI tool for income and expense tracking

Quickly analyze your income and expenses from the command line using a single
CSV file as your data source.

You can use this to help with budgeting or getting your numbers in order for
filing taxes. It's focused on individuals who want a simple way to help gain
insight on their finances.

It's a zero dependency Python script. No package managers required! Installing
it is a matter of curling down 1 file, or perhaps a few files if you want to
use any of the importers to help you migrate from other tools.

## 🖥 Demo video

[![Plutus](https://img.youtube.com/vi/mwVnKbne9v4/0.jpg)](https://www.youtube.com/watch?v=mwVnKbne9v4)

The above video covers using all of Plutus' features as of 0.4.0. This project
will evolve over time so check this readme file or the
[changelog](./CHANGELOG.md) for the latest features and updates.

With that said, the project does have core goals and ideas which are its DNA
and vision. Most of what you see in the video will stick around in one way or
another.

## 🧬 Vision

You just want to keep track of your income from a few sources, separate out
personal / business expenses and keep tabs on how much you paid in taxes.
You're not especially interested in double-entry bookkeeping for balancing
funds between accounts. You want to get your numbers and move on with life.

**You want little to no complexity** with the freedom to add as little or as
much detail as you want. If you want to track every last personal expense down
to the penny with deeply nested categories you can, or if you want to skip that
and optimize for business income / expenses you can do that too. It should be
painless to refactor how items are categorized.

**You want to answer questions like:**

- "How much did I spend on personal expenses this month?"
- "How much income did I generate and from where?"
- "How much did I spend on any of my businesses?"
- "What is my business' taxable income (income - business expenses - tax deductions)?"
- "It's time to file quarterly taxes, what numbers do I need to give my accountant?"
- "It's time to officially file taxes, how can I be sure my numbers are accurate?"

**You're busy** and want to see these results in about 1 second with a way to
quickly filter and sort by different column types in a concise way. You also
don't want to spend time tinkering with options that are easy to forget.

**You're paranoid about incorrect data** so you want explicit feedback to help
you validate and confirm that each item being reported on was inputted
correctly.

**You enjoy the command line** and the philosophy of "it's just text". You want
to deal with text input that produces text output. At the same time if it does
come up, you want a data format that an accountant is ok with (CSV). It's also
nice to have a single CSV file in case you want to do visual analysis in Excel.

*As an aside, I've worked with a few accountants. None of them asked for a CSV
or any formal export from another tool. They only wanted my income and business
expenses broken down by category and Plutus alone can do that and more.*

If any of the above resonates with you, I encourage you to give Plutus a try.
**I've imported 9 years worth of data from GnuCash and everything lines up to
the penny**. It generates reports for over 12,000 items in ~100ms.

There's also a demo feature to try it out with no time investment on your part!
This also doubles as a nice way to generate test data because correctness and
accuracy is a major concern for a tool like this.

### Why not just use GnuCash, Ledger or XYZ?

I used GnuCash for 9 years. It's a graphical tool and worked pretty well but I
always had an itch to use something different because it runs a little slow and
it's not super convenient for adding new categories and items.

I looked into Ledger but it does more than I'd like and it has a less portable
text format by default.

As for XYZ, I'm sure there's a lot of tools out there. One thing is for
certain, I do not want to link my bank account or provide financial details to
a SAAS company.

Ultimately I decided that I'm done making compromises on tools I use on a
regular basis and the first version is what I came up with after 2 weekends of
development based on nearly a decade of finance tracking.

### Name

Plutus is the mythological [Greek god of
wealth](https://en.wikipedia.org/wiki/Plutus).

## 🤑 Show me the money

Before diving into features, here's a couple of example commands with demo data
because you might be thinking "I don't care about the name, let me see what the
thing looks like because if I don't like it or it looks too complicated I will
close this browser tab and never think about it again". I know that's what I
would be thinking!

**Show items from calendar year 2025, in this case "2025" is an optional regex
pattern:**

```
plutus show 2025

--------------------------------------------------------------------------------------------------------------------------------
   | Date       | Category                                | Amount     | Total      | Method      | Notes
--------------------------------------------------------------------------------------------------------------------------------
1  | 2025-02-05 | Personal Expenses:Entertainment:Games   | -$5.03     | -$5.03     | FreedomCard | Hollow Knight
2  | 2025-02-28 | Personal Expenses:Transportation        | -$1,244.03 | -$1,249.06 | FreedomCard | Plane trip to Antartica
3  | 2025-03-17 | Personal Expenses:Groceries             | -$14.14    | -$1,263.20 | FreedomCard |
4  | 2025-04-30 | Personal Expenses:Groceries             | -$84.21    | -$1,347.41 | FreedomCard |
5  | 2025-05-02 | Tax:Refunds                             | $1,614.00  | $266.59    | ACH         | Federal
6  | 2025-05-04 | Tax:Refunds                             | $236.00    | $502.59    | ACH         | NY State
7  | 2025-05-19 | Personal Expenses:Entertainment:Netflix | -$16.83    | $485.76    | FreedomCard |
8  | 2025-06-05 | Income:Merch                            | $360.28    | $846.04    | Zelle       | Programming stickers
9  | 2025-07-06 | Income:Consulting                       | $300.00    | $1,146.04  | Zelle       | Johnny Tables (Flask)
10 | 2025-07-14 | Personal Expenses:Entertainment:Games   | -$10.17    | $1,135.87  | FreedomCard | Ori and the Blind Forest
11 | 2025-07-16 | Income:Consulting                       | $600.00    | $1,735.87  | ACH         | Acme Inc (Docker deployment)
12 | 2025-08-01 | Business Expenses:Affiliates            | -$17.70    | $1,718.17  | Zelle       | William Thatcher
13 | 2025-08-01 | Business Expenses:Hosting:DigitalOcean  | -$12.00    | $1,706.17  | FreedomCard |
14 | 2025-08-18 | Business Expenses:Rent                  | -$3,200.00 | -$1,493.83 | Cash        | 2 months
15 | 2025-09-01 | Business Expenses:Affiliates            | -$24.90    | -$1,518.73 | Zelle       | William Thatcher
16 | 2025-09-01 | Business Expenses:Hosting:DigitalOcean  | -$12.00    | -$1,530.73 | FreedomCard |
17 | 2025-09-03 | Business Expenses:Hosting:Domain Names  | -$10.95    | -$1,541.68 | PayPal      | nickjanetakis.com
18 | 2025-10-11 | Income:Consulting                       | $1,500.00  | -$41.68    | PayPal      | Alice (Docker)
19 | 2025-10-17 | Income:Consulting                       | $600.00    | $558.32    | Zelle       | Johnny Tables (Flask)
20 | 2025-10-30 | Income:Affiliates:Amazon                | $123.45    | $681.77    | ACH         |
21 | 2025-11-30 | Income:Affiliates:Amazon                | $345.67    | $1,027.44  | ACH         |
22 | 2025-11-30 | Income:Affiliates:DigitalOcean          | $25.00     | $1,052.44  | ACH         |
23 | 2025-11-30 | Income:Affiliates:DigitalOcean          | $50.00     | $1,102.44  | ACH         |
24 | 2025-12-30 | Income:Affiliates:Amazon                | $234.56    | $1,337.00  | ACH         |
```

**Show items from tax year 2025 Q4 and sort largest amounts on the bottom,
reverse it with `--sort amount-`:**

```
plutus show 2025-q4 --sort amount

----------------------------------------------------------------------------------------------------------------------
   | Date       | Category                               | Amount    | Total     | Method      | Notes
----------------------------------------------------------------------------------------------------------------------
1  | 2025-09-01 | Business Expenses:Affiliates           | -$24.90   | -$24.90   | Zelle       | William Thatcher
2  | 2025-09-01 | Business Expenses:Hosting:DigitalOcean | -$12.00   | -$36.90   | FreedomCard |
3  | 2025-09-03 | Business Expenses:Hosting:Domain Names | -$10.95   | -$47.85   | PayPal      | nickjanetakis.com
4  | 2025-11-30 | Income:Affiliates:DigitalOcean         | $25.00    | -$22.85   | ACH         |
5  | 2025-11-30 | Income:Affiliates:DigitalOcean         | $50.00    | $27.15    | ACH         |
6  | 2025-10-30 | Income:Affiliates:Amazon               | $123.45   | $150.60   | ACH         |
7  | 2025-12-30 | Income:Affiliates:Amazon               | $234.56   | $385.16   | ACH         |
8  | 2025-11-30 | Income:Affiliates:Amazon               | $345.67   | $730.83   | ACH         |
9  | 2025-10-17 | Income:Consulting                      | $600.00   | $1,330.83 | Zelle       | Johnny Tables (Flask)
10 | 2025-10-11 | Income:Consulting                      | $1,500.00 | $2,830.83 | PayPal      | Alice (Docker)
```

**Aggregate amount totals for each category (default), date, amount, method or
notes:**

```
plutus show --summary

--------------------------------------------------------------------------------------
   | Category                                | Amount     | Total      | Items | Total
--------------------------------------------------------------------------------------
1  | Business Expenses:Affiliates            | -$42.60    | -$42.60    | 2     | 2
2  | Business Expenses:Dining Out            | -$56.02    | -$98.62    | 1     | 3
3  | Business Expenses:Hosting:DigitalOcean  | -$24.00    | -$122.62   | 2     | 5
4  | Business Expenses:Hosting:Domain Names  | -$10.95    | -$133.57   | 1     | 6
5  | Business Expenses:Rent                  | -$4,800.00 | -$4,933.57 | 2     | 8
6  | Income:Affiliates:Amazon                | $703.68    | -$4,229.89 | 3     | 11
7  | Income:Affiliates:DigitalOcean          | $100.00    | -$4,129.89 | 3     | 14
8  | Income:Consulting                       | $3,000.00  | -$1,129.89 | 4     | 18
9  | Income:Merch                            | $360.28    | -$769.61   | 1     | 19
10 | Income:Sponsors:OpenSource              | $0.01      | -$769.60   | 1     | 20
11 | Personal Expenses:Dining Out            | -$10.00    | -$779.60   | 1     | 21
12 | Personal Expenses:Entertainment:Games   | -$15.20    | -$794.80   | 2     | 23
13 | Personal Expenses:Entertainment:Netflix | -$16.83    | -$811.63   | 1     | 24
14 | Personal Expenses:Groceries             | -$182.56   | -$994.19   | 3     | 27
15 | Personal Expenses:Transportation        | -$1,296.04 | -$2,290.23 | 3     | 30
16 | Tax:Refunds                             | $1,850.00  | -$440.23   | 2     | 32
```

**Filter only the business expenses category, using `:` helps avoid false
positive matches:**

```
plutus show "Business Expenses:"

--------------------------------------------------------------------------------------------------------------------------
  | Date       | Category                               | Amount     | Total      | Method       | Notes
--------------------------------------------------------------------------------------------------------------------------
1 | 2024-07-17 | Business Expenses:Rent                 | -$1,600.00 | -$1,600.00 | Cash         |
2 | 2024-08-24 | Business Expenses:Dining Out           | -$56.02    | -$1,656.02 | SapphireCard | Meeting with King Midas
3 | 2025-08-01 | Business Expenses:Affiliates           | -$17.70    | -$1,673.72 | Zelle        | William Thatcher
4 | 2025-08-01 | Business Expenses:Hosting:DigitalOcean | -$12.00    | -$1,685.72 | FreedomCard  |
5 | 2025-08-18 | Business Expenses:Rent                 | -$3,200.00 | -$4,885.72 | Cash         | 2 months
6 | 2025-09-01 | Business Expenses:Affiliates           | -$24.90    | -$4,910.62 | Zelle        | William Thatcher
7 | 2025-09-01 | Business Expenses:Hosting:DigitalOcean | -$12.00    | -$4,922.62 | FreedomCard  |
8 | 2025-09-03 | Business Expenses:Hosting:Domain Names | -$10.95    | -$4,933.57 | PayPal       | nickjanetakis.com
```

**Show the raw contents of the CSV file for 2024**:

```
plutus show 2024 --raw

Date,Category,Amount,Method,Notes
2024-01-12,"Personal Expenses:Transportation",-20.01,"FreedomCard","Gas"
2024-02-28,"Personal Expenses:Transportation",-32.00,"FreedomCard","Train to NYC"
2024-04-30,"Personal Expenses:Groceries",-84.21,"FreedomCard",
2024-06-09,"Personal Expenses:Dining Out",-10.00,"SapphireCard","Pinneapple Pizza"
2024-07-17,"Business Expenses:Rent",-1600.00,"Cash",
2024-08-24,"Business Expenses:Dining Out",-56.02,"SapphireCard","Meeting with King Midas"
2024-09-15,"Income:Sponsors:OpenSource",0.01,"Venmo","Zero Cool"
2024-11-30,"Income:Affiliates:DigitalOcean",25.00,"ACH",
```

**I introduced issues into the CSV file on purpose, the linter exposes them
with color highlighting:**

```
plutus lint

WARNING [EXPENSE_IS_POSITIVE] [L3]: 2024-02-28,"Personal Expenses:Transportation",32.00,"FreedomCard","Train to NYC"
ERROR [DATE_MISMATCH] [L8]: 2024-99-15,"Income:Sponsors:OpenSource",0.01,"Venmo","Zero Cool"
ERROR [CATEGORY_MISMATCH] [L12]: 2025-03-17,"Personal Expenses::Groceries",-14.14,"FreedomCard",
ERROR [NOTES_MISMATCH] [L23]: 2025-08-18,"Business Expenses:Rent",-3200.00,"Cash","2 months, commas aren't allow"
ERROR [SORT_BY_DATE_MISMATCH]:
--- yours
+++ expected
@@ -4,8 +4,8 @@
 2024-06-09,"Personal Expenses:Dining Out",-10.00,"SapphireCard","Pinneapple Pizza"
 2024-07-17,"Business Expenses:Rent",-1600.00,"Cash",
 2024-08-24,"Business Expenses:Dining Out",-56.02,"SapphireCard","Meeting with King Midas"
+2024-11-30,"Income:Affiliates:DigitalOcean",25.00,"ACH",
 2024-99-15,"Income:Sponsors:OpenSource",0.01,"Venmo","Zero Cool"
-2024-11-30,"Income:Affiliates:DigitalOcean",25.00,"ACH",
 2025-02-05,"Personal Expenses:Entertainment:Games",-5.03,"FreedomCard","Hollow Knight"
 2025-02-28,"Personal Expenses:Transportation",-1244.03,"FreedomCard","Plane trip to Antartica"
 2025-03-17,"Personal Expenses::Groceries",-14.14,"FreedomCard",

4 linting errors occurred, here's all of the rules to check into:

CSV_HEADERS_MISMATCH
  - CSV headers match Date,Category,Amount,Method,Notes

PARSE_FAILURE
  - Items have exactly 4 commas (5 fields)

WHITESPACE_MISMATCH
  - Item fields have no leading or trailing whitespace
  - Item fields cannot be empty except for notes

DATE_MISMATCH
  - Dates match ^\d{4}-\d{2}-\d{2}$, can be parsed into a date and are not quoted
  - ^\d{4}-q(1|2|3|4)$ is also accepted for easy quarterly tax filtering

CATEGORY_MISMATCH
  - Categories match (:{2,}|^:|:$|,|'|\"|\\n) and are quoted

AMOUNT_MISMATCH
  - Amounts match ^-?[0-9]*\.[0-9]{2}$ and are not quoted

METHOD_MISMATCH
  - Methods match (,|'|:|\"|\\n) and are quoted

NOTES_MISMATCH
  - Notes match (,|:|\"|\\n) and are quoted if they exist

SORT_BY_DATE_MISMATCH
  - Items are sorted by date

UNIQUENESS_MISMATCH
  - Items are unique
  - Set --no-unique-errors to not exit 1 if there are duplicates

INCOME_IS_NEGATIVE
  - Amounts in income related categories are negative

EXPENSE_IS_POSITIVE
  - Amounts in expense related categories are positive
```

**Performance is "good enough", here are results from my computer built in
2014 (yes 2014):**

```
plutus demo --init-benchmarks

[Generating 1000 items]
generation took 8.73ms
wrote /tmp/plutus.csv-1000 in 4.19ms
'plutus show --summary' finished reporting in 56.32ms

[Generating 10000 items]
generation took 89.73ms
wrote /tmp/plutus.csv-10000 in 41.20ms
'plutus show --summary' finished reporting in 92.88ms

[Generating 100000 items]
generation took 842.81ms
wrote /tmp/plutus.csv-100000 in 404.58ms
'plutus show --summary' finished reporting in 566.45ms

Optionally confirm these results on your own with your shell's time command:

time PLUTUS_PROFILE="/tmp/plutus.csv-1000" plutus show --summary > /dev/null
time PLUTUS_PROFILE="/tmp/plutus.csv-10000" plutus show --summary > /dev/null
time PLUTUS_PROFILE="/tmp/plutus.csv-100000" plutus show --summary > /dev/null

Remove '> /dev/null' to see the output printed, it won't take much longer,
it redirects to /dev/null to avoid spamming your terminal output
```

There's a few more options and commands but that's the core of it.

## ✨ Features

- A single CSV data file for easy backups and peace of mind to know it won't get corrupt from an upgrade
  - Supports multiple "profiles" if you want separate isolated tracking between businesses
- Since it's just lines of text in a CSV file:
  - You can easily track it in git
    - Even with being a CLI tool, you can set up CI pipelines to run reports from your phone!
  - Use whatever code editor you're comfy with for adding or editing items
  - Pipe its output into other tools if you want to do custom processing
  - View it in any spreadsheet program if you want occasional GUI features
  - Easy to write custom importers (ie. bank CSVs) since you just produce a CSV file
  - Easy to share with accountants if requested (1 file and a common format)
- Most commands only open the CSV file in read-only mode to protect against corruption
  - The few commands that write to it are super explicit (ie. `insert` and `edit`)
- An extensive `lint` command to help identify any input errors
- Categories and subcategories are unrestricted along with being easy to change later
- Flexible summary reporting options to see your data from different angles
  - For example:
    - *"How much more or less do I make during certain times of the year?"*
      - `plutus show --summary date`
    - *"Show me all of my categories so I can quickly spot off by 1 character typos"*
      - `plutus show --summary` (it's grouped by category by default)
    - *"Show me all income and business expenses for 2025"*
      - `plutus show "^2025-.*(Income|Business Expenses):" --summary-with-items`
        - This filter pattern is dependent on your category names
- Bidirectionally sort items by date (default), category, amount and more
  - Items are always sorted by date on disk in the CSV file, sorting is done in memory for displaying
- Supports creating custom aliases as shortcuts to quickly generate reports
  - This helps avoid needing to type regex filters or always passing the same flags
- Display helpful and potentially custom information with an `info` command
  - This could be example categories, tax payment schedules or anything you define
- It is reasonably fast, a sorted summary for 12,000 items takes ~100ms on my 10 year old computer
  - Printing a summary with 100,000 items takes 560ms
    - For my use case, that would be around 70 years of finance tracking
  - Printing all 12,000 item details (not a summary) takes 700ms
  - `plutus demo --init-benchmarks` will benchmark 1,000, 10,000 and 100,000 items
- Supports various formatting symbols depending on your locale and preference
  - Optionally show currency symbols / separators and display `()` instead of `-` for negatives

## ⚡️ Installation

It'll work on any Linux distro, macOS and within WSL 2 on Windows with Python
3.10+ (2021 release date) which should come installed by default on most
systems.  There's no additional packages to install.

```sh
# Install it on a well known system path that will work on most systems
sudo curl \
  -L https://raw.githubusercontent.com/nickjj/plutus/0.5.1/src/plutus \
  -o /usr/local/bin/plutus && sudo chmod +x /usr/local/bin/plutus
```

Nothing about this script requires sudo or it living in `/usr/local/bin` but
that path is available on most Linux distros, macOS and within WSL 2 on
Windows. You're more than welcome to install it for your specific user, such as
in `~/.local/bin` if you already have that set up and on your system path.

## 🚀 Getting started

You can run `plutus` to start things off. It will prompt you to set a "profile"
which is basically just your CSV file that contains your items. Don't sweat the
location, you can change it at any time in your config file.

At this point you're technically done and can start adding items to your
profile, but I would suggest running `plutus demo --init` and following the
help text.

That will create a separate demo profile that you can start using immediately
to get a feel for using this tool without spending time importing or manually
inputting your data.

The section below on using Plutus covers how everything works.

## ⚙️  Using Plutus

For actively using the tool, I encourage you to run `plutus --help`.

There is also quite a bit of help text when running the tool for the first
time. After the onboarding and demo commands it adheres to the Unix
philosophy of no news is good news.

### Commands

Here's a list of commands and flags to get a quick idea of what's available:

```
# View items
plutus show [-h] [-s FIELD] [-m [COLUMN]] [-w [COLUMN]] [-r] [PATTERN]

positional arguments:
  PATTERN               optionally filter results by a regex pattern

options:
  -h, --help            show this help message and exit
  -s FIELD, --sort FIELD
                        bidirectionally sort results by a specific field
  -m [COLUMN], --summary [COLUMN]
                        aggregate amount totals and item counts for a specific column type
  -w [COLUMN], --summary-with-items [COLUMN]
                        view both a summary of column types and items
  -r, --raw             view your profile's lines without any processing except filtering

```

```
# Insert new items
plutus insert [-h]

options:
  -h, --help  show this help message and exit
```

```
# Edit or insert items in your code editor
plutus edit [-h] [-s]

options:
  -h, --help  show this help message and exit
  -s, --sort  sort your profile and show a diff if anything changed
```

```
# View tips, examples and custom templates
plutus info [-h] [-c] [-i] [-l] [-t | -p]

options:
  -h, --help            show this help message and exit
  -c, --categories      view example categories to use as a starting point
  -i, --items           view example items to see how they are structured
  -l, --lint-rules      view the rules used to validate your profile
  -t, --template        view the custom template in your config directory
  -p, --template-example
                        view the example custom template as a reference
```

```
# Identify formatting issues
plutus lint [-h] [-r] [-E] [-U] [-W] [-a]

options:
  -h, --help            show this help message and exit
  -E, --no-errors       don't exit with status code 1 (could be useful in CI)
  -U, --no-unique-errors
                        don't exit with status code 1 if items are duplicated
  -W, --no-warnings     don't show warnings
```

```
# Generate sample data and run benchmarks
plutus demo [-h] (-n | -b)

options:
  -h, --help            show this help message and exit
  -n, --init            write a demo profile to disk
  -b, --init-benchmarks
                        write multiple demo profiles to disk and measure their performance
```

```
# View or edit your config files
plutus config [-h] [-e | -i]

options:
  -h, --help       show this help message and exit
  -e, --edit       edit your config file
  -i, --edit-info  edit your custom info template
```

```
plutus alias [-h] [NAME ...] ...

positional arguments:
  NAME        an alias name that you have defined in your config
  ARGS        any arguments will be passed directly to your alias

options:
  -h, --help  show this help message and exit
```

### Ready to add items?

There's a couple of options depending on your preference.

#### Using your code editor

The `plutus edit` command will open your profile in your code editor and now
you can add them however you see fit. Keep in mind this file is expected to be
sorted by date but manually inserting old items from years ago could be error
prone so there's a separate `plutus edit --sort` command you can run to
auto-sort the items for you.

What I like to do is always add items at the end of the file, and I even add in
a couple of line breaks before my new items so I know what's new with no
confusion as I'm editing. Then I save the file as is when I'm done.

The `plutus edit --sort` command auto-sorts them for you, removes empty lines
and shows you a diff.

#### Using Plutus

The `plutus insert` command will start an interactive prompt with you. It will
actively verify the data you enter and do its best to make adding new items
quick and painless.

I use this method when adding 1 item at a time. For multiple items I tend to
use my code editor but it really depends on your preference. Both options
exist.

### Filtering tips

Filters are regular expressions. They help you narrow down your data on
whatever criteria you're interested in. The regex is ran across the entire item
so you can match on multiple fields at once.

Here's a breakdown of some of the commands referenced earlier:

- `plutus show 2025`
  - Filter results for 2025 but under the hood Plutus will look for any regex that matches 4 digits and automatically anchor it to the start of the line with `^2025` in the regex to avoid false positives
  - Similarly `2025-q1` will get the tax year's quarter with the same `^` auto-anchoring
- `plutus show "Business Expenses:"`
  - Filter results by a category name, using `:` at the end helps avoid false positive matches since `:` can only exist in category names
- `plutus show "^2025-.*(Income|Business Expenses):"`
  - This combines both of the above examples into 1 filter
    - `^` ensures the date only matches the start of the line
    - `2025-` is anything in the year 2025, we include `-` to be even more precise
    - `.*` matches any number of any characters
    - `(Income|Business Expenses)` is an OR match for either category name
    - `:` helps reduce false positives by only including category name matches

You can optionally add `--summary` to get aggregate stats for all items that
are returned and `--summary [date|category|amount|method|notes]` to group items
by that column.

There's also `--summary-with-items` which returns both a summary and your
item's details. You should see your total at the bottom of both outputs be the
same.

### Level up with aliases

Typing regular expressions is rarely fun but you might find yourself wanting
to filter by certain dates and categories on a regular basis such as the case
to answer *"show me my income and business expenses for 2025 Q4"*.

You can totally do that with `plutus show "2025-q4-.*(Income|Business
Expenses):" --summary-with-items --sort category-`, the sort flag is a nice
touch to get your income listed before your expenses.

The above command isn't too crazy but I wouldn't want to type that every
quarter or depend on my shell's history but then have to adjust the date period.

We can do better, Plutus supports adding as many or as little aliases as you
want. Think of them like shell aliases, they're shortcuts. They also support
arguments so you can create custom reports as needed.

Here's one showing how to use variables, you can add aliases to your config
file:

```ini
[Aliases]
ibe = plutus show "^$$.*(Income|Business Expenses):.*$$.*" --summary-with-items --sort category-
```

- `ibe` is the name of the alias, it can be whatever you want (ibe = income and business expenses)
- `plutus` is the command to run, it can be anything your shell can run including pipes and redirects
- Everything else are arguments passed into the above command

`$$` is a special value, it is a variable. You can have more than one `$$`, the
above example has 2 of them. Any args you pass into the alias when you call it
will be swapped in as strings in order for each `$$` like `printf "%s %s"
"hello" "world"` on the shell. This lets your alias support arguments to make
them more generic.

As a quality of life enhancement, Plutus will detect how many variables your
alias has and if you're missing them when you run the alias they will be
replaced with empty strings.

This lets you call the above alias in a few different ways, such as:

```sh
plutus alias ibe                # get all items
plutus alias ibe 2025-q4        # filtered by 2025-q4
plutus alias ibe 2025-q4 Zelle  # filtered by 2025-q4 and Zelle
plutus alias ibe "" Zelle       # filtered by Zelle

# Here's what each of the 4 examples expand to:
plutus show "^.*(Income|Business Expenses):.*.*" --summary-with-items --sort category-
plutus show "^2025-q4.*(Income|Business Expenses):.*.*" --summary-with-items --sort category-
plutus show "^2025-q4.*(Income|Business Expenses):.*Zelle.*" --summary-with-items --sort category-
plutus show "^.*(Income|Business Expenses):.*Zelle.*" --summary-with-items --sort category-
```

I use the above alias a lot for getting quarterly numbers.

You can even create aliases to open specific directories or run any program
accessible in your shell. This can let you create shortcuts to open up finance
related things like maybe you have a `~/business/taxes/2025` directory with a
bunch of notes and files that you edit elsewhere. You can use your OS' commands
to open that directory.

### Environment variables

#### `PLUTUS_PROFILE`

Used to customize which profile (CSV file) to use.

You can either provide this environment variable when running any command such
as `PLUTUS_PROFILE=/tmp/demo.csv plutus <command>` or it will fall back to
using your default profile that you configured when first running the app.

#### `PLUTUS_CONFIG`

Used to customize the config path, such as `PLUTUS_CONFIG=/tmp/plutus.ini
plutus`. It defaults to `~/.config/plutus/config.ini` and respects
`XDG_CONFIG_HOME` if you have it defined.

Unless you have a strong preference, consider leaving it undefined and use the
default. That's because you'll need to set it every time or configure your
shell to export it if you want to use a custom path long term.

It exists mainly to make it easier for integration tests (I didn't want to
overwrite my real config) and for temporarily experimenting with a fresh set
up without needing to rename your real config.

### Config file

It exists at `~/.config/plutus/config.ini` by default and contains a few
settings:

```ini
[Settings]
# This will be your configured path when you first ran plutus.
default_profile = /home/nick/business/plutus.csv

# If True, amounts will be shown as $1,000.00 and it will read your system's
# locale to use the correct currency symbol and separator. If no locale is
# found it will fallback to using $ with commas.
#
# If False, it will be displayed straight from your CSV file, example: 1000.00.
format_amounts = True

# If False, negative amounts will be shown as -$777.77.
# If True, negative amounts will be shown as ($777.77).
format_negatives_with_parentheses = False

# Comma separated list of words to search for when linting amounts to make
# sure income is not accidentally a negative number.
#
# It is not case sensitive and partial matches are ok. For example if you have
# a category name of "Tax:Refunds" then "refund" will match.
lint_income_words = income,refund

# Comma separated list of words to search for when linting amounts to make
# sure expenses are not accidentally a positive number.
#
# It is not case sensitive and partial matches are ok. For example if you have
# a category name of "Business Expenses" then "expense" will match.
lint_expense_words = expense

[Aliases]
# Add your custom aliases here.
```

### Info template

You can create a custom template file at `~/.config/plutus/info_template.txt`
and it will be displayed when you run `plutus info --template` or `plutus info`
if you're displaying all information.

This template is to help remind you of important things like tax schedules, tax
checklists or whatever you find important or note worthy related to your
finances.

Running that command without a custom template file will provide an example
template to use as inspiration. You can always access this example with `plutus
info --template-example`.

You can quickly access your custom template with `plutus config --edit-info`.

### CSV file format

The `plutus demo --categories --items` command goes over the file format and
its syntax rules in more detail but here's the TL;DR for now to explain my
thought process:

#### Headers

- **Date**
  - YYYY-MM-DD so it's naturally sortable and easy to filter on YYYY or YYYY-MM
- **Category**
  - Break items up into filterable sections (income, taxes, business expenses, etc.)
- **Amount**
  - A positive or negative amount which gets calculated using addition or subtraction
- **Method**
  - The payment method so you know what to double check at the source
- **Notes**
  - Arbitrary metadata, it can be empty or anything you want such as tags to filter on

If the structure changes over time that's ok, it's just text. Since I use the
tool all the time I will provide a battle hardened script to do 1-off
migrations.

#### Dynamic headers

You will notice `Total` and `Items` columns in some of the outputs. These are
dynamically calculated columns and do not exist on disk. The `Total` will keep
a running total of all amounts and `Items` counts the number of items in the
result. These help you gain insight on your numbers.

#### Items

```csv
2025-10-17,"Income:Consulting",600.00,"Zelle","Johnny Tables (Flask)"
```

Each field is separated by commas and all string fields except the date always
require quotes for consistency to reduce potential parsing errors. The `lint
--rules` command explains all of the rules in more detail.

## 📑 Importing from other tools

At the moment there is an importer for GnuCash. I could see a future where
importers are added for common bank CSV export formats too. Check out the
[importers/](./src/importers/) directory for more details.

The good news is, there is nothing specific about this tool in relation to
import scripts. The GnuCash importer is a standalone script. All importers take
whatever input you have and produce a CSV file in Plutus' format.

That means you can start importing things in an automated way on your own.

## 🤝 Feedback and code contributions

There is a pretty extensive test suite and GitHub Actions runs it on every PR
commit to test things. You're more than welcome to offer suggestions and
improvements.

## 🍀 Donations

GitHub tips is available in the side bar of this repo.

I'm not expecting anything. I'm doing this because I enjoy it but if this tool
helps save you time or helps you file accurate taxes, tips would be greatly
appreciated.

## 👀 Who am I and can you trust me?

Good question, I would be asking the same thing for anything related to
finances. The code is available to look at. You're more than welcome to audit
it. Nothing phones home or anything crazy like that.

I'm just a dude on the internet who has been building and deploying web apps
for 20+ years. I [blog](https://nickjanetakis.com/blog) and create [YouTube
videos](https://www.youtube.com/c/nickjanetakis) about everything I've learned
along the way and have a bunch of other [open source
projects](https://github.com/nickjj?tab=repositories).
