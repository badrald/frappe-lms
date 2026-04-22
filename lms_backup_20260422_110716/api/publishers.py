# Copyright (c) 2025, badr.alden.abdullah@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def get_all_publishers():
    """Get all publishers with book counts"""
    publishers = frappe.db.sql("""
        SELECT p.name, p.publisher_name, p.website, p.email, COUNT(b.name) as books_count
        FROM tabPublisher p
        LEFT JOIN tabBook b ON b.publisher = p.name
        GROUP BY p.name, p.publisher_name, p.website, p.email
        ORDER BY p.publisher_name
    """, as_dict=True)
    
    return {"success": True, "data": publishers}


@frappe.whitelist()
def get_publisher_by_id(publisher_id):
    """Get specific publisher by ID with books"""
    try:
        publisher = frappe.get_doc("Publisher", publisher_id)
        
        # Get books by this publisher
        books = frappe.get_all("Book",
            filters={"publisher": publisher_id},
            fields=[
                "name", 
                "article_name", 
                "isbn", 
                "cover", 
                "category",
                "available_copies"
            ]
        )
        
        publisher_dict = publisher.as_dict()
        publisher_dict['books'] = books
        publisher_dict['books_count'] = len(books)
        
        return {"success": True, "data": publisher_dict}
    except frappe.DoesNotExistError:
        return {"success": False, "message": "Publisher not found"}


@frappe.whitelist()
def search_publishers(query="", limit=20):
    """Search publishers by name"""
    filters = []
    
    if query:
        filters.append(['publisher_name', 'like', f'%{query}%'])
    
    publishers = frappe.get_all("Publisher", 
        filters=filters if filters else None,
        fields=[
            "name", 
            "publisher_name", 
            "website",
            "email"
        ],
        limit=int(limit),
        order_by="publisher_name"
    )
    return {"success": True, "data": publishers}


@frappe.whitelist()
def get_top_publishers(limit=10):
    """Get publishers with most books"""
    publishers = frappe.db.sql("""
        SELECT p.name, p.publisher_name, COUNT(b.name) as books_count
        FROM tabPublisher p
        LEFT JOIN tabBook b ON b.publisher = p.name
        GROUP BY p.name, p.publisher_name
        HAVING books_count > 0
        ORDER BY books_count DESC
        LIMIT %s
    """, int(limit), as_dict=True)
    
    return {"success": True, "data": publishers}
