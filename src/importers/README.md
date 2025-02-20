# Plutus: CLI for income and expense tracking

This documentation is specific to importing data into Plutus from other tools
and data sources.

## 📑 Importers

All of the importers try to follow these philosophies:

- Your Plutus profile is a sacred file and should never be directly modified
- Your input file (bank CSV export, etc.) should never be directly modified
- Idempotent so if you run it more than once it won't keep adding duplicates
- Provide a number of outputs to help you understand every single item being parsed
- Make it as easy as possible to take these outputs and import them into your profile
- Flexible category mappings so you can balance correctness vs convenience

### General CSV

```sh
# Install it on a well known system path that will work on most systems, feel
# free to adjust this path if you want.
sudo curl \
  -L https://raw.githubusercontent.com/nickjj/plutus/0.6.1/src/importers/import-general-csv \
  -o /usr/local/bin/import-general-csv && sudo chmod +x /usr/local/bin/import-general-csv
```

This is aimed at importing data from any CSV file that has at least the
following 3 columns:

- Date
  - Records when the transaction occurred
- Amount
  - Tracks how much the transaction was for
- Category or description
  - So you can map it to a category or note

Here's a few use cases on how I used this importer to import thousands of items
from GnuCash along with bank exports for both a checking account and credit
card. Everything worked without any manual adjustments or "fixing" files. I'm
really happy with how it turned out and importing new items is painless.

We'll go over the CSV file formats first and focus on how regex filtering works
afterwards.

#### GnuCash (accounting tool)

*You can export your GnuCash transaction to a CSV file. When doing so please
enable "Use Quotes" and "Simple Layout" in the export settings.*

CSV export file format:

```
"Date","Account Name","Number","Description","Full Category Path","Reconcile","Amount With Sym","Amount Num.","Rate/Price"
"Fri, 03/01/2024","Assets","","Invoice","Business Expenses:DigitalOcean","n","$(12.00)","(12.00)","1.0000"
```

- The date is column 0 `Fri, 03/01/2024`
- The amount is column 7 `(12.00)`
- The note is column 3 `Invoice`
- The category mapping is column 4 `Business Expenses:DigitalOcean`

#### Chase Checking (bank)

*Most banks support exporting your transactions to a CSV file.*

CSV export file format:

```
Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #
DEBIT,01/02/2024,"DIGITALOCEAN.COM DIGITALOCEAN. NY            01/01",-12.00,DEBIT_CARD,555.55,,
```

- The date is column 1 `01/02/2024`
- The amount is column 3 `-12.00`
- The note / category mapping is column 2 `DIGITALOCEAN.COM DIGITALOCEAN. NY            01/01`

#### Chase Freedom (credit card)

*Most credit cards support exporting your transactions to a CSV file.*

CSV export file format:

```
Transaction Date,Post Date,Description,Category,Type,Amount,Memo
12/01/2024,12/01/2024,DIGITALOCEAN.COM,Shopping,Sale,-12.00,
```

- The date is column 0 `12/01/2024`
- The amount is column 5 `-12.00`
- The note / category mapping is column 2 `DIGITALOCEAN.COM`

#### Regex filtering

There's 2 different sections. Ignoring items and mapping categories.

Ignoring items can be useful if you know for sure you don't want to track these
items in Plutus. Maybe you don't care about them for whatever reasons you have.

Mapping categories is how you can say "this item needs to be placed in XYZ"
because doing all of that by hand for hundreds or thousands of items would be
painful.

Both filters can be set in `~/.config/plutus/import-general-csv.ini` and you
can have as many as you'd like. Each entry goes on its own new line in its
respective section:

```ini
[Ignore]
# The key (left) is ignored, it can be literally anything.
# The value (right) is the regex to search for in the line being processed.
_ = ^(CREDIT|DEBIT),.+STRIPE           TRANSFER   ST-.+ CCD ID: .+ACH_(CREDIT|DEBIT).+
# In this example I wanted to ignore Stripe transactions because I track Stripe
# income and expenses through my course platform and Stripe's dashboards.

[Map_Categories]
# The key (left) is what category you want it to be in Plutus.
# The value (right) is the regex to search for in the line being processed.
Business Expenses:Hosting:DigitalOcean = ^.+,"Business Expenses:DigitalOcean","n",.+
# In this example I wanted to refactor my GnuCash categories to namespace
# DigitalOcean in a Hosting sub-category.

# In this example I wanted to map DigitalOcean payments to its respective
# category. Unlike GnuCash, this pattern is different because it matches either
# debit card or credit card lines but the concept is the same.
Business Expenses:Hosting:DigitalOcean = (^DEBIT,.+|,)?DIGITALOCEAN.COM ?.+(DEBIT_CARD|Sale),.+
```

Now we have everything in place to perform the import:

```sh
import-general-csv \
  --input /tmp/chase-checking.csv \
  --input-col-indexes 1,3,2 \
  --payment-method ChaseChecking \
  --profile /tmp/plutus.csv
```

Notice `--input-col-indexes 1,3,2` matches up with the Chase checking bank
CSV file.  We also supply the `--payment-method` so Plutus knows where this
transaction originated from.

You can keep re-running this script while you add more filters and ensure your
items get categorized correctly.

#### Outputs

There are 2 types of outputs. There's running this script normally and also
providing the `--summary` flag.

##### Running this script normally

I've broken the output up into sections so we can go over each part.

There were hundreds of items output but I only included the last one below:

```
2024-01-02,"Business Expenses:Hosting:DigitalOcean",-12.00,"ChaseChecking","DIGITALOCEAN.COM DIGITALOCEAN. NY            01/01"
DEBUG (#60 on L582 - -1337.00): DEBIT,01/02/2024,"DIGITALOCEAN.COM DIGITALOCEAN. NY            01/01",-12.00,DEBIT_CARD,3485.70,,
```

- Each item is output in the format Plutus expects
- DEBUG output is shown to help you verify everything (it's color coded)
  - `#60` is the item count for new items being added
  - `L582` is the line number in your input CSV file
  - `-1337.00` is a running total of new items
  - Everything else is the raw line being processed

What the above shows is our regex filter worked to map the DigitalOcean bank
transaction to `Business Expenses:Hosting:DigitalOcean`. If the mapping didn't
work the category will be `TODOUnknown` in red so you know it needs to be
handled. We're also able to verify the date was parsed correctly, the amount is
good, the payment method is good and the bank description was included as a
note.

```
OK: 514 ignored items were written to /tmp/plutus-import-general-csv-ChaseChecking-ignored.csv
OK: 8 skipped items were written to /tmp/plutus-import-general-csv-ChaseChecking-skipped.csv
OK: 60 new items were written to /tmp/plutus-import-general-csv-ChaseChecking-new.csv
OK: 582 items were parsed
```

*I used real numbers from my original import.*

There were 514 ignored items because my real `[Ignore]` list has quite a few
things. Ignored items are not printed to the screen.

There were 8 skipped items because the importer checked each item against your
profile and saw it existed already. In my case I already added 8 of those items
in manually before this script was written. It compares the raw Plutus item but
ignores notes in case you change them. Skipped items are not printed to the
screen.

There were 60 new items and these could be added to your profile pending your
human review.

```
WARNING: 2 new items are uncategorized as TODOUnknown
```

There's also a warning that shows you a count of your uncategorized items. You
can scroll up in your terminal to find them or pipe the output of this script
to grep such as `... | grep TODOUnknown` to quickly see them all. The warning
is meant to let you know they exist at a glance.

```sh
PLUTUS_PROFILE="/tmp/plutus-import-general-csv-ChaseChecking-ignored.csv" plutus show --summary-with-items --sort category
PLUTUS_PROFILE="/tmp/plutus-import-general-csv-ChaseChecking-skipped.csv" plutus show --summary-with-items --sort category
PLUTUS_PROFILE="/tmp/plutus-import-general-csv-ChaseChecking-new.csv" plutus show --summary-with-items --sort category
```

In all 3 cases, individual files were created for you to investigate for
correctness. They are valid Plutus files so you can explore them quickly.

When you're happy with everything you can copy the new items into your real
Plutus profile. This script provides additional help and tips when you run it.

##### Summary

This script supports an optional `--summary` flag which will go through your
input CSV file and group up each unique value for each column you have. It does
this for all of your items. This can help you explore your data quickly,
perhaps to help with knowing which regex filters to create.

For example, here's a few columns from a Chase credit card file:

```
Column 3: "Category" (14)
  Education
  Travel
  Groceries
  Entertainment
  Professional Services
  Bills & Utilities
  Health & Wellness
  Shopping
  Gas
  Food & Drink
  Fees & Adjustments
  Gifts & Donations
  Automotive
  Home

Column 4: "Type" (5)
  Fee
  Payment
  Sale
  Return
  Adjustment
```

With a lot of items this can create a lot of output. Maybe you only care about
specific columns. In that case you can supply `--summary 2,3` to only show
those columns instead of everything by default.

##### Conclusion

I was able to import everything from my bank accounts, complete with writing
regex filters in about half an hour. Keep in mind that's a year's worth of
transactions and now that most of the regex filters are set up it will be much
quicker moving forward.

#### Correctness vs convenience with category mappings

This is up to you depending on your preference. Here's a few ways to think
about it.

If you go full convenience mode you can choose to leave everything as
`TODOUnknown` because the amounts will even out since they are positive and
negative. That means you don't have to write any regular expressions except
maybe for the things you want to ignore.

If you go full correctness mode it would mean writing regex filters for every
item to have it perfectly categorized. A lot of items will be captured from a
single regex (like 12 monthly transactions for 1 service in a year) so it's not
too bad unless you buy a ton of stuff from many different places.

You can also meet somewhere in the middle by filtering on common credit card
categories that exist in your bank's CSV file. This way everything gets
bucketed into your customized categories and you're leaning on your credit card
company to do the heavy lifting to categorize items correctly. Then you can
write custom filters to make adjustments. Make sure your more specific filters
are defined before the general ones because the first match wins.

Another approach would be the 80 / 20 rule. Write filters for things that need
to be correct like business income or expenses and leave the rest as
`TODOUnknown` or let them get auto-categorized by your credit card company.

Personally I ensured all of my business income and expenses were rock solid,
then wrote a few regex filters to categorize my credit card company's
categories into the names I wanted to use and polished things off with a few
more regular expressions to use more specific category names on a few things.

### Custom importers

You can look at the General CSV importer as a guide but really it's just taking
data from a source and writing CSV items to a file in the format that Plutus
expects.

Depending on what you're doing an importer could be as simple as using a combo
of `grep`, `cut` and `sed` with a few lines of shell scripting to write the
results out somewhere. I whipped up a proof of concept GnuCash importer in ~10
minutes using this strategy but decided to expand on it in Python to make it
general purpose. An entire day later I accidentally wrote a general purpose CSV
importing tool.
