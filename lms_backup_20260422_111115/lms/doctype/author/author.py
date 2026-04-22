# Copyright (c) 2025, badr.alden.abdullah@gmail.com  and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

class Author(Document):
    @frappe.whitelist()
    def get_authors(self):
        authors = frappe.get_all("Author", fields=["name", "author_name"])
        return authors
