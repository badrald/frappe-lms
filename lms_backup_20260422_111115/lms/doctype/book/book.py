# Copyright (c) 2025, badr.alden.abdullah@gmail.com  and contributors
# For license information, please see license.txt

import frappe
import requests
from frappe.model.document import Document
from frappe import _


class Book(Document):

    @frappe.whitelist()
    def fetch_book_details_from_isbn(self):
        """Fetch book details from Google Books API using this document's ISBN,
        upsert related Author/Publisher, and populate Book fields.
        """
        isbn = (self.isbn or '').strip()
        if not isbn:
            frappe.throw(_('Please enter an ISBN first'))

        # Normalize: remove dashes/spaces
        clean_isbn = isbn.replace('-', '').replace(' ', '')
        if len(clean_isbn) not in (10, 13):
            frappe.throw(_('Please enter a valid ISBN (10 or 13 digits)'))

        url = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{clean_isbn}'
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json() or {}
        except Exception as exc:
            frappe.throw(_('Failed to fetch from Google Books API: {0}').format(frappe.safe_decode(str(exc))))

        items = data.get('items') or []
        if not items:
            frappe.throw(_('No book details found for ISBN {0}').format(clean_isbn))

        volume_info = (items[0] or {}).get('volumeInfo') or {}

        title = volume_info.get('title')
        authors = volume_info.get('authors') or []
        publisher_name = volume_info.get('publisher')
        description = volume_info.get('description')
        image_links = volume_info.get('imageLinks') or {}
        categories = volume_info.get("categories") or []


        # Prefer higher-res image if available
        category = categories[0] if categories else ''
        

        cover_url = image_links.get('thumbnail').split("&zoom=1")[0]

        # Ensure Author docs exist (by author_name) and collect their docnames
        author_docnames = []
        for author_title in authors:
            existing_name = frappe.db.get_value("Author", {"author_name": author_title}, "name")
            if existing_name:
                author_docnames.append(existing_name)
            else:
                author_doc = frappe.get_doc({
                    "doctype": "Author",
                    "author_name": author_title
                })
                author_doc.insert(ignore_permissions=True)
                author_docnames.append(author_doc.name)

       
        # Only create category if it exists and is not empty
        if category:
            existing_category = frappe.db.get_value("Category", {"category_name": category}, "name")
            if not existing_category:
                category_doc = frappe.get_doc({
                    "doctype": "Category",
                    "category_name": category
                })
                category_doc.insert(ignore_permissions=True)

        # Ensure Publisher exists (by publisher_name)
        if publisher_name:
            exists_publisher = frappe.db.get_value("Publisher", {"publisher_name": publisher_name}, "name")
            if not exists_publisher:
                new_publisher = frappe.get_doc({
                    "doctype": "Publisher",
                    "publisher_name": publisher_name
                })
                new_publisher.insert(ignore_permissions=True)


        # Prepare updates
        updated_fields = {}
        if title:
            updated_fields['title'] = title
        if description:
            updated_fields['description'] = description
        if cover_url:
            updated_fields['cover'] = cover_url
        if publisher_name:
            updated_fields['publisher'] = publisher_name
        if category: 
            updated_fields['category'] = category

        # Clear existing authors and add new ones through child table
        self.authors_names = []
        author_rows = []
        for i, author_docname in enumerate(author_docnames):
            row = self.append("authors_names", {})
            row.author = author_docname
            row.role = "Author" if i == 0 else "Co-Author"
            author_rows.append({"author": author_docname, "role": row.role})

        return {
            'updated': True,
            'fields': updated_fields,
            'authors': author_rows,
        }

    @frappe.whitelist()
    def clear_fetched_data(self):
        """Clear fields populated from external sources, keeping only ISBN."""
        fields_to_clear = {
            'title': None,
            'publisher': None,
            'description': None,
            'cover': None,
            'category': None,
        }
        self.update(fields_to_clear)
        # Clear authors child table
        self.authors_names = []
        return {'cleared': True}

    def before_save(self):
        """Before saving, ensure all authors in the child table have proper roles"""
        if self.authors_names:
            seen_authors = set()
            for i, author_row in enumerate(self.authors_names):
                # Validate no duplicate authors within the same book
                author_name = (author_row.author or '').strip()
                if not author_name:
                    frappe.throw(_(f"Row {i+1}: Author is required in Authors Names"))
                if author_name in seen_authors:
                    frappe.throw(_(f'Duplicate author "{author_name}" in Authors Names'))
                seen_authors.add(author_name)

                # Set default role if not set
                if not author_row.role:
                    author_row.role = "Author" if i == 0 else "Co-Author"
        return
