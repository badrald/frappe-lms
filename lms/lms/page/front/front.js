frappe.pages["front"].on_page_load = function (wrapper) {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("front"),
		single_column: true,
	});
};

frappe.pages["front"].on_page_show = function (wrapper) {
	load_desk_page(wrapper); 
};

function load_desk_page(wrapper) {
	let $parent = $(wrapper).find(".layout-main-section");
	$parent.empty();

	frappe.require("front.bundle.js").then(() => {
		frappe.front = new frappe.ui.Front({
			wrapper: $parent,
			page: wrapper.page,
		});
	});
}