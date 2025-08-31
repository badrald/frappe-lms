<template>
  <div class="space-y-8">
    <!-- Welcome Section -->
    <div class="text-center">
      <h1 class="text-4xl font-bold text-secondary-900 dark:text-secondary-100 mb-4">
        أهلاً وسهلاً بك في نظام إدارة المكتبة
      </h1>
      <p class="text-lg text-secondary-600 dark:text-secondary-400">
        مرحباً {{ session.user }}! إليك نظرة سريعة على أداء مكتبتك اليوم
      </p>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <!-- Total Books -->
      <div class="card-3d p-6 text-center hover:scale-105 transition-transform duration-300">
        <div class="w-16 h-16 bg-gradient-primary rounded-full mx-auto mb-4 flex items-center justify-center">
          <BookOpenIcon class="w-8 h-8 text-white" />
        </div>
        <h3 class="text-2xl font-bold text-secondary-900 dark:text-secondary-100">{{ formatNumber(stats.total_books) }}</h3>
        <p class="text-sm text-secondary-600 dark:text-secondary-400">إجمالي الكتب</p>
      </div>

      <!-- Available Books -->
      <div class="card-3d p-6 text-center hover:scale-105 transition-transform duration-300">
        <div class="w-16 h-16 bg-gradient-to-r from-success-500 to-success-600 rounded-full mx-auto mb-4 flex items-center justify-center">
          <UsersIcon class="w-8 h-8 text-white" />
        </div>
        <h3 class="text-2xl font-bold text-secondary-900 dark:text-secondary-100">{{ formatNumber(stats.available_books) }}</h3>
        <p class="text-sm text-secondary-600 dark:text-secondary-400">الكتب المتاحة</p>
      </div>

      <!-- Books Borrowed -->
      <div class="card-3d p-6 text-center hover:scale-105 transition-transform duration-300">
        <div class="w-16 h-16 bg-gradient-to-r from-warning-500 to-warning-600 rounded-full mx-auto mb-4 flex items-center justify-center">
          <ArrowsRightLeftIcon class="w-8 h-8 text-white" />
        </div>
        <h3 class="text-2xl font-bold text-secondary-900 dark:text-secondary-100">{{ formatNumber(stats.borrowed_books) }}</h3>
        <p class="text-sm text-secondary-600 dark:text-secondary-400">كتب معارة حالياً</p>
      </div>

      <!-- Categories Count -->
      <div class="card-3d p-6 text-center hover:scale-105 transition-transform duration-300">
        <div class="w-16 h-16 bg-gradient-to-r from-danger-500 to-danger-600 rounded-full mx-auto mb-4 flex items-center justify-center">
          <ExclamationTriangleIcon class="w-8 h-8 text-white" />
        </div>
        <h3 class="text-2xl font-bold text-secondary-900 dark:text-secondary-100">{{ formatNumber((stats.categories || []).length) }}</h3>
        <p class="text-sm text-secondary-600 dark:text-secondary-400">عدد التصنيفات</p>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card p-6 hover:shadow-xl transition-shadow duration-300">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center ml-3">
            <PlusIcon class="w-5 h-5 text-primary-600" />
          </div>
          <h3 class="text-lg font-semibold text-secondary-900 dark:text-secondary-100">إضافة كتاب جديد</h3>
        </div>
        <p class="text-sm text-secondary-600 dark:text-secondary-400 mb-4">
          أضف كتاباً جديداً إلى مجموعة المكتبة
        </p>
        <Button variant="solid" class="btn-primary w-full" @click="navigateToBooks">
          إضافة كتاب
        </Button>
      </div>

      <div class="card p-6 hover:shadow-xl transition-shadow duration-300">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-success-100 rounded-lg flex items-center justify-center ml-3">
            <UserPlusIcon class="w-5 h-5 text-success-600" />
          </div>
          <h3 class="text-lg font-semibold text-secondary-900 dark:text-secondary-100">عضو جديد</h3>
        </div>
        <p class="text-sm text-secondary-600 dark:text-secondary-400 mb-4">
          سجل عضواً جديداً في المكتبة
        </p>
        <Button variant="solid" class="bg-success-600 hover:bg-success-700 text-white w-full" @click="navigateToMembers">
          تسجيل عضو
        </Button>
      </div>

      <div class="card p-6 hover:shadow-xl transition-shadow duration-300">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-warning-100 rounded-lg flex items-center justify-center ml-3">
            <ArrowsRightLeftIcon class="w-5 h-5 text-warning-600" />
          </div>
          <h3 class="text-lg font-semibold text-secondary-900 dark:text-secondary-100">معاملة جديدة</h3>
        </div>
        <p class="text-sm text-secondary-600 dark:text-secondary-400 mb-4">
          إجراء عملية إعارة أو إرجاع كتاب
        </p>
        <Button variant="solid" class="bg-warning-600 hover:bg-warning-700 text-white w-full" @click="navigateToTransactions">
          معاملة جديدة
        </Button>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Borrowings -->
      <div class="card">
        <div class="p-6 border-b border-secondary-200 dark:border-secondary-700">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-secondary-900 dark:text-secondary-100">أحدث العمليات</h3>
            <Button variant="ghost" size="sm" @click="navigateToTransactions">
              عرض الكل
            </Button>
          </div>
        </div>
        <div class="p-6 space-y-4">
          <div v-for="activity in recentActivities" :key="activity.id" class="flex items-center">
            <div class="w-10 h-10 rounded-full flex items-center justify-center ml-3" :class="activity.bgColor">
              <component :is="activity.icon" class="w-5 h-5" :class="activity.iconColor" />
            </div>
            <div class="flex-1">
              <p class="text-sm font-medium text-secondary-900 dark:text-secondary-100">{{ activity.title }}</p>
              <p class="text-xs text-secondary-500">{{ activity.time }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- System Status -->
      <div class="card">
        <div class="p-6 border-b border-secondary-200 dark:border-secondary-700">
          <h3 class="text-lg font-semibold text-secondary-900 dark:text-secondary-100">حالة النظام</h3>
        </div>
        <div class="p-6 space-y-4">
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <div class="w-3 h-3 bg-success-500 rounded-full ml-2 animate-pulse"></div>
              <span class="text-sm text-secondary-700 dark:text-secondary-300">النظام يعمل بشكل طبيعي</span>
            </div>
            <span class="text-xs text-success-600">متصل</span>
          </div>
          
          <div class="flex items-center justify-between">
            <span class="text-sm text-secondary-700 dark:text-secondary-300">آخر نسخة احتياطية</span>
            <span class="text-xs text-secondary-500">منذ ساعتين</span>
          </div>
          
          <div class="flex items-center justify-between">
            <span class="text-sm text-secondary-700 dark:text-secondary-300">استخدام التخزين</span>
            <span class="text-xs text-secondary-500">65%</span>
          </div>
          
          <div class="w-full bg-secondary-200 dark:bg-secondary-700 rounded-full h-2">
            <div class="bg-success-600 h-2 rounded-full" style="width: 65%"></div>
          </div>

          <Button variant="outline" size="sm" class="w-full mt-4" @click="navigateToReports">
            عرض التقارير التفصيلية
          </Button>
        </div>
      </div>
    </div>

    <!-- Dialog -->
    <Dialog title="الإعدادات" v-model="showDialog">
      <div class="p-4">
        <p>محتوى النافذة المنبثقة</p>
      </div>
    </Dialog>
  </div>
</template>

<script setup>
import { Dialog, Button } from "frappe-ui"
import { createResource } from "frappe-ui"
import { ref, computed } from "vue"
import { useRouter } from "vue-router"
import { session } from "../data/session"
import { statsResource } from "../data/books"
import {
  BookOpenIcon,
  UsersIcon,
  ArrowsRightLeftIcon,
  ExclamationTriangleIcon,
  PlusIcon,
  UserPlusIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon
} from '@heroicons/vue/24/outline'

const router = useRouter()
const ping = createResource({
	url: "ping",
	auto: true,
})

const showDialog = ref(false)
const isDevelopment = computed(() => import.meta.env.DEV)

// Stats from backend
const stats = computed(() => statsResource.data?.data || {})
const formatNumber = (v) => {
  if (v === null || v === undefined) return '—'
  const n = Number(v)
  return Number.isFinite(n) ? n.toLocaleString() : '—'
}

// Sample recent activities data
const recentActivities = ref([
  {
    id: 1,
    title: 'تم إعارة كتاب "الأسود يليق بك" لفاطمة علي',
    time: 'منذ 5 دقائق',
    icon: BookOpenIcon,
    bgColor: 'bg-primary-100',
    iconColor: 'text-primary-600'
  },
  {
    id: 2,
    title: 'تم إرجاع كتاب "1984" من أحمد محمد',
    time: 'منذ 15 دقيقة',
    icon: CheckCircleIcon,
    bgColor: 'bg-success-100',
    iconColor: 'text-success-600'
  },
  {
    id: 3,
    title: 'عضو جديد: سارة حسين تم تسجيلها',
    time: 'منذ 30 دقيقة',
    icon: UserPlusIcon,
    bgColor: 'bg-info-100',
    iconColor: 'text-info-600'
  },
  {
    id: 4,
    title: 'تحذير: كتاب "مئة عام من العزلة" متأخر',
    time: 'منذ ساعة',
    icon: ExclamationTriangleIcon,
    bgColor: 'bg-warning-100',
    iconColor: 'text-warning-600'
  }
])

// Navigation methods
const navigateToBooks = () => {
  router.push('/books')
}

const navigateToMembers = () => {
  router.push('/members')
}

const navigateToTransactions = () => {
  router.push('/transactions')
}

const navigateToReports = () => {
  router.push('/reports')
}
</script>
