import configparser
import contextlib
import importlib.util
import io
import os
import sys
import unittest
from subprocess import PIPE
from subprocess import Popen

PLUTUS = None
TEST_CONFIG = "/tmp/plutus.ini"
TEST_PROFILE = "/tmp/plutus.csv"


def load_plutus_module():
    # This was an adventure to be able to load the src/plutus module without
    # it having a .py file extension.
    module_path = "src/plutus"
    module_name = "module_name"

    spec = importlib.util.spec_from_file_location(module_name, module_path)

    sys.argv = ["src/plutus"]

    if spec is None:
        spec = importlib.machinery.ModuleSpec(module_name, None)
        spec.loader = importlib.machinery.SourceFileLoader(
            module_name, module_path
        )

    module = importlib.util.module_from_spec(spec)

    sys.modules[module_name] = module

    spec.loader.exec_module(module)

    return module


def call_script(*args):
    args = list(args)
    args.insert(0, "src/plutus")

    # Remove None items from the args.
    args = [arg for arg in args if arg is not None]

    process = Popen(args, stdout=PIPE, stderr=PIPE, text=True)
    stdout, stderr = process.communicate()
    rc = process.returncode

    return stdout, stderr, rc


def replace_csv_line(line_number, line, extra_lint_flag=None):
    with open(TEST_PROFILE) as file:
        lines = file.readlines()

    original_line = lines[line_number]

    lines[line_number] = f"{line}\n"

    with open(TEST_PROFILE, "w") as file:
        file.writelines(lines)

    stdout, stderr, rc = call_script("lint", extra_lint_flag)

    lines[line_number] = original_line

    with open(TEST_PROFILE, "w") as file:
        file.writelines(lines)

    return stdout, stderr, rc


def replace_config_line(setting, old_value, new_value, *command):
    with open(TEST_CONFIG) as file:
        lines = file.readlines()

    original_line_number = None
    original_line = ""

    for i, line in enumerate(lines):
        if setting in line:
            original_line_number = i
            original_line = line
            lines[i] = line.replace(old_value, new_value)

    with open(TEST_CONFIG, "w") as file:
        file.writelines(lines)

    stdout, stderr, rc = call_script(*command)

    lines[original_line_number] = original_line

    with open(TEST_CONFIG, "w") as file:
        file.writelines(lines)

    return stdout, stderr, rc


class TestCLI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.path.exists(TEST_CONFIG):
            PLUTUS = load_plutus_module()

            config = configparser.ConfigParser()

            config["Settings"] = PLUTUS.CONFIG_DEFAULTS | {
                "default_profile": TEST_PROFILE
            }

            os.makedirs(os.path.dirname(TEST_CONFIG), exist_ok=True)
            with open(TEST_CONFIG, "w") as file:
                config.write(file)

        os.environ["PLUTUS_CONFIG"] = TEST_CONFIG
        _stdout, _stderr, _rc = call_script(
            "demo", "--init", "--no-dynamic-years"
        )

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(TEST_PROFILE)
            os.remove(TEST_CONFIG)
        except OSError:
            pass

    def setUp(self):
        os.environ["LC_ALL"] = "en_US.UTF-8"
        os.environ["PLUTUS_PROFILE"] = TEST_PROFILE
        os.environ["EDITOR"] = "cat"

    def test_missing_profile(self):
        os.environ["PLUTUS_PROFILE"] = "tmp/invalid.csv"

        stdout, _stderr, rc = call_script("show")

        self.assertIn("MISSING_PROFILE", stdout)
        self.assertEqual(rc, 1)

    def test_demo_categories(self):
        stdout, _stderr, _rc = call_script("demo", "--categories")

        lines = stdout.splitlines()

        first_category = "Business Expenses:Accountant"
        last_category = "Tax:Refunds"

        expected_categories = [first_category, last_category]
        actual_categories = []

        for line in lines:
            if line == first_category:
                actual_categories.append(line)
            elif line == last_category:
                actual_categories.append(line)

        # This does check to make sure they are sorted correctly.
        self.assertEqual(expected_categories, actual_categories)
        self.assertNotIn("SCRIPT_NAME", stdout)

    def test_demo_items(self):
        stdout, _stderr, _rc = call_script("demo", "--items")

        lines = stdout.splitlines()

        first_line = '2024-01-12,"Personal Expenses:Transportation",-20.01,"FreedomCard","Gas"'  # noqa: E501
        last_line = '2025-12-30,"Income:Affiliates:Amazon",234.56,"ACH",'

        expected_headers = "Date,Category,Amount,Method,Notes"
        actual_headers = ""

        expected_items = [first_line, last_line]
        actual_items = []

        for line in lines:
            if line == expected_headers:
                actual_headers = expected_headers

            if line == first_line:
                actual_items.append(line)
            elif line == last_line:
                actual_items.append(line)

        self.assertEqual(expected_headers, actual_headers)
        self.assertEqual(expected_items, actual_items)
        self.assertNotIn("SCRIPT_NAME", stdout)

    def test_demo_items_benchmark(self):
        PLUTUS = load_plutus_module()

        categories = ["a", "b"]

        # Without this, the output was always being printed to stdout.
        with contextlib.redirect_stdout(io.StringIO()):
            PLUTUS.run_demo_benchmark(10, categories)

        items = []
        benchmark_profile_path = f"{PLUTUS.DEMO_PROFILE}-10"
        with open(benchmark_profile_path) as file:
            for line in file:
                items.append(line.strip())

        self.assertEqual(11, len(items))
        self.assertEqual(items[0], PLUTUS.CSV_HEADERS)
        self.assertEqual(items[1].count(","), 4)

        if os.path.exists(benchmark_profile_path):
            os.remove(benchmark_profile_path)

    def test_lint_rules(self):
        stdout, _stderr, _rc = call_script("lint", "--rules")
        self.assertIn("CSV headers match", stdout)

    def test_lint_valid(self):
        stdout, _stderr, _rc = call_script("lint")
        self.assertEqual("", stdout)

    def test_lint_invalid_headers(self):
        stdout, _stderr, rc = replace_csv_line(
            0, "Oops,Bad,Headers,Exist,,Here"
        )

        self.assertIn("CSV_HEADERS_MISMATCH", stdout)
        self.assertIn("1 linting error", stdout)
        self.assertEqual(1, rc)

        stdout, _stderr, rc = replace_csv_line(
            0, "Oops,Bad,Headers,Exist,,Here", "--no-errors"
        )
        self.assertIn("CSV_HEADERS_MISMATCH", stdout)
        self.assertIn("1 linting error", stdout)  # We still want the help text
        self.assertEqual(0, rc)

    def test_lint_invalid_item_count(self):
        stdout, _stderr, rc = replace_csv_line(1, "a,b,c")
        self.assertIn("PARSE_FAILURE", stdout)
        self.assertIn("L2", stdout)
        self.assertIn("2 commas", stdout)
        self.assertEqual(1, rc)

    def test_lint_invalid_whitespace_empty(self):
        stdout, _stderr, rc = replace_csv_line(3, '2024-01-12,"A",0.01,"",')
        self.assertIn("WHITESPACE_MISMATCH", stdout)
        self.assertIn("L4", stdout)
        self.assertEqual(1, rc)

    def test_lint_invalid_date(self):
        stdout, _stderr, rc = replace_csv_line(3, 'a2024-01-12,"A",0.01,"B",')
        self.assertIn("DATE_MISMATCH", stdout)
        self.assertEqual(1, rc)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-99-12,"A",0.01,"B",')
        self.assertIn("DATE_MISMATCH", stdout)

    def test_lint_invalid_category(self):
        stdout, _stderr, rc = replace_csv_line(1, '2024-01-12,":A",0.01,"B",')
        self.assertIn("CATEGORY_MISMATCH", stdout)
        self.assertEqual(1, rc)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-01-12,"A:",0.01,"B",')
        self.assertIn("CATEGORY_MISMATCH", stdout)

        stdout, _stderr, _rc = replace_csv_line(
            1, '2024-01-12,"A::B",0.01,"B",'
        )
        self.assertIn("CATEGORY_MISMATCH", stdout)

        stdout, _stderr, _rc = replace_csv_line(
            1, '2024-01-12,"A,B",0.01,"B",'
        )
        self.assertIn("CATEGORY_MISMATCH", stdout)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-01-12,A,0.01,"B",')
        self.assertIn("CATEGORY_MISMATCH", stdout)

        stdout, _stderr, _rc = replace_csv_line(
            1, '2024-01-12,"\'A",0.01,"B",'
        )
        self.assertIn("CATEGORY_MISMATCH", stdout)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-01-12,""A",0.01,"B",')
        self.assertIn("CATEGORY_MISMATCH", stdout)

    def test_lint_invalid_amount(self):
        stdout, stderr, rc = replace_csv_line(1, '2024-01-12,"A",+1.00,"B",')
        self.assertIn("AMOUNT_MISMATCH", stdout)
        self.assertEqual(1, rc)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-01-12,"A",100,"B",')
        self.assertIn("AMOUNT_MISMATCH", stdout)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-01-12,"A",--1,"B",')
        self.assertIn("PARSE_FAILURE", stdout)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-01-12,"A",ZZZ,"B",')
        self.assertIn("PARSE_FAILURE", stdout)

    def test_lint_warning_amount(self):
        stdout, stderr, rc = replace_csv_line(
            1, '2024-01-12,"Income",-1.00,"B",'
        )
        self.assertIn("INCOME_IS_NEGATIVE", stdout)

        stdout, stderr, rc = replace_csv_line(
            1, '2024-01-12,"Tax:Refunds",-1.00,"B",'
        )
        self.assertIn("INCOME_IS_NEGATIVE", stdout)

        stdout, stderr, rc = replace_csv_line(
            1, '2024-01-12,"Business Expense",1.00,"B",'
        )
        self.assertIn("EXPENSE_IS_POSITIVE", stdout)

    def test_lint_warning_amount_ignored(self):
        stdout, stderr, rc = replace_csv_line(
            1, '2024-01-12,"Income",-1.00,"B",', "--no-warnings"
        )
        self.assertNotIn("INCOME_IS_NEGATIVE", stdout)

        stdout, stderr, rc = replace_csv_line(
            1, '2024-01-12,"Tax:Refunds",-1.00,"B",', "--no-warnings"
        )

        self.assertNotIn("INCOME_IS_NEGATIVE", stdout)

        stdout, stderr, rc = replace_csv_line(
            1, '2024-01-12,"Business Expense",1.00,"B",', "--no-warnings"
        )
        self.assertNotIn("EXPENSE_IS_POSITIVE", stdout)

    def test_lint_invalid_method(self):
        stdout, stderr, rc = replace_csv_line(1, '2024-01-12,"A",1.00,"B\'",')
        self.assertIn("METHOD_MISMATCH", stdout)
        self.assertEqual(1, rc)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-01-12,"A",1.00,"B:",')
        self.assertIn("METHOD_MISMATCH", stdout)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-01-12,"A",1.00,B,')
        self.assertIn("METHOD_MISMATCH", stdout)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-01-12,"A",1.00,"B"",')
        self.assertIn("FIELDS_COUNT_MISMATCH", stdout)

    def test_lint_invalid_notes(self):
        stdout, _stderr, rc = replace_csv_line(
            1, '2024-01-12,"A",1.00,"B","C:"'
        )
        self.assertIn("NOTES_MISMATCH", stdout)
        self.assertEqual(1, rc)

        stdout, _stderr, _rc = replace_csv_line(1, '2024-01-12,"A",1.00,"B",C')
        self.assertIn("NOTES_MISMATCH", stdout)

        stdout, _stderr, _rc = replace_csv_line(
            1, '2024-01-12,"A",1.00,"B","C""'
        )
        self.assertIn("FIELDS_COUNT_MISMATCH", stdout)

    def test_lint_invalid_sort(self):
        first_line = '2024-01-12,"Personal Expenses:Transportation",-20.01,"FreedomCard","Gas"'  # noqa: E501
        last_line = '2025-12-30,"Income:Affiliates:Amazon",234.56,"ACH",'

        with open(TEST_PROFILE) as file:
            lines = file.readlines()

        # Swap the lines.
        lines[1] = f"{last_line}\n"
        lines[-1] = f"{first_line}\n"

        with open(TEST_PROFILE, "w") as file:
            file.writelines(lines)

        stdout, _stderr, rc = call_script("lint")

        # Swap the lines back.
        lines[1] = f"{first_line}\n"
        lines[-1] = f"{last_line}\n"

        with open(TEST_PROFILE, "w") as file:
            file.writelines(lines)

        self.assertIn("SORT_BY_DATE_MISMATCH", stdout)
        self.assertIn("@@ -1,4 +1,4 @@", stdout)
        self.assertEqual(1, rc)

    def test_lint_invalid_uniqueness(self):
        duplicate_line = '2025-12-30,"Income:Affiliates:Amazon",234.56,"ACH",'

        with open(TEST_PROFILE, "a") as file:
            file.write(f"{duplicate_line}\n")

        stdout, _stderr, rc = call_script("lint")

        self.assertIn("UNIQUENESS_MISMATCH", stdout)
        self.assertIn("@@ -30,4 +30,3 @@", stdout)
        self.assertEqual(1, rc)

        _, _, rc_no_uniue_errors = call_script("lint", "--no-unique-errors")

        with open(TEST_PROFILE) as file:
            lines = file.readlines()

        # Restore the file back without the duplicate.
        del lines[-1]

        with open(TEST_PROFILE, "w") as file:
            file.writelines(lines)

        self.assertEqual(0, rc_no_uniue_errors)

    def test_show(self):
        stdout, _stderr, _rc = call_script("show")

        lines = stdout.splitlines()

        self.assertEqual(len(lines), 35)
        self.assertIn("| Date", stdout)
        self.assertIn("2025-12-30", lines[-1])
        self.assertIn("Income:Affiliates:Amazon", lines[-1])
        self.assertIn("$234.56", lines[-1])
        self.assertIn("ACH", lines[-1])
        self.assertIn("-$440.23", lines[-1])

    def test_show_filtered_by_q3(self):
        stdout, _stderr, _rc = call_script("show", "2025-q3")

        lines = stdout.splitlines()

        self.assertEqual(len(lines), 10)
        self.assertIn("2025-06-05", lines[3])
        self.assertIn("2025-08-18", lines[9])

    def test_show_raw(self):
        stdout, _stderr, _rc = call_script("show", "--raw")
        self.assertIn("Date,Category,Amount,Method,Notes", stdout)
        self.assertIn(
            '2024-01-12,"Personal Expenses:Transportation",-20.01,"FreedomCard","Gas"',  # noqa: E501
            stdout,
        )

    def test_show_raw_filtered(self):
        stdout, _stderr, _rc = call_script("show", "2025", "--raw")
        self.assertIn("Date,Category,Amount,Method,Notes", stdout)
        self.assertNotIn(
            '2024-01-12,"Personal Expenses:Transportation",-20.01,"FreedomCard","Gas"',  # noqa: E501
            stdout,
        )

    def test_show_sort_by_date(self):
        stdout, _stderr, _rc = call_script("show", "--sort", "date")

        lines = stdout.splitlines()

        self.assertIn("2024-01-12", lines[3])
        self.assertIn("2025-12-30", lines[-1])

    def test_show_sort_by_date_rev(self):
        stdout, _stderr, _rc = call_script("show", "--sort", "date-")

        lines = stdout.splitlines()

        self.assertIn("2025-12-30", lines[3])
        self.assertIn("2024-01-12", lines[-1])
        self.assertIn("Gas", lines[-1])

    def test_show_sort_by_category(self):
        stdout, _stderr, _rc = call_script("show", "--sort", "category")

        lines = stdout.splitlines()

        self.assertIn("Business Expenses:Affiliates", lines[3])
        self.assertIn("Tax:Refunds", lines[-1])

    def test_show_sort_by_category_rev(self):
        stdout, _stderr, _rc = call_script("show", "--sort", "category-")

        lines = stdout.splitlines()

        self.assertIn("Tax:Refunds", lines[3])
        self.assertIn("Business Expenses:Affiliates", lines[-1])

    def test_show_sort_by_amount(self):
        stdout, _stderr, _rc = call_script("show", "--sort", "amount")

        lines = stdout.splitlines()

        self.assertIn("-$3,200.00", lines[3])
        self.assertIn("-$440.23", lines[-1])

    def test_show_sort_by_amount_rev(self):
        stdout, _stderr, _rc = call_script("show", "--sort", "amount-")

        lines = stdout.splitlines()

        self.assertIn("-$3,200.00", lines[-1])
        self.assertIn("-$440.23", lines[-1])

    def test_show_sort_by_method(self):
        stdout, _stderr, _rc = call_script("show", "--sort", "method")

        lines = stdout.splitlines()

        self.assertIn("ACH", lines[3])
        self.assertIn("Zelle", lines[-1])

    def test_show_sort_by_method_rev(self):
        stdout, _stderr, _rc = call_script("show", "--sort", "method-")

        lines = stdout.splitlines()

        self.assertIn("Zelle", lines[3])
        self.assertIn("ACH", lines[-1])

    def test_show_sort_by_notes(self):
        stdout, _stderr, _rc = call_script("show", "--sort", "notes")

        lines = stdout.splitlines()

        self.assertIn("2024-04-30", lines[3])
        self.assertIn("nickjanetakis.com", lines[-1])

    def test_show_sort_by_notes_rev(self):
        stdout, _stderr, _rc = call_script("show", "--sort", "notes-")

        lines = stdout.splitlines()

        self.assertIn("nickjanetakis.com", lines[3])
        self.assertIn("2024-04-30", lines[-1])

    def test_show_summary(self):
        stdout, _stderr, _rc = call_script("show", "--summary")

        lines = stdout.splitlines()

        self.assertEqual(len(lines), 19)
        self.assertIn("| Category", lines[1])
        self.assertIn("Tax:Refunds", lines[-1])
        self.assertIn("$1,850.00", lines[-1])
        self.assertIn("$440.23", lines[-1])
        self.assertIn("2", lines[-1])
        self.assertIn("32", lines[-1])

    def test_show_summary_date(self):
        stdout, _stderr, _rc = call_script("show", "--summary", "date")

        lines = stdout.splitlines()

        self.assertEqual(len(lines), 31)
        self.assertIn("| Date", lines[1])
        self.assertIn("2025-12-30", lines[-1])
        self.assertIn("$234.56", lines[-1])
        self.assertIn("$440.23", lines[-1])
        self.assertIn("| 1", lines[-1])
        self.assertIn("| 32", lines[-1])

    def test_show_summary_amount(self):
        stdout, _stderr, _rc = call_script("show", "--summary", "amount")

        lines = stdout.splitlines()

        self.assertEqual(len(lines), 31)
        self.assertIn("| Amount", lines[1])
        self.assertIn("1614.0", lines[-1])
        self.assertIn("$1,614.00", lines[-1])
        self.assertIn("-$440.23", lines[-1])
        self.assertIn("| 1", lines[-1])
        self.assertIn("| 32", lines[-1])

    def test_show_summary_method(self):
        stdout, _stderr, _rc = call_script("show", "--summary", "method")

        lines = stdout.splitlines()

        self.assertEqual(len(lines), 10)
        self.assertIn("| Method", lines[1])
        self.assertIn("Zelle", lines[-1])
        self.assertIn("$1,217.68", lines[-1])
        self.assertIn("$440.23", lines[-1])
        self.assertIn("| 5", lines[-1])
        self.assertIn("| 32", lines[-1])

    def test_show_summary_notes(self):
        stdout, _stderr, _rc = call_script("show", "--summary", "notes")

        lines = stdout.splitlines()

        self.assertEqual(len(lines), 21)
        self.assertIn("| Notes", lines[1])
        self.assertIn("nickjanetakis.com", lines[-1])
        self.assertIn("-$10.95", lines[-1])
        self.assertIn("$440.23", lines[-1])
        self.assertIn("| 1", lines[-1])
        self.assertIn("| 32", lines[-1])

    def test_show_summary_sort_by_category(self):
        stdout, _stderr, _rc = call_script("show", "-m", "--sort", "category")

        lines = stdout.splitlines()

        self.assertIn("Business Expenses:Affiliates", lines[3])
        self.assertIn("Tax:Refunds", lines[-1])

    def test_show_summary_sort_by_category_rev(self):
        stdout, _stderr, _rc = call_script("show", "-m", "--sort", "category-")

        lines = stdout.splitlines()

        self.assertIn("Tax:Refunds", lines[3])
        self.assertIn("Business Expenses:Affiliates", lines[-1])

    def test_show_summary_sort_by_amount(self):
        stdout, _stderr, _rc = call_script("show", "-m", "--sort", "amount")

        lines = stdout.splitlines()

        self.assertIn("-$4,800.00", lines[3])
        self.assertIn("$3,000.00", lines[-1])

    def test_show_summary_sort_by_amount_rev(self):
        stdout, _stderr, _rc = call_script("show", "-m", "--sort", "amount-")

        lines = stdout.splitlines()

        self.assertIn("$3,000.00", lines[3])
        self.assertIn("-$4,800.00", lines[-1])

    def test_show_summary_sort_by_items(self):
        stdout, _stderr, _rc = call_script("show", "-m", "--sort", "items")

        lines = stdout.splitlines()

        self.assertIn("Business Expenses:Dining Out", lines[3])
        self.assertIn("1", lines[3])
        self.assertIn("Income:Consulting", lines[-1])
        self.assertIn("4", lines[-1])

    def test_show_summary_sort_by_items_rev(self):
        stdout, _stderr, _rc = call_script("show", "-m", "--sort", "items-")

        lines = stdout.splitlines()

        self.assertIn("Income:Consulting", lines[3])
        self.assertIn("4", lines[3])
        self.assertIn("Business Expenses:Dining Out", lines[-1])
        self.assertIn("1", lines[-1])

    def test_show_summary_with_items(self):
        stdout, _stderr, _rc = call_script("show", "--summary-with-items")

        lines = stdout.splitlines()

        self.assertEqual(len(lines), 56)
        self.assertIn("| Category", lines[1])
        self.assertIn("$42.60", lines[3])
        self.assertIn("| Date", lines[22])
        self.assertIn("$20.01", lines[24])

    def test_show_format_amounts(self):
        stdout, _stderr, _rc = replace_config_line(
            "format_amounts", "True", "False", "show"
        )

        lines = stdout.splitlines()

        self.assertEqual(len(lines), 35)
        self.assertNotIn("-$440.23", lines[-1])
        self.assertIn("-440.23", lines[-1])

    def test_show_format_negatives_with_parentheses(self):
        stdout, _stderr, _rc = replace_config_line(
            "format_negatives_with_parentheses", "False", "True", "show"
        )

        lines = stdout.splitlines()

        self.assertEqual(len(lines), 35)
        self.assertNotIn("-$1,600.00", lines[7])
        self.assertIn("($1,600.00)", lines[7])

    def test_edit(self):
        stdout, _stderr, _rc = call_script("edit")
        self.assertIn("Date,Category,Amount,Method,Notes", stdout)

    def test_edit_sort_without_changes(self):
        stdout, _stderr, _rc = call_script("edit", "--sort")
        self.assertEqual(stdout, "")

    def test_edit_sort_with_changes(self):
        first_line = '2024-01-12,"Personal Expenses:Transportation",-20.01,"FreedomCard","Gas"'  # noqa: E501
        last_line = '2025-12-30,"Income:Affiliates:Amazon",234.56,"ACH",'

        with open(TEST_PROFILE) as file:
            lines = file.readlines()

        # Swap the lines.
        lines[1] = f"{last_line}\n"
        lines[-1] = f"{first_line}\n"

        with open(TEST_PROFILE, "w") as file:
            file.writelines(lines)

        stdout, _stderr, _rc = call_script("edit", "--sort")

        with open(TEST_PROFILE) as file:
            lines = file.readlines()

        expected_headers = "Date,Category,Amount,Method,Notes"
        expected_items = [f"{first_line}", f"{last_line}"]

        self.assertIn("@@ -1,4 +1,4 @@", stdout)
        self.assertEqual(lines[0].strip(), expected_headers.strip())
        self.assertEqual([lines[1].strip(), lines[-1].strip()], expected_items)

    def test_config(self):
        stdout, _stderr, _rc = call_script("config")

        self.assertIn("default_profile", stdout)
        self.assertIn("format_amounts", stdout)
        self.assertIn("format_negatives_with_parentheses", stdout)

    def test_config_edit(self):
        stdout, _stderr, _rc = call_script("config", "--edit")
        self.assertIn("[Settings]", stdout)

    def test_config_edit_undefined_editor(self):
        del os.environ["EDITOR"]

        stdout, _stderr, rc = call_script("config", "--edit")
        self.assertIn("is unset", stdout)
        self.assertEqual(rc, 1)

    def test_config_edit_empty_editor(self):
        os.environ["EDITOR"] = ""

        _stdout, stderr, _rc = call_script("config", "--edit")
        self.assertIn("Permission denied", stderr)

    def test_config_edit_invalid_editor(self):
        os.environ["EDITOR"] = "this/should/never/exist"

        _stdout, stderr, _rc = call_script("config", "--edit")
        self.assertIn("not found", stderr)

    def test_version(self):
        stdout, _stderr, rc = call_script("version")
        self.assertIn(".", stdout)
        self.assertEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
