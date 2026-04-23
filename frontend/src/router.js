import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("@/pages/Home.vue"),
		meta: {
			title: 'الرئيسية - نظام إدارة المكتبة'
		}
	},
	{
		path: "/books",
		name: "Books",
		component: () => import("@/pages/Books.vue"),
		meta: {
			title: 'الكتب - نظام إدارة المكتبة'
		}
	},
	{
		path: "/books/:id",
		name: "BookDetails",
		component: () => import("@/pages/BookDetails.vue"),
		meta: {
			title: 'تفاصيل الكتاب - نظام إدارة المكتبة'
		}
	},
	{
		path: "/members",
		name: "Members",
		component: () => import("@/pages/Members.vue"),
		meta: {
			title: 'الأعضاء - نظام إدارة المكتبة'
		}
	},
	{
		path: "/authors",
		name: "Authors",
		component: () => import("@/pages/Authors.vue"),
		meta: {
			title: 'المؤلفون - نظام إدارة المكتبة'
		}
	},
	{
		path: "/categories",
		name: "Categories",
		component: () => import("./pages/Categories.vue"),
		meta: {
			title: 'التصنيفات - نظام إدارة المكتبة'
		}
	},
	{
		path: "/transactions",
		name: "Transactions",
		component: () => import("@/pages/Transactions.vue"),
		meta: {
			title: 'المعاملات - نظام إدارة المكتبة'
		}
	},
	{
		path: "/reports",
		name: "Reports",
		component: () => import("@/pages/Reports.vue"),
		meta: {
			title: 'التقارير - نظام إدارة المكتبة'
		}
	},
	{
		name: "Login",
		path: "/accounts/login",
		component: () => import("@/pages/Login.vue"),
	},
]

const router = createRouter({
	history: createWebHistory("/frontend"),
	routes,
})

// Update page title on route change
router.beforeEach(async (to, from, next) => {
	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
	}

	// Update page title
	if (to.meta.title) {
		document.title = to.meta.title
	}

	if (to.name === "Login" && isLoggedIn) {
		next({ name: "Home" })
	} else if (to.name !== "Login" && !isLoggedIn) {
		next({ name: "Login" })
	} else {
		next()
	}
})

export default router