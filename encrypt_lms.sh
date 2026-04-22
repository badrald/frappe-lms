#!/bin/bash
# ============================================================
#   LMS PyArmor Encryption Script (Deployment Version)
#   يشفّر ملفات المنطق التجاري ويدمج Runtime بداخل التطبيق
# ============================================================

set -e

APP_DIR="/home/badretms/erp15_enc/apps/lms"
LMS_PKG="$APP_DIR/lms"
BACKUP_DIR="$APP_DIR/lms_backup_$(date +%Y%m%d_%H%M%S)"
DIST_DIR="$APP_DIR/lms_dist_v4"

# استخدام بايثون و pyarmor الخاصين بـ bench حصراً
BENCH_PYARMOR="/home/badretms/erp15_enc/env/bin/pyarmor"

echo ""
echo "======================================================"
echo "  🔐 LMS PyArmor Encryption (Deployment Mode)"
echo "======================================================"
echo ""

# ─── Step 1: نسخة احتياطية ───────────────────────────────
echo "📦 [1/4] إنشاء نسخة احتياطية في: $BACKUP_DIR"
cp -r "$LMS_PKG" "$BACKUP_DIR"
echo "    ✅ تم الحفظ"

# ─── Step 2: تشفير الملفات بـ PyArmor (بشكل مجمّع وهرمي) ──
echo ""
echo "🔒 [2/4] تشفير الملفات ودمج Runtime..."
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

cd "$APP_DIR"

# تشفير المجلدات مع الحفاظ على الهيكلية وتجاهل الملفات غير المطلوبة
$BENCH_PYARMOR gen \
    --prefix lms \
    -O "$DIST_DIR" \
    -r lms/api lms/lms/doctype lms/lms/report lms/tasks.py \
    --exclude "*/__init__.py" \
    --exclude "*/test_*.py" > /dev/null 2>&1

echo "    ✅ اكتملت عملية التشفير الأساسية"

# ─── Step 3: استبدال الملفات ونقل Runtime ───────────────
echo ""
echo "📋 [3/4] تطبيق التشفير على التطبيق الفعلي..."

# نسخ الملفات المشفّرة فوق الأصلية
cp -r "$DIST_DIR/api/"* "$LMS_PKG/api/" 2>/dev/null || true
cp -r "$DIST_DIR/doctype/"* "$LMS_PKG/lms/doctype/" 2>/dev/null || true
cp -r "$DIST_DIR/report/"* "$LMS_PKG/lms/report/" 2>/dev/null || true
cp "$DIST_DIR/tasks.py" "$LMS_PKG/tasks.py" 2>/dev/null || true
echo "    ✅ استُبدلت الملفات الأصلية"

# نقل الـ Runtime ليكون جزءاً من التطبيق
RUNTIME_NAME=$(ls -d "$DIST_DIR/lms/pyarmor_runtime_"* 2>/dev/null | head -n 1 | awk -F'/' '{print $NF}')

if [ -n "$RUNTIME_NAME" ]; then
    rm -rf "$LMS_PKG/lms/$RUNTIME_NAME"
    mkdir -p "$LMS_PKG/lms/$RUNTIME_NAME"
    cp -r "$DIST_DIR/lms/$RUNTIME_NAME/"* "$LMS_PKG/lms/$RUNTIME_NAME/"
    echo "    ✅ تم دمج Runtime بالمسار: lms/lms/$RUNTIME_NAME"
else
    echo "    ⚠️ لم يتم العثور على Runtime."
fi

# تنظيف الكاش الخاص بالتطبيق
find "$LMS_PKG" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# إزالة مجلد التشفير المؤقت
rm -rf "$DIST_DIR"

echo ""
echo "======================================================"
echo "  🎉 اكتمل التشفير بنجاح! التطبيق الآن مستقل."
echo "======================================================"
