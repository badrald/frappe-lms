# Copyright (c) 2025, badr.alden.abdullah@gmail.com  and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

class Category(Document):
    @frappe.whitelist()
    def get_categories(self):
        categories = frappe.get_all("Category", fields=["name", "category_name"])
        return categories
