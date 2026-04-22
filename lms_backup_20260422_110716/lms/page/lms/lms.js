frappe.pages["lms"].on_page_load = function (wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("lms"),
		single_column: true,
	});
};

frappe.pages["lms"].on_page_show = function (wrapper) {
	load_desk_page(wrapper);
};

function load_desk_page(wrapper) {
	let $parent = $(wrapper).find(".layout-main-section");
	$parent.empty();

	frappe.require("lms.bundle.js").then(() => {
		frappe.lms = new frappe.ui.Lms({
			wrapper: $parent,
			page: wrapper.page,
		});
	});
}