import { createResource } from 'frappe-ui'
import { frappeRequest } from 'frappe-ui'

// Resource for fetching all books
export const booksResource = createResource({
  url: "lms.api.books.get_all_books",
  auto: true,
})

export const statsResource = createResource({
  url: 'lms.api.books.get_book_stats',
  auto: true,
})

// Resource factory to fetch details of a single book by id
export const createBookDetailsResource = (bookId) =>
  createResource({
    url: 'lms.api.books.get_book_by_id',
    makeParams() {
      return { book_id: bookId }
    },
    auto: true,
  })

// - Restricts to known fields to avoid unknown-field errors
function buildBookPayload(input = {}, { requireMandatory = true } = {}) {
  const payload = {
    // Mandatory in Book: title
    title:input.title,
    isbn: input.isbn,
    publisher: input.publisher,
    status: input.status,
    cover: input.cover, // Attach/Attach Image field expects file_url
    total_copies: input.total_copies ?? input.totalCopies,
    available_copies: input.available_copies ?? input.availableCopies,
    category: input.category ?? input.category_id ?? input.categoryName,
    description: input.description,
  }
  // Remove undefined keys
  Object.keys(payload).forEach((k) => payload[k] === undefined && delete payload[k])
  if (requireMandatory) {
    if (!payload.title || String(payload.title).trim() === '') {
      throw new Error('Missing mandatory field: title')
    }
  } else {
    // For partial updates, do not send empty title
    if (
      payload.title === undefined ||
      String(payload.title ?? '').trim() === ''
    ) {
      delete payload.title
    }
  }
  return payload
}

// Function to add a new book
export const addBook = async (bookData) => {
  try {
    const data = buildBookPayload(bookData, { requireMandatory: true })
    const res = await frappeRequest({
      method: 'POST',
      url: 'lms.api.books.add_book',
      params:data,
    })
    const payload = res?.message ?? res
    const created = payload?.data ?? payload
    const name = created?.name
    if (name) {
      booksResource.reload()
      return { success: true, name }
    }
    const msg = payload?.message || 'Failed to add book'
    return { success: false, error: new Error(msg), server: payload }
  } catch (error) {
    console.error('Error adding book:', error)
    return { success: false, error }
  }
}

export const FeatchBookData = async (isbn) => {
  try {
    if (!isbn) {
      throw new Error('ISBN is required')
    }

    const res = await frappeRequest({
      method: 'GET',
      url: 'lms.api.books.fetch_book_details_from_isbn',
      params: { isbn: isbn }
    })

    const payload = res?.message ?? res
    if (payload?.success) {
      return { success: true, data: payload.data }
    } else {
      const msg = payload?.message || 'Failed to fetch book data'
      return { success: false, error: new Error(msg), server: payload }
    }
  } catch (error) {
    console.error('Error fetching book data:', error)
  }
}

// Function to update an existing book
export const updateBook = async (bookData) => {
  try {
    const name = bookData?.name
    if (!name) {
      throw new Error('Book "name" is required for update')
    }
    const data = buildBookPayload(bookData, { requireMandatory: false })
    // name is in the URL; avoid sending it in the body if present
    delete data.name
    const res = await frappeRequest({
      method: 'PUT',
      url: `/api/resource/Book/${encodeURIComponent(name)}`,
      params: data,
    })
    const payload = res?.message ?? res
    const updated = payload?.data ?? payload
    const updatedName = updated?.name
    if (updatedName) {
      booksResource.reload()
      return { success: true, name: updatedName }
    }
    const msg = payload?.message || 'Failed to update book'
    return { success: false, error: new Error(msg), server: payload }
  } catch (error) {
    console.error('Error updating book:', error)
    return { success: false, error }
  }
}

// Function to delete a book
export const deleteBook = async (bookName) => {
  try {
    if (!bookName) {
      throw new Error('Book name is required for delete')
    }
    const res = await frappeRequest({
      method: 'DELETE',
      url: `/api/resource/Book/${encodeURIComponent(bookName)}`,
    })
    const payload = res?.message ?? res
    const ok = payload?.message === 'ok'
    if (ok) {
      booksResource.reload()
      return { success: true }
    }
    const msg = payload?.message || 'Failed to delete book'
    return { success: false, error: new Error(msg), server: payload }
  } catch (error) {
    console.error('Error deleting book:', error)
    return { success: false, error }
  }
}

// Upload cover image and return file_url
export const uploadBookCover = async (file, options = {}) => {
  try {
    const { attach = false, doctype = 'Book', docname, fieldname = 'cover', is_private = false } = options
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
    console.error('Error uploading cover:', error)
    return { success: false, error }
  }
}

// Helper to create a book and attach a cover file in one flow
export const addBookWithCover = async (bookData, file) => {
  // 1) Create the Book first (without cover)
  const created = await addBook({ ...bookData, cover: undefined })
  if (!created.success) return created
  const name = created.name
  // 2) Upload and attach file to Book.cover
  if (file) {
    const up = await uploadBookCover(file, { attach: true, doctype: 'Book', docname: name, fieldname: 'cover' })
    if (!up.success) return up
    // 3) Ensure cover field has file_url (in case server didn't set it during upload)
    await updateBook({ name, cover: up.file_url })
  }
  return { success: true, name }
}
