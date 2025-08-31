// Copyright (c) 2025, badr.alden.abdullah@gmail.com  and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Book", {
// 	refresh(frm) {

// 	},
// });





frappe.ui.form.on('Book', {
	refresh: function(frm) {
		let upove_button = frm.add_custom_button("Featch Data From Api",()=>{
			fetch_book_details(frm);
		})
        const isbn_ctrl = frm.get_field('isbn');
        if (isbn_ctrl && isbn_ctrl.$wrapper) {
            const $container = isbn_ctrl.$wrapper.find('.control-input');
            if ($container.length && !$container.find('.isbn-inline-btn').length) {
                const $btnFetch = $('<button type="button" class="btn btn-sm btn-success isbn-inline-btn mt-2 " >Featch Data</button>');
                $btnFetch.on('click', function() {
                    fetch_book_details(frm);
                });
				const $btnClear = $('<button type="button" class="btn btn-sm btn-danger isbn-inline-btn mt-2 ml-2 " >Clear Data</button>');
                $btnClear.on('click', function() {
                    clear_fetched_data(frm);
                });
				$container.append($btnFetch);
				$container.append($btnClear);
            }
        }
		frm.add_custom_button(__('Fetch Book Details'), function() {
			fetch_book_details(frm);
		}, __('Actions'));
		
	},
	
	isbn: function(frm) {	
	},
	
	before_save: function(frm) {
		// Validate ISBN before saving
		if (frm.doc.isbn) {
			let clean_isbn = frm.doc.isbn.replace(/[-\s]/g, '');
			if (clean_isbn.length !== 10 && clean_isbn.length !== 13) {
				frappe.msgprint(__('Please enter a valid ISBN (10 or 13 digits)'));
				frappe.validated = false;
				return false;
			}
		}
	}
});

function fetch_book_details(frm) {
	if (!frm.doc.isbn) {
		frappe.msgprint(__('Please enter an ISBN first'));
		return;
	}
	
	// Show loading indicator
	frappe.show_alert({
		message: __('Fetching book details...'),
		indicator: 'blue'
	});
	
	// Call server method
	frappe.call({
		method: 'fetch_book_details_from_isbn',
		doc: frm.doc,
        callback: function(response) {
            if (response.message) {
                const f = response.message.fields || {};
                if (f.title) frm.set_value('title', f.title);
                if (f.description) frm.set_value('description', f.description);
                if (f.publisher) frm.set_value('publisher', f.publisher);
                if (f.cover) frm.set_value('cover', f.cover);
				if(f.category) frm.set_value('category',f.category);
				frm.set_value("total_copies",10);
				frm.set_value("available_copies",10);
				const authors = Array.isArray(response.message.authors) ? response.message.authors : [];
				if (authors.length) {
					frm.clear_table('authors_names');
					authors.forEach((a, idx) => {
						const row = frm.add_child('authors_names');
						row.author = a.author; // Link to Author (docname)
						row.role = a.role || (idx === 0 ? 'Primary' : 'Secondary');
					});
					frm.refresh_field('authors_names');
				}

                frappe.show_alert({
                    message: __('Book details fetched successfully'),
                    indicator: 'green'
                });
            }
        },
		error: function(error) {
			console.error('Error fetching book details:', error);
			frappe.show_alert({
				message: __('Failed to fetch book details'),
				indicator: 'red'
			});
		}
	});
}

function clear_fetched_data(frm) {
	frappe.confirm(
		__('Are you sure you want to clear all fetched data? This will keep only the ISBN.'),
		function() {
			frappe.call({
				method: 'clear_fetched_data',
				doc: frm.doc,
				callback: function(response) {
					frm.refresh();
					frappe.show_alert({
						message: __('Fetched data cleared successfully'),
						indicator: 'green'
					});
				}
			});
		}
	);
}

// Helper function to format ISBN
function format_isbn(isbn) {
	if (!isbn) return isbn;
	
	let clean = isbn.replace(/[-\s]/g, '');
	
	if (clean.length === 10) {
		// Format as ISBN-10: XXX-X-XX-XXXXXX-X
		return clean.replace(/(\d{3})(\d{1})(\d{2})(\d{6})(\d{1})/, '$1-$2-$3-$4-$5');
	} else if (clean.length === 13) {
		// Format as ISBN-13: XXX-X-XX-XXXXXX-X
		return clean.replace(/(\d{3})(\d{1})(\d{3})(\d{6})(\d{1})/, '$1-$2-$3-$4-$5');
	}
	
	return isbn;
}

// Auto-format ISBN on blur
frappe.ui.form.on('Book', {
	isbn: function(frm) {
		if (frm.doc.isbn) {
			let formatted = format_isbn(frm.doc.isbn);
			if (formatted !== frm.doc.isbn) {
				frm.set_value('isbn', formatted);
			}
		}
	}
});