# Copyright (c) 2025, badr.alden.abdullah@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import requests


@frappe.whitelist()
def get_all_books():
    """Get all books with basic information"""
    books = frappe.get_all("Book", fields=[
        "name", 
        "title", 
        "isbn", 
        "publisher", 
        "status", 
        "cover",
        "total_copies",
        "available_copies",
        "category"
    ], order_by="creation desc")
    return {"success": True, "data": books}


@frappe.whitelist()
def get_book_by_id(book_id):
    """Get specific book by ID with full details"""
    try:
        # Using frappe.get_doc following Frappe's document API pattern
        book = frappe.get_doc("Book", book_id)
        
        # Get authors
        authors = []
        if hasattr(book, 'authors_names') and book.authors_names:
            for author_row in book.authors_names:
                if author_row.author:
                    author_doc = frappe.get_doc("Author", author_row.author)
                    authors.append({
                        "name": author_doc.name,
                        "author_name": author_doc.author_name
                    })
        
        book_dict = book.as_dict()
        book_dict['authors'] = authors
        
        return {"success": True, "data": book_dict}
    except frappe.DoesNotExistError:
        frappe.throw(_("Book not found"), frappe.DoesNotExistError)


@frappe.whitelist()
def search_books(query="", category="", status="", limit=20):
    """Search books with filters"""
    filters = []
    
    if query:
        filters.extend([
            ['title', 'like', f'%{query}%'],
            'or',
            ['isbn', 'like', f'%{query}%'],
        ])
    
    if category:
        filters.append(['category', '=', category])
    
    if status:
        filters.append(['status', '=', status])
    
    books = frappe.get_all("Book", 
        filters=filters if filters else None,
        fields=[
            "name", 
            "title", 
            "isbn", 
            "publisher", 
            "status", 
            "cover",
            "category",
            "available_copies"
        ],
        limit=int(limit),
        order_by="creation desc"
    )
    return {"success": True, "data": books}


@frappe.whitelist()
def get_available_books():
    """Get only available books"""
    books = frappe.get_all("Book", 
        filters=[
            ["available_copies", ">", 0],
            ["status", "=", "Active"]
        ],
        fields=[
            "name", 
            "title", 
            "isbn", 
            "publisher", 
            "cover",
            "category",
            "available_copies"
        ],
        order_by="creation desc"
    )
    return {"success": True, "data": books}


@frappe.whitelist()
def get_books_by_category(category):
    """Get books by category"""
    books = frappe.get_all("Book", 
        filters={"category": category},
        fields=[
            "name", 
            "title", 
            "isbn", 
            "publisher", 
            "description",
            "status", 
            "cover",
            "available_copies"
        ],
        order_by="creation desc"
    )
    return {"success": True, "data": books}


@frappe.whitelist()
def get_book_stats():
    """Get books statistics"""
    total_books = frappe.db.count("Book")
    available_books = frappe.db.count("Book", {"available_copies": [">", 0]})
    borrowed_books = frappe.db.sql("""
        SELECT COALESCE(SUM(total_copies - available_copies), 0) as borrowed
        FROM tabBook
    """)[0][0]
    
    categories = frappe.get_all("Book", 
        fields=["category", "count(*) as count"],
        group_by="category",
        order_by="count desc"
    )
    
    return {
        "success": True, 
        "data": {
            "total_books": total_books,
            "available_books": available_books,
            "borrowed_books": borrowed_books,
            "categories": categories
        }
    }

@frappe.whitelist()
def add_book(**book_data):
    try:
        # Ensure related docs exist (Category, Publisher) by label if provided
        category = book_data.get("category")
        publisher_name = book_data.get("publisher")

        if category:
            existing_category = frappe.db.get_value("Category", {"category_name": category}, "name")
            if not existing_category:
                frappe.get_doc({
                    "doctype": "Category",
                    "category_name": category,
                }).insert(ignore_permissions=True)

        if publisher_name:
            existing_publisher = frappe.db.get_value("Publisher", {"publisher_name": publisher_name}, "name")
            if not existing_publisher:
                frappe.get_doc({
                    "doctype": "Publisher",
                    "publisher_name": publisher_name,
                }).insert(ignore_permissions=True)

        # Handle authors data
        authors_data = book_data.pop("authors_names", None)
        
        # Create the Book document from provided fields
        book = frappe.get_doc({
            "doctype": "Book",
            **book_data,
        })
        
        # Handle authors if provided
        if authors_data and isinstance(authors_data, list):
            for author_info in authors_data:
                # Check if author is a string (author name) or dict with author and role
                if isinstance(author_info, str):
                    # If it's just a string, treat it as author name with default role
                    author_name = author_info
                    role = "Author"
                elif isinstance(author_info, dict):
                    # If it's a dict, extract author and role
                    author_name = author_info.get("author") or author_info.get("author_name")
                    role = author_info.get("role", "Author")
                else:
                    continue  # Skip invalid author data
                
                if author_name:
                    # Check if author exists, create if not
                    existing_author = frappe.db.get_value("Author", {"author_name": author_name}, "name")
                    if not existing_author:
                        author_doc = frappe.get_doc({
                            "doctype": "Author",
                            "author_name": author_name
                        })
                        author_doc.insert(ignore_permissions=True)
                        author_name = author_doc.name
                    else:
                        author_name = existing_author
                    
                    # Add author to book
                    book.append("authors_names", {
                        "author": author_name,
                        "role": role
                    })

        book.insert()

        return {"success": True, "data": book.as_dict()}
    except frappe.PermissionError as e:
        return {"success": False, "error": _(f"Permission denied: {str(e)}")}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error adding book")
        return {"success": False, "error": str(e)}

@frappe.whitelist()
def update_book(**bookdata):
    try:
        book = frappe.get_doc("Book", bookdata["name"])
        book.update(bookdata)
        book.save()
        return {"success": True, "data": book.as_dict()}
    except :
        frappe.log_error(frappe.get_traceback(), "Error updating book")
        return {"success": False, "error": "Error updating book"}



@frappe.whitelist()
def fetch_book_details_from_isbn(isbn):
        """Fetch book details from Google Books API using this document's ISBN,
        upsert related Author/Publisher, and populate Book fields.
        """
        isbn = (isbn or '').strip()
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
        
        cover_url = None
        if image_links.get('thumbnail'):
            # Safely handle thumbnail URL processing
            thumbnail = image_links.get('thumbnail')
            if "&zoom=1" in thumbnail:
                cover_url = thumbnail.split("&zoom=1")[0]
            else:
                cover_url = thumbnail

        # Ensure Author docs exist (by author_name) and collect their docnames
        author_docnames = []
        if authors:
            # Batch check existing authors to improve performance
            existing_authors = frappe.db.get_all(
                "Author", 
                filters={"author_name": ["in", authors]}, 
                fields=["name", "author_name"]
            )
            existing_author_map = {author.author_name: author.name for author in existing_authors}
            
            # Handle new authors
            for author_title in authors:
                if author_title in existing_author_map:
                    author_docnames.append(existing_author_map[author_title])
                else:
                    try:
                        author_doc = frappe.get_doc({
                            "doctype": "Author",
                            "author_name": author_title
                        })
                        author_doc.insert(ignore_permissions=True)
                        author_docnames.append(author_doc.name)
                    except Exception:
                        # Continue with other authors even if one fails
                        frappe.log_error(f"Failed to create author: {author_title}")
                        continue

        # Only create category if it exists and is not empty
        if category:
            existing_category = frappe.db.get_value("Category", {"category_name": category}, "name")
            if not existing_category:
                try:
                    category_doc = frappe.get_doc({
                        "doctype": "Category",
                        "category_name": category
                    })
                    category_doc.insert(ignore_permissions=True)
                except Exception:
                    frappe.log_error(f"Failed to create category: {category}")

        # Ensure Publisher exists (by publisher_name)
        publisher_created = False
        if publisher_name:
            exists_publisher = frappe.db.get_value("Publisher", {"publisher_name": publisher_name}, "name")
            if not exists_publisher:
                try:
                    new_publisher = frappe.get_doc({
                        "doctype": "Publisher",
                        "publisher_name": publisher_name
                    })
                    new_publisher.insert(ignore_permissions=True)
                    publisher_created = True
                except Exception:
                    frappe.log_error(f"Failed to create publisher: {publisher_name}")

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

        # Prepare author rows (without using 'self' since this is a standalone function)
        author_rows = []
        for i, author_docname in enumerate(author_docnames):
            role = "Author" if i == 0 else "Co-Author"
            author_rows.append({"author": author_docname, "role": role})

        print(updated_fields)
        return {
            'updated': True,
            'fields': updated_fields,
            'authors': author_rows,
        }