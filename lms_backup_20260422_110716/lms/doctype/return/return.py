# Copyright (c) 2025, badr.alden.abdullah@gmail.com  and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe

class Return(Document):
	def before_insert(self):
		borrow = frappe.get_doc("Borrow", self.borrow_id)
		book = frappe.get_doc("Book", borrow.book)
		member = frappe.get_doc("Member",borrow.member)
		book.available_copies += 1
		book.save()

		member_status = member.status

		# Assume there is a single value doctype "Library Fine Settings" with fields for each member status
		fine_settings = frappe.get_single("Library Fine Settings")
		fine_tax = 0
		if member_status == "VIP":
			fine_tax = fine_settings.vip_fine
		else:
			fine_tax = fine_settings.normal_fine

		borrow.status = "Returned"
		borrow.return_date = self.return_date
		borrow.save()

		# حساب الغرامة
		if self.return_date > borrow.due_date:
			days_late = (self.return_date - borrow.due_date).days
			self.fine = days_late * fine_tax

	def on_cancel(self):
		# If a return is cancelled, decrement available copies again and reset borrow status
		if not self.borrow_id:
			return
		borrow = frappe.get_doc("Borrow", self.borrow_id)
		book = frappe.get_doc("Book", borrow.book)
		if (book.available_copies or 0) > 0:
			book.available_copies -= 1
			book.save()
		borrow.status = "Borrowed"
		borrow.save()
	