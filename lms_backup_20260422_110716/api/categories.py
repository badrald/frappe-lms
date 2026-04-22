# Copyright (c) 2025, badr.alden.abdullah@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def get_all_categories():
    """Get all categories with book counts"""
    categories = frappe.get_all("Category", fields=[
        "name", 
        "category_name", 
    ], order_by="category_name")
    return {"success": True, "data": categories}


@frappe.whitelist()
def get_category_by_id(category_id):
    """Get specific category by ID with books"""
    try:
        category = frappe.get_doc("Category", category_id)
        
        # Get books in this category
        books = frappe.get_all("Book",
            filters={"category": category_id},
            fields=[
                "name", 
                "article_name", 
                "isbn", 
                "cover", 
                "publisher",
                "available_copies"
            ]
        )
        
        category_dict = category.as_dict()
        category_dict['books'] = books
        category_dict['books_count'] = len(books)
        
        return {"success": True, "data": category_dict}
    except frappe.DoesNotExistError:
        return {"success": False, "message": "Category not found"}


@frappe.whitelist()
def search_categories(query="", limit=20):
    """Search categories by name"""
    filters = []
    
    if query:
        filters.append(['category_name', 'like', f'%{query}%'])
    
    categories = frappe.get_all("Category", 
        filters=filters if filters else None,
        fields=[
            "name", 
            "category_name", 
            "description"
        ],
        limit=int(limit),
        order_by="category_name"
    )
    return {"success": True, "data": categories}


@frappe.whitelist()
def get_popular_categories(limit=10):
    """Get categories with most books"""
    categories = frappe.db.sql("""
        SELECT c.name, c.category_name, COUNT(b.name) as books_count
        FROM tabCategory c
        LEFT JOIN tabBook b ON b.category = c.name
        GROUP BY c.name, c.category_name
        HAVING books_count > 0
        ORDER BY books_count DESC
        LIMIT %s
    """, int(limit), as_dict=True)
    
    return {"success": True, "data": categories}
