# Plutus: CLI for income and expense tracking

This documentation is specific to importing data into Plutus from other tools
and formats.

## 📑 Importers

### GnuCash

```sh
# Install it on a well known system path that will work on most systems, feel
# free to adjust this path if you want, you can delete the script when you're done
sudo curl \
  -L https://raw.githubusercontent.com/nickjj/plutus/0.5.0/src/importers/import-gnucash \
  -o /usr/local/bin/import-gnucash && sudo chmod +x /usr/local/bin/import-gnucash
```

GnuCash supports exporting transactions to a CSV file. We can import from that.

`import-gnucash --help` has a walk through on how to perform the export and
contains a number of example commands and import strategies.

Here's one to look at and a mini guide on how I imported ~60 GnuCash accounts
in about 30 minutes which included spending time thinking about how I wanted to
refactor my categories after nearly a decade of usage.

```sh
# Import a specific GnuCash account and change the plutus category to
# something different (Consulting to Freelancing)
import-gnucash \
  --gnucash-account "Income:Consulting" \
  --plutus-category "Income:Freelancing" \
  --payment-method ACH \
  --input /tmp/gnucash.csv
```

The above command won't write anything to disk, it prints a bunch of debug
information so you can verify the data before you supply an `--output <path>`
flag.

Here's a small subset of output from my GnuCash export with a bit of anonymous
data. The first line is what will be written to your Plutus profile. The DEBUG
line includes the GnuCash CSV line number, a running total to help verify the
amounts in GnuCash along with an array of the exact line from GnuCash's CSV:

```
2017-01-06,"Income:Consulting",2100.00,"ACH","X"
DEBUG (117 - $2100.00): ['Fri, 01/06/2017', 'Income:Consulting', '', 'X', 'Assets', 'n', '$(2,100.00)', '(2,100.00)', '1.0000']

2017-04-27,"Income:Consulting",2750.00,"ACH","X"
DEBUG (118 - $4850.00): ['Thu, 04/27/2017', 'Income:Consulting', '', 'X', 'Assets', 'n', '$(2,750.00)', '(2,750.00)', '1.0000']

2017-05-19,"Income:Consulting",500.00,"ACH","X"
DEBUG (119 - $5350.00): ['Fri, 05/19/2017', 'Income:Consulting', '', 'X', 'Assets', 'n', '$(500.00)', '(500.00)', '1.0000']
```

You can go through your GnuCash accounts 1 by 1 and run commands until you're
done. Run it once for each account without `--output` to verify the numbers and
then add `--output` when you're happy.

In my case 10,000+ items were imported and there wasn't a single discrepancy or
manual adjustment needed. Everything lined up to the penny.

The command is idempotent (it won't add the same items twice). Once you supply
the `--output <path>` flag it will tell you how many new items were appended to
the file, such as `OK: 197 items were appended to /tmp/test.csv`.

I highly suggest running the commands with your Plutus CSV file open in a
code editor off to the side. This way you can undo the changes easily in case
you want to revert the latest import command.

### Custom importers

You can look at the GnuCash one as a guide but really it's just taking data
from a source and writing CSV items to a file in the format that Plutus
expects.

Depending on what you're doing an importer could be as simple as using a combo
of `grep`, `cut` and `sed` with a few lines of shell scripting to write the
results out somewhere. I whipped up a proof of concept GnuCash importer in ~10
minutes using this strategy but decided to expand on it in Python for
robustness.
