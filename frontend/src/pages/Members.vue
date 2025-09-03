<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">إدارة الأعضاء</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">إدارة أعضاء المكتبة والعضويات</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <Button @click="showAddMemberModal = true"
          class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded inline-flex items-center">
          <FeatherIcon name="user-plus" class="fill-current w-4 h-4 mr-2" />
          <span>إضافة عضو جديد</span>
        </Button>
      </div>
    </div>

    <!-- Members Table -->
    <div class="bg-white dark:bg-secondary-800 rounded-lg shadow overflow-hidden">
      <FancyDataTable :columns="columns" :data="filteredMembers" :page-size="12" :sortable="true">
        <template #actions="{ row }">
          <div class="flex items-center space-x-2">
            <Button @click="editMember(row)" size="sm" theme="gray" class="flex items-center">
              <FeatherIcon name="edit" class="w-4 h-4 ml-1" />
              <span>تعديل</span>
            </Button>
            <Button @click="deleteMember(row)" size="sm" theme="red" class="flex items-center">
              <FeatherIcon name="trash-2" class="w-4 h-4 ml-1" />
              <span>حذف</span>
            </Button>
          </div>
        </template>
        <template #is_membership_valid="{ row }">
          <Badge v-if="row.is_membership_valid" theme="green">
            <FeatherIcon name="check-circle" class="w-4 h-4 ml-1 inline" />
            سارية
          </Badge>
          <Badge v-else theme="red">
            <FeatherIcon name="x-circle" class="w-4 h-4 ml-1 inline" />
            منتهية
          </Badge>
        </template>
      </FancyDataTable>
    </div>

    <!-- Add Member Modal -->
    <ModernDialog v-model="showAddMemberModal" size="xl">
      <template #title>
        إضافة عضو جديد
      </template>
      <template #description>
        أدخل بيانات المستخدم وسيتم استخدامها لإنشاء حساب العضو تلقائيًا.
      </template>

      <form @submit.prevent="addMember" class="space-y-4">
        <!-- User Profile Image Preview -->
        <div class="flex items-center justify-center mb-4">
          <div class="relative">
            <div
              class="w-24 h-24 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
              <img v-if="memberImagePreview" :src="memberImagePreview" class="w-full h-full object-cover" />
              <UserIcon v-else class="w-12 h-12 text-gray-400 dark:text-gray-500" />
            </div>
            <label class="absolute bottom-0 right-0 bg-primary-600 rounded-full p-1 cursor-pointer">
              <CameraIcon class="w-4 h-4 text-white" />
              <input type="file" accept="image/*" class="hidden" @change="onImageSelected" />
            </label>
          </div>
        </div>

        <!-- User Account Section -->
        <div class="border-b border-gray-200 dark:border-gray-700 pb-2">
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 flex items-center">
            <FeatherIcon name="user" class="w-5 h-5 ml-2 text-primary-600" />
            معلومات المستخدم
          </h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormInput v-model="newUser.first_name" label="الاسم الأول" :required="true" />
          <FormInput v-model="newUser.last_name" label="اسم العائلة" :required="true" />
          <FormInput v-model="newUser.email" label="البريد الإلكتروني" type="email" :required="true" />
          <FormInput v-model="newUser.phone_number" label="رقم الهاتف" />
        </div>

        <!-- Member Information Section -->
        <div class="border-b border-gray-200 dark:border-gray-700 pb-2 mt-6">
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 flex items-center">
            <FeatherIcon name="users" class="w-5 h-5 ml-2 text-primary-600" />
            معلومات العضو
          </h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Member name will be auto-populated from user first and last name -->
          <div class="md:col-span-2">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">اسم العضو</label>
            <div class="px-3 py-2 bg-gray-100 dark:bg-gray-700 rounded-md text-gray-900 dark:text-gray-100">
              {{ newUser.first_name }} {{ newUser.last_name }}
            </div>
          </div>

          <FormInput v-model="newUser.address" label="العنوان" />
          <FormInput v-model="newUser.join_date" label="تاريخ الانضمام" type="date" :required="true" />
          <FormSelect v-model="newUser.member_type" label="نوع العضوية" :options="[
            { label: 'Normal', value: 'Normal' },
            { label: 'VIP', value: 'VIP' },
          ]" />
          <div class="flex items-center mt-6">
            <input v-model="newUser.is_membership_valid" type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" :value="1"
              :unchecked-value="0" />
            <label class="ml-2 block text-sm text-gray-900 dark:text-gray-100 flex items-center">
              <FeatherIcon name="award" class="w-4 h-4 ml-1" />
              العضوية سارية
            </label>
          </div>
        </div>
      </form>

      <template #actions>
        <Button @click="showAddMemberModal = false" theme="gray" class="mr-2">
          <FeatherIcon name="x" class="w-4 h-4 ml-1" />
          إلغاء
        </Button>
        <Button @click="addMember" theme="primary"
          class="bg-primary-600 hover:bg-primary-700 text-white font-bold py-2 px-4 rounded inline-flex items-center">
          <FeatherIcon name="save" class="w-4 h-4 ml-1" />
          حفظ
        </Button>
      </template>
    </ModernDialog>

    <!-- Edit Member Modal -->
    <ModernDialog v-model="showEditMemberModal" size="xl">
      <template #title>
        تعديل بيانات العضو
      </template>
      <template #description>
        تعديل بيانات العضو وحساب المستخدم المرتبط.
      </template>

      <form @submit.prevent="updateMember" class="space-y-4">
        <!-- User Profile Image Preview -->
        <div class="flex items-center justify-center mb-4">
          <div class="relative">
            <div
              class="w-24 h-24 rounded-full overflow-hidden bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
              <img v-if="editImagePreview || editMemberData.user_image"
                :src="editImagePreview || editMemberData.user_image" class="w-full h-full object-cover" />
              <UserIcon v-else class="w-12 h-12 text-gray-400 dark:text-gray-500" />
            </div>
            <label class="absolute bottom-0 right-0 bg-primary-600 rounded-full p-1 cursor-pointer">
              <CameraIcon class="w-4 h-4 text-white" />
              <input type="file" accept="image/*" class="hidden" @change="onEditImageSelected" />
            </label>
          </div>
        </div>

        <!-- User Account Section -->
        <div class="border-b border-gray-200 dark:border-gray-700 pb-2">
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 flex items-center">
            <FeatherIcon name="user" class="w-5 h-5 ml-2 text-primary-600" />
            معلومات المستخدم
          </h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormInput v-model="editMemberData.first_name" label="الاسم الأول" :required="true" />
          <FormInput v-model="editMemberData.last_name" label="اسم العائلة" :required="true" />
          <FormInput v-model="editMemberData.user_email" label="البريد الإلكتروني" type="email" :required="true" />
          <FormInput v-model="editMemberData.phone_number" label="رقم الهاتف" />
        </div>

        <!-- Member Information Section -->
        <div class="border-b border-gray-200 dark:border-gray-700 pb-2 mt-6">
          <h3 class="text-lg font-medium text-gray-900 dark:text-gray-100 flex items-center">
            <FeatherIcon name="users" class="w-5 h-5 ml-2 text-primary-600" />
            معلومات العضو
          </h3>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <FormInput v-model="editMemberData.memeber_name" label="اسم العضو" :required="true" />
          <FormInput v-model="editMemberData.address" label="العنوان" />
          <FormInput v-model="editMemberData.phone_number" label="رقم الهاتف" />
          <FormInput v-model="editMemberData.join_date" label="تاريخ الانضمام" type="date" />
          <FormSelect v-model="editMemberData.member_type" label="نوع العضوية" :options="[
            { label: 'Normal', value: 'Normal' },
            { label: 'VIP', value: 'VIP' },
          ]" />
          <div class="flex items-center mt-6">
            <input v-model="editMemberData.is_membership_valid" type="checkbox"
              class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded" :value="1"
              :unchecked-value="0" />
            <label class="ml-2 block text-sm text-gray-900 dark:text-gray-100 flex items-center">
              <FeatherIcon name="award" class="w-4 h-4 ml-1" />
              العضوية سارية
            </label>
          </div>
        </div>
      </form>

      <template #actions>
        <Button @click="showEditMemberModal = false" theme="gray" class="mr-2">
          <FeatherIcon name="x" class="w-4 h-4 ml-1" />
          إلغاء
        </Button>
        <Button @click="updateMember" theme="primary">
          <FeatherIcon name="save" class="w-4 h-4 ml-1" />
          حفظ
        </Button>
      </template>
    </ModernDialog>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Button, FeatherIcon, Badge } from 'frappe-ui'
import FancyDataTable from '../components/FancyDataTable.vue'
import ModernDialog from '../components/ModernDialog.vue'
import FormInput from '../components/FormInput.vue'
import FormSelect from '../components/FormSelect.vue'
import { membersResource, createUserForMember, uploadMemberImage } from '../data/members'
import { UserIcon, CameraIcon } from '@heroicons/vue/24/outline'

const showAddMemberModal = ref(false)
const showEditMemberModal = ref(false)
const memberImageFile = ref(null)
const memberImagePreview = ref(null)
const editImageFile = ref(null)
const editImagePreview = ref(null)

const newUser = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone_number: '',
  address: '',
  join_date: '',
  member_type: 'Normal',
  is_membership_valid: 1,
  password: '',
  user_image: ''
})

const editMemberData = ref({
  name: '',
  first_name: '',
  last_name: '',
  user_email: '',
  phone_number: '',
  address: '',
  join_date: '',
  member_type: 'Normal',
  is_membership_valid: 1,
  user_image: '',
  memeber_name: ''
})

const columns = ref([
  { key: 'memeber_name', label: 'اسم العضو', sortable: true },
  { key: 'user_email', label: 'البريد الإلكتروني', sortable: true },
  { key: 'phone_number', label: 'رقم الهاتف', sortable: false },
  { key: 'member_type', label: 'نوع العضوية', sortable: false },
  { key: 'is_membership_valid', label: 'العضوية', sortable: false },
])

const filteredMembers = computed(() => {
  if (!membersResource.data) return []
  console.log(membersResource.data)
  return membersResource.data
})

const onImageSelected = (e) => {
  const file = e.target.files[0]
  if (file) {
    memberImageFile.value = file
    memberImagePreview.value = URL.createObjectURL(file)
  }
}

const onEditImageSelected = (e) => {
  const file = e.target.files[0]
  if (file) {
    editImageFile.value = file
    editImagePreview.value = URL.createObjectURL(file)
  }
}

const addMember = async () => {
  // Basic validation for user
  if (!newUser.value.first_name || !newUser.value.last_name || !newUser.value.email || !newUser.value.join_date || !newUser.value.member_type) {
    alert('الرجاء إدخال جميع بيانات المستخدم المطلوبة')
    return
  }

  // Upload image if available
  if (memberImageFile.value) {
    const uploadResult = await uploadMemberImage(memberImageFile.value)
    if (uploadResult.success) {
      newUser.value.user_image = uploadResult.file_url
    } else {
      toast('حدث خطأ أثناء رفع الصورة')
      return
    }
  }

  // First create the member with basic data
  const memberData = {
    memeber_name: `${newUser.value.first_name} ${newUser.value.last_name}`,
    address: newUser.value.address,
    phone_number: newUser.value.phone_number,
    join_date: newUser.value.join_date,
    member_type: newUser.value.member_type,
    is_membership_valid: newUser.value.is_membership_valid,
    image: newUser.value.user_image
  }

  // For now, we'll need to create a simple member creation function
  // In a real implementation, this would call an API endpoint
  try {
    const response = await fetch('/api/resource/Member', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token
      },
      body: JSON.stringify(memberData)
    });

    if (!response.ok) {
      throw new Error('Failed to create member');
    }

    const memberResult = await response.json();

    // Then create the user and link to member using the ready API
    const userData = {
      ...newUser.value,
      member_id: memberResult.data.name
    }

    const userResponse = await createUserForMember(userData)
    if (userResponse.success) {
      showAddMemberModal.value = false
      // Reset form
      newUser.value = {
        first_name: '',
        last_name: '',
        email: '',
        phone_number: '',
        address: '',
        join_date: '',
        member_type: 'Normal',
        is_membership_valid: 1,
        password: '',
        user_image: ''
      }
      memberImageFile.value = null
      memberImagePreview.value = null
      membersResource.reload()
    } else {
      alert('حدث خطأ أثناء إنشاء حساب المستخدم')
    }
  } catch (error) {
    alert('حدث خطأ أثناء إضافة العضو: ' + error.message)
  }
}

const editMember = (member) => {
  // Populate edit form with member data
  editMemberData.value = {
    name: member.name,
    memeber_name: member.memeber_name || '',
    first_name: member.user_name ? member.user_name.split(' ')[0] : '',
    last_name: member.user_name ? member.user_name.split(' ').slice(1).join(' ') : '',
    user_email: member.user_email || '',
    phone_number: member.phone_number || '',
    address: member.address || '',
    join_date: member.join_date || '',
    member_type: member.member_type || 'Normal',
    is_membership_valid: member.is_membership_valid || 0,
    user_image: member.user_image || ''
  }
  showEditMemberModal.value = true
}

const updateMember = async () => {
  // Handle image upload if a new image was selected
  if (editImageFile.value) {
    const uploadResult = await uploadMemberImage(editImageFile.value)
    if (uploadResult.success) {
      editMemberData.value.user_image = uploadResult.file_url
    } else {
      alert('حدث خطأ أثناء رفع الصورة')
      return
    }
  }

  // In a real implementation, you would update both the member and user data here
  console.log("Update member with data:", editMemberData.value)
  showEditMemberModal.value = false
  editImageFile.value = null
  editImagePreview.value = null
  membersResource.reload()
}

const deleteMember = async (member) => {
  if (confirm(`Are you sure you want to delete ${member.memeber_name}?`)) {
    // Note: In a real implementation, you would also need to import deleteMemberApi
    console.log("Delete member:", member.name)
    // const response = await deleteMemberApi(member.name)
    // if (response.success) {
    //   // Member deleted successfully
    // }
  }
}
</script>