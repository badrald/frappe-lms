<template>
  <div id="app" dir="rtl">
    <template v-if="$route.name === 'Login'">
      <router-view />
    </template>
    <template v-else>
      <div
        class="h-screen bg-gradient-to-br from-secondary-50 via-primary-50 to-purple-50 dark:from-secondary-900 dark:via-secondary-800 dark:to-secondary-900 flex overflow-hidden transition-colors duration-500">
        <!-- Sidebar -->
        <Sidebar />
        <!-- Main Content Area -->
        <div class="flex-1 flex flex-col min-w-0 transition-all duration-300 ease-in-out"
          :class="sidebarOpen ? 'lg:mr-64' : 'lg:mr-0'">
          <!-- Header -->
          <Header />
          <!-- Main Content -->
          <main class="flex-1 overflow-y-auto">
            <div class="p-4 sm:p-6 lg:p-8">
              <div class="animate-fade-in">
                <router-view />
              </div>
            </div>
            <!-- Footer -->
            <footer class="bg-white/80 backdrop-blur-sm border-t mt-8 dark:bg-secondary-800/80">
              <div class="px-4 sm:px-6 lg:px-8 py-6">
                <div class="flex flex-col md:flex-row justify-between items-center">
                  <div class="flex items-center space-x-4">
                    <div class="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center">
                      <BookOpenIcon class="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <p class="text-sm font-medium text-secondary-900 dark:text-secondary-100">نظام إدارة المكتبة</p>
                      <p class="text-xs text-secondary-500 dark:text-secondary-400">© 2025 جميع الحقوق محفوظة</p>
                    </div>
                  </div>
                  <div class="mt-4 md:mt-0">
                    <p class="text-xs text-secondary-500 dark:text-secondary-400">
                      تم التطوير بواسطة <a href="https://github.com/badrald" class="text-secondary-700 hover:text-primary-600 dark:text-secondary-300 dark:hover:text-primary-400">بدر الدين عبد الله </a>
                    </p>
                  </div>
                </div>
              </div>
            </footer>
          </main>
        </div>
        <!-- Loading Overlay -->
        <div v-if="isLoading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div class="bg-white rounded-lg p-6 flex items-center space-x-4">
            <div class="loading-spinner w-6 h-6"></div>
            <span class="text-secondary-700">جاري التحميل...</span>
          </div>
        </div>
        <!-- Toast Notifications -->
        <div class="fixed top-4 right-4 z-50 space-y-2">
          <div v-for="toast in toasts" :key="toast.id"
            class="bg-white rounded-lg shadow-large border-r-4 p-4 max-w-sm animate-slide-in"
            :class="getToastBorderClass(toast.type)">
            <div class="flex items-start">
              <div class="flex-shrink-0">
                <component :is="getToastIcon(toast.type)" class="w-5 h-5" :class="getToastIconClass(toast.type)" />
              </div>
              <div class="mr-3 flex-1">
                <p class="text-sm font-medium text-secondary-900">{{ toast.title }}</p>
                <p v-if="toast.message" class="text-sm text-secondary-600 mt-1">{{ toast.message }}</p>
              </div>
              <button @click="removeToast(toast.id)"
                class="flex-shrink-0 p-1 text-secondary-400 hover:text-secondary-600">
                <XMarkIcon class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { toasts, addToast, removeToast } from './utils/toast'
import { useAppStore } from './stores/app'
import Sidebar from './components/Sidebar.vue'
import Header from './components/Header.vue'
import {
  BookOpenIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  InformationCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline'

// Stores
const appStore = useAppStore()

// Toast notifications are provided by utils/toast.js

// Computed properties
const sidebarOpen = computed(() => appStore.sidebarOpen)
const isLoading = ref(false)

// Methods are imported from utils/toast.js

const getToastBorderClass = (type) => {
  switch (type) {
    case 'success':
      return 'border-success-500'
    case 'error':
      return 'border-danger-500'
    case 'warning':
      return 'border-warning-500'
    default:
      return 'border-primary-500'
  }
}

const getToastIconClass = (type) => {
  switch (type) {
    case 'success':
      return 'text-success-500'
    case 'error':
      return 'text-danger-500'
    case 'warning':
      return 'text-warning-500'
    default:
      return 'text-primary-500'
  }
}

const getToastIcon = (type) => {
  switch (type) {
    case 'success':
      return CheckCircleIcon
    case 'error':
      return XCircleIcon
    case 'warning':
      return ExclamationTriangleIcon
    default:
      return InformationCircleIcon
  }
}

// Initialize app on mount
onMounted(async () => {
  try {
    // Initialize the app store
    await appStore.initializeApp()

    addToast({
      type: 'success',
      title: 'مرحباً بك',
      message: 'تم تحميل البيانات بنجاح'
    })
  } catch (error) {
    console.error('Error initializing app:', error)
    addToast({
      type: 'error',
      title: 'خطأ في التحميل',
      message: 'فشل في تحميل بعض البيانات'
    })
  }
})
</script>
