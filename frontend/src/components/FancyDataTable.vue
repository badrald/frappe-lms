<template>
    <div class="w-full bg-white rounded-lg shadow-sm overflow-hidden">
        <!-- Toolbar -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 p-4 border-b">
            <div class="flex items-center gap-3">
                <div v-if="showSearch" class="relative">
                    <input v-model="searchQuery" type="search" :placeholder="searchPlaceholder"
                        class="border rounded-lg px-3 py-2 w-64 focus:outline-none focus:ring-2 focus:ring-indigo-300" />
                </div>

                <div class="flex items-center gap-2 text-sm text-gray-500">
                    <span v-if="total">عرض {{ startItem }} - {{ endItem }} من {{ total }}</span>
                </div>
            </div>

            <div class="flex items-center gap-3">
                <div v-if="showPageSize" class="flex items-center gap-2">
                    <label class="text-sm text-gray-600">صفحة</label>
                    <select v-model.number="pageSize" class="form-select border rounded px-2 py-1">
                        <option v-for="s in pageSizeOptions" :key="s" :value="s">{{ s }}</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto">
            <table class="min-w-full table-auto">
                <thead class="bg-gray-50">
                    <tr>
                        <th v-if="selectable" class="p-3 text-center">
                            <input type="checkbox" :checked="allSelected"
                                @change="toggleSelectAll($event.target.checked)" />
                        </th>
                        <th v-for="col in columns" :key="col.key" class="p-3 text-cetner">
                            <button v-if="col.sortable !== false && sortable" @click="toggleSort(col.key)"
                                class="flex items-center gap-2">
                                <span>{{ col.label }}</span>
                                <span v-if="sortBy === col.key">
                                    <svg v-if="!sortDesc" xmlns="http://www.w3.org/2000/svg"
                                        class="h-4 w-4 text-gray-500" fill="none" viewBox="0 0 24 24"
                                        stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M5 15l7-7 7 7" />
                                    </svg>
                                    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500"
                                        fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M19 9l-7 7-7-7" />
                                    </svg>
                                </span>
                                <svg v-else-if="col.sortable !== false && sortable" xmlns="http://www.w3.org/2000/svg"
                                    class="h-3 w-3 text-gray-300" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M5 15l7-7 7 7" />
                                </svg>
                            </button>
                            <span v-else>{{ col.label }}</span>
                        </th>
                        <th v-if="$slots.actions" class="p-3">&nbsp;</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="row in paginatedData" :key="getRowKey(row)" class="border-b hover:bg-gray-50">
                        <td v-if="selectable" class="p-3 text-center" >
                            <input type="checkbox" :checked="isSelected(row)"
                                @change="toggleRow(row, $event.target.checked)" />
                        </td>
                        <td v-for="col in columns" :key="col.key + '-cell'" class="p-3 align-top">
                            <slot :name="`cell-${col.key}`" :row="row">
                                <div class="text-sm text-gray-800 text-center">
                                    {{ formatCell(row[col.key], col) }}
                                </div>
                            </slot>
                        </td>
                        <td v-if="$slots.actions" class="p-3 align-top">
                            <slot name="actions" :row="row"></slot>
                        </td>
                    </tr>

                    <tr v-if="paginatedData.length === 0">
                        <td :colspan="(columns.length + (selectable ? 1 : 0) + ($slots.actions ? 1 : 0))"
                            class="p-6 text-center text-gray-500">
                            <slot name="empty">لا توجد بيانات لعرضها.</slot>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Pagination -->
        <div v-if="showPagination" class="p-4 flex items-center justify-between">
            <div class="flex items-center gap-2">
                <button @click="prevPage" :disabled="currentPage === 1"
                    class="px-3 py-1 rounded border bg-white">السابق</button>
                <span class="text-sm text-gray-600">صفحة {{ currentPage }} من {{ totalPages }}</span>
                <button @click="nextPage" :disabled="currentPage === totalPages"
                    class="px-3 py-1 rounded border bg-white">التالي</button>
            </div>

            <div class="flex items-center gap-2 text-sm text-gray-600">
                <span>اذهب إلى الصفحة:</span>
                <input type="number" min="1" :max="totalPages" v-model.number="goto"
                    class="w-20 border rounded px-2 py-1" />
                <button @click="goToPage(goto)" class="px-3 py-1 rounded border bg-white">اذهب</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
    columns: { type: Array, required: true }, // [{ key, label, sortable }]
    data: { type: Array, required: true },
    pageSize: { type: Number, default: 10 },
    pageSizeOptions: { type: Array, default: () => [5, 10, 20, 50] },
    sortable: { type: Boolean, default: true },
    showSearch: { type: Boolean, default: true },
    showPagination: { type: Boolean, default: true },
    showPageSize: { type: Boolean, default: true },
    searchPlaceholder: { type: String, default: 'ابحث...' },
    initialSort: { type: Object, default: null }, // { key, desc }
    selectable: { type: Boolean, default: false },
    rowKey: { type: String, default: 'name' },
})

const emit = defineEmits(['select', 'update:pageSize', 'sort'])

const searchQuery = ref('')
const sortBy = ref(props.initialSort ? props.initialSort.key : null)
const sortDesc = ref(props.initialSort ? !!props.initialSort.desc : false)
const currentPage = ref(1)
const pageSize = ref(props.pageSize)
const selected = ref(new Set())
const goto = ref(1)

watch(pageSize, (v) => emit('update:pageSize', v))

const total = computed(() => filtered.length)
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize.value)))
const startItem = computed(() => (total.value === 0 ? 0 : (currentPage.value - 1) * pageSize.value + 1))
const endItem = computed(() => Math.min(total.value, currentPage.value * pageSize.value))

const compareValues = (a, b) => {
    if (a == null) return -1
    if (b == null) return 1
    if (!isNaN(Number(a)) && !isNaN(Number(b))) return Number(a) - Number(b)
    return String(a).localeCompare(String(b))
}

const filtered = computed(() => {
    if (!props.data) return []
    const q = searchQuery.value && String(searchQuery.value).toLowerCase()
    let rows = props.data.slice()
    if (q) {
        rows = rows.filter(r => props.columns.some(c => {
            const val = r[c.key]
            return val != null && String(val).toLowerCase().includes(q)
        }))
    }
    if (sortBy.value) {
        rows.sort((a, b) => compareValues(a[sortBy.value], b[sortBy.value]) * (sortDesc.value ? -1 : 1))
    }
    return rows
})

const paginatedData = computed(() => {
    if (!props.showPagination) return filtered.value
    const start = (currentPage.value - 1) * pageSize.value
    return filtered.value.slice(start, start + pageSize.value)
})

const toggleSort = (key) => {
    if (!props.sortable) return
    if (sortBy.value === key) {
        sortDesc.value = !sortDesc.value
    } else {
        sortBy.value = key
        sortDesc.value = false
    }
    emit('sort', { key: sortBy.value, desc: sortDesc.value })
}

const prevPage = () => { if (currentPage.value > 1) currentPage.value-- }
const nextPage = () => { if (currentPage.value < totalPages.value) currentPage.value++ }
const goToPage = (p) => {
    const n = Math.max(1, Math.min(totalPages.value, Number(p) || 1))
    currentPage.value = n
}

watch([filtered, pageSize], () => { currentPage.value = 1 }, { immediate: true })

const formatCell = (val, col) => {
    if (col.format) return col.format(val)
    return val
}

const getRowKey = (row) => row[props.rowKey] ?? JSON.stringify(row)
const toggleRow = (row, checked) => {
    const k = getRowKey(row)
    if (checked) selected.value.add(k)
    else selected.value.delete(k)
    emit('select', Array.from(selected.value))
}
const isSelected = (row) => selected.value.has(getRowKey(row))
const allSelected = computed(() => paginatedData.value.length > 0 && paginatedData.value.every(r => isSelected(r)))
const toggleSelectAll = (checked) => {
    if (checked) paginatedData.value.forEach(r => selected.value.add(getRowKey(r)))
    else paginatedData.value.forEach(r => selected.value.delete(getRowKey(r)))
    emit('select', Array.from(selected.value))
}

// sync goto input with current page
watch(currentPage, (v) => { goto.value = v })

// expose
const start = startItem
const end = endItem

</script>

<style scoped>
/* small niceties */
.form-select {
    background: white;
}
</style>
