<template>
    <transition name="modal">
        <div v-if="modelValue" class="fixed inset-0 z-50 flex items-center justify-center p-4"
            @click.self="onBackdropClick">
            <!-- خلفية ناعمة ومتدرجة -->
            <div class="absolute inset-0 bg-black/30 dark:bg-black/50 backdrop-blur-sm"></div>

            <!-- المودال الرئيسي -->
            <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-xl w-full mx-4 overflow-hidden modal-container"
                :class="dialogWidthClass">

                <button v-if="closable" @click="closeDialog"
                    class="absolute top-3 right-3 w-8 h-8 rounded-full bg-red-100 hover:bg-red-200 dark:bg-red-900/50 dark:hover:bg-red-800 transition-all duration-200 flex items-center justify-center group z-10">
                    <svg class="w-4 h-4 text-gray-500 group-hover:text-gray-700 dark:text-gray-400 dark:group-hover:text-gray-200 transition-colors"
                        fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                        <path d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
                <!-- زر الإغلاق المحدث -->



                <!-- الجزء العلوي المبسط -->
                <div class="px-6 pt-6 pb-4">
                    <div class="flex items-start">
                        <!-- العنوان -->
                        <div class="flex-1 min-w-0">
                            <h3 class="text-lg font-semibold text-gray-900 dark:text-white leading-6">
                                <slot name="title">{{ title }}</slot>
                            </h3>
                            <p v-if="$slots.description" class="mt-1 text-sm text-gray-500 dark:text-gray-300">
                                <slot name="description" />
                            </p>
                        </div>

                        <!-- الأيقونة -->
                        <div class="flex-shrink-0 mr-4">
                            <div
                                class="w-12 h-12  rounded-2xl bg-gradient-to-br from-blue-500 to-blue-600 dark:from-blue-600 dark:to-blue-800 flex items-center justify-center shadow-lg">
                                <slot name="icon">
                                    <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" stroke-width="1.5"
                                        viewBox="0 0 24 24">
                                        <path
                                            d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
                                    </svg>
                                </slot>
                            </div>
                        </div>


                    </div>
                </div>

                <!-- محتوى الرسالة -->
                <div class="px-6 pb-6">
                    <div v-if="$slots.media || layout === 'split'" class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <section class="lg:col-span-2 order-1 lg:order-2">
                            <div class="text-gray-600 dark:text-gray-200 text-sm leading-relaxed">
                                <slot />
                            </div>
                        </section>
                        <aside class="order-1 lg:order-2">
                            <slot name="media" />
                        </aside>
                    </div>
                    <div v-else class="text-gray-600 dark:text-gray-200 text-sm leading-relaxed">
                        <slot />
                    </div>
                </div>

                <!-- منطقة الأزرار -->
                <div class="px-6 py-4 bg-gray-50 dark:bg-gray-700/50 border-t border-gray-200 dark:border-gray-600">
                    <div class="flex justify-end space-x-3 rtl:space-x-reverse">
                        <slot name="actions">
                            <button v-if="closable" @click="closeDialog"
                                class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800">
                                إغلاق
                            </button>
                        </slot>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
    modelValue: { type: Boolean, required: true },
    title: { type: String, default: "حوار النظام" },
    persistent: { type: Boolean, default: false },
    closable: { type: Boolean, default: true },
    size: { type: String, default: 'md' }, // sm, md, lg, xl
    layout: { type: String, default: 'default' }, // default | split
})

const emit = defineEmits(["update:modelValue"])

const closeDialog = () => {
    emit("update:modelValue", false)
}

const onBackdropClick = () => {
    if (!props.persistent) {
        closeDialog()
    }
}

const dialogWidthClass = computed(() => {
    switch (props.size) {
        case 'sm':
            return 'max-w-md'
        case 'lg':
            return 'max-w-2xl'
        case 'xl':
            return 'max-w-4xl'
        case 'md':
        default:
            return 'max-w-lg'
    }
})
</script>

<style scoped>
/* تأثيرات الانتقال المحسنة */
.modal-enter-active {
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-leave-active {
    transition: all 0.2s cubic-bezier(0.4, 0, 1, 1);
}

.modal-enter-from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
}

.modal-leave-to {
    opacity: 0;
    transform: scale(0.98) translateY(5px);
}

/* تأثير ظهور المودال */
.modal-container {
    animation: modalSlideIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow:
        0 25px 50px -12px rgba(0, 0, 0, 0.25),
        0 0 0 1px rgba(0, 0, 0, 0.05);
}

@keyframes modalSlideIn {
    0% {
        transform: scale(0.95) translateY(-10px);
        opacity: 0;
    }

    100% {
        transform: scale(1) translateY(0);
        opacity: 1;
    }
}

/* تأثير hover ناعم */
.modal-container:hover {
    transform: translateY(-1px);
    box-shadow:
        0 32px 64px -12px rgba(0, 0, 0, 0.3),
        0 0 0 1px rgba(0, 0, 0, 0.05);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* تحسينات للشاشات الصغيرة */
@media (max-width: 640px) {
    .modal-container {
        margin: 1rem;
        max-width: calc(100% - 2rem);
        border-radius: 1.5rem;
    }
}

/* تأثير التركيز المحسن */
button:focus {
    outline: none;
}

/* تأثير hover للأزرار */
button {
    position: relative;
    overflow: hidden;
}

button::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
    transform: translate(-50%, -50%);
    transition: width 0.3s ease, height 0.3s ease;
}

button:hover::before {
    width: 200%;
    height: 200%;
}

/* تحسين الظلال في الوضع المظلم */
@media (prefers-color-scheme: dark) {
    .modal-container {
        box-shadow:
            0 25px 50px -12px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(255, 255, 255, 0.1);
    }

    .modal-container:hover {
        box-shadow:
            0 32px 64px -12px rgba(0, 0, 0, 0.6),
            0 0 0 1px rgba(255, 255, 255, 0.1);
    }
}

/* تأثير النبض للأيقونة */
.modal-container .bg-gradient-to-br {
    animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {

    0%,
    100% {
        box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4);
    }

    50% {
        box-shadow: 0 0 0 8px rgba(59, 130, 246, 0);
    }
}

/* تحسين المساحات والخط */
.leading-relaxed {
    line-height: 1.7;
}

/* تأثير انتقال ناعم للخلفية */
.bg-black\/20 {
    animation: backdropFadeIn 0.3s ease-out;
}

@keyframes backdropFadeIn {
    0% {
        opacity: 0;
    }

    100% {
        opacity: 1;
    }
}

/* تحسين زر الإغلاق */
.modal-container button:first-of-type {
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
}

/* تأثير التمرير على الأزرار */
button {
    transform: translateZ(0);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

button:hover {
    transform: translateY(-1px);
}

button:active {
    transform: translateY(0);
}
</style>