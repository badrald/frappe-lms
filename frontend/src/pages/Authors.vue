<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">إدارة المؤلفين</h1>
        <p class="mt-2 text-gray-600">إدارة معلومات المؤلفين وكتبهم</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <Button @click="showAddAuthorModal = true" class="btn bg-primary-500  text-white">
          <FeatherIcon name="user-plus" class="w-4 h-4 mr-2" />
          إضافة مؤلف جديد
        </Button>
      </div>
    </div>


    <!-- Authors Table -->
    <FancyDataTable :columns="columns" :data="filteredAuthors" :page-size="10" :sortable="true" :show-page-size="true">
      <template #actions="{ row }">
        <div class="flex space-x-2">
          <Button @click="editAuthor(row)" size="sm" theme="gray">
            <FeatherIcon name="edit-2" class="w-4 h-4" />
          </Button>
          <Button @click="deleteAuthor(row)" size="sm" theme="red">
            <FeatherIcon name="trash-2" class="w-4 h-4" />
          </Button>
        </div>
      </template>
      <template #empty>
        <div class="py-6">لا يوجد مؤلفون لعرضهم.</div>
      </template>
    </FancyDataTable>

    <!-- Add Author Modal -->
    <ModernDialog v-model="showAddAuthorModal">
      <template #title>
        إضافة مؤلف جديد
      </template>

      <form @submit.prevent="addAuthor" class="space-y-4">
        <Input v-model="newAuthor.author_name" label="الاسم" />
        <Input v-model="newAuthor.bio" label="نبذة قصيرة" />
      </form>

      <template #actions>
        <Button @click="showAddAuthorModal = false" theme="gray" class="mr-2">إلغاء</Button>
        <Button @click="addAuthor" theme="primary">حفظ</Button>
      </template>
    </ModernDialog>

    <!-- Edit Author Modal -->
    <ModernDialog v-model="showEditAuthorModal">
      <template #title>
        تعديل بيانات المؤلف
      </template>

      <form @submit.prevent="updateAuthor" class="space-y-4">
        <Input v-model="editAuthorData.author_name" label="الاسم" />
        <Input v-model="editAuthorData.bio" label="نبذة قصيرة" />
      </form>

      <template #actions>
        <Button @click="showEditAuthorModal = false" theme="gray" class="mr-2">إلغاء</Button>
        <Button @click="updateAuthor" theme="primary">تحديث</Button>
      </template>
    </ModernDialog>

    <!-- Delete Author Confirmation -->
    <ModernDialog v-model="showDeleteAuthorModal">
      <template #title>
        حذف مؤلف
      </template>

      <div class="space-y-4">
        <p>هل أنت متأكد أنك تريد حذف <span class="font-bold">{{ deleteAuthorData.author_name }}</span>؟</p>
      </div>

      <template #actions>
        <Button @click="showDeleteAuthorModal = false" theme="gray" class="mr-2">إلغاء</Button>
        <Button @click="confirmDeleteAuthor" theme="danger">حذف</Button>
      </template>
    </ModernDialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createResource, Button, Card, Input, FeatherIcon, frappeRequest } from 'frappe-ui'
import ModernDialog from '../components/ModernDialog.vue'
import FancyDataTable from '../components/FancyDataTable.vue'

const showAddAuthorModal = ref(false)
const showEditAuthorModal = ref(false)
const showDeleteAuthorModal = ref(false)
const searchQuery = ref('')

const newAuthor = ref({
  author_name: '',
  bio: '',
})

const editAuthorData = ref({
  name: '',
  author_name: '',
  bio: '',
})

const deleteAuthorData = ref({
  name: '',
  author_name: '',
})

const authorsResource = createResource({
  url: 'lms.api.authors.get_all_authors',
  auto: true,
})

const columns = ref([
  { key: 'author_name', label: 'الاسم', sortable: true },
  { key: 'bio', label: 'نبذة', sortable: false },
])

const filteredAuthors = computed(() => {
  if (!authorsResource.data || !authorsResource.data.data) return []
  let authors = authorsResource.data.data
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    authors = authors.filter(a => (a.author_name && a.author_name.toLowerCase().includes(q)))
  }
  return authors
})

const addAuthor = async () => {
  try {
    await frappeRequest({ method: 'POST', url: 'lms.api.authors.add_author', data: newAuthor.value })
    authorsResource.reload()
    showAddAuthorModal.value = false
    newAuthor.value = { author_name: '', bio: '' }
  } catch (e) {
    console.error('Error adding author:', e)
  }
}

const editAuthor = (author) => {
  editAuthorData.value = { ...author }
  showEditAuthorModal.value = true
}

const updateAuthor = async () => {
  try {
    await frappeRequest({ method: 'PUT', url: 'lms.api.authors.update_author', data: editAuthorData.value })
    authorsResource.reload()
    showEditAuthorModal.value = false
  } catch (e) {
    console.error('Error updating author:', e)
  }
}

const deleteAuthor = (author) => {
  deleteAuthorData.value = { name: author.name, author_name: author.author_name }
  showDeleteAuthorModal.value = true
}

const confirmDeleteAuthor = async () => {
  try {
    await frappeRequest({ method: 'DELETE', url: 'lms.api.authors.delete_author', data: { name: deleteAuthorData.value.name } })
    authorsResource.reload()
    showDeleteAuthorModal.value = false
  } catch (e) {
    console.error('Error deleting author:', e)
  }
}
</script>