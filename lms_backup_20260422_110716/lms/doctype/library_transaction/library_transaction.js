// Copyright (c) 2025, badr.alden.abdullah@gmail.com  and contributors
// For license information, please see license.txt

frappe.ui.form.on("Library Transaction", {
    setup(frm) {
        // Filter Library Member to show only valid members
        frm.set_query("library_member", function() {
            return {
                filters: {
                    is_membership_valid: 1,
                },
            };
        });

        // Filter Article to show only available ones (status = Active)
        frm.set_query("article", function() {
            return {
                filters: {
                    status: "Active",
                },
            };
        });
    },
});
