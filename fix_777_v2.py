"""
Вытаскивает JSON-файлы из вложенных папок data_777
Запуск: python fix_777_v2.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).parent / "data_777"

if not ROOT.exists():
    print(f"[ОШИБКА] Папка не найдена: {ROOT}")
    exit(1)

moved = 0
skipped = 0

for subdir in ROOT.iterdir():
    if not subdir.is_dir():
        continue
    if not subdir.name.endswith(".json"):
        continue  # пропускаем selfdev и другие "настоящие" папки
    
    # Найти JSON файл внутри
    json_files = list(subdir.glob("*.json"))
    if not json_files:
        print(f"[ПУСТО] {subdir.name}")
        continue
    
    if len(json_files) > 1:
        print(f"[ВНИМАНИЕ] {subdir.name}: больше одного JSON ({len(json_files)})")
    
    # Берём первый JSON
    source = json_files[0]
    # Целевое имя = имя папки (которое уже заканчивается на .json)
    target = ROOT / subdir.name
    
    if target.exists():
        print(f"[ПРОПУСК] Уже есть файл с именем папки: {subdir.name}")
        skipped += 1
        continue
    
    shutil.move(str(source), str(target))
    moved += 1
    print(f"[OK] {source.name} -> {subdir.name}")
    
    # Удалить пустую папку
    try:
        subdir.rmdir()
    except OSError:
        pass  # папка не пустая, не страшно

print(f"\n=== ГОТОВО ===")
print(f"Перемещено: {moved}")
print(f"Пропущено:  {skipped}")
