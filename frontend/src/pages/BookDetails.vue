<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">تفاصيل الكتاب</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">عرض وتعديل بيانات الكتاب</p>
      </div>
      <div class="mt-4 sm:mt-0 flex gap-2">
        <Button theme="gray" @click="goBack" class="flex items-center">
          <FeatherIcon name="arrow-right" class="w-4 h-4 ml-2" /> رجوع
        </Button>
        <Button theme="primary" @click="openEdit" class="flex items-center">
          <FeatherIcon name="edit-2" class="w-4 h-4 ml-2" /> تعديل
        </Button>
        <Button theme="red" @click="openDelete" class="flex items-center">
          <FeatherIcon name="trash-2" class="w-4 h-4 ml-2" /> حذف
        </Button>
      </div>
    </div>

    <!-- Content -->
    <Card class="bg-white dark:bg-secondary-800 border border-secondary-100 dark:border-secondary-700">
      <div class="p-6 grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Details -->
        <div class="lg:col-span-2">
          <div class="space-y-4">
            <div class="flex items-center gap-3">
              <h2 class="text-2xl font-semibold text-gray-900 dark:text-gray-100">{{ book?.title || '—' }}</h2>
              <Badge :theme="book?.status === 'Active' ? 'green' : 'yellow'">{{ book?.status || 'Unknown' }}</Badge>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div class="rounded-lg p-4 bg-secondary-50 dark:bg-secondary-900/40">
                <p class="text-secondary-500">ISBN</p>
                <p class="font-medium text-secondary-900 dark:text-secondary-100">{{ book?.isbn || '—' }}</p>
              </div>
              <div class="rounded-lg p-4 bg-secondary-50 dark:bg-secondary-900/40">
                <p class="text-secondary-500">الناشر</p>
                <p class="font-medium text-secondary-900 dark:text-secondary-100">{{ book?.publisher || '—' }}</p>
              </div>
              <div class="rounded-lg p-4 bg-secondary-50 dark:bg-secondary-900/40">
                <p class="text-secondary-500">الفئة</p>
                <p class="font-medium text-secondary-900 dark:text-secondary-100">{{ book?.category || '—' }}</p>
              </div>
              <div class="rounded-lg p-4 bg-secondary-50 dark:bg-secondary-900/40">
                <p class="text-secondary-500">التوفر</p>
                <p class="font-medium text-secondary-900 dark:text-secondary-100">{{ book?.available_copies ?? '—' }} /
                  {{ book?.total_copies ?? '—' }}</p>
              </div>
            </div>

            <div v-if="book?.authors?.length" class="mt-2">
              <p class="text-secondary-500 mb-2">المؤلفون</p>
              <div class="flex flex-wrap gap-2">
                <Badge v-for="a in book.authors" :key="a.name" theme="blue">{{ a.author_name }}</Badge>
              </div>
            </div>
            <div class="mt-2">
              <p class="text-secondary-500 mb-2">الوصف</p>
              <p class="font-medium text-secondary-900 dark:text-secondary-100 whitespace-pre-line">
                {{ book?.description || '—' }}
              </p>
            </div>
          </div>
        </div>
        <!-- Cover -->
        <div>
          <div
            class="aspect-[3/4] bg-gradient-to-br from-primary-100 to-primary-200 dark:from-primary-900 dark:to-primary-800 rounded-lg flex items-center justify-center overflow-hidden">
            <img v-if="book?.cover" :src="book.cover" :alt="book.title" class="w-full h-full object-cover" />
            <BookOpenIcon v-else class="w-16 h-16 text-primary-600 dark:text-primary-400" />
          </div>
        </div>

      </div>
    </Card>

    <!-- Edit Dialog -->
    <ModernDialog v-model="showEdit">
      <template #title>تعديل بيانات الكتاب</template>
      <form @submit.prevent="submitEdit" class="space-y-4">
        <FormInput v-model="editData.title" label="Title" />
        <FormInput v-model="editData.isbn" label="ISBN" />
        <FormInput v-model="editData.publisher" label="Publisher" />
        <FormInput v-model="editData.status" label="Status" />
        <FormInput v-model="editData.category" label="Category" />
        <div class="space-y-2">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300" for="description">الوصف</label>
          <textarea id="description" name="description" v-model="editData.description" rows="4"
            class="block w-full rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 focus:border-transparent transition duration-200 ease-in-out placeholder-gray-400 dark:placeholder-gray-500 px-4 py-2"></textarea>
        </div>
        <FormInput v-model.number="editData.total_copies" label="Total Copies" />
        <FormInput v-model.number="editData.available_copies" label="Available Copies" />
      </form>
      <template #actions>
        <Button theme="gray" @click="showEdit = false">إلغاء</Button>
        <Button theme="primary" @click="submitEdit">حفظ</Button>
      </template>
    </ModernDialog>

    <!-- Delete Dialog -->
    <ModernDialog v-model="showDelete">
      <template #title>تأكيد الحذف</template>
      <div>هل تريد حذف <span class="font-bold">{{ book?.title }}</span>؟</div>
      <template #actions>
        <Button theme="gray" @click="showDelete = false">إلغاء</Button>
        <Button theme="red" @click="confirmDelete">حذف</Button>
      </template>
    </ModernDialog>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Button, Card, Badge, FeatherIcon } from 'frappe-ui'
import ModernDialog from '@/components/ModernDialog.vue'
import FormInput from '@/components/FormInput.vue'
import { createBookDetailsResource, updateBook as updateBookApi, deleteBook as deleteBookApi } from '@/data/books'
import { BookOpenIcon } from '@heroicons/vue/24/outline'

const route = useRoute()
const router = useRouter()

const bookId = ref(route.params.id)
let detailsResource = createBookDetailsResource(bookId.value)

watch(() => route.params.id, (id) => {
  bookId.value = id
  detailsResource = createBookDetailsResource(bookId.value)
})

const book = computed(() => detailsResource.data?.data || null)

const showEdit = ref(false)
const showDelete = ref(false)

const editData = ref({})

const openEdit = () => {
  if (!book.value) return
  editData.value = { ...book.value }
  showEdit.value = true
}

const openDelete = () => {
  showDelete.value = true
}

const submitEdit = async () => {
  if (!book.value?.name) return
  const payload = { ...editData.value, name: book.value.name }
  const res = await updateBookApi(payload)
  if (res.success) {
    showEdit.value = false
    detailsResource.reload()
  }
}

const confirmDelete = async () => {
  if (!book.value?.name) return
  const res = await deleteBookApi(book.value.name)
  if (res.success) {
    showDelete.value = false
    router.replace({ name: 'Books' })
  }
}

const goBack = () => {
  router.back()
}
</script>
