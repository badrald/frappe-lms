# Copyright (c) 2025, badr.alden.abdullah@gmail.com  and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
class Borrow(Document):
	
	def before_insert(self):
		book = frappe.get_doc("Book", self.book)
		if book.available_copies <= 0:
			frappe.throw("No copies available for this book")
		book.available_copies -= 1
		book.save()
		self.status = "Borrowed"

	def on_cancel(self):
		# Revert available copies when a borrow is cancelled
		if not self.book:
			return
		try:
			book = frappe.get_doc("Book", self.book)
			book.available_copies = (book.available_copies or 0) + 1
			book.save()
		except Exception:
			pass

