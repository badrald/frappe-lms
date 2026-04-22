# Copyright (c) 2025, badr.alden.abdullah@gmail.com  and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff, getdate


class LibraryTransaction(Document):
    def validate(self):
        self.set_member_full_name()

    def before_submit(self):
        self.validate_member_has_valid_membership()

        if self.transaction_type == "Issue":
            self.validate_article_available_for_issue()
        elif self.transaction_type == "Return":
            self.validate_can_return()
            self.validate_loan_period()

    def on_submit(self):
        self.update_article_status_on_submit()

    def on_cancel(self):
        self.update_article_status_on_cancel()

    def set_member_full_name(self):
        if self.library_member:
            first, last = frappe.db.get_value(
                "Library Member", self.library_member, ["first_name", "last_name"], as_dict=False
            ) or (None, None)
            if first or last:
                self.member_full_name = (f"{first or ''} {last or ''}").strip()

    def validate_member_has_valid_membership(self):
        if not self.library_member:
            frappe.throw(_("Library Member is required."))

        is_valid = frappe.db.get_value(
            "Library Member", self.library_member, "is_membership_valid"
        )
        if not is_valid:
            frappe.throw(
                _("Selected member does not have a valid membership. Create/renew a paid membership that is currently active.")
            )

    def validate_article_available_for_issue(self):
        if not self.article:
            frappe.throw(_("Article is required."))

        latest = self.get_latest_submitted_transaction_for_article(self.article)
        if latest and latest.get("transaction_type") == "Issue":
            frappe.throw(_("This article is currently issued and cannot be issued again until it is returned."))

    def validate_can_return(self):
        latest = self.get_latest_submitted_transaction_for_article(self.article)
        if not latest or latest.get("transaction_type") != "Issue":
            frappe.throw(_("This article is not currently issued. Nothing to return."))

    def validate_loan_period(self):
        # Only applicable on Return
        last_issue = self.get_latest_issue_for_article(self.article)
        if not last_issue:
            return

        # Use document transaction_date if provided else today
        return_date = getdate(self.transaction_date) if self.transaction_date else getdate()
        issue_date = getdate(last_issue.get("transaction_date"))

        # Fetch loan period from settings (fallback to 14 days if missing)
        loan_days = self.get_loan_period_days()

        if loan_days is not None and date_diff(return_date, issue_date) > int(loan_days):
            frappe.throw(
                _(
                    "Loan period exceeded ({0} days). Issue Date: {1}, Return Date: {2}."
                ).format(loan_days, issue_date, return_date)
            )

    def get_loan_period_days(self):
        # Try to read from settings; fallback to 14 if settings doctype/record doesn't exist
        try:
            val = frappe.db.get_single_value("Library Management Settings", "loan_period")
            return int(val) if val is not None else 14
        except Exception:
            # Settings doctype may not exist yet
            return 14

    def update_article_status_on_submit(self):
        if not self.article:
            return

        # We will reuse the existing Status field on Article:
        #   Active     -> available
        #   Inactive   -> issued/out
        #   Discontinued -> ignored
        if self.transaction_type == "Issue":
            frappe.db.set_value("Article", self.article, "status", "Inactive")
        elif self.transaction_type == "Return":
            # Only set back to Active if not explicitly Discontinued
            current_status = frappe.db.get_value("Article", self.article, "status")
            if current_status != "Discontinued":
                frappe.db.set_value("Article", self.article, "status", "Active")

    def update_article_status_on_cancel(self):
        if not self.article:
            return

        # After cancel, recompute availability based on latest submitted transaction
        latest = self.get_latest_submitted_transaction_for_article(self.article)
        new_status = "Inactive" if (latest and latest.get("transaction_type") == "Issue") else "Active"

        current_status = frappe.db.get_value("Article", self.article, "status")
        if current_status != "Discontinued":
            frappe.db.set_value("Article", self.article, "status", new_status)

    def get_latest_submitted_transaction_for_article(self, article):
        records = frappe.get_all(
            "Library Transaction",
            filters={"article": article, "docstatus": 1},
            fields=["name", "transaction_type", "transaction_date", "creation"],
            order_by="transaction_date desc, creation desc",
            limit=1,
        )
        return records[0] if records else None

    def get_latest_issue_for_article(self, article):
        records = frappe.get_all(
            "Library Transaction",
            filters={
                "article": article,
                "transaction_type": "Issue",
                "docstatus": 1,
            },
            fields=["name", "transaction_type", "transaction_date", "creation"],
            order_by="transaction_date desc, creation desc",
            limit=1,
        )
        return records[0] if records else None

    @frappe.whitelist()
    def get_transactions(self):
        transactions = frappe.get_all("Library Transaction", fields=["name", "transaction_type", "transaction_date", "article", "article_name", "library_member", "member_full_name"])
        return transactions
