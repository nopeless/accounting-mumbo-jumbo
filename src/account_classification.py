from datetime import datetime
from enum import Enum
import sys
from typing import Any
import prettytable

prettytable: Any = prettytable

import re

# class OwnerType:
#     ASSET = "Asset"
#     LIABILITY = "Liability"
#     EQUITY = "Equity"

# class PeriodType:
#     AGGREGATE = "Aggregate"
#     CURRENT = "Current"
#     LONG_TERM = "Long Term"

# class ActivityType:
#     OPERATING = "Operating"
#     INVESTING = "Investing"
#     FINANCING = "Financing"
#     OTHER = "Other"

# class AccountClassification:

#     @staticmethod
#     def get(period: PeriodType, owner_type: OwnerType):
#         pass


class NormalBalance(Enum):
    DEBIT = "Debit"
    CREDIT = "Credit"
    SPECIAL = "Special"


class FinancialStatement(Enum):
    BALANCE_SHEET = "Balance Sheet"
    INCOME_STATEMENT = "Income Statement"
    RETAINED_EARNINGS = "Retained Earnings"
    NOT_APPLICABLE = "Not Applicable"


class Account:
    def __init__(
        self,
        title: str,
        classification: str,
        statement: FinancialStatement,
        normal_balance: NormalBalance,
    ):
        self.title = title
        self.classification = classification
        self.statement = statement
        self.normal_balance = normal_balance

    @staticmethod
    def get_column_names():
        return ["Title", "Classification", "Statement", "Normal Balance"]

    def get_column_values(self):
        return [
            self.title,
            self.classification,
            self.statement.value,
            self.normal_balance.value,
        ]


# fmt: off
accounts = [
    Account("Accounts Payable",                     "Current Liability",            FinancialStatement.BALANCE_SHEET,    NormalBalance.CREDIT),
    Account("Accounts Receivable",                  "Current Asset",                FinancialStatement.BALANCE_SHEET,    NormalBalance.DEBIT ),
    Account("Accumulated Depreciation - Buildings", "Plant Asset - Contra",         FinancialStatement.BALANCE_SHEET,    NormalBalance.CREDIT),
    Account("Accumulated Depreciation - Equipment", "Plant Asset - Contra",         FinancialStatement.BALANCE_SHEET,    NormalBalance.CREDIT),
    Account("Administrative Expenses",              "Operating Expense",            FinancialStatement.INCOME_STATEMENT, NormalBalance.DEBIT ),
    Account("Allowance for Doubtful Accounts",      "Current Asset - Contra",       FinancialStatement.BALANCE_SHEET,    NormalBalance.CREDIT),
    Account("Amortization Expense",                 "Operating Expense",            FinancialStatement.INCOME_STATEMENT, NormalBalance.DEBIT ),
    Account("Bad Debt Expense",                     "Operating Expense",            FinancialStatement.INCOME_STATEMENT, NormalBalance.DEBIT ),
    Account("Bonds Payable",                        "Long Term Liability",          FinancialStatement.BALANCE_SHEET,    NormalBalance.CREDIT),
    Account("Buildings",                            "Plant Asset",                  FinancialStatement.BALANCE_SHEET,    NormalBalance.DEBIT ),
    Account("Cash",                                 "Current Asset",                FinancialStatement.BALANCE_SHEET,    NormalBalance.DEBIT ),
    Account("Common Stock",                         "Stockholders' Equity",         FinancialStatement.BALANCE_SHEET,    NormalBalance.CREDIT),
    Account("Cost of Goods Sold",                   "Operating Expense",            FinancialStatement.INCOME_STATEMENT, NormalBalance.DEBIT ),
    Account("Debt Investments",                     "Current Asset",                FinancialStatement.BALANCE_SHEET,    NormalBalance.DEBIT ),
    Account("Depreciation Expense - Buildings",     "Operating Expense",            FinancialStatement.INCOME_STATEMENT, NormalBalance.DEBIT ),
    Account("Discount on Bonds Payable",            "Long Term Liability - Contra", FinancialStatement.BALANCE_SHEET,    NormalBalance.DEBIT ),
    Account("Dividends Revenue",                    "OtherIncome",                  FinancialStatement.INCOME_STATEMENT, NormalBalance.CREDIT),
    Account("Dividends",                            "Temporary Account",            FinancialStatement.RETAINED_EARNINGS,NormalBalance.DEBIT ),
    Account("Dividends Payable",                    "Current Liability",            FinancialStatement.BALANCE_SHEET,    NormalBalance.CREDIT),
    Account("Equipment",                            "Plant Asset",                  FinancialStatement.BALANCE_SHEET,    NormalBalance.DEBIT ),
    Account("Freight Out",                          "Operating Expense",            FinancialStatement.INCOME_STATEMENT, NormalBalance.DEBIT ),
    Account("Gain on Sale of Equipment",            "Other Income",                 FinancialStatement.INCOME_STATEMENT, NormalBalance.CREDIT),
    Account("Goodwill",                             "Intangible Asset",             FinancialStatement.BALANCE_SHEET,    NormalBalance.DEBIT ),
    Account("Income Summary",                       "Temporary Account",            FinancialStatement.NOT_APPLICABLE,   NormalBalance.SPECIAL),
    Account("Income Tax Expense",                   "Operating Expense",            FinancialStatement.INCOME_STATEMENT, NormalBalance.DEBIT ),
    Account("Income Tax Payable",                   "Current Liability",            FinancialStatement.BALANCE_SHEET,    NormalBalance.CREDIT),
    Account("Insurance Expense",                    "Operating Expense",            FinancialStatement.INCOME_STATEMENT, NormalBalance.DEBIT ),
    Account("Interest Expense",                     "Operating Expense",            FinancialStatement.INCOME_STATEMENT, NormalBalance.DEBIT ),
    Account("Interest Payable",                     "Current Liability",            FinancialStatement.BALANCE_SHEET,    NormalBalance.CREDIT),
    Account("Interest Receivable",                  "Current Asset",                FinancialStatement.BALANCE_SHEET,    NormalBalance.DEBIT ),
    Account("Interest Revenue",                     "Other Income",                 FinancialStatement.INCOME_STATEMENT, NormalBalance.CREDIT),
    Account("Inventory",                            "Current Asset",                FinancialStatement.BALANCE_SHEET,    NormalBalance.DEBIT ),
]
# fmt: on

column_names = Account.get_column_names()


def normalize(string: str):
    string = string.lower()
    # Remove all non ascii characters
    string = re.sub(r"[^\x00-\x7f]", "", string)

    return string


def fuzzy_find(items: list[str], query: str):
    query = normalize(query)
    return min(
        (item for item in items if normalize(item).startswith(query)),
        key=len,
        default=None,
    )


def sortby_to_index(sortby: list[str]):
    return [column_names.index(v) for s in sortby if (v := fuzzy_find(column_names, s))]


def get_account_classification_table(sortby: list[str]):
    column_values = [account.get_column_values() for account in accounts]

    if sortby:
        column_values.sort(key=lambda row: [row[s] for s in sortby_to_index(sortby)])

    pt = prettytable.PrettyTable()

    pt.field_names = column_names
    pt.add_rows(column_values)
    pt.align = "l"
    # This is just how the library works
    pt.align[column_names[-1]] = "r"  # type: ignore

    table = pt.get_string()

    # Delete first and last line
    table = "\n".join(table.split("\n")[1:-1])

    # Replace all + with | for markdown table
    table = re.sub(r"\+", "|", table)

    # Right align final
    table = re.sub(r"--\|\n", "-:|\n", table)

    return table


def print_footer():
    # Markdown footer
    print(
        f"\n> generated by [account_classification.py](../src/account_classification.py) at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC"
    )


def main():
    # pretty print the accounts
    # with the column names at the top
    # print a table

    sortby = sys.argv[1:]

    if sortby == ["all"]:
        # print all sorted

        print(f"# Account Classifications")

        for column in column_names:
            print()
            out = get_account_classification_table([column])
            print(f"## Sorted by {column}\n")
            print(out)

        print_footer()
        return

    # Markdown header
    optional = (
        ""
        if not sortby
        else f" (sorted by {', '.join(column_names[s] for s in sortby_to_index(sortby))})"
    )
    print(f"# Account Classification{optional}\n")

    # Table
    print(get_account_classification_table(sortby))

    print_footer()


if __name__ == "__main__":
    main()
