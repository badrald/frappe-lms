# Copyright (c) 2025, badr.alden.abdullah@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def get_all_authors():
    """Get all authors with basic information"""
    authors = frappe.get_all("Author", fields=[
        "name", 
        "author_name", 
    ], order_by="author_name")
    return {"success": True, "data": authors}


@frappe.whitelist()
def get_author_by_id(author_id):
    """Get specific author by ID with full details"""
    try:
        author = frappe.get_doc("Author", author_id)
        
        # Get books by this author
        books = frappe.db.sql("""
            SELECT b.name, b.article_name, b.isbn, b.cover, b.publisher
            FROM tabBook b
            INNER JOIN `tabArticle Author` aa ON aa.parent = b.name
            WHERE aa.author = %s
        """, author_id, as_dict=True)
        
        author_dict = author.as_dict()
        author_dict['books'] = books
        author_dict['books_count'] = len(books)
        
        return {"success": True, "data": author_dict}
    except frappe.DoesNotExistError:
        return {"success": False, "message": "Author not found"}


@frappe.whitelist()
def search_authors(query="", limit=20):
    """Search authors by name"""
    filters = []
    
    if query:
        filters.append(['author_name', 'like', f'%{query}%'])
    
    authors = frappe.get_all("Author", 
        filters=filters if filters else None,
        fields=[
            "name", 
            "author_name", 
            "biography",
            "nationality"
        ],
        limit=int(limit),
        order_by="author_name"
    )
    return {"success": True, "data": authors}


@frappe.whitelist()
def get_authors_stats():
    """Get authors statistics"""
    total_authors = frappe.db.count("Author")
    
    # Authors with most books
    top_authors = frappe.db.sql("""
        SELECT a.name, a.author_name, COUNT(aa.author) as books_count
        FROM tabAuthor a
        LEFT JOIN `tabArticle Author` aa ON aa.author = a.name
        GROUP BY a.name, a.author_name
        ORDER BY books_count DESC
        LIMIT 10
    """, as_dict=True)
    
    return {
        "success": True, 
        "data": {
            "total_authors": total_authors,
            "top_authors": top_authors
        }
    }
