#!/bin/bash

echo "📛 /var/log altı temizleniyor (root yetkisi olmadan)..."

deleted=0
skipped=0

find /var/log -type f 2>/dev/null | while read -r file; do
    if rm -f "$file" 2>/dev/null; then
        echo "[✅] Silindi: $file"
        ((deleted++))
    else
        echo "[❌] İzin yok: $file"
        ((skipped++))
    fi
done

echo -e "\n🔍 Toplam: $deleted silindi, $skipped atlandı."
