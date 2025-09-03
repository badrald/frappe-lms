import { createResource } from 'frappe-ui'
import { frappeRequest } from 'frappe-ui'

// Resource for fetching all members
export const membersResource = createResource({
  method: "GET",
  url: "lms.api.members.get_all_members",
  auto: true,
})



// Function to add a new member
export const addMember = async (memberData) => {
  try {
    const response = await frappeRequest({
      method: 'POST',
      url: '/api/resource/Member',
      data: memberData,
    })
    membersResource.reload()
    return { success: true, data: response.data }
  } catch (error) {
    console.error('Error adding member:', error)
    return { success: false, error }
  }
}

// Function to update an existing member
export const updateMember = async (memberData) => {
  try {
    await frappeRequest({
      method: 'PUT',
      url: 'lms.lms.doctype.member.member.update_member',
      data: memberData,
    })
    membersResource.reload()
    return { success: true }
  } catch (error) {
    console.error('Error updating member:', error)
    return { success: false, error }
  }
}

// Function to delete a member
export const deleteMember = async (memberName) => {
  try {
    await frappeRequest({
      method: 'DELETE',
      url: 'lms.lms.doctype.member.member.delete_member',
      data: { name: memberName },
    })
    membersResource.reload()
    return { success: true }
  } catch (error) {
    console.error('Error deleting member:', error)
    return { success: false, error }
  }
}

// Function to create a user for a member
export const createUserForMember = async (userData) => {
  try {
    const response = await frappeRequest({
      method: 'POST',
      url: 'lms.api.members.create_user_for_member',
      params: userData,
    })
    membersResource.reload()
    return { success: true, data: response }
  } catch (error) {
    console.error('Error creating user for member:', error)
    return { success: false, error }
  }
}

// Upload member image and return file_url
export const uploadMemberImage = async (file, options = {}) => {
  try {
    const { attach = false, doctype = 'Member', docname, fieldname = 'image', is_private = false } = options
    const formData = new FormData()
    formData.append('file', file, file?.name || 'upload')
    formData.append('is_private', is_private ? '1' : '0')
    if (attach && docname) {
      formData.append('doctype', doctype)
      formData.append('docname', docname)
      if (fieldname) formData.append('fieldname', fieldname)
    }

    const res = await fetch('/api/method/upload_file', {
      method: 'POST',
      body: formData,
      credentials: 'include',
      headers: {
        'X-Frappe-CSRF-Token': window.csrf_token || ''
      }
    })
    if (!res.ok) {
      const text = await res.text()
      throw new Error(text || `Upload failed with ${res.status}`)
    }
    const data = await res.json()
    const payload = data?.message ?? data
    const file_url = payload?.file_url
    if (!file_url) throw new Error('No file_url returned')
    return { success: true, file_url, file_name: payload?.name, attached: Boolean(attach && docname) }
  } catch (error) {
    console.error('Error uploading image:', error)
    return { success: false, error }
  }
}