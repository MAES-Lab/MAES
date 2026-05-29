"""
MAES Phase 1 — Универсальный анализатор (v4)
Читает все JSON из одной папки, сам разбирает по типам по имени файла.
Запуск: python analyze_all.py
"""
import json
import statistics
from pathlib import Path
from collections import defaultdict

# Папка с файлами — рядом со скриптом
ROOT = Path(__file__).parent

print("=" * 78)
print("MAES Phase 1 — УНИВЕРСАЛЬНЫЙ АНАЛИЗ (v4)")
print("Иларион Иванович Шаповал × Клод Викторович Антропиков")
print("24 мая 2026")
print("=" * 78)
print(f"Папка: {ROOT}")
print()

# Собираем все JSON
all_jsons = list(ROOT.glob("*.json"))
print(f"Всего JSON-файлов найдено: {len(all_jsons)}")
print()

# Разбираем по типам
main_data = defaultdict(list)  # основной прогон по условиям
selfdev_runs = []
diverse_runs = []
pair_runs = []
unknown = []

for f in all_jsons:
    try:
        with open(f, encoding="utf-8") as fp:
            d = json.load(fp)
    except Exception as e:
        print(f"  [ERROR] {f.name}: {e}")
        continue
    
    name = f.stem.lower()
    
    if "selfdev" in name:
        selfdev_runs.append((f.name, d))
    elif "diverse" in name:
        diverse_runs.append((f.name, d))
    elif "pair" in name:
        pair_runs.append((f.name, d))
    elif name.startswith("seed"):
        # Основной прогон: seed001_v3_0_A или seed001_v3_0_B_d5 или seed001_v3_1_A или seed001_v3_1_B_d5
        parts = f.stem.split("_")
        # parts: ['seed001', 'v3', '0' или '1', 'A' или 'B', опц. 'd5']
        if len(parts) >= 4:
            version = f"v3.{parts[2]}"
            condition = parts[3]
            if len(parts) > 4 and parts[4].lower() == "d5":
                condition += "_d5"
            key = f"{version}_{condition}"
            main_data[key].append(d)
        else:
            unknown.append(f.name)
    else:
        unknown.append(f.name)

print("РАЗБОР ПО ТИПАМ:")
print(f"  Основной прогон: {sum(len(v) for v in main_data.values())} файлов")
for k in sorted(main_data.keys()):
    print(f"    {k}: {len(main_data[k])}")
print(f"  SELFDEV: {len(selfdev_runs)}")
print(f"  DIVERSE: {len(diverse_runs)}")
print(f"  PAIR:    {len(pair_runs)}")
if unknown:
    print(f"  НЕИЗВЕСТНЫЕ: {len(unknown)} — {unknown[:5]}")
print()

# ========== СВОДКА ПО ОСНОВНОМУ ПРОГОНУ ==========
if main_data:
    print("=" * 78)
    print("СВОДНАЯ СТАТИСТИКА ПО УСЛОВИЯМ")
    print("=" * 78)
    print()
    print(f"{'Условие':<20} {'N':>4} {'ai_peak':>10} {'ai_mean20':>11} {'dims_pk':>8} {'agents':>8} {'species':>8} {'ideas':>7} {'catas':>6} {'top_idea':>10}")
    print("-" * 100)
    
    for key in sorted(main_data.keys()):
        runs = main_data[key]
        n = len(runs)
        def m(field):
            vals = [r.get(field, 0) for r in runs if r.get(field) is not None]
            return statistics.mean(vals) if vals else 0
        
        print(f"{key:<20} {n:>4} {m('ai_peak'):>10.2f} {m('ai_mean_final20'):>11.2f} {m('dims_peak'):>8.1f} {m('agents_final'):>8.1f} {m('species_final'):>8.1f} {m('ideas_alive'):>7.1f} {m('catastrophes'):>6.1f} {m('top_idea'):>10.2f}")
    
    # Cognitive styles
    print()
    print("-" * 78)
    print("COGNITIVE STYLES (% распределение, среднее по runs)")
    print("-" * 78)
    all_styles = set()
    for runs in main_data.values():
        for r in runs:
            all_styles.update(r.get("styles_final", {}).keys())
    all_styles = sorted(all_styles)
    
    print(f"{'Условие':<20} " + " ".join(f"{s[:11]:>12}" for s in all_styles))
    for key in sorted(main_data.keys()):
        runs = main_data[key]
        row = []
        for s in all_styles:
            vals = []
            for r in runs:
                styles = r.get("styles_final", {})
                total = sum(styles.values()) if styles else 0
                if total > 0:
                    vals.append(styles.get(s, 0) / total * 100)
            row.append(statistics.mean(vals) if vals else 0)
        print(f"{key:<20} " + " ".join(f"{v:>12.1f}" for v in row))
    
    # A* planner
    print()
    print("-" * 78)
    print("A* PLANNER (только условия v3.1)")
    print("-" * 78)
    for key in sorted(main_data.keys()):
        if "v3.1" not in key:
            continue
        runs = main_data[key]
        plans = statistics.mean([r.get("plans_total", 0) for r in runs])
        win_rate = statistics.mean([r.get("plan_win_rate_mean", 0) for r in runs])
        horizon = statistics.mean([r.get("plan_horizon_mean", 0) for r in runs])
        print(f"  {key}: plans_total={plans:.1f}, win_rate={win_rate:.3f}, horizon={horizon:.2f}")
    
    # Min/Max
    print()
    print("-" * 78)
    print("РАЗБРОС ai_peak ПО УСЛОВИЯМ")
    print("-" * 78)
    for key in sorted(main_data.keys()):
        runs = main_data[key]
        peaks = sorted([r.get("ai_peak", 0) for r in runs])
        print(f"  {key}: min={peaks[0]:.2f}, median={peaks[len(peaks)//2]:.2f}, max={peaks[-1]:.2f}")

# ========== SELFDEV ==========
if selfdev_runs or diverse_runs or pair_runs:
    print()
    print("=" * 78)
    print("ТЕСТЫ САМОРАЗВИТИЯ")
    print("=" * 78)
    
    for label, group in [("SELFDEV", selfdev_runs), ("DIVERSE", diverse_runs), ("PAIR", pair_runs)]:
        if not group:
            continue
        print(f"\n{label} ({len(group)} файлов):")
        for name, d in sorted(group):
            ai = d.get("ai_peak", 0)
            dims = d.get("dims_peak", 0)
            agents = d.get("agents_final", 0)
            ideas = d.get("ideas_alive", 0)
            top = d.get("top_idea", 0)
            catas = d.get("catastrophes", 0)
            print(f"  {name:<40} ai_peak={ai:>7.2f}  dims={dims:>2}  agents={agents:>4}  ideas={ideas:>4}  top={top:>8.2f}  catas={catas}")
        
        # Aggregate
        peaks = [d.get("ai_peak", 0) for _, d in group]
        if peaks:
            print(f"  AGGREGATE: ai_peak mean={statistics.mean(peaks):.2f}, min={min(peaks):.2f}, max={max(peaks):.2f}")

# Сохранить отчёт в файл
report_path = ROOT / "REPORT_777.txt"
print()
print("=" * 78)
print(f"Сохраняю текстовый отчёт: {report_path}")

import io, sys
buf = io.StringIO()
sys.stdout = buf

# Повторяем вывод в буфер
print(f"MAES Phase 1 Report — {len(all_jsons)} файлов")
print(f"Основной прогон: {sum(len(v) for v in main_data.values())}, selfdev: {len(selfdev_runs)}, diverse: {len(diverse_runs)}, pair: {len(pair_runs)}")
print()
print("УСЛОВИЯ:")
for key in sorted(main_data.keys()):
    runs = main_data[key]
    n = len(runs)
    def m2(field, runs=runs):
        vals = [r.get(field, 0) for r in runs if r.get(field) is not None]
        return statistics.mean(vals) if vals else 0
    print(f"  {key} (N={n}): ai_peak={m2('ai_peak'):.2f}, dims={m2('dims_peak'):.1f}, agents={m2('agents_final'):.1f}, ideas={m2('ideas_alive'):.1f}, catas={m2('catastrophes'):.1f}, top={m2('top_idea'):.2f}")

sys.stdout = sys.__stdout__
report_path.write_text(buf.getvalue(), encoding="utf-8")
print("Готово!")
