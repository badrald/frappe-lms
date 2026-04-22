app_name = "lms"
app_title = "LMS"
app_publisher = "badr.alden.abdullah@gmail.com "
app_description = "it's LMS aka (library managemnt System )  "
app_email = "badr.alden.Abdullah@gmail.com "
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
add_to_apps_screen = [
    {
        "name": "lms website",
        "logo": "/assets/lms/frontend/assets/website_logo.png",
        "title": "LMS website",
        "route": "/frontend",
        "color": "#3498db",
    },
    {
        "name": "LMS app",
        "logo": "/assets/lms/frontend/assets/mange_logo.png",
        "title": "LMS App",
        "route": "/app",
        "color": "#3498db",
    },
]


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/lms/css/lms.css"
# app_include_js = "/assets/lms/js/lms.js"

# include js, css files in header of web template
# web_include_css = "/assets/lms/css/lms.css"
# web_include_js = "/assets/lms/js/lms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "lms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "lms/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# Set the login page route
login_page = "frontend/accounts/login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "lms.utils.jinja_methods",
# 	"filters": "lms.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "lms.install.before_install"
# after_install = "lms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "lms.uninstall.before_uninstall"
# after_uninstall = "lms.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "lms.utils.before_app_install"
# after_app_install = "lms.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "lms.utils.before_app_uninstall"
# after_app_uninstall = "lms.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "lms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    "daily": [
        "lms.tasks.recompute_all_membership_validity",
        "lms.tasks.mark_overdue_borrows",
    ],
}

# Testing
# -------

# before_tests = "lms.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "lms.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "lms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["lms.utils.before_request"]
# after_request = ["lms.utils.after_request"]

# Job Events
# ----------
# before_job = ["lms.utils.before_job"]
# after_job = ["lms.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",

# Exempt frontend routes from CSRF validation
csrf_exempt_routes = ["/frontend", "/frontend/*"]

# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"lms.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


website_route_rules = [
    {"from_route": "/dashboard/<path:app_path>", "to_route": "frontend"},
    {"from_route": "/api/session", "to_route": "session_api_handler"},
]
