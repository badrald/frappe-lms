import router from "@/router"
import { createResource, setConfig } from "frappe-ui"
import { computed, reactive } from "vue"

import { userResource } from "./user"

export function sessionUser() {
	const cookies = new URLSearchParams(document.cookie.split("; ").join("&"))
	let _sessionUser = cookies.get("user_id")
	setConfig("fetchOptions", {
		credentials: "include",
		headers: {
			"X-Frappe-CSRF-Token": window.csrf_token || ""
		}
	})
	if (_sessionUser === "Guest") {
		_sessionUser = null
	}
	return _sessionUser
}

export function sessionCSRFToken() {
	const cookies = new URLSearchParams(document.cookie.split("; ").join("&"))
	return cookies.get("csrf_token")
}

export const session = reactive({
	login: createResource({
		url: "login",
		makeParams({ email, password }) {
			return {
				usr: email,
				pwd: password,
			}
		},
		onSuccess(data) {
			userResource.reload()
			session.user = sessionUser()
			const token = sessionCSRFToken()
			if (token) {
				window.csrf_token = token
				session.csrf_token = token
			}
			session.login.reset()
			router.replace(data.default_route || "/")
		},
	}),
	logout: createResource({
		url: "logout",
		onSuccess() {
			userResource.reset()
			session.user = sessionUser()
			// Clear csrf token on logout
			window.csrf_token = null
			session.csrf_token = null
			router.replace({ name: "Login" })
		},
	}),
	user: sessionUser(),
	csrf_token: sessionCSRFToken(),
	isLoggedIn: computed(() => !!session.user),
})

// Initialize global csrf token on first load if already logged in via cookies
const initialCsrf = sessionCSRFToken()
if (initialCsrf) {
    window.csrf_token = initialCsrf
}



