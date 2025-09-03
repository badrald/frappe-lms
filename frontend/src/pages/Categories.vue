<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">إدارة التصنيفات</h1>
        <p class="mt-2 text-gray-600">تنظيم الكتب حسب التصنيفات والمواضيع</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <Button @click="showAddCategoryModal = true">
          <FeatherIcon name="plus" class="w-4 h-4 mr-2" />
          إضافة تصنيف جديد
        </Button>
      </div>
    </div>
     
    <!-- Search and Filters -->
    <Card>
      <div class="card-body">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Search -->
          <div class="md:col-span-2">
            <Input v-model="searchQuery" placeholder="البحث بالاسم..." />
          </div>
        </div>
      </div>
    </Card>

    <!-- Categories Table -->
    <FancyDataTable :columns="columns" :data="filteredCategories" :page-size="12" :sortable="true">
      <template #actions="{ row }">
        <div class="flex space-x-2">
          <Button @click="editCategory(row)"  theme="gray">Edit</Button>
          <Button @click="deleteCategory(row)"  theme="red" class="ml-2">Delete</Button>
        </div>
      </template>
    </FancyDataTable>

    <Dialog v-model="showAddCategoryModal" title="Add Category">
      <form @submit.prevent="addCategory">
        <div class="space-y-4">
          <Input v-model="newCategory.category_name" label="Name" />
        </div>
        <div class="mt-6 flex justify-end">
          <Button @click="showAddCategoryModal = false" theme="gray" class="mr-2">Cancel</Button>
          <Button type="submit" theme="primary">Save</Button>
        </div>
      </form>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button, Card, Dialog, Input, FeatherIcon } from 'frappe-ui'
import FancyDataTable from '../components/FancyDataTable.vue'
import { categoriesResource, addCategory as addCategoryApi, updateCategory as updateCategoryApi, deleteCategory as deleteCategoryApi } from '../data/categories'

const showAddCategoryModal = ref(false)
const searchQuery = ref('')

const newCategory = ref({
  category_name: '',
})

const columns = ref([
  { key: 'category_name', label: 'الاسم', sortable: true },
])


const filteredCategories = computed(() => {
  if (!categoriesResource.data) return []
  return categoriesResource.data.filter(category => {
    const matchesSearch = !searchQuery.value ||
      category.category_name.toLowerCase().includes(searchQuery.value.toLowerCase())

    return matchesSearch
  })
})

const addCategory = async () => {
  const response = await addCategoryApi(newCategory.value)
  if (response.success) {
    showAddCategoryModal.value = false
    newCategory.value = { category_name: '' }
  }
}

const editCategory = (category) => {
  // Implementation for editing a category
  console.log("editCategory", category)
  // You can add edit functionality here
}

const deleteCategory = async (category) => {
  if (confirm(`Are you sure you want to delete ${category.category_name}?`)) {
    const response = await deleteCategoryApi(category.name)
    if (response.success) {
      // Category deleted successfully
    }
  }
}
</script>