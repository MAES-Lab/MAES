"""
MAES Phase 1 — Анализатор расширенного прогона 777 (v3, рабочий)
Подстроен под реальную структуру файлов Илариона
24 мая 2026
"""
import json
import os
from pathlib import Path
from collections import defaultdict
import statistics

ROOT = Path(__file__).parent
DATA = ROOT / "data_777"
SELFDEV = DATA / "selfdev"

print("=" * 78)
print("MAES Phase 1 — АНАЛИЗ РАСШИРЕННОГО ПРОГОНА 777 (v3)")
print("Иларион Иванович Шаповал × Клод Викторович Антропиков")
print("24 мая 2026")
print("=" * 78)
print(f"Data:    {DATA}  {'OK' if DATA.exists() else 'NOT FOUND'}")
print(f"Selfdev: {SELFDEV}  {'OK' if SELFDEV.exists() else 'NOT FOUND'}")
print()

# ========== 1. ОСНОВНОЙ ПРОГОН ==========
print("=" * 78)
print("1. ОСНОВНОЙ ПРОГОН — seed001-seed020, 4 условия (v3.0/v3.1 × A/B_d5)")
print("=" * 78)

# Структура: condition -> list of dicts
data = defaultdict(list)

for f in DATA.glob("seed*_v3_*.json"):
    if "SELFDEV" in f.name.upper():
        continue
    if "_777" in f.name:
        continue  # старые/пустые если остались
    try:
        with open(f) as fp:
            d = json.load(fp)
        name = f.stem  # seed001_v3_0_A
        parts = name.split("_")
        # parts: ['seed001', 'v3', '0' (или '1'), 'A' (или 'B'), 'd5' (опционально)]
        version = f"v3.{parts[2]}"
        condition = parts[3]
        if len(parts) > 4 and parts[4] == "d5":
            condition += "_d5"
        key = f"{version}_{condition}"
        data[key].append(d)
    except Exception as e:
        print(f"  ERROR {f.name}: {e}")

print(f"\nНайдено файлов: {sum(len(v) for v in data.values())}")
for k in sorted(data.keys()):
    print(f"  {k}: {len(data[k])} runs")

if not data:
    print("[ОШИБКА] Нет данных")
    exit(1)

# Сводная статистика по условиям
print()
print("-" * 78)
print(f"{'Условие':<20} {'N':>4} {'ai_peak':>10} {'ai_mean':>10} {'dims':>6} {'agents':>8} {'species':>8} {'ideas':>7} {'catas':>6}")
print("-" * 78)

for key in sorted(data.keys()):
    runs = data[key]
    n = len(runs)
    def mean_safe(field):
        vals = [r.get(field, 0) for r in runs]
        return statistics.mean(vals) if vals else 0
    
    ai_peak = mean_safe("ai_peak")
    ai_mean = mean_safe("ai_mean_final20")
    dims = mean_safe("dims_peak")
    agents = mean_safe("agents_final")
    species = mean_safe("species_final")
    ideas = mean_safe("ideas_alive")
    catas = mean_safe("catastrophes")
    
    print(f"{key:<20} {n:>4} {ai_peak:>10.2f} {ai_mean:>10.2f} {dims:>6.1f} {agents:>8.1f} {species:>8.1f} {ideas:>7.1f} {catas:>6.1f}")

# Стили
print()
print("-" * 78)
print("РАСПРЕДЕЛЕНИЕ COGNITIVE STYLES (% среднее по runs)")
print("-" * 78)
all_styles = set()
for runs in data.values():
    for r in runs:
        all_styles.update(r.get("styles_final", {}).keys())
all_styles = sorted(all_styles)

print(f"{'Условие':<20} " + " ".join(f"{s[:10]:>10}" for s in all_styles))
for key in sorted(data.keys()):
    runs = data[key]
    style_means = {}
    for s in all_styles:
        vals = []
        for r in runs:
            styles = r.get("styles_final", {})
            total = sum(styles.values()) if styles else 0
            if total > 0:
                vals.append(styles.get(s, 0) / total * 100)
        style_means[s] = statistics.mean(vals) if vals else 0
    print(f"{key:<20} " + " ".join(f"{style_means[s]:>10.1f}" for s in all_styles))

# A* planner (только v3.1)
print()
print("-" * 78)
print("A* PLANNER (только v3.1)")
print("-" * 78)
for key in sorted(data.keys()):
    if "v3.1" not in key:
        continue
    runs = data[key]
    plans_total = statistics.mean([r.get("plans_total", 0) for r in runs])
    plan_win_rate = statistics.mean([r.get("plan_win_rate_mean", 0) for r in runs])
    plan_horizon = statistics.mean([r.get("plan_horizon_mean", 0) for r in runs])
    print(f"  {key}: plans_total={plans_total:.1f}, win_rate={plan_win_rate:.3f}, horizon_mean={plan_horizon:.2f}")

# Топ идеи
print()
print("-" * 78)
print("TOP IDEAS (среднее по condition)")
print("-" * 78)
for key in sorted(data.keys()):
    runs = data[key]
    tops = [r.get("top_idea", 0) for r in runs]
    print(f"  {key}: mean={statistics.mean(tops):.2f}, max={max(tops):.2f}, min={min(tops):.2f}")

# ========== 2. SELFDEV ==========
print()
print("=" * 78)
print("2. SELFDEV — тесты саморазвития")
print("=" * 78)

if SELFDEV.exists():
    selfdev_files = list(SELFDEV.glob("*.json"))
    print(f"\nНайдено: {len(selfdev_files)}")
    
    # Разделим: pair, diverse, selfdev по именам
    diverse_runs = []
    pair_runs = []
    selfdev_runs = []
    
    for f in selfdev_files:
        try:
            with open(f) as fp:
                d = json.load(fp)
            if "diverse" in f.name.lower():
                diverse_runs.append((f.name, d))
            elif "pair" in f.name.lower():
                pair_runs.append((f.name, d))
            elif "SELFDEV" in f.name.upper():
                selfdev_runs.append((f.name, d))
        except Exception as e:
            print(f"  ERROR {f.name}: {e}")
    
    print(f"  diverse: {len(diverse_runs)}")
    print(f"  pair:    {len(pair_runs)}")
    print(f"  selfdev: {len(selfdev_runs)}")
    
    for label, runs in [("DIVERSE", diverse_runs), ("PAIR", pair_runs), ("SELFDEV", selfdev_runs)]:
        if not runs:
            continue
        print(f"\n{label}:")
        for name, d in sorted(runs):
            ai = d.get("ai_peak", 0)
            dims = d.get("dims_peak", 0)
            agents = d.get("agents_final", 0)
            ideas = d.get("ideas_alive", 0)
            print(f"  {name}: ai_peak={ai:.2f}, dims={dims}, agents={agents}, ideas={ideas}")

print()
print("=" * 78)
print("АНАЛИЗ ЗАВЕРШЁН")
print("=" * 78)
