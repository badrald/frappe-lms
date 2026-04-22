# Copyright (c) 2025, badr.alden.abdullah@gmail.com  and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, nowdate


class LibraryMembership(Document):
    def validate(self):
        self.validate_dates()

    def on_submit(self):
        if self.paid and self.is_currently_active():
            self.set_member_validity(True)

    def on_cancel(self):
        self.recompute_member_validity()

    def validate_dates(self):
        if self.from_date and self.to_date and getdate(self.to_date) < getdate(self.from_date):
            frappe.throw(_("To Date cannot be before From Date"))

    def is_currently_active(self):
        today = getdate(nowdate())
        start_ok = (not self.from_date) or getdate(self.from_date) <= today
        end_ok = (not self.to_date) or today <= getdate(self.to_date)
        return start_ok and end_ok

    def set_member_validity(self, valid: bool):
        if not self.library_member:
            return
        frappe.db.set_value("Library Member", self.library_member, "is_membership_valid", 1 if valid else 0)

    def recompute_member_validity(self):
        if not self.library_member:
            return
        today = getdate(nowdate())
        exists = frappe.get_all(
            "Library Membership",
            filters={
                "library_member": self.library_member,
                "paid": 1,
                "docstatus": 1,
            },
            fields=["name", "from_date", "to_date"],
        )
        def is_active(row):
            start_ok = (not row.get("from_date")) or getdate(row.get("from_date")) <= today
            end_ok = (not row.get("to_date")) or today <= getdate(row.get("to_date"))
            return start_ok and end_ok
        any_active = any(is_active(r) for r in exists)
        self.set_member_validity(any_active)
