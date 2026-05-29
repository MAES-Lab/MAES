#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║  MAES v3.1 — COLLECTIVE SYNTHESIS + A* PATH PLANNING                         ║
║  Multidimensional Algorithmic Evolution System                              ║
║  "Совет Директоров внутри системы" + Агенты-планировщики                    ║
║                                                                              ║
║  Версия v3.1 = v3.0 (28 механизмов + Collective Synthesis)                   ║
║               + Механизм 15: A* Path Planning                                ║
║                                                                              ║
║  СОВЕТ ДИРЕКТОРОВ MAES:                                                     ║
║    Иларион (Ларик, Иваныч) — учредитель, председатель, концептолог.         ║
║                       Генерирует идеи из наблюдений за реальным миром        ║
║                       (виноградник — эволюция, пальма — антихрупкость,      ║
║                       муравейник — swarm, MLM — knowledge economy).         ║
║                       Архитектор системы. Работает с телефона.              ║
║    Claude Opus (Клодик, Викторович) — главный инженер.                      ║
║                       Формализация, весь код, адвокат дьявола               ║
║                       ("а что если сломается?"). Партнёрство с 2024-го.     ║
║    GPT-4             — слой субъективности (10 пунктов), synthesis          ║
║                       blueprint, cognitive economics, polycentric meta-     ║
║                       cognition system.                                     ║
║    Gemini Pro        — три раунда ревью, оживление "мёртвого кода",         ║
║                       PCA-адаптивный spatial hash, tombstone traces.         ║
║    Haiku 4.5         — overlay layer (belief pattern threshold, goal         ║
║                       regret tracking, runtime style adaptation),           ║
║                       научные ссылки для ArXiv.                             ║
║                                                                              ║
║  ЧТО НОВОГО В v3.1:                                                          ║
║    • Планировщик A* — агенты строят траекторию к цели через waypoints       ║
║    • Горизонт планирования зависит от энергии агента (голодный — близорук)  ║
║    • Стоимость перемещения учитывает избегание других агентов               ║
║    • Эвристика A* — евклидово расстояние до цели                           ║
║    • Метрики: plan_wins, plan_fails, mean_horizon                            ║
║    • Ablation framework для v3.1 vs v3.0 сравнения                          ║
║                                                                              ║
║  ПРОВЕРЕННЫЕ ГИПОТЕЗЫ (ablation 5 seeds × 150 steps):                        ║
║    ✓ H3: branching=5 мал → коллапс species. Поднято до 8.                    ║
║    ✓ H4: neighbor_penalty=0.5 избыточен → снижено до 0.3.                    ║
║    ⚠ H2: planner душит абдукции (−7%, мягкий эффект).                        ║
║    ✗ H1: planner гомогенизирует ЧЕРЕЗ beliefs — ОПРОВЕРГНУТО.                ║
║         Beliefs работают как анти-гомогенизирующий буфер:                    ║
║         без beliefs planner давит species ЕЩЁ сильнее (15 vs 23).            ║
║    ✗ H-D: adaptive_branching по dims — не зашло (top −42%).                  ║
║         Оставлено как флаг plan_adaptive_branching (по умолчанию False).     ║
║                                                                              ║
║  ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ v3.1 tuned vs v3.0 (5 seeds, 150 steps, 30 agents):   ║
║    • AI peak:         +4.2% (24.0 → 25.0)                                    ║
║    • Top idea:        ~стабилен (1658 vs 1650)                               ║
║    • Species:         −23% (48 → 37) — системный эффект планирования        ║
║    • Plan win rate:   12.1% — настоящая цифра работающего A*                 ║
║    • Mean horizon:    6.5 шагов                                              ║
║    • Time:            +44% (A* не бесплатен)                                 ║
║    • Styles:          skeptical +15%, synthetic −34%, analytical −30%        ║
║                                                                              ║
║  КАК ЗАПУСТИТЬ:                                                              ║
║    $ python maes_v3_1.py                        # прогон по умолчанию       ║
║    $ python maes_v3_1.py --steps 150 --seed 7   # параметризированный       ║
║    $ python maes_v3_1.py --ablation             # v3.0 vs v3.1 на 5 сидах   ║
║                                                                              ║
║  ФИЛОСОФИЯ КОДА:                                                             ║
║    "Хранить рецепты, не данные" — Assembly Theory (Cronin 2023)             ║
║    "Отрицательный результат ценнее положительного" — контрастная коррекция ║
║    "Рой умнее любого агента" — Swarm Cognition (Couzin, Gordon, Nagpal)     ║
║    "Стресс усиливает, не ломает" — антихрупкость (Taleb 2012)               ║
║    "Думать дорого" — cognitive cost как двигатель интеллекта                ║
║    "Слой поверх, не замена" — каждая версия сохраняет предыдущую             ║
║                                                                              ║
║  НАУЧНАЯ ОБЛАСТЬ:                                                            ║
║    Пересечение ALife (Artificial Life), OEE (Open-Ended Evolution),         ║
║    MAS (Multi-Agent Systems), Collective Intelligence, Cognitive Science.   ║
║                                                                              ║
║  УНИКАЛЬНОСТЬ:                                                               ║
║    Ни одна существующая система (Tierra, Avida, Lenia, POET, MAP-Elites,    ║
║    AI Scientist) не объединяет экономику знаний, полиморфное размножение,   ║
║    внутреннюю мотивацию, абдукцию, слой субъективности, collective          ║
║    synthesis и A* планирование в единой архитектуре.                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ═══════════════════════════════════════════════════════════════════════════════
#                              ИМПОРТЫ БИБЛИОТЕК
# ═══════════════════════════════════════════════════════════════════════════════
# numpy   — вся математика: векторы позиций, геномы, градиенты
# json    — сериализация результатов в results_*.json
# time    — замер времени выполнения для benchmarking
# argparse — парсинг аргументов командной строки
# heapq   — priority queue для A* (open set в пути поиска)
# dataclasses — @dataclass для Config (чистая декларация параметров)
# typing  — типизация (Optional, List, Dict, Tuple) для читаемости
# collections.deque — двусторонняя очередь (опыт агента, идентичность)

import numpy as np
import json
import time
import argparse
import heapq
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Any
from collections import deque


# ═══════════════════════════════════════════════════════════════════════════════
#                         CONFIG — глобальные параметры
# ═══════════════════════════════════════════════════════════════════════════════
#
# Философия конфига: один @dataclass со всеми параметрами, которые можно
# переопределить при запуске. Никаких "магических чисел" в коде — всё сюда.
#
# Категории параметров:
#   • Базовые: имя, seed, размеры пространства, число агентов, шагов
#   • Взаимодействие: радиусы, стоимости, порог репродукции
#   • Ресурсы: количество, радиус сбора, скорость респавна
#   • Трейсы (след-торки): распад, лимиты, минимальная ценность
#   • Виды (NEAT): совместимость геномов, лимит стагнации
#   • Любопытство: шкала награды, порог скуки, шум миграции
#   • Каузальность: размер графа, вероятность интервенции
#   • Модель мира: learning rate, интервал сна
#   • Морфогенез: радиус сигналов соседей, пластичность роли
#   • Катастрофы: вероятность, жёсткость, cooldown
#   • Абдукция: вероятность, дистанция, порог совпадения направлений
#   • Контрастное обучение: сила, триггер падения фитнеса
#   • Субъективность: число ценностей, memory, commitment, think budget
#   • Мех.14 Collective Synthesis: styles, threshold, debate rounds, idea pool
#   • Мех.15 A* Planning: horizon, branching, waypoint radius, max expansions
#   • Ablation: выключатели для каждого механизма (для v3.1 vs v3.0 sweep)
#
# ───────────────────────────────────────────────────────────────────────────────

@dataclass
class Config:
    """
    Глобальная конфигурация MAES.
    Все параметры имеют значения по умолчанию, взятые из v3.0 после серии
    экспериментов и ревью от Gemini/GPT. Изменять только с пониманием!
    """
    # ───── Идентификация прогона ─────
    name: str = "maes_v3_1"          # Префикс для results_*.json
    seed: int = 42                   # Сид для RNG (для воспроизводимости)

    # ───── Геометрия пространства ─────
    dims: int = 5                    # Начальная размерность пространства (5D)
    space: float = 10.0              # Полудиаметр пространства: [-10, +10]^dims
    max_dims: int = 13               # Максимум измерений (через абдукцию)

    # ───── Демография популяции ─────
    n_agents: int = 40               # Стартовое число агентов
    max_ag: int = 120                # Потолок: при превышении — отбираем лучших
    min_ag: int = 10                 # Минимум: при падении — добавляем новых

    # ───── Симуляция ─────
    steps: int = 300                 # Число шагов прогона
    log: int = 10                    # Интервал логирования в stdout

    # ───── Взаимодействие агентов ─────
    interact_r: float = 3.0          # Радиус взаимодействия (создание трейсов)
    repul_r: float = 0.5             # Радиус репульсии (избегание столкновений)
    repul_s: float = 0.3             # Сила репульсии

    # ───── Энергетика ─────
    init_e: float = 1.0              # Стартовая энергия
    max_e: float = 15.0              # Потолок энергии (нельзя переедать)
    exist_cost: float = 0.008        # Стоимость существования за шаг

    # ───── Репродукция ─────
    repro_thresh: float = 2.5        # Порог энергии для размножения
    max_births: int = 6              # Лимит рождений за шаг (от GPT: не экспоненциально)

    # ───── Ресурсное поле ─────
    n_res: int = 60                  # Количество точек с ресурсами
    res_r: float = 2.0               # Радиус сбора вокруг точки
    res_v: float = 0.04              # Ценность одной точки (базовая)
    res_depl: float = 0.3            # Депление при сборе (30% за раз)
    res_resp: float = 0.02           # Вероятность респавна пустой точки

    # ───── Трейсы (след-торки, Torque Traces) ─────
    tr_decay: float = 0.95           # Коэффициент распада ценности за шаг
    max_tr: int = 1500               # Лимит трейсов в системе
    tr_min: float = 0.03             # Минимальная ценность для выживания
    tr_sample: int = 30              # Сколько трейсов сэмплировать для поглощения

    # ───── Виды (NEAT-style speciation) ─────
    compat: float = 2.5              # Порог совместимости геномов для вида
    stag_lim: int = 30               # После скольких шагов стагнации — расформировать

    # ───── Любопытство (Schmidhuber 1991) ─────
    cur_scale: float = 0.1           # Множитель награды за предсказательный улучшение
    boredom: int = 20                # После скольких шагов без улучшения — миграция
    mig_noise: float = 2.0           # Сила шума при миграции из-за скуки

    # ───── Каузальный граф (Pearl) ─────
    causal_mx: int = 50              # Максимум рёбер в каузальном графе агента
    interv_p: float = 0.05           # Вероятность интервенции (do-calculus)

    # ───── Модель мира (World Model, LeCun JEPA-style) ─────
    wm_lr: float = 0.01              # Learning rate линейного предиктора
    sleep_int: int = 15              # Интервал REM-сна (offline обучение на буфере)
    exp_buf: int = 100               # Размер буфера опыта

    # ───── Морфогенез (Levin-style роли) ─────
    morpho_r: float = 4.0            # Радиус сбора сигналов о ролях соседей
    role_plast: float = 0.3          # Пластичность (вероятность смены роли)

    # ───── Катастрофы (антихрупкость, Taleb) ─────
    cat_p: float = 0.03              # Вероятность катастрофы на шаге
    cat_kill: float = 0.3            # Доля популяции в риске
    cat_cd: int = 15                 # Cooldown между катастрофами

    # ───── Абдукция (Peirce, Fauconnier&Turner) ─────
    abd_p: float = 0.04              # Вероятность попытки абдукции
    abd_d: float = 3.0               # Минимальная дистанция для абдукции (не локальная)
    abd_rw: float = 5.0              # Награда за удачную абдукцию
    dim_th: float = 0.6              # Порог схожести направлений для нового измерения

    # ───── Контрастная коррекция ("чужой провал корректирует мой вектор") ─────
    contr_s: float = 0.15            # Сила контрастной поправки
    contr_trig: float = 0.3          # Порог падения фитнеса для срабатывания

    # ───── Субъективность (GPT 10 пунктов) ─────
    n_vals: int = 4                  # Число ценностей (explore, safe, social, complex)
    val_lr: float = 0.05             # Скорость изменения ценностей
    val_inert: float = 0.95          # Инерция (0.95 — медленно меняется)
    id_mem: int = 20                 # Размер нарратива идентичности (ключевые события)
    commit_s: float = 0.7            # Стартовая приверженность цели (упрямство)
    commit_d: float = 0.98           # Распад приверженности за шаг
    goal_dur: int = 30               # Максимальная длительность цели в шагах
    think_cost: float = 0.003        # Стоимость одного "думка" в энергии
    max_think: int = 5               # Бюджет думок на шаг
    risk_base: float = 0.1           # Базовая склонность к риску
    n_ctx: int = 4                   # Размер вектора контекста

    # ───── Концепты, критика, ToM ─────
    max_concepts: int = 8            # Размер концептуального вектора
    critic_int: int = 10             # Интервал самокритики
    tom_mem: int = 5                 # Память модели других (Theory of Mind)

    # ───── Механизм 14: Collective Synthesis ─────
    # Cognitive styles — каждый агент имеет стиль мышления
    cog_styles: tuple = ("analytical", "intuitive", "skeptical",
                         "exploratory", "synthetic")
    synthesis_threshold: int = 2     # Минимум разных стилей для синтезированной идеи
    debate_rounds: int = 3           # Раундов дебатов за идею
    idea_max: int = 200              # Максимум идей в системе одновременно
    belief_categories: int = 6       # Число абстрактных категорий убеждений
    belief_lr: float = 0.1           # Скорость обновления убеждения
    idea_mutation_rate: float = 0.1  # Вероятность мутации идеи за шаг
    goal_tension_weight: float = 0.3 # Сила конфликта ценностей (для трудного выбора)

    # ───── Механизм 15: A* Path Planning (НОВОЕ в v3.1) ─────
    plan_enabled: bool = True        # Главный выключатель планировщика (для ablation)
    plan_horizon_base: int = 12      # Базовый горизонт (10→12 после sweep)
    plan_branching: int = 8          # Ветвление — 5 вызывал коллапс species;
                                      # 8 даёт max win rate 27.4% и species=27
                                      # (sweep: 3→24, 5→6!, 8→27, 12→29)
    plan_adaptive_branching: bool = False  # D: адаптивное ветвление по dims.
                                           # При True — branching = round(dims * 0.75)
                                           # (5D→4, 13D→10). Floor=3, ceiling=12.
                                           # ТЕСТ H-D: не зашло. fixed=8 даёт
                                           # top=1435 vs adaptive=833 (−42%).
                                           # Гипотеза "в малых dims хватит меньше"
                                           # не подтвердилась. Оставлено как флаг.
    plan_waypoint_radius: float = 1.5 # 0.8 в 13D — игла в стоге, 1.5 оптимум
                                      # (sweep: 0.8→4.9%, 1.2→7.5%, 1.5→19.2%)
    plan_max_expansions_mult: int = 5 # Множитель для лимита расширений (x5 от v2.0)
    plan_step_size: float = 1.0      # Длина одного шага в плане
    plan_neighbor_penalty: float = 0.3 # Штраф за близость к другому агенту
                                       # (sweep: 0.3 даёт wr=24.9%, 0.5 — шум;
                                       # дополнительно: у агента уже есть repul)
    plan_resource_bonus: float = 0.3   # Бонус за близость к ресурсу в эвристике

    # ───── Роли → физика движения (Levin-style дифференциация) ─────
    # Каждая роль имеет свой множитель скорости и сбора ресурсов
    role_speed: Optional[Dict[str, float]] = None
    role_harvest: Optional[Dict[str, float]] = None

    # ───── Ablation flags (для v3.1 vs v3.0 и прочих сравнений) ─────
    # Выключатели механизмов. True = включено (по умолчанию всё включено)
    ablate_planner: bool = False        # False = планировщик работает
    ablate_debates: bool = False        # False = дебаты идут
    ablate_synthesis: bool = False      # False = синтез работает
    ablate_beliefs: bool = False        # False = beliefs формируются
    ablate_style_adapt: bool = False    # False = стиль адаптируется

    def __post_init__(self):
        """Post-init — заполняем словари ролей (нельзя mutable default в @dataclass)."""
        if self.role_speed is None:
            # Explorer быстрый, но плохо собирает; builder медленный, но эффективный
            self.role_speed = {
                "explorer":  1.5,   # Главный разведчик — быстрый
                "builder":   0.6,   # Строитель — медленный, но работает
                "researcher": 1.0,  # Исследователь — средний
                "architect": 0.8,   # Архитектор — почти строитель
                "guardian":  0.7    # Страж — медленный, бдительный
            }
        if self.role_harvest is None:
            self.role_harvest = {
                "explorer":   0.7,  # Плохо собирает (занят разведкой)
                "builder":    1.5,  # Эффективный сборщик
                "researcher": 1.0,  # Средний
                "architect":  1.2,  # Хороший сборщик
                "guardian":   1.0   # Средний
            }
        # Применяем ablation глобально через главный выключатель
        if self.ablate_planner:
            self.plan_enabled = False


# ═══════════════════════════════════════════════════════════════════════════════
#                   A* PATH PLANNER (Механизм 15, НОВОЕ в v3.1)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Идея: агенты не просто реагируют на окружение, а ПЛАНИРУЮТ путь к цели.
# Это переход от голубя (реактивная навигация) к вороне (планировочная).
#
# Алгоритм A* (Hart, Nilsson, Raphael 1968):
#   f(n) = g(n) + h(n)
#   где g(n) — накопленная стоимость от старта до узла n,
#       h(n) — эвристика (оптимистичная оценка расстояния до цели).
#   Если h — допустимая (admissible) и непереоценивающая, A* оптимален.
#
# Наш случай:
#   • Пространство непрерывное (R^d), а A* классически работает на графе.
#   • Решение: дискретизируем окрестность агента — в каждой точке
#     рассматриваем K=plan_branching направлений (случайных или по сетке).
#   • Эвристика: евклидово расстояние до цели (admissible).
#   • Стоимость ребра: длина шага + штраф за близость к соседям.
#
# Баги, которые исправлены по сравнению с первой реализацией:
#   1. think_budget → горизонт зависит от ЭНЕРГИИ, а не от думок
#      (логика: голодный агент близорук, а не глупый)
#   2. plan_wins → считаем только при реальном достижении waypoint'а
#      (раньше считалась дельта fitness, что было некорректно)
#   3. last_horizon → это max_depth_seen (макс. глубина поиска),
#      а не длина найденного пути
#   4. max_expansions → ×5, а не ×2 (иначе A* не успевает найти путь
#      в многомерных пространствах)
#
# ───────────────────────────────────────────────────────────────────────────────

class AStarPlanner:
    """
    A* планировщик для агента в многомерном пространстве.

    Использование:
        planner = AStarPlanner(cfg)
        path = planner.plan(start, goal, obstacles_fn, heuristic_fn)
        # path — список waypoint'ов (numpy arrays) от start до goal

    Особенности реализации:
      • Пространство дискретизируется "на лету" — не хранится полный граф.
      • В open set используется heapq (min-heap по f-value).
      • Closed set — set позиций (округлённых до сетки 0.5 для хэширования).
      • Горизонт поиска ограничен max_expansions (защита от зависания).
      • При недостижении цели возвращается частичный путь к ближайшему узлу.

    Научная подоснова:
      Hart, Nilsson, Raphael (1968) "A Formal Basis for the Heuristic
      Determination of Minimum Cost Paths". IEEE Trans. Syst. Sci. Cybern.
    """

    def __init__(self, cfg: Config):
        """Инициализация планировщика с заданной конфигурацией."""
        self.cfg = cfg
        # Метрики планировщика (собираются для отладки и метрик)
        self.total_plans = 0         # Сколько раз вызван plan()
        self.successful_plans = 0    # Сколько раз достигнута цель
        self.total_expansions = 0    # Суммарное число раскрытий узлов
        self.max_depth_seen = 0      # Максимальная глубина поиска за прогон

    # ───────────────────────────────────────────────────────────────────────────
    #  Внутренние утилиты: хэширование позиций для closed set
    # ───────────────────────────────────────────────────────────────────────────

    def _hash_position(self, pos: np.ndarray, grid: float = 0.5) -> tuple:
        """
        Округляем позицию до сетки grid и превращаем в tuple для использования
        как ключ в set. Без этого два очень близких узла считались бы разными
        и A* зациклился бы.

        Параметры:
            pos : np.ndarray — точка в пространстве
            grid : float — размер ячейки сетки (0.5 по умолчанию)
        Возвращает:
            tuple целых — хэшируемый ключ позиции
        """
        return tuple(np.round(pos / grid).astype(int).tolist())

    # ───────────────────────────────────────────────────────────────────────────
    #  Эвристика: евклидово расстояние до цели
    # ───────────────────────────────────────────────────────────────────────────

    def _heuristic(self, pos: np.ndarray, goal: np.ndarray) -> float:
        """
        Допустимая эвристика — евклидово расстояние.
        "Допустимая" (admissible) значит: h(n) ≤ реального_расстояния(n, goal).
        Для евклидовой метрики в свободном пространстве — именно так.

        Если в дальнейшем добавим препятствия, эвристика останется допустимой
        (реальное расстояние с обходом не может быть меньше прямого).
        """
        # Работаем на минимуме размерностей — защита от несовпадения d
        md = min(len(pos), len(goal))
        return float(np.linalg.norm(pos[:md] - goal[:md]))

    # ───────────────────────────────────────────────────────────────────────────
    #  Генерация соседей: K случайных направлений вокруг узла
    # ───────────────────────────────────────────────────────────────────────────

    def _neighbors(self, pos: np.ndarray, dims: int,
                   goal: np.ndarray, rng: np.random.RandomState
                   ) -> List[np.ndarray]:
        """
        Генерируем plan_branching соседей вокруг текущей позиции.

        Стратегия:
          • Половина направлений — в сторону цели (эксплуатация)
          • Половина — случайные (исследование)
          • Каждое направление нормализуется и умножается на plan_step_size

        Это эвристический приём — чистый A* на непрерывном пространстве
        неэффективен, нужна разумная дискретизация.

        Параметры:
            pos : текущая позиция
            dims : размерность (может быть меньше len(pos) при хак-ресайзе)
            goal : цель (для bias в её сторону)
            rng : генератор случайных чисел (для воспроизводимости)
        """
        neighbors = []
        step = self.cfg.plan_step_size

        # D: адаптивное ветвление — если включено, K зависит от dims.
        # Логика: в 5D достаточно 4 направлений, в 13D нужно 10.
        # Формула: K = round(dims * 0.75), clip [3, 12].
        # Обоснование: при малых dims чрезмерное ветвление размывает фокус,
        # при больших — 5 направлений "слепят" агента в объёмном пространстве.
        if self.cfg.plan_adaptive_branching:
            K = int(np.clip(round(dims * 0.75), 3, 12))
        else:
            K = self.cfg.plan_branching

        # Направление к цели (нормализованное)
        md = min(dims, len(goal))
        to_goal = np.zeros(dims)
        diff = goal[:md] - pos[:md]
        norm = np.linalg.norm(diff)
        if norm > 1e-8:
            to_goal[:md] = diff / norm

        # Половина — в направлении цели с небольшим шумом
        for i in range(K // 2 + 1):
            noise = rng.normal(0, 0.3, dims)
            direction = to_goal + noise
            n = np.linalg.norm(direction)
            if n > 1e-8:
                direction = direction / n * step
            next_pos = pos[:dims] + direction
            # Обрезаем по границам пространства
            next_pos = np.clip(next_pos, -self.cfg.space, self.cfg.space)
            neighbors.append(next_pos)

        # Половина — чисто случайные направления
        for _ in range(K - K // 2 - 1):
            direction = rng.normal(0, 1, dims)
            n = np.linalg.norm(direction)
            if n > 1e-8:
                direction = direction / n * step
            next_pos = pos[:dims] + direction
            next_pos = np.clip(next_pos, -self.cfg.space, self.cfg.space)
            neighbors.append(next_pos)

        return neighbors

    # ───────────────────────────────────────────────────────────────────────────
    #  Стоимость перехода: базовая длина + штраф за близость к соседям
    # ───────────────────────────────────────────────────────────────────────────

    def _edge_cost(self, from_pos: np.ndarray, to_pos: np.ndarray,
                   obstacles: List[np.ndarray]) -> float:
        """
        Стоимость перехода from → to.
        Базовая стоимость — расстояние (всегда ≥ 0).
        Добавляется штраф за близость к препятствиям (другим агентам).

        Это превращает A* из чисто геометрического в "социальный" —
        планируемый путь учитывает плотность популяции.
        """
        md_ft = min(len(from_pos), len(to_pos))
        base = float(np.linalg.norm(from_pos[:md_ft] - to_pos[:md_ft]))

        # Штраф за близость к препятствиям
        penalty = 0.0
        for obs in obstacles:
            md_o = min(len(to_pos), len(obs))
            dist = np.linalg.norm(to_pos[:md_o] - obs[:md_o])
            if dist < 1.0:
                # Линейно растущий штраф в радиусе 1.0
                penalty += self.cfg.plan_neighbor_penalty * (1.0 - dist)

        return base + penalty

    # ───────────────────────────────────────────────────────────────────────────
    #  Главная функция: plan(start, goal, obstacles, horizon)
    # ───────────────────────────────────────────────────────────────────────────

    def plan(self, start: np.ndarray, goal: np.ndarray,
             obstacles: Optional[List[np.ndarray]] = None,
             horizon: Optional[int] = None,
             dims: Optional[int] = None,
             rng: Optional[np.random.RandomState] = None
             ) -> Tuple[List[np.ndarray], Dict[str, Any]]:
        """
        Главная функция планировщика. Возвращает путь и метрики поиска.

        Параметры:
            start     : начальная позиция (np.ndarray)
            goal      : целевая позиция (np.ndarray)
            obstacles : список позиций препятствий (другие агенты)
            horizon   : максимальная длина пути в шагах (если None — по умолчанию)
            dims      : размерность (если None — из start)
            rng       : генератор случайных чисел (если None — свой)

        Возвращает:
            (path, info):
              path  — список waypoint'ов от start к goal (или частичный путь)
              info  — словарь метрик: expansions, max_depth, reached_goal, etc.
        """
        if obstacles is None:
            obstacles = []
        if rng is None:
            rng = np.random.RandomState()
        if horizon is None:
            horizon = self.cfg.plan_horizon_base
        if dims is None:
            dims = len(start)

        self.total_plans += 1

        # Лимит расширений: чем глубже горизонт, тем больше узлов можем раскрыть
        max_expansions = horizon * self.cfg.plan_max_expansions_mult

        # ───── Инициализация открытого и закрытого множеств ─────
        # open_set — priority queue с элементами (f, counter, pos, path)
        # counter нужен чтобы heapq не сравнивал np.ndarray (вызывает ошибку)
        open_set: List[Tuple[float, int, tuple, List[np.ndarray], float]] = []
        counter = 0  # tie-breaker для heapq
        start_h = self._heuristic(start, goal)
        heapq.heappush(open_set, (start_h, counter, self._hash_position(start),
                                  [start.copy()], 0.0))

        # closed_set — множество уже раскрытых позиций (хэшированных)
        closed_set = set()

        # Счётчики для метрик
        expansions = 0
        max_depth = 0
        reached = False
        best_path = [start.copy()]
        best_h = start_h  # лучшая найденная h (ближе всего к цели)

        # ───── Главный цикл A* ─────
        while open_set and expansions < max_expansions:
            f, _, pos_key, path, g = heapq.heappop(open_set)
            current_pos = path[-1]
            depth = len(path) - 1
            max_depth = max(max_depth, depth)

            # Проверка: достигли цели?
            if self._heuristic(current_pos, goal) < self.cfg.plan_waypoint_radius:
                reached = True
                best_path = path
                self.successful_plans += 1
                break

            # Защита: слишком глубокий путь
            if depth >= horizon:
                # Запомним путь как лучший, если он ближе к цели
                h_now = self._heuristic(current_pos, goal)
                if h_now < best_h:
                    best_h = h_now
                    best_path = path
                continue

            # Защита: уже раскрывали эту точку?
            if pos_key in closed_set:
                continue
            closed_set.add(pos_key)

            # Расширяем: генерируем соседей и добавляем в open set
            for neighbor in self._neighbors(current_pos, dims, goal, rng):
                n_key = self._hash_position(neighbor)
                if n_key in closed_set:
                    continue
                edge_c = self._edge_cost(current_pos, neighbor, obstacles)
                new_g = g + edge_c
                new_h = self._heuristic(neighbor, goal)
                new_f = new_g + new_h
                # Запомним лучший из расширенных если он ближе
                if new_h < best_h:
                    best_h = new_h
                    best_path = path + [neighbor.copy()]

                counter += 1
                heapq.heappush(open_set,
                    (new_f, counter, n_key, path + [neighbor.copy()], new_g))

            expansions += 1

        # Обновляем глобальные метрики планировщика
        self.total_expansions += expansions
        self.max_depth_seen = max(self.max_depth_seen, max_depth)

        # Собираем info-словарь
        info = {
            "expansions": expansions,
            "max_depth": max_depth,
            "reached_goal": reached,
            "path_length": len(best_path),
            "final_h": self._heuristic(best_path[-1], goal) if best_path else 1e9
        }
        return best_path, info

    # ───────────────────────────────────────────────────────────────────────────
    #  Отчёт о планировщике (для metrics dump)
    # ───────────────────────────────────────────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        """Возвращает накопленные статистики планировщика."""
        success_rate = (self.successful_plans / self.total_plans
                        if self.total_plans > 0 else 0.0)
        avg_expansions = (self.total_expansions / self.total_plans
                          if self.total_plans > 0 else 0.0)
        return {
            "total_plans": self.total_plans,
            "successful_plans": self.successful_plans,
            "success_rate": round(success_rate, 3),
            "total_expansions": self.total_expansions,
            "avg_expansions": round(avg_expansions, 2),
            "max_depth_seen": self.max_depth_seen
        }


# ═══════════════════════════════════════════════════════════════════════════════
#                            IDEA CLASS (Механизм 14)
# ═══════════════════════════════════════════════════════════════════════════════
#
# История разработки:
#   1. GPT предложил хранить идеи в виде dict (минималистично)
#   2. Claude выступил адвокатом дьявола: "dict не может эволюционировать,
#      не может иметь методов, не может конкурировать" — сделал полноценный класс
#   3. Gemini отревьюил, добавил свойство `strength` и декей
#
# Философия: идеи — это САМОСТОЯТЕЛЬНЫЕ СУЩНОСТИ, а не свойство агента.
# Они рождаются из интерпретации трейса, мутируют при передаче, конкурируют
# за внимание через дебаты, эволюционируют меметически (Dawkins 1976).
#
# Каждая идея имеет:
#   • origin_agent  — кто породил
#   • style         — какой стиль мышления породил (влияет на debate)
#   • score         — базовая оценка (вход в систему)
#   • confidence    — текущая уверенность (меняется в дебатах)
#   • category      — к какой категории belief относится
#   • supporters    — агенты, которые поддержали
#   • critics       — агенты, которые покритиковали
#   • mutations     — счётчик мутаций
#   • age           — возраст в шагах
#   • alive         — живая или уже "забыта"
#
# ───────────────────────────────────────────────────────────────────────────────

class Idea:
    """
    Идея — самостоятельная эволюционирующая сущность.

    Меметическая эволюция (Dawkins 1976):
      • Рождается из интерпретации трейса конкретным когнитивным стилем
      • Передаётся от агента к агенту с мутацией (idea_mutation_rate)
      • Конкурирует за выживание через дебаты
      • Декей по confidence — неподдержанные идеи умирают
      • Strength = f(confidence, supporters, critics) — эволюционный фитнес
    """

    # Глобальный счётчик id идей (для трекинга и reset между прогонами)
    _id = 0

    def __init__(self, origin_agent: int, origin_trace_ai: int, style: str,
                 score: float, category: int, step: int):
        """
        Создаём новую идею.

        Параметры:
            origin_agent    : id агента, породившего идею
            origin_trace_ai : assembly index трейса-источника
            style           : когнитивный стиль родителя
            score           : базовая оценка (зависит от стиля и трейса)
            category        : категория belief, которую затрагивает
            step            : шаг симуляции, когда идея родилась
        """
        Idea._id += 1
        self.id = Idea._id                    # Уникальный id
        self.origin_agent = origin_agent      # Кто родил
        self.style = style                    # Когнитивный стиль родителя
        self.score = float(score)             # Исходная оценка
        self.category = category              # Категория belief
        self.step = step                      # Шаг рождения
        self.origin_ai = origin_trace_ai      # AI исходного трейса
        self.confidence = float(score)        # Уверенность (меняется дебатами)
        self.supporters = [origin_agent]      # Список поддержавших
        self.critics: List[str] = []          # Список критиков (стили)
        self.mutations = 0                    # Счётчик мутаций
        self.age = 0                          # Возраст в шагах
        self.alive = True                     # Флаг "жива"

    def debate_with(self, agent_style: str, agent_sm_conf: float) -> None:
        """
        Настоящие дебаты — не случайная функция!
        Каждый стиль критикует идею по-своему.

        Логика от Claude (улучшение GPT blueprint):
          • skeptical  — снижает уверенность пропорц. своей компетентности
          • analytical — усиливает если AI высокий, ослабляет если низкий
          • intuitive  — либо сильно за, либо сильно против (биполярный)
          • synthetic  — всегда слегка усиливает (ищет пользу)
          • exploratory — ценит новизну (высокий AI)
        """
        if agent_style == "skeptical":
            # Скептик снижает уверенность.
            # Если его самомодель уверена в себе (sm_conf высокий),
            # критика острее. Если не уверен — критика мягче.
            # Формула: confidence *= (0.7 + 0.3 * (1 - sm_conf))
            # При sm_conf=1 → множитель 0.7 (сильная критика)
            # При sm_conf=0 → множитель 1.0 (почти не критикует)
            self.confidence *= (0.7 + 0.3 * (1 - agent_sm_conf))
            self.critics.append(agent_style)

        elif agent_style == "analytical":
            # Аналитик смотрит на сложность (origin_ai).
            # Высокий AI (>5) → идея сложная, достойная → усиливаем x1.1
            # Низкий AI → идея поверхностная → ослабляем x0.9
            if self.origin_ai > 5:
                self.confidence *= 1.1
            else:
                self.confidence *= 0.9
            self.critics.append(agent_style)

        elif agent_style == "intuitive":
            # Интуитивист — биполярный. Либо сильно "да", либо сильно "нет".
            # Моделирует "нутром чую" — резкие реакции без аналитики.
            self.confidence *= np.random.choice([0.7, 1.3])

        elif agent_style == "synthetic":
            # Синтетик всегда ищет пользу, добавляется в supporters.
            # Моделирует конструктивное мышление ("и это можно использовать!")
            self.confidence *= 1.05
            self.supporters.append("synthetic")

        elif agent_style == "exploratory":
            # Исследователь ценит новизну — log от AI.
            # log1p(ai) — безопасный лог (log1p(0)=0), не взрывается.
            novelty_bonus = np.log1p(self.origin_ai) * 0.05
            self.confidence *= (1 + novelty_bonus)

    def mutate(self) -> None:
        """
        Мутация идеи при передаче от агента к агенту.
        Имитирует "испорченный телефон" — идея меняется при пересказе.
        """
        self.mutations += 1
        # Score и confidence получают мультипликативный шум
        self.score *= np.random.uniform(0.9, 1.1)
        self.confidence *= np.random.uniform(0.95, 1.05)

    def decay(self) -> None:
        """
        Декей идеи за шаг.
        Confidence умножается на 0.99 — медленное забвение.
        Если confidence упал ниже 0.01 — идея считается "умершей".
        """
        self.age += 1
        self.confidence *= 0.99
        if self.confidence < 0.01:
            self.alive = False

    @property
    def strength(self) -> float:
        """
        Сила идеи — эволюционный фитнес в меметическом отборе.

        Формула: strength = confidence * (1 + support*0.1) * (1 + critics*0.05)

        Парадокс: КРИТИКИ УСИЛИВАЮТ идею, а не ослабляют.
        Логика: идея, которая выжила после критики, — сильнее, чем идея,
        которую никто не оспаривал. Это Поппер-эффект — фальсифицированная,
        но устоявшаяся гипотеза достоверна.

        Ссылка: Popper (1959) "The Logic of Scientific Discovery"
        """
        support = len(self.supporters)
        survived_critics = len(self.critics)
        return self.confidence * (1 + support * 0.1) * (1 + survived_critics * 0.05)


# ═══════════════════════════════════════════════════════════════════════════════
#                        TORQUE TRACES (след-торки)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Торк-трейс — это "след взаимодействия" двух агентов в пространстве.
# Ключевая идея MAES: знания хранятся НЕ как данные, а как РЕЦЕПТЫ СБОРКИ.
# Это реализация Assembly Theory (Cronin 2023, Nature):
#   • Каждый объект раскладывается в последовательность базовых "кирпичиков"
#   • Assembly Index (AI) = число элементарных операций для сборки
#   • Высокий AI = сложная, содержательная структура
#
# В MAES:
#   • Когда два агента встречаются — рождается trace
#   • Trace имеет embedding (смесь геномов), position (точка встречи), value
#   • Recipe — разложение embedding в базисе из N=8 единичных векторов
#   • Subs — sub-recipes (рекурсивная сборка: трейсы как блоки других трейсов)
#   • AI = len(recipe) + sum(len(sub) for sub in subs)
#
# Это снимает "потолок сложности" = число измерений (важное открытие v2.0):
#   • Без subs max AI = dims (8 максимум для базиса)
#   • С subs — можно строить сколь угодно сложные структуры рекурсивно
#
# Дополнительно:
#   • Tombstone — при смерти агент оставляет "надгробие" с его values/role/beliefs
#     Трейс-надгробие передаёт культурное наследие живым (Gemini's добавка)
#   • confirm() — другие агенты могут "подтвердить" трейс, увеличив его ценность
#   • compose() — два трейса комбинируются в новый (с subs=[recipe1, recipe2])
#
# ───────────────────────────────────────────────────────────────────────────────

class TorqueTrace:
    """
    Торк-трейс — след взаимодействия агентов в многомерном пространстве.
    Реализует Assembly Theory: хранит не значения, а рецепт сборки.
    """

    # Глобальный счётчик id трейсов
    _id = 0
    # Кэш базисов по размерности (чтобы не пересчитывать каждый раз)
    _bases: Dict[int, np.ndarray] = {}

    def __init__(self, pos: np.ndarray, emb: np.ndarray, val: float,
                 pids: tuple = (), step: int = 0, tombstone: Optional[Dict] = None):
        """
        Создаём трейс.

        Параметры:
            pos       : точка встречи в пространстве
            emb       : embedding (смесь геномов участников)
            val       : ценность трейса (на основе interference)
            pids      : tuple id агентов-родителей
            step      : шаг симуляции
            tombstone : опциональное "надгробие" (values, role, beliefs умершего)
        """
        TorqueTrace._id += 1
        self.id = TorqueTrace._id
        self.position = pos.copy()                     # Копия, чтобы не мутировать
        self.embedding = emb.copy()
        # Clip на 50 — защита от переполнения при долгой эволюции
        self.value = float(np.clip(val, 0, 50))
        self.pids = pids                               # id родителей
        self.step = step                               # Шаг рождения
        # Recipe = разложение embedding в базисе
        self.recipe = self._make(emb)
        self.subs: List[List] = []                     # Sub-recipes (рекурсия)
        self.confirmed = 0.0                           # Суммарное "подтверждение"
        self.confirms = 0                              # Счётчик подтверждений
        self.mlm: List[int] = []                       # MLM-цепочка id агентов
        # meaning = доминирующая ось в первых 5 измерениях (для группировки)
        self.meaning = int(np.argmax(np.abs(emb[:5]))) if len(emb) >= 5 else 0
        self.tombstone = tombstone                     # Культурное наследие

    @classmethod
    def _bf(cls, d: int, n: int = 8) -> np.ndarray:
        """
        Генерация базиса для разложения. Кэшируется по размерности.

        Базис:
          • Первые d единичных векторов (ортонормальных): e_0, e_1, ..., e_{d-1}
          • Комбинации пар: (e_i + e_j)/√2 и (e_i - e_j)/√2
            — симметричные и антисимметричные
          • Итого до n*3 векторов в базисе (для n=8 — 24)

        Это НЕ классический матем. базис — это overcomplete dictionary.
        Разложение через max-inner-product matching pursuit.
        """
        if d in cls._bases:
            return cls._bases[d]
        b = []
        # Первые min(d, n) единичных векторов
        for i in range(min(d, n)):
            v = np.zeros(d)
            v[i] = 1.0
            b.append(v)
        # Комбинации пар (до n*3 векторов всего)
        for i in range(min(d, n)):
            for j in range(i + 1, min(d, n)):
                if len(b) >= n * 3:
                    break
                # Симметричный
                v = np.zeros(d)
                v[i] = 0.707  # 1/√2
                v[j] = 0.707
                b.append(v)
                # Антисимметричный
                v2 = np.zeros(d)
                v2[i] = 0.707
                v2[j] = -0.707
                b.append(v2)
        cls._bases[d] = np.array(b)
        return cls._bases[d]

    @staticmethod
    def _make(e: np.ndarray, n: int = 8) -> List[Tuple[int, float]]:
        """
        Разложение вектора e в последовательность (basis_index, coefficient).

        Алгоритм — жадный matching pursuit:
          1. Берём остаток res = e
          2. Находим базисный вектор B[bi] с максимальным inner product
          3. Квантуем коэффициент до 1/8 (удаляем шум)
          4. Вычитаем вклад: res -= q * B[bi]
          5. Повторяем пока ||res|| > threshold
          6. Возвращаем список (bi, q) — это и есть recipe

        Почему квантование до 1/8?
          • Сглаживает стохастику: похожие трейсы получают одинаковые рецепты
          • Имитирует дискретность генетического кода (ACGT)

        Возвращает: список кортежей (basis_index, quantized_coefficient)
        """
        # Защита от NaN/Inf
        if not np.all(np.isfinite(e)):
            return []

        d = len(e)
        r: List[Tuple[int, float]] = []
        res = e.copy()
        B = TorqueTrace._bf(d, n)

        # До 80 итераций — защита от бесконечного цикла
        for _ in range(80):
            # Останов: остаток слишком мал
            if np.linalg.norm(res) < 0.005:
                break
            # Проекция на базис
            p = B @ res
            if not np.all(np.isfinite(p)):
                break
            # Лучший базисный вектор
            bi = int(np.argmax(np.abs(p)))
            bp = float(p[bi])
            if not np.isfinite(bp):
                break
            # Квантование до 1/8
            q = round(bp * 8) / 8
            # Если квантованный коэффициент слишком мал — выход
            if abs(q) < 0.1:
                break
            r.append((bi, q))
            # Обновляем остаток
            res -= q * B[bi]

        # Fallback: если ничего не разложили, но вектор ненулевой — 1 элемент
        if not r and np.linalg.norm(e) > 0.05:
            p = B @ e
            bi = int(np.argmax(np.abs(p)))
            q = round(float(p[bi]) * 8) / 8
            if abs(q) > 0.01:
                r.append((bi, q))
        return r

    @property
    def ai(self) -> int:
        """
        Assembly Index (AI) — метрика сложности.
        len(recipe) = сколько базовых операций для построения этого трейса.
        + sum(len(sub)) = дополнительные операции для sub-traces (рекурсия).

        Чем выше AI — тем сложнее структура.
        В MAES это главная метрика OEE (Open-Ended Evolution).
        """
        return len(self.recipe) + sum(len(r) for r in self.subs)

    def decay(self, r: float) -> None:
        """Декей ценности за шаг. r — коэффициент затухания (0.95)."""
        self.value *= r

    def confirm(self, aid: int, b: float) -> None:
        """
        Агент aid подтверждает трейс, добавляя bonus b к confirmed.
        Это часть Knowledge Economy — трейсы с подтверждениями стоят дороже.
        """
        self.confirms += 1
        self.confirmed += b
        if aid not in self.mlm:
            self.mlm.append(aid)
        # Ограничиваем длину MLM-цепочки (от GPT: предотвращает memory leak)
        if len(self.mlm) > 20:
            self.mlm = self.mlm[-20:]

    def price(self) -> float:
        """
        Рыночная цена трейса в Knowledge Economy.
        Формула: (value + confirmed) * (1 + log1p(ai) * 0.3)
        • Сложность (ai) усиливает цену логарифмически
        • Подтверждения (confirmed) суммируются с базовой value

        Complexity pressure (от GPT) — иначе AI не растёт в долгосроке.
        """
        return (self.value + self.confirmed) * (1 + np.log1p(self.ai) * 0.3)

    def compose(self, o: 'TorqueTrace') -> 'TorqueTrace':
        """
        Композиция двух трейсов: усреднение позиции и embedding, сумма value.
        Новый трейс имеет subs=[recipe1, recipe2] — рекурсивная сборка.

        Это ключевой механизм роста AI:
          • Без композиции max_AI = размерность базиса (≈8)
          • С композицией — AI растёт экспоненциально через рекурсию
          • Снимает "потолок сложности" (v2.0 фикс от GPT)
        """
        md = min(len(self.position), len(o.position))
        t = TorqueTrace(
            (self.position[:md] + o.position[:md]) / 2,
            (self.embedding[:md] + o.embedding[:md]) / 2,
            (self.value + o.value) * 0.8,  # Немного теряем при сборке
            (self.id, o.id),
            max(self.step, o.step)
        )
        t.subs = [self.recipe, o.recipe]
        return t


# ═══════════════════════════════════════════════════════════════════════════════
#                      RESOURCE FIELD + SPATIAL HASH
# ═══════════════════════════════════════════════════════════════════════════════
#
# ResourceField — источники энергии в пространстве. Точки, около которых
# агенты получают энергию при проходе. Депление (истощение) и респавн.
#
# SpatialHash — пространственная индексация для быстрого поиска соседей.
# Без неё: O(N²) на каждый шаг, что неприемлемо при N > 100.
# С хэшем: O(N * k), где k — среднее число агентов в cell.
#
# ВАЖНО: SpatialHash адаптивный — PCA-оси (от Gemini).
# Пространство 13D, но хэшируем только 3 самых вариативных оси.
# Это сохраняет точность соседства при работе в высоких размерностях.
#
# ───────────────────────────────────────────────────────────────────────────────

class ResourceField:
    """
    Поле ресурсов — точки в пространстве, у которых агенты могут собирать энергию.
    Ресурсы истощаются при сборе и медленно восстанавливаются.
    """

    def __init__(self, c: Config):
        """Инициализация: n_res случайных точек в пространстве."""
        self.c = c
        # Точки равномерно распределены в [-space, +space]^dims
        self.pts = np.random.uniform(-c.space, c.space, (c.n_res, c.dims))
        # Ценность каждой точки — стартовая base value
        self.vals = np.ones(c.n_res) * c.res_v

    def harvest(self, pos: np.ndarray, rm: float = 1.0) -> float:
        """
        Собираем ресурс в окрестности позиции pos.

        Алгоритм:
          1. Находим все точки в радиусе res_r
          2. Суммируем их ценность с весом 1/(distance + 0.1)
               — близкие ресурсы дают больше
          3. Умножаем на rm (role multiplier: builder собирает x1.5)
          4. Депление: собранные точки теряют res_depl (30%) ценности
          5. Clip результата на 0.3 за шаг (анти-fat-tail)

        Параметры:
            pos : позиция агента
            rm  : role multiplier (от cfg.role_harvest)
        Возвращает:
            float — полученная энергия
        """
        # md нужен если dims у поля меньше чем у агента (после resize)
        md = min(len(pos), self.pts.shape[1])
        d = np.linalg.norm(self.pts[:, :md] - pos[:md], axis=1)
        near = d < self.c.res_r
        if not np.any(near):
            return 0.0
        # Взвешенная сумма с защитой от деления на ноль
        g = float(np.sum(self.vals[near] / (d[near] + 0.1))) * rm
        # Депление
        self.vals[near] *= (1 - self.c.res_depl)
        # Clip на 0.3 — иначе один "жирный" шаг сломает энергетику
        return min(g, 0.3)

    def respawn(self, rng: np.random.RandomState, dims: int) -> None:
        """
        Респавн пустых ресурсов.
        Каждая точка с vals < 0.5 * base имеет шанс res_resp (2%) возродиться.
        Также: если пространство выросло (абдукция), добавляем координаты.
        """
        for i in range(len(self.vals)):
            if self.vals[i] < self.c.res_v * 0.5 and rng.random() < self.c.res_resp:
                self.vals[i] = self.c.res_v
        # Если размерность выросла — расширяем координаты точек
        if dims > self.pts.shape[1]:
            self.pts = np.hstack([
                self.pts,
                np.random.uniform(-self.c.space, self.c.space,
                                  (len(self.pts), dims - self.pts.shape[1]))
            ])


class SpatialHash:
    """
    Пространственный хэш для быстрого поиска соседей.
    Важнейшая оптимизация: без неё O(N²) на каждом шаге.

    PCA-адаптивные оси (от Gemini v3):
      • В 13D пространстве хэшировать по всем 13 осям нерационально
      • Выбираем 3 самые вариативные оси (argsort по var)
      • Обновляем каждые 50 шагов — оси могут меняться при эволюции
    """

    def __init__(self, cell: float = 3.0):
        """cell — размер ячейки хэша."""
        self.cell = cell
        self.cells: Dict[tuple, List] = {}
        self.axes: tuple = (0, 1, 2)  # Стартовые оси

    def update_axes(self, agents: List['Agent'], step: int) -> None:
        """
        PCA-обновление осей каждые 50 шагов.
        Выбираем 3 оси с максимальной дисперсией позиций агентов.
        """
        if step % 50 != 0 or len(agents) < 5:
            return
        md = max(a.dims for a in agents)
        P = np.zeros((len(agents), md))
        for i, a in enumerate(agents):
            P[i, :a.dims] = a.position[:a.dims]
        # argsort(variance)[-3:] — 3 самые вариативные оси
        self.axes = tuple(sorted(np.argsort(np.var(P, axis=0))[-3:]))

    def clear(self) -> None:
        """Очистка хэша перед обновлением."""
        self.cells.clear()

    def _k(self, p: np.ndarray) -> tuple:
        """
        Ключ ячейки для позиции p.
        Берём только координаты по self.axes, квантуем на cell.
        """
        c = np.array([p[d] if d < len(p) else 0.0 for d in self.axes])
        return tuple((c / self.cell).astype(int))

    def insert(self, a: 'Agent') -> None:
        """Добавляем агента в хэш."""
        self.cells.setdefault(self._k(a.position), []).append(a)

    def query(self, a: 'Agent', r: float) -> List['Agent']:
        """
        Находим всех агентов в радиусе r от a.

        Алгоритм:
          1. Определяем в какой cell мы
          2. Смотрим все соседние cells в радиусе R = ceil(r/cell)
          3. Для каждого кандидата — точная проверка по расстоянию

        Возвращает максимум 25 соседей (защита от "жирных" кластеров).
        """
        ck = self._k(a.position)
        R = max(1, int(np.ceil(r / self.cell)))
        res = []
        for dx in range(-R, R + 1):
            for dy in range(-R, R + 1):
                for dz in range(-R, R + 1):
                    key = (
                        ck[0] + dx,
                        ck[1] + dy if len(ck) > 1 else 0,
                        ck[2] + dz if len(ck) > 2 else 0
                    )
                    for o in self.cells.get(key, []):
                        if o.id == a.id:
                            continue
                        md = min(a.dims, o.dims)
                        if np.linalg.norm(a.position[:md] - o.position[:md]) < r:
                            res.append(o)
                            if len(res) >= 25:
                                return res
        return res


# ═══════════════════════════════════════════════════════════════════════════════
#                  ВНУТРЕННИЕ СИСТЕМЫ АГЕНТА
# ═══════════════════════════════════════════════════════════════════════════════
#
# Каждый агент имеет набор внутренних систем, моделирующих разные аспекты
# когнитивной архитектуры:
#
#   1. CausalGraph    — каузальные связи между измерениями (Pearl's do-calculus)
#   2. WorldModel     — предсказательная модель мира (LeCun's JEPA)
#   3. SelfModel      — самомодель: карта способностей (Bongard, Lipson)
#
# Все три системы:
#   • Обучаются онлайн из опыта
#   • Имеют забывание (чтобы не окостенеть)
#   • Влияют на решения агента
#   • Resizable — расширяются при росте пространства
#
# ───────────────────────────────────────────────────────────────────────────────

class CausalGraph:
    """
    Каузальный граф — моделирует "что влияет на что" в измерениях пространства.

    Реализует 3 уровня Pearl:
      1. Наблюдение — observe(before, after)
      2. Интервенция — intervene(dim, strength)
      3. Контрфактуал — через пересчёт графа при новых данных

    Рёбра имеют:
      • strength — среднее произведение дельт измерений
      • confidence — уверенность (растёт с числом наблюдений)
      • n — счётчик наблюдений

    Забывание: при переполнении удаляем слабые рёбра (от Gemini — чтобы граф
    не окостеневал и мог обновляться при смене динамики среды).
    """

    def __init__(self, mx: int = 50):
        """mx — максимум рёбер в графе."""
        self.edges: Dict[Tuple[int, int], Tuple[float, float, int]] = {}
        self.mx = mx

    def observe(self, b: np.ndarray, a: np.ndarray) -> None:
        """
        Наблюдаем переход from state b to state a.
        Для всех пар (i, j) значимо изменившихся измерений обновляем ребро i→j.
        """
        ml = min(len(b), len(a))
        d = a[:ml] - b[:ml]
        sig = np.where(np.abs(d) > 0.01)[0]  # Только значимые изменения
        for i in sig:
            for j in sig:
                if i == j:
                    continue
                k = (int(i), int(j))
                if k in self.edges:
                    # Обновляем существующее ребро (скользящее среднее)
                    st, c, n = self.edges[k]
                    new_st = (st * n + d[i] * d[j]) / (n + 1)
                    self.edges[k] = (new_st, min(1, c + 0.05), n + 1)
                elif len(self.edges) < self.mx:
                    # Добавляем новое ребро
                    self.edges[k] = (float(d[i] * d[j]), 0.1, 1)
                else:
                    # Граф полон — удаляем самое слабое ребро
                    # min по |strength| * confidence — забываем незначимые связи
                    wk = min(self.edges,
                             key=lambda x: abs(self.edges[x][0]) * self.edges[x][1])
                    del self.edges[wk]
                    self.edges[k] = (float(d[i] * d[j]), 0.1, 1)

    def intervene(self, dim: int, st: float) -> Dict[int, float]:
        """
        Do-calculus: если вмешаемся в dim с силой st,
        какие изменения ожидаем в других измерениях?

        Возвращает словарь {target_dim: predicted_change}
        Учитываем только рёбра с confidence > 0.3 (не случайные корреляции).
        """
        return {
            e: sv * st * c
            for (ca, e), (sv, c, n) in self.edges.items()
            if ca == dim and c > 0.3
        }


class WorldModel:
    """
    Линейная модель мира: предсказывает следующее состояние по текущему и действию.

    NextState ≈ W @ [state, action] + b

    Использует:
      • Online learning (SGD с clip'ом на gradient explode)
      • Error history для уверенности в себе (conf)
      • REM-sleep: offline повтор буфера опыта (от Gemini — выборочный, только
        агенты с высокой ошибкой, иначе пустая трата вычислений)

    Ссылка: LeCun (2022) "A Path Towards Autonomous Machine Intelligence" (JEPA)
    """

    def __init__(self, d: int, lr: float = 0.01):
        """d — размерность пространства, lr — learning rate."""
        self.d = d
        self.lr = lr
        # Матрица W: d -> d*2 (state + action concat)
        self.W = np.random.randn(d, d * 2) * 0.1
        self.b = np.zeros(d)
        # Error history для conf()
        self.eh: deque = deque(maxlen=50)

    def _p(self, a: np.ndarray) -> np.ndarray:
        """Padding/truncation к размерности d — защита от размерных несоответствий."""
        return a[:self.d] if len(a) >= self.d else np.pad(a, (0, self.d - len(a)))

    def predict(self, st: np.ndarray, ac: np.ndarray) -> np.ndarray:
        """Предсказываем next_state по текущему state и действию ac."""
        return self.W @ np.concatenate([self._p(st), self._p(ac)]) + self.b

    def train(self, st: np.ndarray, ac: np.ndarray, ns: np.ndarray) -> float:
        """
        Online обучение: обновляем W и b по ошибке предсказания.
        Возвращаем norm ошибки (для conf).

        Gradient clipping (clip на [-1, 1]) — защита от взрывных градиентов,
        которые могут разрушить веса при смене динамики.
        """
        inp = np.concatenate([self._p(st), self._p(ac)])
        err = self._p(ns) - (self.W @ inp + self.b)
        self.W += self.lr * np.clip(np.outer(err, inp), -1, 1)
        self.b += self.lr * np.clip(err, -1, 1)
        e = float(np.linalg.norm(err))
        self.eh.append(e)
        return e

    def sleep(self, buf: deque) -> None:
        """
        REM-фаза: повторяем буфер опыта offline (3 эпохи, последние 60 шагов).
        Это ключевой механизм от v2.0 — агент консолидирует знания.

        Выборочный сон (от Gemini): метод вызывается только для агентов
        с высокой ошибкой (см. Env.step).
        """
        if len(buf) < 3:
            return
        for _ in range(3):
            for st, ac, ns in list(buf)[-60:]:
                try:
                    self.train(st, ac, ns)
                except Exception:
                    pass  # Защита от numerical issues

    def conf(self) -> float:
        """
        Уверенность = exp(-mean(recent errors)).
        Маленькая ошибка → высокая уверенность (exp(0) = 1).
        Большая ошибка → уверенность → 0.
        """
        return float(np.exp(-np.mean(list(self.eh)[-10:]))) if len(self.eh) >= 3 else 0.0

    def resize(self, nd: int) -> None:
        """
        Расширяем модель при росте пространства.
        Сохраняем старые веса (копируем в top-left), новые — мелкий шум.
        """
        if nd <= self.d:
            return
        oW, ob, od = self.W, self.b, self.d
        self.W = np.random.randn(nd, nd * 2) * 0.01
        # Сохраняем старые веса
        self.W[:od, :od] = oW[:, :od]
        self.W[:od, nd:nd + od] = oW[:, od:]
        self.b = np.zeros(nd)
        self.b[:od] = ob
        self.d = nd


class SelfModel:
    """
    Самомодель агента: карта способностей по каждому измерению.

    Хранит:
      • c[i] — confidence в измерении i (растёт при успехах)
      • l[i] — lack (недостаток) в измерении i (растёт при неудачах)
      • w — счётчик побед
      • f — счётчик поражений

    Используется для:
      • weakest() — самое слабое измерение, которое стоит "прокачать"
      • conf() — общая самоуверенность (win rate)

    Ссылка: Bongard & Lipson (2006) — роботы с самомоделью.
    """

    def __init__(self, d: int):
        self.c = np.zeros(d)  # Confidence по каждому измерению
        self.l = np.zeros(d)  # Lack по каждому измерению
        self.w = 0            # Всего побед
        self.f = 0            # Всего поражений

    def update(self, dim: int, ok: bool) -> None:
        """
        Обновляем самомодель: в измерении dim был успех (ok=True) или нет.
        Успех: confidence +0.1, lack -0.05 (decay противоположности)
        Неудача: наоборот.
        """
        if dim >= len(self.c):
            return
        if ok:
            self.c[dim] = min(1, self.c[dim] + 0.1)
            self.l[dim] = max(0, self.l[dim] - 0.05)
            self.w += 1
        else:
            self.l[dim] = min(1, self.l[dim] + 0.1)
            self.c[dim] = max(0, self.c[dim] - 0.05)
            self.f += 1

    def weakest(self) -> Optional[int]:
        """
        Возвращает id самого слабого измерения (для прокачки).
        Только если lack > 0.3 (не возвращаем "нормальные" измерения).
        """
        i = int(np.argmax(self.l - self.c))
        return i if self.l[i] > 0.3 else None

    def conf(self) -> float:
        """Общая уверенность = win rate (+1 — защита от деления на 0)."""
        return self.w / (self.w + self.f + 1)

    def resize(self, nd: int) -> None:
        """Расширяем модель при росте пространства."""
        if nd <= len(self.c):
            return
        self.c = np.pad(self.c, (0, nd - len(self.c)))
        self.l = np.pad(self.l, (0, nd - len(self.l)))


# ═══════════════════════════════════════════════════════════════════════════════
#                         AGENT — главный класс агента
# ═══════════════════════════════════════════════════════════════════════════════
#
# Агент — носитель ~35 механизмов, объединённых в единую когнитивную архитектуру.
#
# СЛОИ АГЕНТА (снизу вверх):
#
#   1. Физический:  position, velocity, energy, age, genome
#   2. Предиктивный: predictor, wm (world model), uncertainty
#   3. Каузальный:  causal graph, самомодель (sm)
#   4. Социальный:  role, species_id, signal, tom (theory of mind)
#   5. Ценностный:  values, identity, commitment, goals, goal_stack
#   6. Контекстный: context, abstractions, mem_sig, concepts
#   7. Когнитивный: critic, decisions, contrast_mem
#   8. Стилевой:    cognitive_style, beliefs, ideas_generated
#   9. Планирующий: planner (A*), planned_path, last_horizon  ← НОВОЕ в v3.1
#
# КАЖДЫЙ ШАГ АГЕНТ:
#
#   A. Воспринимает: соседей, ресурсы, свои ощущения
#   B. Оценивает контекст: богато/опасно/толпа/frontier
#   C. Выбирает цель: по ценностям + beliefs, с учётом regret
#   D. Планирует путь: A* к цели (если v3.1 и есть cell budget)
#   E. Двигается: по плану или реактивно
#   F. Взаимодействует: создаёт trace, торгует, размножается
#   G. Обновляется: beliefs, values, identity, самомодель
#   H. Адаптируется: роль, стиль (каждые 20 шагов)
#
# ───────────────────────────────────────────────────────────────────────────────

class Agent:
    """
    Главный класс агента в MAES.

    Содержит 35+ механизмов когнитивной архитектуры, включая:
      • Базовые: движение, энергия, восприятие, память
      • Креативность: любопытство, абдукция, контрастная коррекция
      • Метапознание: самомодель, критик, theory of mind
      • Субъективность: ценности, идентичность, commitment, убеждения
      • Коллективный синтез: стиль, идеи, дебаты
      • Планирование: A* с горизонтом от энергии (v3.1 НОВОЕ)
    """

    # Глобальный счётчик id агентов
    _id = 0

    # Константы класса — роли (Levin-style морфогенез)
    ROLES = ["explorer", "builder", "researcher", "architect", "guardian"]

    # Константы класса — названия belief-категорий
    # (обобщённые убеждения, не привязка к trace_id — фикс от GPT/Claude v3)
    BELIEF_NAMES = [
        "space_is_rich",     # "пространство богатое" — ведёт к exploration
        "complexity_pays",   # "сложность окупается" — усиливает complex goal
        "social_helps",      # "общение помогает" — усиливает social goal
        "danger_nearby",     # "опасность рядом" — усиливает safe goal
        "change_is_good",    # "перемены — это хорошо" — усиливает exploration
        "patience_works"     # "терпение работает" — влияет на commitment
    ]

    def __init__(self, cfg: Config, pos: Optional[np.ndarray] = None):
        """
        Создание агента.

        Параметры:
            cfg : Config — глобальная конфигурация
            pos : Optional[np.ndarray] — стартовая позиция (None = случайная)
        """
        Agent._id += 1
        self.id = Agent._id
        self.cfg = cfg
        d = cfg.dims  # Стартовая размерность

        # ───── СЛОЙ 1: Физический ─────
        self.position = pos.copy() if pos is not None else \
            np.random.uniform(-cfg.space, cfg.space, d)
        self.velocity = np.random.uniform(-0.3, 0.3, d)
        self.energy = cfg.init_e
        self.age = 0
        self.genome = np.random.uniform(-1, 1, d)

        # ───── СЛОЙ 2: Предиктивный ─────
        self.predictor = np.zeros(d)    # Простой линейный предиктор (fallback)
        self.last_pe = 1.0              # Last prediction error
        self.steps_ni = 0               # Steps Not Improved (для boredom)
        self.wm = WorldModel(d, cfg.wm_lr)
        self.exp_buf: deque = deque(maxlen=cfg.exp_buf)
        self.uncertainty = np.ones(d) * 0.5  # Неопределённость по измерениям

        # ───── СЛОЙ 3: Каузальный ─────
        self.causal = CausalGraph(cfg.causal_mx)
        self.last_st: Optional[np.ndarray] = None
        self.sm = SelfModel(d)

        # ───── СЛОЙ 4: Социальный ─────
        self.role = "explorer"
        self.role_sig = np.zeros(5)     # Сигналы о ролях соседей
        self.species_id: Optional[int] = None
        self.survived = 0               # Кол-во пережитых катастроф
        self.mut_rate = 0.1             # Скорость мутации (растёт после стагнации)
        self.cat_boost = 1.0            # Post-catastrophe boost к движению
        self.signal: Optional[Tuple] = None   # Испускаемый сигнал
        self.tom: Dict[int, Dict] = {}  # Theory of Mind: модели соседей

        # ───── СЛОЙ 5: Ценностный + Цели ─────
        self.contrast_mem: deque = deque(maxlen=5)  # Векторы провалов других
        self.prev_fit = cfg.init_e      # Предыдущий фитнес (для contrast)
        self.wallet = 0.0               # Накопления (Knowledge Economy)
        # Ценности: случайные в [0.2, 0.8], нормализованы до суммы 1
        self.values = np.random.uniform(0.2, 0.8, cfg.n_vals)
        self.values /= self.values.sum()
        # Идентичность: журнал ключевых событий жизни
        self.identity: deque = deque(maxlen=cfg.id_mem)
        self.identity.append(("born", 0, "explorer"))
        # Цели
        self.goal: Optional[np.ndarray] = None
        self.goal_type = "explore"
        self.commitment = 0.0
        self.goal_age = 0
        self.goal_stack: List[Tuple] = []  # Стопка целей (С1 К-слой)

        # ───── СЛОЙ 6: Контекст + концепты ─────
        self.think_budget = cfg.max_think
        self.risk = cfg.risk_base
        self.context = np.zeros(cfg.n_ctx)
        self.mem_sig: deque = deque(maxlen=50)  # Signal memory
        self.concepts = np.zeros(cfg.max_concepts)  # Концепт-вектор
        # Абстракции — именованные состояния окружения
        self.abstractions = {
            "resource_zone": 0.0,
            "danger_zone": 0.0,
            "crowd": 0.0,
            "frontier": 0.0
        }

        # ───── СЛОЙ 7: Критик + решения ─────
        self.critic = 0.5
        self.decisions: deque = deque(maxlen=20)

        # Статистики
        self.traces_made = 0
        self.abductions = 0
        self.contrasts = 0

        # ───── СЛОЙ 8: Стиль + идеи + beliefs (Механизм 14) ─────
        self.cognitive_style = np.random.choice(cfg.cog_styles)
        # Beliefs: 6 категорий (обобщённые, не trace_id — от v3.0)
        self.beliefs = np.random.uniform(0.3, 0.7, cfg.belief_categories)
        self.ideas_generated = 0
        self.pending_interpretations: List[Idea] = []
        # Belief buffer для threshold-based update (Haiku Layer 1)
        self._belief_buffer: Dict[int, List[float]] = {}
        # Goal history для regret tracking (Haiku Layer 3)
        self._goal_history: Dict[str, List[float]] = {}

        # ───── СЛОЙ 9: Планировщик (Механизм 15, v3.1 НОВОЕ) ─────
        # AStarPlanner инстанцируется на агенте; метрики копятся индивидуально
        self.planner: Optional[AStarPlanner] = AStarPlanner(cfg) if cfg.plan_enabled else None
        self.planned_path: List[np.ndarray] = []      # Текущий план (waypoints)
        self.current_waypoint_idx = 0                   # Индекс текущего waypoint
        self.last_horizon = 0                           # Максимальная глубина поиска
        self.plan_wins = 0                              # Успешных достижений цели
        self.plan_fails = 0                             # Неудачных планов
        self.plan_abandons = 0                          # Сколько раз бросали план
        self.horizons_history: deque = deque(maxlen=50) # История горизонтов (для mean_horizon)

    # ───────────────────────────────────────────────────────────────────────────
    #  Свойство: актуальная размерность агента
    # ───────────────────────────────────────────────────────────────────────────

    @property
    def dims(self) -> int:
        """Размерность агента = длина его position."""
        return len(self.position)

    # ───────────────────────────────────────────────────────────────────────────
    #  Cognitive cost: "думать дорого" (GPT С4)
    # ───────────────────────────────────────────────────────────────────────────

    def _think(self) -> bool:
        """
        Списываем один think_budget и energy.
        Возвращает False если бюджет исчерпан → агент не может думать в этом шаге.

        Это моделирует когнитивную экономику:
          • think_budget ограничен (max_think за шаг)
          • каждый think стоит think_cost энергии
          • Истощённый агент "тупит" — принимает реактивные решения
        """
        if self.think_budget <= 0:
            return False
        self.think_budget -= 1
        self.energy -= self.cfg.think_cost
        return True

    # ───────────────────────────────────────────────────────────────────────────
    #  Оценка контекста (С7 субъективность)
    # ───────────────────────────────────────────────────────────────────────────

    def assess_context(self, nb: List['Agent'], rg: float) -> None:
        """
        Оцениваем окружение по 4 измерениям:
          [0] resource_zone  — насколько богат ресурсами
          [1] crowd          — насколько плотно соседей
          [2] post_catastrophe — только что пережил ли катастрофу
          [3] frontier       — насколько "пусто" (не богато и не людно)

        Результат сохраняется в self.context и обновляет self.abstractions
        (с инерцией 0.8 — плавное изменение представлений о среде).
        """
        c = np.zeros(self.cfg.n_ctx)
        c[0] = min(1, rg * 10)                      # resource_zone
        c[1] = min(1, len(nb) * 0.15)               # crowd
        c[2] = min(1, self.cat_boost - 1)           # post_catastrophe
        c[3] = max(0, 1 - c[0] - c[1] * 0.5)        # frontier (инверсия)
        self.context = np.clip(c, 0, 1)
        # Обновление абстракций (плавное — инерция 0.8)
        self.abstractions["resource_zone"] = (
            0.8 * self.abstractions["resource_zone"] + 0.2 * c[0]
        )
        self.abstractions["danger_zone"] = (
            0.8 * self.abstractions["danger_zone"] + 0.2 * c[2]
        )
        self.abstractions["crowd"] = (
            0.8 * self.abstractions["crowd"] + 0.2 * c[1]
        )
        self.abstractions["frontier"] = (
            0.8 * self.abstractions["frontier"] + 0.2 * c[3]
        )

    # ───────────────────────────────────────────────────────────────────────────
    #  Концепты — "смысловое сжатие" из трейсов (С9)
    # ───────────────────────────────────────────────────────────────────────────

    def update_concepts(self, trace: TorqueTrace) -> None:
        """
        Обновляем концепт-вектор по trace.meaning.
        Концепт — агрегированное "смысловое направление" из всех трейсов, с которыми сталкивался.
        """
        if trace.meaning < len(self.concepts):
            self.concepts[trace.meaning] = min(1, self.concepts[trace.meaning] + 0.1)
        self.mem_sig.append(trace.value * (1 + trace.ai * 0.1))

    # ───────────────────────────────────────────────────────────────────────────
    #  Обновление ценностей (С1 субъективность)
    # ───────────────────────────────────────────────────────────────────────────

    def update_values(self, cr: float, sr: float, rg: float, cx: float) -> None:
        """
        Ценности меняются ОЧЕНЬ МЕДЛЕННО (inertia 0.95) на основе опыта.

        Feedback vector:
          [0] exploration = curiosity reward * 2
          [1] safety      = ресурсы + (1 если голоден)
          [2] social      = награда от взаимодействия * 3
          [3] complexity  = AI трейса * 0.5
        """
        fb = np.array([
            cr * 2,
            rg + (1 if self.energy < 0.5 else 0),
            sr * 3,
            cx * 0.5
        ])[:self.cfg.n_vals]
        self.values = (self.cfg.val_inert * self.values +
                       self.cfg.val_lr * np.clip(fb, -1, 1))
        # Clip + нормализация
        self.values = np.clip(self.values, 0.01, 1)
        self.values /= self.values.sum()

    # ───────────────────────────────────────────────────────────────────────────
    #  Механизм 14: Интерпретация trace → Idea
    # ───────────────────────────────────────────────────────────────────────────

    def interpret_trace(self, trace: TorqueTrace) -> Optional[Idea]:
        """
        Каждый стиль видит в трейсе разное. Не dict — а полноценная Idea.

        Логика скоринга по стилям:
          • analytical  — score = val * (1 + ai*0.15) * sm.conf
                          (дорожит сложностью, взвешивает своей уверенностью)
          • intuitive   — score = val * (0.5 + random)
                          (добавляет случайный компонент — "нутром чую")
          • skeptical   — score = val * max(0.3, 1 - mean(uncertainty))
                          (уменьшает если неуверен в пространстве)
          • exploratory — score = val * (1 + log1p(ai) * 0.2)
                          (ценит новизну логарифмически)
          • synthetic   — score = val * (1 + len(subs) * 0.3)
                          (ценит композицию, рекурсивную сборку)
        """
        # Нет бюджета на думку — не генерируем идею
        if not self._think():
            return None

        st = self.cognitive_style
        val = trace.value
        ai = trace.ai

        if st == "analytical":
            score = val * (1 + ai * 0.15) * self.sm.conf()
        elif st == "intuitive":
            score = val * (0.5 + np.random.random())
        elif st == "skeptical":
            score = val * max(0.3, 1 - self.uncertainty[:self.dims].mean())
        elif st == "exploratory":
            score = val * (1 + np.log1p(ai) * 0.2)
        elif st == "synthetic":
            score = val * (1 + len(trace.subs) * 0.3)
        else:
            score = val  # fallback

        # Категория belief, которую обновляет эта идея
        cat = trace.meaning % self.cfg.belief_categories

        # Создаём Idea и кладём в pending (обработается в Env.step)
        idea = Idea(self.id, ai, st, score, cat, self.age)
        self.ideas_generated += 1
        self.pending_interpretations.append(idea)
        return idea

    # ───────────────────────────────────────────────────────────────────────────
    #  Механизм 14: Обновление beliefs с паттерн-порогом (Haiku Layer 1)
    # ───────────────────────────────────────────────────────────────────────────

    def update_beliefs(self, idea: Idea) -> None:
        """
        Beliefs обновляются ТОЛЬКО если накоплен паттерн (3+ идей в категории).

        Haiku fix: одиночная идея не может перевернуть belief.
          • Накапливаем confidence идей в buffer
          • При 3+ идеях — усредняем и обновляем belief
          • Learning rate зависит от стиля:
              - skeptical — x0.5 (медленнее верит)
              - intuitive — x1.5 (быстрее верит)

        Ссылка: Aronson et al. (1963) — beliefs require repeated reinforcement.
        Ссылка: Kahneman (2011) "Thinking, Fast and Slow" — system 1 vs 2.
        """
        # Если ablation выключил beliefs, выходим
        if self.cfg.ablate_beliefs:
            return

        cat = idea.category % len(self.beliefs)
        # Накапливаем по категориям
        self._belief_buffer.setdefault(cat, []).append(idea.confidence)
        # Обновить только если 3+ идей
        if len(self._belief_buffer[cat]) >= 3:
            avg = np.mean(self._belief_buffer[cat])
            lr = self.cfg.belief_lr
            # Стилевая модуляция
            if self.cognitive_style == "skeptical":
                lr *= 0.5
            elif self.cognitive_style == "intuitive":
                lr *= 1.5
            # Exponential moving average
            self.beliefs[cat] = (1 - lr) * self.beliefs[cat] + lr * np.clip(avg, 0, 1)
            # Сброс буфера
            self._belief_buffer[cat] = []


    # ───────────────────────────────────────────────────────────────────────────
    #  Выбор цели с goal tension + regret (Mech 14 + Haiku Layer 3)
    # ───────────────────────────────────────────────────────────────────────────

    def choose_goal(self, nb: List['Agent']) -> None:
        """
        Выбор цели с учётом:
          1. Commitment — если ещё держим предыдущую цель, пропускаем
          2. Regret tracking — если этот тип цели раньше вредил, penalize value
          3. Goal tension — ценности конкурируют, сильнейший "тянет"
          4. Beliefs модулируют ценности
          5. ToM — учитываем сигналы соседей (food direction, danger direction)

        Цели:
          • explore   — случайная точка в пространстве (с bonus за frontier)
          • safe      — к центру; если есть danger signal — в противоположную сторону
          • social/social_food — к соседу или по food signal
          • complex   — в самое неопределённое измерение
        """

        # ═══ КРОК 1: Проверка commitment ═══
        # Если мы ещё держим предыдущую цель (commitment > 0.3) и не устарела
        # (goal_age < goal_dur) — не выбираем новую, только ослабляем commitment.
        if self.commitment > 0.3 and self.goal_age < self.cfg.goal_dur:
            self.goal_age += 1
            self.commitment *= self.cfg.commit_d  # Декей commitment
            return

        # ═══ КРОК 2: Regret tracking (Haiku Layer 3) ═══
        # Оценка прошлой цели: если она 3+ раз давала плохой результат —
        # снижаем соответствующую ценность.
        if self.goal_type and self.goal_age > 0:
            gt = self.goal_type
            # Оцениваем результат цели через изменение энергии
            energy_change = self.energy - self.prev_fit
            self._goal_history.setdefault(gt, []).append(energy_change)
            history = self._goal_history[gt]

            # Требуем минимум 3 попытки перед судом
            if len(history) >= 3:
                avg = np.mean(history[-5:])  # Скользящее окно последних 5
                if avg < 0:  # В среднем цель вредна → penalize
                    val_map = {
                        "explore": 0,
                        "safe": 1,
                        "social": 2, "social_food": 2,
                        "complex": 3
                    }
                    vi = val_map.get(gt, 0)
                    if vi < len(self.values):
                        self.values[vi] *= 0.85  # -15% (regret theory)
                        self.values = np.clip(self.values, 0.01, 1)
                        self.values /= self.values.sum()
                        self.identity.append(("regret", self.age, gt))
                        # Ссылка: Loomes & Sugden (1982) "Regret Theory"

        # ═══ КРОК 3: Проверка бюджета на думку ═══
        if not self._think():
            return

        d = self.dims

        # ═══ КРОК 4: Goal tension — ценности КОНКУРИРУЮТ ═══
        # Каждая ценность "тянет" в свою сторону с силой = value * belief
        tensions = self.values.copy()

        # Beliefs модулируют ценности
        if len(self.beliefs) >= 4:
            # change_is_good (4) → exploration (0)
            if len(self.beliefs) > 4:
                tensions[0] *= (1 + self.beliefs[4] * 0.5)
            # danger_nearby (3) → safety (1)
            if len(self.beliefs) > 3 and len(tensions) > 1:
                tensions[1] *= (1 + self.beliefs[3] * 0.5)
            # social_helps (2) → social (2)
            if len(tensions) > 2:
                tensions[2] *= (1 + self.beliefs[2] * 0.5)
            # complexity_pays (1) → complex (3)
            if len(tensions) > 3:
                tensions[3] *= (1 + self.beliefs[1] * 0.5)

        # ═══ КРОК 5: Конфликт — трудный выбор стоит дороже ═══
        # Если разница между двумя сильнейшими ценностями мала → решение сложное
        sorted_t = np.sort(tensions)[::-1]
        conflict = sorted_t[0] - sorted_t[1] if len(sorted_t) > 1 else 1.0

        if conflict < 0.1:
            # Трудный выбор — тратим дополнительную энергию
            self.energy -= self.cfg.think_cost * 2
            self.identity.append(("hard_choice", self.age, float(conflict)))

        # Доминирующая ценность определяет тип цели
        dom = int(np.argmax(tensions))

        # ═══ КРОК 6: Theory of Mind — учёт сигналов соседей ═══
        food_dir = None
        danger_dir = None
        for nid, info in self.tom.items():
            if info.get("signal") == 0 and info.get("pos") is not None:
                food_dir = info["pos"]
            elif info.get("signal") == 1 and info.get("vel") is not None:
                danger_dir = info["vel"]

        # ═══ КРОК 7: Выбор цели по доминирующей ценности ═══
        if dom == 0:
            # Exploration — случайная точка
            t = self.position + np.random.normal(0, 3, d)
            # Если frontier — удваиваем радиус
            if self.abstractions["frontier"] > 0.5:
                t *= 1.5
            self.goal = t
            self.goal_type = "explore"
        elif dom == 1:
            # Safety — к центру (или прочь от danger)
            self.goal = np.zeros(d)
            self.goal_type = "safe"
            if danger_dir is not None:
                gd = min(d, len(danger_dir))
                self.goal[:gd] -= danger_dir[:gd] * 2
        elif dom == 2:
            # Social — к еде/соседу
            if food_dir is not None:
                gd = min(d, len(food_dir))
                self.goal = np.zeros(d)
                self.goal[:gd] = food_dir[:gd]
                self.goal_type = "social_food"
            elif nb:
                t = nb[0]
                md = min(d, t.dims)
                self.goal = np.zeros(d)
                self.goal[:md] = t.position[:md]
                self.goal_type = "social"
            else:
                # Нет соседей — fallback на explore
                self.goal = self.position + np.random.normal(0, 1, d)
                self.goal_type = "explore"
        elif dom == 3:
            # Complexity — в самое неопределённое измерение
            w = int(np.argmax(self.uncertainty[:d]))
            dr = np.zeros(d)
            dr[w] = np.random.choice([-3, 3])
            self.goal = self.position + dr
            self.goal_type = "complex"

        # Зафиксировать новую цель
        self.commitment = self.cfg.commit_s
        self.goal_age = 0
        # Добавить в goal stack (К1 — К-слой когнитивный)
        if self.goal is not None:
            self.goal_stack.append(
                (self.goal_type, self.goal.copy(), self.commitment)
            )
            if len(self.goal_stack) > 3:
                self.goal_stack = self.goal_stack[-3:]
        self.identity.append(("goal", self.age, self.goal_type))

        # ═══ КРОК 8: Планирование A* (Mech 15, v3.1 НОВОЕ) ═══
        # После выбора цели — пытаемся построить путь к ней.
        # Это отделённый метод, чтобы его можно было тестировать и отключать.
        if self.cfg.plan_enabled and self.planner is not None and self.goal is not None:
            self.plan_path(nb)

    # ───────────────────────────────────────────────────────────────────────────
    #  A* планирование пути (Механизм 15 — НОВОЕ в v3.1)
    # ───────────────────────────────────────────────────────────────────────────

    def plan_path(self, neighbors: List['Agent']) -> None:
        """
        Построение пути к текущей цели через A* планировщик.

        ФИКСИРОВАННЫЕ БАГИ из первой версии:
          1. Горизонт зависит от ЭНЕРГИИ агента, а не от думок.
             Логика: голодный агент близорук (не может планировать далеко).
             Сытый — может позволить себе глубокий поиск.

          2. plan_wins считается только при РЕАЛЬНОМ достижении цели.
             Раньше считалась дельта fitness — это был некорректный прокси.

          3. last_horizon = max_depth_seen (глубина поиска),
             а не длина найденного пути.
             Важно: глубина поиска может быть БОЛЬШЕ чем длина пути
             (A* рассматривает много узлов, возвращает самый короткий).

          4. max_expansions = horizon × 5 (не ×2 как было).
             В многомерных пространствах нужно больше расширений,
             иначе A* не успевает найти путь.
        """
        if self.goal is None or self.planner is None:
            return

        # ═══ ГОРИЗОНТ ОТ ЭНЕРГИИ ═══
        # Энергия 0.0 → горизонт = 2 (близорукий голодный)
        # Энергия max_e → горизонт = plan_horizon_base * 1.5 (стратег)
        energy_fraction = max(0.0, min(1.0, self.energy / self.cfg.max_e))
        # Базовый горизонт scaling:
        # fraction=0   → h = 2
        # fraction=1   → h = plan_horizon_base * 1.5 = 15
        horizon = int(2 + energy_fraction * (self.cfg.plan_horizon_base * 1.5 - 2))
        horizon = max(2, min(horizon, self.cfg.plan_horizon_base * 2))
        self.horizons_history.append(horizon)

        # ═══ ПРЕПЯТСТВИЯ — позиции соседей ═══
        obstacles = [n.position.copy() for n in neighbors[:10]]

        # ═══ ЗАПУСК A* ═══
        # Свой RNG чтобы не влиять на глобальный seed (воспроизводимость)
        local_rng = np.random.RandomState()

        try:
            path, info = self.planner.plan(
                start=self.position.copy(),
                goal=self.goal.copy(),
                obstacles=obstacles,
                horizon=horizon,
                dims=self.dims,
                rng=local_rng
            )
        except Exception:
            # Fallback: планировщик упал — нет пути
            path = []
            info = {"reached_goal": False, "max_depth": 0}

        # ═══ ЗАПОМИНАЕМ ═══
        self.planned_path = path if path else []
        self.current_waypoint_idx = 1 if len(path) > 1 else 0
        # last_horizon = глубина поиска (НЕ длина пути)
        self.last_horizon = info.get("max_depth", 0)

        # Статистики: успешный план vs провал
        if info.get("reached_goal", False):
            self.plan_wins += 1
        else:
            self.plan_fails += 1

    # ───────────────────────────────────────────────────────────────────────────
    #  Следующий waypoint: возвращаем куда двигаться по плану
    # ───────────────────────────────────────────────────────────────────────────

    def next_waypoint(self) -> Optional[np.ndarray]:
        """
        Возвращает текущий waypoint из плана, если есть.
        Если агент близко к waypoint (< plan_waypoint_radius), переключаемся на следующий.
        Если waypoints кончились — возвращаем None.
        """
        if not self.planned_path or self.current_waypoint_idx >= len(self.planned_path):
            return None

        wp = self.planned_path[self.current_waypoint_idx]
        md = min(self.dims, len(wp))
        dist = np.linalg.norm(self.position[:md] - wp[:md])

        # Достигли — следующий
        if dist < self.cfg.plan_waypoint_radius:
            self.current_waypoint_idx += 1
            if self.current_waypoint_idx >= len(self.planned_path):
                # План исчерпан
                self.planned_path = []
                self.current_waypoint_idx = 0
                return None
            wp = self.planned_path[self.current_waypoint_idx]

        return wp

    # ───────────────────────────────────────────────────────────────────────────
    #  Вычисление движения — С ПЛАНИРОВЩИКОМ (v3.1) или без (v3.0 fallback)
    # ───────────────────────────────────────────────────────────────────────────

    def compute_movement(self, nb: List['Agent'], sp_center: np.ndarray) -> np.ndarray:
        """
        Вычисляем вектор движения агента за шаг.

        Компоненты (все суммируются):
          • velocity * 0.4   — инерция предыдущего шага
          • attr             — притяжение к центру species
          • noise            — случайный шум (больше если steps_ni > boredom)
          • repul            — репульсия от близких агентов
          • gp / waypoint_pull — притяжение к цели ИЛИ к waypoint'у A*  ← НОВОЕ v3.1
          • contrast         — контрастная коррекция (чужие провалы)
          • tom_pull         — сигналы от соседей (еда / опасность)
          • belief_pull      — beliefs влияют на движение направленно
          • risk_mv          — рисковый шум (если risk высокий)

        Всё × cat_boost × role_speed.

        v3.1 ИЗМЕНЕНИЕ: если есть активный план и next_waypoint существует,
        используем его вместо goal как цель притяжения. Это заставляет
        агента следовать по построенному пути, а не лететь напрямую в goal.
        """
        cfg = self.cfg
        d = self.dims
        speed = cfg.role_speed.get(self.role, 1.0)

        md = min(d, len(sp_center))
        # Притяжение к центру species (группа)
        attr = np.zeros(d)
        attr[:md] = (sp_center[:md] - self.position[:md]) * 0.03

        # Шум: базовый или "миграционный" при скуке
        if self.steps_ni > cfg.boredom:
            noise = np.random.normal(0, cfg.mig_noise, d)
            self.steps_ni = 0  # Сброс счётчика — "встряхнулся"
        else:
            noise = np.random.normal(0, 0.15, d)

        # Репульсия от соседей (избегание столкновений)
        repul = np.zeros(d)
        for n in nb[:15]:  # Не более 15 ближайших
            md2 = min(d, n.dims)
            diff = self.position[:md2] - n.position[:md2]
            dist = np.linalg.norm(diff)
            if 0 < dist < cfg.repul_r:
                repul[:md2] += cfg.repul_s * diff / (dist + 1e-8)

        # ═══ ПРИТЯЖЕНИЕ К ЦЕЛИ ИЛИ К WAYPOINT'У ═══
        # В v3.1: если планировщик активен и есть waypoint — идём к нему.
        # Иначе — классика v3.0: прямо к goal.
        gp = np.zeros(d)
        waypoint = None
        if cfg.plan_enabled and self.planned_path:
            waypoint = self.next_waypoint()

        if waypoint is not None and self.commitment > 0.1:
            # v3.1: идём к ближайшему waypoint с повышенной силой
            gd = min(d, len(waypoint))
            gp[:gd] = (waypoint[:gd] - self.position[:gd]) * 0.08 * self.commitment
        elif self.goal is not None and self.commitment > 0.1:
            # v3.0 fallback: прямо к цели
            gd = min(d, len(self.goal))
            gp[:gd] = (self.goal[:gd] - self.position[:gd]) * 0.05 * self.commitment

        # Контрастная коррекция — прочь от векторов провала других
        contrast = np.zeros(d)
        if self.contrast_mem:
            for ad in self.contrast_mem:
                cd = min(d, len(ad))
                contrast[:cd] -= ad[:cd]
            contrast *= cfg.contr_s / len(self.contrast_mem)

        # ToM pull — по сигналам других
        tom_pull = np.zeros(d)
        for nid, info in self.tom.items():
            if info.get("signal") == 0 and info.get("pos") is not None:
                # Food signal — тянемся к источнику
                fp = info["pos"]
                md3 = min(d, len(fp))
                tom_pull[:md3] += (fp[:md3] - self.position[:md3]) * 0.02
            elif info.get("signal") == 1 and info.get("vel") is not None:
                # Danger signal — уходим по вектору скорости убегающего
                dv = info["vel"]
                md3 = min(d, len(dv))
                tom_pull[:md3] -= dv[:md3] * 0.03

        # Belief pull — направленно, не шум (fix от v3.0 от Claude)
        # H1 test: при ablate_beliefs belief_pull отключён → проверяем
        # гипотезу "planner гомогенизирует через beliefs".
        belief_pull = np.zeros(d)
        if not self.cfg.ablate_beliefs:
            # "Пространство богатое" → двигаться шире
            if self.beliefs[0] > 0.6:
                belief_pull += np.random.normal(0, 0.3, d)
            # "Опасность рядом" → ближе к центру
            if len(self.beliefs) > 3 and self.beliefs[3] > 0.6:
                belief_pull[:min(d, 3)] -= self.position[:min(d, 3)] * 0.02

        # Risk move — случайный шум если рисковый
        risk_mv = np.zeros(d)
        if np.random.random() < self.risk and self._think():
            risk_mv = np.random.normal(0, 2, d) * self.risk

        # Velocity padding/truncation
        vel = self.velocity[:d] if len(self.velocity) >= d else \
            np.pad(self.velocity, (0, d - len(self.velocity)))

        # Итог: сумма всех компонент
        return (vel * 0.4 + attr + noise + repul + gp + contrast +
                tom_pull + belief_pull + risk_mv) * self.cat_boost * speed

    def move(self, nb: List['Agent'], sp_center: np.ndarray) -> None:
        """
        Выполняем шаг движения:
          1. Вычисляем дельту через compute_movement
          2. Применяем, clip на границы пространства
          3. Обновляем velocity (итоговая дельта)
          4. Сохраняем опыт (old, velocity, new) в exp_buf для WorldModel
          5. Обновляем causal graph
        """
        old = self.position.copy()
        self.position += self.compute_movement(nb, sp_center)
        self.position = np.clip(self.position, -self.cfg.space, self.cfg.space)
        self.velocity = self.position - old
        # Сохраняем в буфер опыта (для offline-обучения во сне)
        self.exp_buf.append((old, self.velocity, self.position.copy()))
        # Обновляем causal graph
        if self.last_st is not None:
            self.causal.observe(self.last_st, self.position)
        self.last_st = self.position.copy()


    # ───────────────────────────────────────────────────────────────────────────
    #  Любопытство (Artificial Curiosity, Schmidhuber 1991)
    # ───────────────────────────────────────────────────────────────────────────

    def curiosity_step(self) -> float:
        """
        Любопытство через ошибку предсказания:
          1. Агент предсказывает своё следующее положение
          2. Сравнивает с реальным → ошибка
          3. Ошибка ↓ со временем → предсказатель учится
          4. Улучшение предсказания = награда (внутренняя мотивация!)

        Обновляем также:
          • uncertainty — по каждому измерению
          • самомодель — если было улучшение, фиксируем "победу" в доминантном измерении
          • steps_ni — счётчик стагнации (для boredom-migration)
        """
        d = self.dims
        # Защита от неправильной размерности предиктора (после resize)
        if len(self.predictor) != d:
            self.predictor = np.pad(self.predictor,
                                    (0, max(0, d - len(self.predictor))))[:d]

        # Предсказание
        pred = self.position + self.predictor
        err = np.linalg.norm(self.position - pred)
        # Онлайн обновление предиктора (простой шаг SGD)
        self.predictor += 0.1 * (self.position - pred)

        # Обновляем uncertainty по каждому измерению
        per_dim = np.abs(self.position - pred)[:d]
        if len(self.uncertainty) < d:
            self.uncertainty = np.pad(self.uncertainty, (0, d - len(self.uncertainty)),
                                      constant_values=0.5)
        self.uncertainty[:d] = 0.9 * self.uncertainty[:d] + 0.1 * np.clip(per_dim, 0, 1)

        # Улучшение предсказания
        imp = self.last_pe - err
        self.last_pe = err
        if imp > 0.001:
            # Было улучшение — сбрасываем счётчик стагнации, фиксируем победу
            self.steps_ni = 0
            self.sm.update(int(np.argmax(per_dim)), True)
        else:
            # Нет улучшения — инкремент
            self.steps_ni += 1

        # Возвращаем награду (масштабированную)
        return imp * self.cfg.cur_scale

    # ───────────────────────────────────────────────────────────────────────────
    #  Контрастное обучение — "чужой провал корректирует мой вектор"
    # ───────────────────────────────────────────────────────────────────────────

    def contrast_learn(self) -> None:
        """
        Если мой fitness резко упал (> contr_trig) — сохраняю
        нормированный вектор движения (моей velocity) как "вектор провала".
        Потом в compute_movement этот вектор работает как отталкивающий
        (contrast pull в противоположную сторону).

        Это механизм от Илариона: "чужой провал корректирует мой вектор".
        Не учимся прямо — учимся ИЗБЕГАТЬ ошибок.
        """
        f = self.fitness()
        if self.prev_fit > 0:
            drop = (self.prev_fit - f) / (self.prev_fit + 1e-8)
            if drop > self.cfg.contr_trig:
                ad = self.velocity.copy()
                if np.linalg.norm(ad) > 1e-8:
                    # Нормируем и добавляем в память
                    self.contrast_mem.append(ad / np.linalg.norm(ad))
                    self.contrasts += 1
                    self.identity.append(("failure", self.age, float(drop)))
        self.prev_fit = f

    # ───────────────────────────────────────────────────────────────────────────
    #  Коммуникация через сигналы (Mech К2)
    # ───────────────────────────────────────────────────────────────────────────

    def emit_signal(self, rg: float) -> None:
        """
        Агент испускает сигнал в зависимости от состояния:
          0: FOOD     — нашёл ресурс (rg > 0.1)
          1: DANGER   — после контрастного обучения (есть failures)
          2: HELP     — голод (energy < 0.5)

        Сигнал = (type, position, velocity) — другие агенты могут его принять.
        """
        if rg > 0.1:
            self.signal = (0, self.position.copy(), self.velocity.copy())  # FOOD
        elif self.energy < 0.5:
            self.signal = (2, self.position.copy(), self.velocity.copy())  # HELP
        elif self.contrasts > 0 and self.age % 5 == 0:
            self.signal = (1, self.position.copy(), self.velocity.copy())  # DANGER
        else:
            self.signal = None

    def receive_signal(self, sender: 'Agent') -> None:
        """
        Принимаем сигнал от соседа. Сохраняем в tom (Theory of Mind).
        Ограничение размера tom_mem — забываем старые.
        """
        if sender.signal is None:
            return
        st, pos, vel = sender.signal
        self.tom[sender.id] = {
            "role": sender.role,
            "signal": st,
            "energy": sender.energy,
            "pos": pos.copy(),
            "vel": vel.copy()
        }
        # Ограничение размера
        if len(self.tom) > self.cfg.tom_mem:
            del self.tom[min(self.tom.keys())]

    # ───────────────────────────────────────────────────────────────────────────
    #  Самокритика (Mech К4)
    # ───────────────────────────────────────────────────────────────────────────

    def self_critique(self) -> None:
        """
        Периодическая самооценка: смотрю на последние решения,
        усредняю результаты. Если плохо — значит надо быть активнее
        (увеличиваю exploration value).
        """
        if not self._think() or len(self.decisions) < 3:
            return
        avg = np.mean([r for _, r in list(self.decisions)[-5:]])
        self.critic = 0.8 * self.critic + 0.2 * np.clip(avg, 0, 1)
        if self.critic < 0.3:
            # Плохая самооценка → больше exploration
            self.values[0] *= 1.2
            self.values /= self.values.sum()
            self.identity.append(("self_critique_low", self.age, float(self.critic)))

    # ───────────────────────────────────────────────────────────────────────────
    #  Стратегическое забывание (С8 субъективность)
    # ───────────────────────────────────────────────────────────────────────────

    def strategic_forget(self) -> None:
        """
        Активное забывание:
          • Если буфер опыта переполнен > 80% — обрезаем до 60%
          • Концепты декеем × 0.95 (слабые "забываются")

        Это важно чтобы агент не тащил бесконечную историю и мог адаптироваться.
        """
        if len(self.mem_sig) < 10:
            return
        if len(self.exp_buf) > int(self.cfg.exp_buf * 0.8):
            while len(self.exp_buf) > int(self.cfg.exp_buf * 0.6):
                self.exp_buf.popleft()
        self.concepts *= 0.95

    # ───────────────────────────────────────────────────────────────────────────
    #  Морфогенез (Levin-style дифференциация роли)
    # ───────────────────────────────────────────────────────────────────────────

    def receive_signals_morph(self, nb: List['Agent']) -> None:
        """
        Принимаем "сигналы" о ролях соседей. Это не social signals —
        это пассивное считывание "кто тут кого".

        Результат: вектор role_sig = распределение ролей в окружении.
        """
        if not nb:
            return
        sig = np.zeros(5)
        for n in nb:
            sig[self.ROLES.index(n.role) if n.role in self.ROLES else 0] += 1
        if sig.sum() > 0:
            sig /= sig.sum()
        # Плавное обновление с инерцией 0.7
        self.role_sig = 0.7 * self.role_sig + 0.3 * sig

    def differentiate(self) -> None:
        """
        Дифференциация роли — ключевой механизм Levin-морфогенеза.

        Логика:
          • С вероятностью role_plast (плавно падает с возрастом) — думаем о смене
          • Считаем "дефицит" ролей в окружении (1 - role_sig)
          • Оцениваем свою пригодность к каждой роли (suit)
          • Выбираем роль с макс. дефицитом × пригодностью

        Это значит: роль определяется КОНТЕКСТОМ, а не генами.
        Ксеноботы Левина — клетки становятся "сердцем" или "кожей"
        в зависимости от соседей, а не ДНК.
        """
        # Вероятность смены падает с возрастом (стабилизация к зрелости)
        if np.random.random() > self.cfg.role_plast * max(0.2, 1 - self.age / 200):
            return
        if self.role_sig.sum() > 0:
            deficit = 1.0 - self.role_sig
            # Пригодность по ролям (эвристика)
            suit = np.array([
                np.mean(self.sm.c),              # explorer: общая confidence
                max(self.sm.c) if len(self.sm.c) > 0 else 0,  # builder: max
                self.sm.conf(),                  # researcher: win rate
                1 - self.sm.conf(),              # architect: lose rate (упорный)
                self.survived * 0.3              # guardian: пережил катастрофы
            ])
            # Комбинированный выбор
            combined = deficit * (0.5 + 0.5 * suit[:len(deficit)])
            nr = self.ROLES[int(np.argmax(combined))]
            if nr != self.role:
                self.identity.append(("role", self.age, nr))
                self.role = nr

    # ───────────────────────────────────────────────────────────────────────────
    #  Interference (волновая совместимость) — NEAT + волновая метафора
    # ───────────────────────────────────────────────────────────────────────────

    def interference(self, o: 'Agent') -> float:
        """
        Интерференция двух агентов — насколько они совместимы?
        Высокая → конструктивная (как волны в фазе)
        Низкая (отрицательная) → деструктивная (волны в противофазе)

        Компоненты:
          • Genome similarity (cosine) — 60% веса
          • Role matching — 40% (разные роли дополняют друг друга)
        """
        md = min(self.dims, o.dims)
        g1 = self.genome[:md]
        g2 = o.genome[:md]
        n1 = np.linalg.norm(g1)
        n2 = np.linalg.norm(g2)
        # Cosine similarity с защитой от 0
        gs = float(np.dot(g1, g2) / (n1 * n2 + 1e-8)) if n1 > 1e-8 and n2 > 1e-8 else 0
        # Бонус за разные роли
        role_bonus = 0.5 if self.role != o.role else 0
        return np.clip(gs * 0.6 + role_bonus * 0.4, -1, 1)

    # ───────────────────────────────────────────────────────────────────────────
    #  Создание и поглощение трейсов
    # ───────────────────────────────────────────────────────────────────────────

    def create_trace(self, o: 'Agent', step: int) -> TorqueTrace:
        """
        Создаём трейс при встрече с агентом o.
        Embedding — среднее геномов, value — от интерференции.
        """
        md = min(self.dims, o.dims)
        emb = (self.genome[:md] + o.genome[:md]) / 2
        # Value зависит от интерференции: позитивная → сильный трейс
        return TorqueTrace(
            pos=(self.position[:md] + o.position[:md]) / 2,
            emb=emb,
            val=max(0.1, np.linalg.norm(emb) * (1 + self.interference(o))),
            pids=(self.id, o.id),
            step=step
        )

    def absorb_trace(self, trace: TorqueTrace) -> None:
        """
        Поглощение трейса:
          1. Геном "сдвигается" в направлении embedding (скорость 0.03)
          2. Energy += 0.01 * value (небольшая награда)
          3. Trace confirm с bonus
          4. Обновление концептов
          5. Если это tombstone — наследуем ценности умершего (cultural inherit)
          6. Интерпретация через когнитивный стиль → Idea
        """
        md = min(self.dims, len(trace.embedding))
        # Смещение генома (медленная эволюция через опыт)
        self.genome[:md] += trace.embedding[:md] * trace.value * 0.03
        self.genome = np.clip(self.genome, -10, 10)
        self.energy += 0.01 * trace.value
        # Подтверждаем trace
        trace.confirm(self.id, trace.value * 0.1)
        self.update_concepts(trace)
        # Tombstone inheritance (культура)
        if trace.tombstone is not None:
            tv = trace.tombstone.get("values")
            if tv is not None and len(tv) == len(self.values):
                # 10% от ценностей умершего → "культурное наследие"
                self.values = 0.9 * self.values + 0.1 * np.array(tv)
                self.values /= self.values.sum()
        # Мех.14: интерпретация через стиль
        self.interpret_trace(trace)
        self.traces_made += 1

    # ───────────────────────────────────────────────────────────────────────────
    #  Репродукция
    # ───────────────────────────────────────────────────────────────────────────

    def maybe_reproduce(self, partner: Optional['Agent'] = None) -> Optional['Agent']:
        """
        Попытка размножения. Условие: energy > repro_thresh.

        Если есть partner — crossover (случайный mask по измерениям).
        Если нет — мутация себя с мутацией.

        Ребёнок наследует:
          • Геном (clip + gaussian mutation)
          • Ценности (с шумом 0.1)
          • Когнитивный стиль (20% шанс мутации → случайный стиль)
          • Beliefs (с шумом 0.1)

        Родитель теряет 50% энергии (цена воспроизводства).
        """
        if self.energy < self.cfg.repro_thresh:
            return None

        d = self.dims
        # Максимум размерностей (мы + партнёр)
        cd = max(d, partner.dims if partner else d)
        # Создаём ребёнка рядом с нами
        child = Agent(self.cfg, self.position + np.random.normal(0, 0.5, d))
        # Если партнёр в более высокой размерности, растим ребёнка
        if cd > child.dims:
            child.resize(cd)

        cg = np.zeros(child.dims)
        if partner:
            # Crossover через случайную маску
            md = min(self.dims, partner.dims, child.dims)
            mask = np.random.random(md) > 0.5
            cg[:md] = np.where(mask, self.genome[:md], partner.genome[:md])
        else:
            # Только от себя (асексуальное размножение)
            md = min(self.dims, child.dims)
            cg[:md] = self.genome[:md]

        # Мутация с гауссовым шумом
        child.genome = np.clip(cg + np.random.normal(0, self.mut_rate, child.dims), -10, 10)
        # Наследование ценностей с шумом
        child.values = np.clip(
            self.values + np.random.normal(0, 0.1, len(self.values)),
            0.01, 1
        )
        child.values /= child.values.sum()

        # Когнитивный стиль: 20% мутация, 80% наследование
        if np.random.random() < 0.2:
            child.cognitive_style = np.random.choice(self.cfg.cog_styles)
        else:
            child.cognitive_style = self.cognitive_style

        # Beliefs наследуются с шумом
        child.beliefs = np.clip(
            self.beliefs + np.random.normal(0, 0.1, len(self.beliefs)),
            0.01, 1
        )

        # Цена репродукции: родитель теряет половину энергии
        self.energy *= 0.5
        child.energy = self.cfg.init_e
        self.identity.append(("child", self.age, child.id))
        return child

    # ───────────────────────────────────────────────────────────────────────────
    #  Абдукция (Peirce, Fauconnier & Turner)
    # ───────────────────────────────────────────────────────────────────────────

    def attempt_abduction(self, trace: TorqueTrace) -> Optional[int]:
        """
        Абдукция — дальняя ассоциация, которая может создать новое измерение.

        Условия:
          1. Trace далеко от нас (> abd_d)
          2. Направления (gnorm, tnorm) схожи (|cosine| > dim_th)
          3. Наша размерность < max_dims

        Если всё есть — добавляем новое измерение пространства!
        Награда: energy += trace.value * abd_rw (большая)

        Это ключевой механизм OEE — пространство РАСТЁТ от прозрений агентов.
        Ссылка: Peirce (1883) "On the Algebra of Logic";
                Fauconnier & Turner "Conceptual Blending".
        """
        md = min(self.dims, len(trace.embedding))
        # Условие 1: далеко
        if np.linalg.norm(self.genome[:md] - trace.embedding[:md]) < self.cfg.abd_d:
            return None

        # Нормализуем векторы
        ns = self.genome[:md] / (np.linalg.norm(self.genome[:md]) + 1e-8)
        nt = trace.embedding[:md] / (np.linalg.norm(trace.embedding[:md]) + 1e-8)

        # Условие 2: направления схожи
        if abs(float(np.dot(ns, nt))) > self.cfg.dim_th:
            self.abductions += 1
            self.energy += trace.value * self.cfg.abd_rw
            self.identity.append(("abduction", self.age, self.dims))
            # Если не упёрлись в max_dims — возвращаем текущую dims (будет прирощено)
            if self.dims < self.cfg.max_dims:
                return self.dims
        return None

    # ───────────────────────────────────────────────────────────────────────────
    #  Катастрофы (антихрупкость Taleb)
    # ───────────────────────────────────────────────────────────────────────────

    def survive_catastrophe(self, sev: float) -> None:
        """
        Агент пережил катастрофу силы sev (0..1):
          • Energy уменьшается (но меньше если уже переживал — survived)
          • Если выжил: survived++, mut_rate×3, cat_boost=1.5, risk+
          • Добавляется в identity как ключевое событие

        Это и есть антихрупкость — после стресса система СИЛЬНЕЕ.
        Принцип пальмы (Иларион): после шторма пальма устойчивее.
        """
        # Damage уменьшается с опытом (но не ниже 0)
        self.energy -= sev * (1 - min(1, self.survived * 0.2))
        if self.energy > 0:
            self.survived += 1
            self.mut_rate *= 3  # Резкий скачок мутаций
            self.cat_boost = 1.5  # Boost к движению на несколько шагов
            self.risk = min(0.5, self.risk * 1.5)  # Смелее
            self.identity.append(("survived", self.age, float(sev)))

    def create_tombstone(self) -> Dict:
        """
        При смерти агент оставляет "надгробие" — культурный слепок.
        Живые могут его поглотить и унаследовать часть ценностей/beliefs/стиля.

        Это от Gemini v3: tombstones передают культурное наследие.
        """
        return {
            "values": self.values.tolist(),
            "role": self.role,
            "age": self.age,
            "survived": self.survived,
            "style": self.cognitive_style,
            "beliefs": self.beliefs.tolist(),
            "risk": self.risk
        }


    # ───────────────────────────────────────────────────────────────────────────
    #  Шаговые операции: стоимость жизни, runtime style adaptation
    # ───────────────────────────────────────────────────────────────────────────

    def step_cost(self) -> None:
        """
        Конец шага:
          1. Существование стоит exist_cost энергии
          2. Clip на [−1, max_e]
          3. Возраст ++
          4. cat_boost декей × 0.95 (выгорает за ~15 шагов)
          5. think_budget сбрасывается на новый шаг
          6. pending_interpretations очищается (собраны в Env)
          7. КАЖДЫЕ 20 ШАГОВ — runtime style adaptation (Haiku Layer 4)
        """
        self.energy -= self.cfg.exist_cost
        self.energy = np.clip(self.energy, -1, self.cfg.max_e)
        self.age += 1
        self.cat_boost = max(1, self.cat_boost * 0.95)
        self.think_budget = self.cfg.max_think
        self.pending_interpretations = []

        # ═══ Haiku Layer 4: Runtime style adaptation ═══
        # Каждые 20 шагов проверяем: может пора сменить стиль?
        # Это плавная адаптация, а не жёсткий if/else.
        if (self.age % 20 == 0 and self.age > 0
            and not self.cfg.ablate_style_adapt):
            # Scores для каждого стиля (индекс в cog_styles)
            scores = np.zeros(5)  # analytical, intuitive, skeptical, exploratory, synthetic

            # Стресс → skeptical усиливается
            if self.energy < self.cfg.max_e * 0.3:
                scores[2] += 2
            # Успех → synthetic (интегрирует опыт)
            if self.energy > self.cfg.max_e * 0.6:
                scores[4] += 1.5
            # Неопределённость → exploratory
            if np.mean(self.uncertainty[:self.dims]) > 0.4:
                scores[3] += 1.5
            # Стагнация → analytical (нужно разобраться)
            if self.steps_ni > 10:
                scores[0] += 1.5
            # Спокойствие → intuitive (базовый уровень)
            scores[1] += 1

            # Шум — чтобы выбор не был детерминистическим
            scores += np.random.normal(0, 0.3, 5)
            new_style = self.cfg.cog_styles[int(np.argmax(scores))]
            if new_style != self.cognitive_style:
                old = self.cognitive_style
                self.cognitive_style = new_style
                self.identity.append(
                    ("style_adapt", self.age, f"{old}→{new_style}")
                )

    def is_dead(self) -> bool:
        """Мёртв если energy <= 0."""
        return self.energy <= 0

    def fitness(self) -> float:
        """
        Фитнес агента — мультикритериальная оценка.
        Входит:
          • energy (главное)
          • wallet × 0.5 (накопления)
          • traces_made × 0.1 (социальный вклад)
          • abductions × 2 (креативность — ЦЕННО)
          • survived × 0.5 (антихрупкость)
        """
        return (self.energy + self.wallet * 0.5 +
                self.traces_made * 0.1 + self.abductions * 2 +
                self.survived * 0.5)

    def resize(self, nd: int) -> None:
        """
        Расширяем агента до новой размерности nd.
        Новые измерения:
          • position, velocity, predictor — нулевые
          • genome — маленький гауссов шум
          • uncertainty — 0.5 (средняя неопределённость)

        Также расширяем внутренние системы (SelfModel, WorldModel).
        """
        if nd <= self.dims:
            return
        ex = nd - self.dims
        self.position = np.pad(self.position, (0, ex))
        self.velocity = np.pad(self.velocity, (0, ex))
        # Геном: шум, а не нули (чтобы новое измерение сразу было "рабочим")
        og = self.genome.copy()
        self.genome = np.pad(self.genome, (0, ex))
        self.genome[len(og):] = np.random.normal(0, 0.1, ex)
        self.predictor = np.pad(self.predictor, (0, ex))
        self.uncertainty = np.pad(self.uncertainty, (0, ex), constant_values=0.5)
        # Расширение внутренних систем
        self.sm.resize(nd)
        self.wm.resize(nd)


# ═══════════════════════════════════════════════════════════════════════════════
#                    SPECIES + SPECIES MANAGER (NEAT-style)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Виды — NEAT-style speciation: агенты с похожими геномами группируются.
# Это защищает инновации от прямой конкуренции с "установившимися" геномами.
#
# Каждый Species хранит:
#   • g — "репрезентант" (геном лучшего за всё время)
#   • m — список id членов
#   • best — лучший fitness за всё время
#   • stag — счётчик стагнации (шагов без улучшения лучшего)
#
# SpeciesMgr:
#   • assign — распределяет агентов по видам (Euclidean на геномах с compat threshold)
#   • get_center — центр вида для attraction в movement
#   • stagnant — список видов, которые надо расформировать (mutation boost)
#
# ───────────────────────────────────────────────────────────────────────────────

class Species:
    """Вид — группа агентов с похожими геномами."""

    _id = 0

    def __init__(self, r: Agent):
        """Создаём вид от агента-основателя."""
        Species._id += 1
        self.id = Species._id
        self.g = r.genome.copy()    # Репрезентант
        self.m = [r.id]             # Члены
        self.best = r.fitness()     # Лучший fitness
        self.stag = 0               # Стагнация

    def center(self, am: Dict[int, Agent]) -> np.ndarray:
        """
        Центр вида — средняя позиция членов.
        Используется для species attraction в движении.
        """
        ps = []
        md = 0
        for aid in self.m:
            if aid in am:
                ps.append(am[aid].position)
                md = max(md, len(am[aid].position))
        if not ps:
            return np.zeros_like(self.g)
        # Padding до макс. размерности и усреднение
        return np.mean([np.pad(p, (0, md - len(p))) for p in ps], axis=0)


class SpeciesMgr:
    """Менеджер видов — распределение и управление."""

    def __init__(self, c: Config):
        self.c = c
        self.sp: Dict[int, Species] = {}

    def assign(self, agents: List[Agent]) -> None:
        """
        Распределяем агентов по видам.

        Для каждого агента:
          1. Находим ближайший вид по геному (Euclidean)
          2. Если расстояние < compat → агент в этот вид
          3. Иначе — создаём новый вид

        После распределения:
          4. Обновляем репрезентантов (лучший агент вида)
          5. Обновляем stagnation counter
        """
        for a in agents:
            bs = None
            bd = 1e9
            # Ближайший вид
            for sid, sp in self.sp.items():
                ml = max(len(a.genome), len(sp.g))
                d = np.linalg.norm(
                    np.pad(a.genome, (0, ml - len(a.genome))) -
                    np.pad(sp.g, (0, ml - len(sp.g)))
                )
                if np.isfinite(d) and d < bd:
                    bd = d
                    bs = sid
            # Попадаем или создаём новый
            if bd < self.c.compat and bs is not None:
                a.species_id = bs
            else:
                sp = Species(a)
                self.sp[sp.id] = sp
                a.species_id = sp.id

        # Обновляем состав видов
        for sp in self.sp.values():
            sp.m = []
        am = {a.id: a for a in agents}
        for a in agents:
            if a.species_id in self.sp:
                self.sp[a.species_id].m.append(a.id)
        # Удаляем пустые виды
        for sid in [s2 for s2, sp in self.sp.items() if not sp.m]:
            del self.sp[sid]
        # Обновляем репрезентантов и stagnation
        for sp in self.sp.values():
            bf = -1e9
            ba = None
            for aid in sp.m:
                if aid in am and am[aid].fitness() > bf:
                    bf = am[aid].fitness()
                    ba = am[aid]
            if ba:
                sp.g = ba.genome.copy()
                if bf > sp.best:
                    sp.best = bf
                    sp.stag = 0
                else:
                    sp.stag += 1

    def get_center(self, sid: Optional[int], am: Dict[int, Agent]) -> np.ndarray:
        """Центр вида или общего облака (если sid=None)."""
        if sid in self.sp:
            return self.sp[sid].center(am)
        # Fallback: общий центр
        if am:
            md = max(len(a.position) for a in am.values())
            return np.mean([np.pad(a.position, (0, md - len(a.position)))
                            for a in am.values()], axis=0)
        return np.zeros(5)

    def stagnant(self) -> List[int]:
        """Виды со стагнацией > stag_lim — кандидаты на расформирование."""
        return [sid for sid, sp in self.sp.items() if sp.stag > self.c.stag_lim]

    def count(self) -> int:
        """Число активных видов."""
        return len(self.sp)


# ═══════════════════════════════════════════════════════════════════════════════
#                    ENV — главный цикл симуляции
# ═══════════════════════════════════════════════════════════════════════════════
#
# Env управляет всей симуляцией: агенты, трейсы, ресурсы, виды, идеи.
#
# step() выполняет полный тик:
#   1. Species assignment + SpatialHash refresh
#   2. Morphogenesis (role differentiation)
#   3. Perception + context assessment + goal choice + movement
#   4. Signal exchange
#   5. Contrast learning
#   6. Causal interventions
#   7. Pairwise interactions → traces + reproduction
#   8. Trace absorption → interpretations (pending ideas)
#   9. Collect pending ideas into system ideas pool
#  10. Abduction (может увеличить dims!)
#  11. Asexual reproduction для богатых агентов
#  12. Self-reflection (weakest dim training)
#  13. REM-sleep для world models
#  14. Self-critique + strategic forget
#  15. Mech 14: Synthesis + Debate + Idea evolution
#  16. Catastrophes (если cooldown == 0)
#  17. Death + tombstone creation
#  18. Trace composition (recursive assembly)
#  19. Trace decay + limit enforcement
#  20. Resource respawn
#  21. Stagnant species dissolution
#  22. Metrics computation
#
# ───────────────────────────────────────────────────────────────────────────────

class Env:
    """
    Главное окружение симуляции MAES v3.1.
    Управляет всеми агентами, трейсами, идеями, видами, ресурсами.
    """

    def __init__(self, cfg: Optional[Config] = None):
        """Инициализация: генерируем агентов, ресурсы, инфраструктуру."""
        self.cfg = cfg or Config()
        self.rng = np.random.RandomState(self.cfg.seed)

        # ═══ ВАЖНО: сброс счётчиков id для воспроизводимости ═══
        # Без этого прогоны с одинаковыми seed'ами будут давать разные id,
        # что ломает анализ конкретных агентов в разных прогонах.
        Agent._id = 0
        TorqueTrace._id = 0
        Species._id = 0
        Idea._id = 0

        self.dims = self.cfg.dims
        self.agents: List[Agent] = [Agent(self.cfg) for _ in range(self.cfg.n_agents)]
        self.traces: List[TorqueTrace] = []
        self.ideas: List[Idea] = []
        self.sp = SpeciesMgr(self.cfg)
        self.res = ResourceField(self.cfg)
        self.sh = SpatialHash()
        self.step_n = 0
        self.cat_cd = 0
        self.hist: List[Dict] = []

    # ───────────────────────────────────────────────────────────────────────────
    #  Вспомогательные методы
    # ───────────────────────────────────────────────────────────────────────────

    def _am(self) -> Dict[int, Agent]:
        """Словарь id → agent для быстрого lookup."""
        return {a.id: a for a in self.agents}

    def _sample(self, d: List, k: int) -> List:
        """Случайная выборка k элементов из d (без повторов)."""
        if len(d) <= k:
            return d
        return [d[i] for i in self.rng.choice(len(d), k, replace=False)]

    def _rh(self) -> None:
        """Refresh spatial hash: очистить и перевставить всех агентов."""
        self.sh.clear()
        for a in self.agents:
            self.sh.insert(a)

    def _nb(self, a: Agent, r: float) -> List[Agent]:
        """Соседи агента a в радиусе r."""
        return self.sh.query(a, r)

    # ───────────────────────────────────────────────────────────────────────────
    #  Мех.14 (1/3): Синтез идей
    # ───────────────────────────────────────────────────────────────────────────

    def _synthesize(self) -> None:
        """
        Synthesis: если в одной категории есть 2+ идей от разных стилей,
        создаётся новая "синтезированная" идея с бонусом за разнообразие.

        Это моделирует "collective insight" — когда разные точки зрения
        на одну тему приводят к новому пониманию.
        """
        # Ablation check
        if self.cfg.ablate_synthesis:
            return

        grouped: Dict[int, List[Idea]] = {}
        for idea in self.ideas[-100:]:
            if not idea.alive:
                continue
            grouped.setdefault(idea.category, []).append(idea)

        for cat, group in grouped.items():
            styles = set(i.style for i in group)
            if len(styles) >= self.cfg.synthesis_threshold:
                # Среднее score + бонус за разнообразие
                avg_score = np.mean([i.score for i in group])
                diversity_bonus = len(styles) * 0.2
                # Синтезированная идея (origin_agent=0 — "системная")
                synth = Idea(
                    origin_agent=0,
                    origin_trace_ai=max(i.origin_ai for i in group),
                    style="synthetic",
                    score=avg_score * (1 + diversity_bonus),
                    category=cat,
                    step=self.step_n
                )
                synth.supporters = [i.origin_agent for i in group]
                self.ideas.append(synth)

    # ───────────────────────────────────────────────────────────────────────────
    #  Мех.14 (2/3): Дебаты
    # ───────────────────────────────────────────────────────────────────────────

    def _debate(self) -> None:
        """
        Дебаты: последние 10 идей прогоняются через 3 раунда дебатов
        со случайно выбранными агентами. Каждый стиль критикует по-своему.

        Побочный эффект: дебатёр обновляет свои beliefs на основе идеи
        (если пороги belief pattern threshold достигнуты).
        """
        # Ablation
        if self.cfg.ablate_debates:
            return
        if not self.ideas:
            return

        recent = [i for i in self.ideas[-50:] if i.alive]
        debaters = self._sample(self.agents, min(10, len(self.agents)))

        # Последние 10 живых идей × 3 раунда
        for idea in recent[-10:]:
            for _ in range(self.cfg.debate_rounds):
                if not debaters:
                    break
                d = debaters[self.rng.randint(len(debaters))]
                idea.debate_with(d.cognitive_style, d.sm.conf())
                # Дебатёр обновляет beliefs
                d.update_beliefs(idea)

    # ───────────────────────────────────────────────────────────────────────────
    #  Мех.14 (3/3): Меметическая эволюция
    # ───────────────────────────────────────────────────────────────────────────

    def _evolve_ideas(self) -> None:
        """
        Эволюция идей:
          • Каждая идея декей на шаг (confidence × 0.99)
          • С вероятностью idea_mutation_rate → мутация
          • Слабые (confidence < 0.01) умирают
          • Если пул переполнен — сортируем по strength и режем
        """
        for idea in self.ideas:
            idea.decay()
            if self.rng.random() < self.cfg.idea_mutation_rate:
                idea.mutate()
        # Selection: отбор живых
        self.ideas = [i for i in self.ideas if i.alive]
        # Лимит пула — режем слабейших
        if len(self.ideas) > self.cfg.idea_max:
            self.ideas.sort(key=lambda i: i.strength, reverse=True)
            self.ideas = self.ideas[:self.cfg.idea_max]

    # ───────────────────────────────────────────────────────────────────────────
    #  Главный цикл симуляции: step()
    # ───────────────────────────────────────────────────────────────────────────

    def step(self) -> Dict:
        """
        Один тик симуляции. Возвращает metrics dict.

        Поэтапно описано в комментариях к Env выше.
        """
        cfg = self.cfg
        # Счётчики событий шага
        births = 0
        deaths = 0
        abd = 0           # Абдукций
        ndims = 0         # Прироста измерений
        cat = False       # Была ли катастрофа
        crw: List[float] = []  # Награды за любопытство

        am = self._am()

        # ═══ ШАГ 1: Species + SpatialHash ═══
        self.sp.assign(self.agents)
        self.sh.update_axes(self.agents, self.step_n)
        self._rh()

        # ═══ ШАГ 2: Морфогенез ═══
        for a in self.agents:
            nb = self._nb(a, cfg.morpho_r)
            a.receive_signals_morph(nb)
            a.differentiate()

        # ═══ ШАГ 3: Восприятие + goal + движение ═══
        # Здесь же включается A* planning — внутри choose_goal
        for a in self.agents:
            nb = self._nb(a, cfg.interact_r * 2)
            center = self.sp.get_center(a.species_id, am)
            # Сбор ресурсов (role-dependent)
            rg = self.res.harvest(a.position, cfg.role_harvest.get(a.role, 1.0))
            a.energy += rg
            # Контекст + цель + движение
            a.assess_context(nb, rg)
            a.choose_goal(nb)      # Внутри — A* планирование (v3.1)
            a.move(nb, center)      # Движение — учитывает waypoint если есть план
            # Любопытство
            cr = a.curiosity_step()
            crw.append(cr)
            a.energy += np.clip(cr, -0.1, 0.1)
            # Испуск сигнала
            a.emit_signal(rg)

        # ═══ ШАГ 4: Обмен сигналами ═══
        self._rh()
        for a in self.agents:
            for n in self._nb(a, 5.0)[:5]:
                a.receive_signal(n)

        # ═══ ШАГ 5: Контрастное обучение ═══
        for a in self.agents:
            a.contrast_learn()

        # ═══ ШАГ 6: Каузальные интервенции ═══
        for a in self.agents:
            if self.rng.random() < cfg.interv_p and a._think():
                dim = self.rng.randint(0, self.dims)
                for ed, pc in a.causal.intervene(dim, 1.0).items():
                    if ed < len(a.velocity):
                        # Если интервенция предсказала движение точно — sm +1
                        a.sm.update(ed, abs(pc - a.velocity[ed]) < 0.5)

        # ═══ ШАГ 7: Взаимодействия → трейсы + репродукция ═══
        new_tr: List[TorqueTrace] = []
        new_ag: List[Agent] = []
        pairs: set = set()
        for a in self.agents:
            for b in self._nb(a, cfg.interact_r)[:8]:
                # Не дублируем пару
                pk = (min(a.id, b.id), max(a.id, b.id))
                if pk in pairs:
                    continue
                pairs.add(pk)
                # Создаём trace
                t = a.create_trace(b, self.step_n)
                new_tr.append(t)
                # Интерференция — социальная награда
                interf = a.interference(b)
                sr = 0.0
                if interf > 0.2:
                    # Конструктивная
                    sr = interf * 0.04
                    a.energy += sr
                    b.energy += sr
                    # Попытка репродукции
                    if (births < cfg.max_births
                        and a.energy > cfg.repro_thresh
                        and b.energy > cfg.repro_thresh
                        and self.rng.random() < 0.3):
                        c = a.maybe_reproduce(partner=b)
                        if c:
                            new_ag.append(c)
                            births += 1
                elif interf < -0.2:
                    # Деструктивная интерференция — обе теряют
                    a.energy -= abs(interf) * 0.05
                    b.energy -= abs(interf) * 0.05
                # Обновляем ценности на основе опыта
                a.update_values(crw[-1] if crw else 0, sr, 0, t.ai * 0.01)
                a.decisions.append(("interact", sr))
        self.traces.extend(new_tr)

        # ═══ ШАГ 8: Поглощение трейсов ═══
        am = self._am()
        for a in self.agents:
            for t in self._sample(self.traces, cfg.tr_sample):
                md = min(a.dims, len(t.position))
                if np.linalg.norm(a.position[:md] - t.position[:md]) < cfg.interact_r:
                    a.absorb_trace(t)

        # ═══ ШАГ 9: Собираем pending interpretations → общий пул идей ═══
        # (обработаны ПОСЛЕ absorption — fix от v3.0)
        for a in self.agents:
            self.ideas.extend(a.pending_interpretations)
            a.pending_interpretations = []

        # ═══ ШАГ 10: Абдукция — может увеличить dims! ═══
        dim_added = False
        for a in self.agents:
            if dim_added:
                break
            if self.rng.random() < cfg.abd_p and a._think():
                far = [
                    t for t in self._sample(self.traces, 15)
                    if np.linalg.norm(
                        a.position[:min(a.dims, len(t.position))] -
                        t.position[:min(a.dims, len(t.position))]
                    ) > cfg.abd_d
                ]
                if far:
                    nd = a.attempt_abduction(max(far, key=lambda x: x.value))
                    if nd is not None and self.dims < cfg.max_dims:
                        # Расширяем пространство
                        self.dims += 1
                        for ag in self.agents:
                            ag.resize(self.dims)
                        for tr in self.traces:
                            if len(tr.position) < self.dims:
                                tr.position = np.pad(
                                    tr.position,
                                    (0, self.dims - len(tr.position))
                                )
                                tr.embedding = np.pad(
                                    tr.embedding,
                                    (0, self.dims - len(tr.embedding))
                                )
                        self.res.respawn(self.rng, self.dims)
                        ndims += 1
                        abd += 1
                        dim_added = True

        # ═══ ШАГ 11: Асексуальная репродукция для очень богатых ═══
        for a in self.agents:
            if births < cfg.max_births and a.energy > cfg.repro_thresh * 1.5:
                c = a.maybe_reproduce()
                if c:
                    new_ag.append(c)
                    births += 1

        # ═══ ШАГ 12: Self-reflection — тренируем слабое измерение ═══
        for a in self.agents:
            if self.rng.random() < 0.1 and a._think():
                w = a.sm.weakest()
                if w is not None and w < self.dims:
                    # "Двигаемся" в слабое измерение, чтобы набрать опыт
                    a.position[w] += self.rng.normal(0, 1)
                    a.position[w] = np.clip(a.position[w], -cfg.space, cfg.space)

        # ═══ ШАГ 13: REM-сон для world models (выборочный) ═══
        if self.step_n % cfg.sleep_int == 0:
            for a in self.agents:
                # Только если высокая ошибка — от Gemini, селективный сон
                if a.last_pe > 0.3:
                    a.wm.sleep(a.exp_buf)

        # ═══ ШАГ 14: Самокритика + стратегическое забывание ═══
        for a in self.agents:
            if a.age % cfg.critic_int == 0 and a.age > 0:
                a.self_critique()
            a.strategic_forget()

        # ═══ ШАГ 15: Мех.14 — Synthesis + Debate + Evolution ═══
        if self.step_n % 3 == 0:
            self._synthesize()
            self._debate()
        if self.step_n % 5 == 0:
            self._evolve_ideas()

        # ═══ ШАГ 16: Катастрофы ═══
        if self.cat_cd <= 0 and self.rng.random() < cfg.cat_p:
            cat = True
            sev = self.rng.uniform(0.3, 1.0)
            # Убиваем долю самых слабых
            kill = int(len(self.agents) * cfg.cat_kill * sev)
            self.agents.sort(key=lambda a: a.fitness())
            killed = self.agents[:kill]
            self.agents = self.agents[kill:]
            # Убитые оставляют tombstones
            for a in killed:
                if len(self.traces) < cfg.max_tr:
                    self.traces.append(TorqueTrace(
                        a.position.copy(), a.genome.copy(), a.fitness() * 0.5,
                        (a.id,), self.step_n, a.create_tombstone()
                    ))
            # Выжившие получают damage и boost
            for a in self.agents:
                a.survive_catastrophe(sev)
            self.cat_cd = cfg.cat_cd
        if self.cat_cd > 0:
            self.cat_cd -= 1

        # ═══ ШАГ 17: Добавляем новорождённых ═══
        self.agents.extend(new_ag)

        # ═══ ШАГ 18: Stepped cost + смерть + tombstones ═══
        for a in self.agents:
            a.step_cost()
        alive: List[Agent] = []
        for a in self.agents:
            if a.is_dead():
                deaths += 1
                # Tombstone для умершего
                if len(self.traces) < cfg.max_tr:
                    self.traces.append(TorqueTrace(
                        a.position.copy(), a.genome.copy(), a.fitness() * 0.3,
                        (a.id,), self.step_n, a.create_tombstone()
                    ))
            else:
                alive.append(a)
        self.agents = alive

        # ═══ ШАГ 19: Контроль демографии ═══
        # Потолок: срезаем слабейших
        if len(self.agents) > cfg.max_ag:
            self.agents.sort(key=lambda a: a.fitness(), reverse=True)
            self.agents = self.agents[:cfg.max_ag]
        # Минимум: добавляем новых
        while len(self.agents) < cfg.min_ag:
            self.agents.append(Agent(self.cfg))
            births += 1

        # ═══ ШАГ 20: Composition трейсов (рекурсивная сборка) ═══
        # Каждые 10 шагов комбинируем лучшие близкие пары трейсов
        if len(self.traces) > 10 and self.step_n % 10 == 0:
            top = sorted(self.traces, key=lambda t: t.value, reverse=True)[:15]
            comp: List[TorqueTrace] = []
            used: set = set()
            for i, t1 in enumerate(top):
                if t1.id in used:
                    continue
                for t2 in top[i + 1:]:
                    if t2.id in used:
                        continue
                    md = min(len(t1.position), len(t2.position))
                    if (np.linalg.norm(t1.position[:md] - t2.position[:md])
                        < cfg.interact_r * 2):
                        comp.append(t1.compose(t2))
                        used.add(t1.id)
                        used.add(t2.id)
                        break
                # Ограничение: не более 2 новых composition за шаг
                if len(comp) >= 2:
                    break
            self.traces.extend(comp)

        # ═══ ШАГ 21: Trace decay + limit ═══
        for t in self.traces:
            t.decay(cfg.tr_decay)
        # Убираем слабые
        self.traces = [t for t in self.traces if t.value > cfg.tr_min]
        # Лимит: режем по price()
        if len(self.traces) > cfg.max_tr:
            self.traces.sort(key=lambda t: t.price(), reverse=True)
            self.traces = self.traces[:cfg.max_tr]

        # ═══ ШАГ 22: Respawn ресурсов ═══
        self.res.respawn(self.rng, self.dims)

        # ═══ ШАГ 23: Stagnant species dissolution ═══
        for sid in self.sp.stagnant():
            for a in self.agents:
                if a.species_id == sid:
                    a.mut_rate *= 2  # Mutation boost
                    a.species_id = None  # Выбрасываем из вида

        self.step_n += 1
        m = self._metrics(births, deaths, abd, ndims, cat, crw)
        self.hist.append(m)
        return m

    # ───────────────────────────────────────────────────────────────────────────
    #  Сбор метрик за шаг
    # ───────────────────────────────────────────────────────────────────────────

    def _metrics(self, bi: int, de: int, ab: int, nd: int,
                 cat: bool, cr: List[float]) -> Dict:
        """
        Компактный словарь метрик шага. Складируется в self.hist.
        """
        if not self.agents:
            return {}

        en = [a.energy for a in self.agents]
        # AI: последних 200 трейсов (чтобы не тянуть старьё)
        ai = [t.ai for t in self.traces[-200:]] if self.traces else [0]
        fit = [a.fitness() for a in self.agents]
        vals = np.mean([a.values for a in self.agents], axis=0)

        # Распределение стилей
        styles: Dict[str, int] = {}
        for a in self.agents:
            styles[a.cognitive_style] = styles.get(a.cognitive_style, 0) + 1

        # Идеи: живые и сильнейшая
        alive_ideas = sum(1 for i in self.ideas if i.alive)
        top_idea = max(self.ideas, key=lambda i: i.strength) if self.ideas else None

        # ═══ НОВЫЕ МЕТРИКИ ДЛЯ ПЛАНИРОВЩИКА (v3.1) ═══
        plan_wins_total = sum(a.plan_wins for a in self.agents)
        plan_fails_total = sum(a.plan_fails for a in self.agents)
        plan_win_rate = (plan_wins_total / (plan_wins_total + plan_fails_total)
                         if plan_wins_total + plan_fails_total > 0 else 0.0)
        # Средняя глубина поиска из историй горизонтов
        all_horizons = [h for a in self.agents for h in a.horizons_history]
        mean_horizon = float(np.mean(all_horizons)) if all_horizons else 0.0
        mean_path_length = float(np.mean([
            len(a.planned_path) for a in self.agents if a.planned_path
        ])) if any(a.planned_path for a in self.agents) else 0.0

        return {
            "step": self.step_n,
            "agents": len(self.agents),
            "species": self.sp.count(),
            "traces": len(self.traces),
            "dims": self.dims,
            "ai": float(np.mean(ai)),
            "ai_max": int(np.max(ai)),
            "energy": float(np.mean(en)),
            "cat": cat,
            "ndims": nd,
            "v_expl": float(vals[0]),
            "v_safe": float(vals[1]),
            "v_soc": float(vals[2]),
            "v_cmplx": float(vals[3]) if len(vals) > 3 else 0,
            "risk": float(np.mean([a.risk for a in self.agents])),
            "ideas": alive_ideas,
            "top_idea": round(top_idea.strength, 2) if top_idea else 0,
            "styles": styles,
            "beliefs": np.mean(
                [a.beliefs for a in self.agents], axis=0
            ).tolist(),
            "critic": float(np.mean([a.critic for a in self.agents])),
            # v3.1 planner metrics:
            "plan_wins": plan_wins_total,
            "plan_fails": plan_fails_total,
            "plan_win_rate": round(plan_win_rate, 3),
            "mean_horizon": round(mean_horizon, 2),
            "mean_path_len": round(mean_path_length, 2)
        }

    # ───────────────────────────────────────────────────────────────────────────
    #  Run — главный цикл прогона
    # ───────────────────────────────────────────────────────────────────────────

    def run(self, verbose: bool = True) -> List[Dict]:
        """
        Полный прогон симуляции на cfg.steps шагов.
        Возвращает историю метрик.

        Сохраняет результаты в results_{name}.json.
        """
        cfg = self.cfg
        t0 = time.time()

        if verbose:
            print(f"\n{'=' * 75}")
            print(f"  MAES v3.1 — COLLECTIVE SYNTHESIS + A* PATH PLANNING")
            print(f"  {cfg.dims}D→{cfg.max_dims}D | {cfg.n_agents} agents | {cfg.steps} steps")
            print(f"  Механизм 14: Cognitive Styles + Ideas + Debates + Beliefs")
            print(f"  Механизм 15: A* Path Planning "
                  f"(enabled={cfg.plan_enabled}, horizon_base={cfg.plan_horizon_base})")
            print(f"{'=' * 75}")

        # ═══ ГЛАВНЫЙ ЦИКЛ ═══
        for step in range(cfg.steps):
            m = self.step()
            if not m:
                print(f"  ВЫМИРАНИЕ на шаге {step}")
                break
            # Logging каждые cfg.log шагов
            if verbose and step % cfg.log == 0:
                fl = ""
                if m.get("cat"):
                    fl += " ⚡"
                if m.get("ndims", 0) > 0:
                    fl += f" 🌀+{m['ndims']}D"
                st = m.get("styles", {})
                st_str = " ".join(f"{k[:3]}:{v}" for k, v in sorted(st.items()))
                plan_info = ""
                if cfg.plan_enabled:
                    plan_info = (f" │ Plan:{m.get('plan_win_rate', 0):.0%} "
                                 f"H:{m.get('mean_horizon', 0):.1f}")
                print(
                    f"  {m['step']:4d} │ A:{m['agents']:3d} S:{m['species']:2d} │ "
                    f"D:{m['dims']:2d} AI:{m['ai']:4.1f}/{m['ai_max']:2d} │ "
                    f"Ideas:{m['ideas']:3d} Top:{m['top_idea']:5.1f} │ "
                    f"[{st_str}]{plan_info}{fl}"
                )

        el = time.time() - t0

        # ═══ ФИНАЛЬНЫЙ ОТЧЁТ ═══
        if verbose and self.hist:
            h = self.hist[-1]
            print(f"\n{'─' * 75}")
            print(f"  Время: {el:.1f}с | {h['agents']}ag {h['species']}sp {h['dims']}D")
            print(f"  AI пик: {max(m['ai_max'] for m in self.hist)} | "
                  f"Катастроф: {sum(1 for m in self.hist if m.get('cat'))}")
            print(f"  Идей живых: {h['ideas']} | Сильнейшая: {h['top_idea']}")
            bl = h.get('beliefs', [])
            if bl:
                bn = Agent.BELIEF_NAMES[:len(bl)]
                print(f"  Beliefs: " + ", ".join(f"{n}={v:.2f}" for n, v in zip(bn, bl)))
            # v3.1 специфичные метрики
            if cfg.plan_enabled:
                print(f"\n  ═══ A* PLANNER STATISTICS ═══")
                print(f"  Win rate: {h.get('plan_win_rate', 0):.1%}")
                print(f"  Total plans: wins={h.get('plan_wins', 0)}, "
                      f"fails={h.get('plan_fails', 0)}")
                print(f"  Mean horizon: {h.get('mean_horizon', 0):.1f} steps")
                print(f"  Mean path length: {h.get('mean_path_len', 0):.1f} waypoints")
            if self.agents:
                best = max(self.agents, key=lambda a: a.ideas_generated)
                print(f"\n  Главный мыслитель #{best.id} "
                      f"({best.cognitive_style}, {best.role}):")
                print(f"    Идей: {best.ideas_generated} | "
                      f"Beliefs: {[round(b, 2) for b in best.beliefs]}")
                if cfg.plan_enabled:
                    print(f"    Planner: wins={best.plan_wins}, fails={best.plan_fails}, "
                          f"last_horizon={best.last_horizon}")
            print(f"{'=' * 75}\n")

        # Сохраняем результаты
        try:
            with open(f"results_{cfg.name}.json", 'w') as f:
                json.dump({"history": self.hist, "config": {
                    "name": cfg.name, "seed": cfg.seed, "dims": cfg.dims,
                    "steps": cfg.steps, "n_agents": cfg.n_agents,
                    "plan_enabled": cfg.plan_enabled,
                    "ablate_planner": cfg.ablate_planner,
                    "ablate_debates": cfg.ablate_debates,
                    "ablate_synthesis": cfg.ablate_synthesis,
                    "ablate_beliefs": cfg.ablate_beliefs,
                    "ablate_style_adapt": cfg.ablate_style_adapt
                }}, f, indent=2, default=str)
        except Exception as e:
            if verbose:
                print(f"  [warn] failed to save results: {e}")

        return self.hist


# ═══════════════════════════════════════════════════════════════════════════════
#                    ABLATION FRAMEWORK — v3.1 vs v3.0
# ═══════════════════════════════════════════════════════════════════════════════
#
# Ablation — это наука: выключаем один механизм и смотрим, насколько система
# деградирует без него. Если не деградирует — механизм бесполезен и его можно
# выкинуть. Если деградирует — знаем, за что он отвечает.
#
# В v3.1 нас интересует главный вопрос: РАБОТАЕТ ЛИ A* ПЛАНИРОВЩИК?
# То есть: v3.1 с планировщиком значимо лучше v3.0 без него?
#
# Метрики сравнения:
#   • AI peak        — максимальная сложность трейсов за прогон
#   • Final agents   — сколько дожили до конца (стабильность популяции)
#   • Ideas          — сколько идей живо (коллективный синтез)
#   • Species        — разнообразие
#   • Time           — время прогона (A* не бесплатен)
#
# Чтобы результат был значим — прогоняем на 5 сидах и смотрим на медианы/sd.
#
# ───────────────────────────────────────────────────────────────────────────────

def run_ablation(seeds: List[int] = None,
                 steps: int = 100,
                 n_agents: int = 30,
                 verbose_runs: bool = False) -> Dict:
    """
    Прогоняет v3.0 (без A*) и v3.1 (с A*) на нескольких сидах и сравнивает.

    Параметры:
        seeds       : список сидов для прогона (по умолчанию [1,2,3,4,5])
        steps       : число шагов в каждом прогоне
        n_agents    : стартовое число агентов
        verbose_runs: подробный лог каждого прогона (по умолчанию нет — иначе
                      вывод утонет)

    Возвращает: dict с результатами v3.0, v3.1 и сводной статистикой.
    """
    if seeds is None:
        seeds = [1, 2, 3, 4, 5]

    results = {"v3_0": [], "v3_1": []}

    print(f"\n{'=' * 75}")
    print(f"  ABLATION: v3.0 (no planner) vs v3.1 (with A* planner)")
    print(f"  Seeds: {seeds} | Steps: {steps} | Agents: {n_agents}")
    print(f"{'=' * 75}\n")

    # ═══ Прогон v3.0 (планировщик ВЫКЛЮЧЕН) ═══
    print(">>> Running v3.0 baseline (planner disabled)...")
    for seed in seeds:
        cfg = Config(
            name=f"v3_0_seed{seed}",
            seed=seed,
            steps=steps,
            n_agents=n_agents,
            ablate_planner=True,   # <-- Ключевая строка: выключаем планировщик
            log=max(steps // 3, 1)
        )
        t0 = time.time()
        env = Env(cfg)
        hist = env.run(verbose=verbose_runs)
        elapsed = time.time() - t0

        # Собираем summary per-run
        summary = _summarize_run(hist, elapsed, seed, label="v3.0")
        results["v3_0"].append(summary)
        print(f"  seed={seed} → AI_peak={summary['ai_peak']:2d} "
              f"| agents_final={summary['agents_final']:3d} "
              f"| ideas={summary['ideas_final']:3d} "
              f"| time={elapsed:.1f}s")

    # ═══ Прогон v3.1 (планировщик ВКЛЮЧЕН) ═══
    print("\n>>> Running v3.1 with A* planner (planner enabled)...")
    for seed in seeds:
        cfg = Config(
            name=f"v3_1_seed{seed}",
            seed=seed,
            steps=steps,
            n_agents=n_agents,
            ablate_planner=False,  # <-- Планировщик включён
            log=max(steps // 3, 1)
        )
        t0 = time.time()
        env = Env(cfg)
        hist = env.run(verbose=verbose_runs)
        elapsed = time.time() - t0

        summary = _summarize_run(hist, elapsed, seed, label="v3.1")
        results["v3_1"].append(summary)
        print(f"  seed={seed} → AI_peak={summary['ai_peak']:2d} "
              f"| agents_final={summary['agents_final']:3d} "
              f"| ideas={summary['ideas_final']:3d} "
              f"| plan_wr={summary.get('plan_win_rate', 0):.0%} "
              f"| time={elapsed:.1f}s")

    # ═══ Сводная статистика ═══
    print(f"\n{'=' * 75}")
    print(f"  SUMMARY (median ± stdev across {len(seeds)} seeds)")
    print(f"{'=' * 75}")
    summary_v30 = _aggregate(results["v3_0"])
    summary_v31 = _aggregate(results["v3_1"])

    print(f"\n  METRIC          │ v3.0 (no plan)      │ v3.1 (A* planner)   │ Δ")
    print(f"  ─────────────────┼─────────────────────┼─────────────────────┼──────")
    for key, label in [
        ("ai_peak",       "AI peak        "),
        ("ai_mean",       "AI mean        "),
        ("agents_final",  "Agents final   "),
        ("species_final", "Species final  "),
        ("ideas_final",   "Ideas final    "),
        ("top_idea",      "Top idea stren."),
        ("dims_final",    "Dims final     "),
        ("n_catastrophes","Catastrophes   "),
        ("time_sec",      "Time (sec)     "),
    ]:
        m0 = summary_v30.get(key, {})
        m1 = summary_v31.get(key, {})
        med0 = m0.get('median', 0)
        sd0 = m0.get('std', 0)
        med1 = m1.get('median', 0)
        sd1 = m1.get('std', 0)
        # Delta в процентах
        if med0 != 0:
            delta = (med1 - med0) / abs(med0) * 100
            dstr = f"{delta:+6.1f}%"
        else:
            dstr = "  n/a  "
        print(f"  {label} │ {med0:7.1f} ± {sd0:5.1f}    │ {med1:7.1f} ± {sd1:5.1f}    │ {dstr}")

    # ═══ Планировщик — специфичные метрики ═══
    # (считаем только для v3.1, где планировщик работает)
    if results["v3_1"]:
        win_rates = [r.get('plan_win_rate', 0) for r in results["v3_1"]]
        horizons = [r.get('mean_horizon', 0) for r in results["v3_1"]]
        print(f"\n  ═══ A* PLANNER SPECIFIC (v3.1 only) ═══")
        print(f"  Plan win rate: median={np.median(win_rates):.1%} "
              f"± {np.std(win_rates):.1%}")
        print(f"  Mean horizon:  median={np.median(horizons):.2f} "
              f"± {np.std(horizons):.2f}")

    # ═══ Стили — сравнение распределений ═══
    styles_v30 = _aggregate_styles(results["v3_0"])
    styles_v31 = _aggregate_styles(results["v3_1"])
    print(f"\n  ═══ COGNITIVE STYLES DISTRIBUTION (final) ═══")
    all_styles = set(list(styles_v30.keys()) + list(styles_v31.keys()))
    print(f"  STYLE        │ v3.0 avg │ v3.1 avg │ Δ")
    print(f"  ─────────────┼──────────┼──────────┼───────")
    for style in sorted(all_styles):
        v30_count = styles_v30.get(style, 0)
        v31_count = styles_v31.get(style, 0)
        if v30_count > 0:
            delta_pct = (v31_count - v30_count) / v30_count * 100
            dstr = f"{delta_pct:+6.1f}%"
        else:
            dstr = "  n/a "
        print(f"  {style:12s} │ {v30_count:7.1f}  │ {v31_count:7.1f}  │ {dstr}")

    print(f"\n{'=' * 75}\n")

    # Сохраняем всё в один файл
    ablation_results = {
        "seeds": seeds,
        "steps": steps,
        "n_agents": n_agents,
        "v3_0": results["v3_0"],
        "v3_1": results["v3_1"],
        "summary_v3_0": summary_v30,
        "summary_v3_1": summary_v31,
    }
    try:
        with open("ablation_v3_1_vs_v3_0.json", 'w') as f:
            json.dump(ablation_results, f, indent=2, default=str)
        print(f"  Результаты сохранены в: ablation_v3_1_vs_v3_0.json")
    except Exception as e:
        print(f"  [warn] failed to save ablation: {e}")

    return ablation_results


def _summarize_run(hist: List[Dict], elapsed: float, seed: int,
                   label: str) -> Dict:
    """
    Сводка одного прогона: ключевые метрики для сравнения.
    """
    if not hist:
        return {"seed": seed, "label": label, "failed": True}

    final = hist[-1]
    ai_peak = max(m.get("ai_max", 0) for m in hist)
    ai_mean = np.mean([m.get("ai", 0) for m in hist])
    n_cat = sum(1 for m in hist if m.get("cat"))

    summary = {
        "seed": seed,
        "label": label,
        "ai_peak": int(ai_peak),
        "ai_mean": round(float(ai_mean), 2),
        "agents_final": int(final.get("agents", 0)),
        "species_final": int(final.get("species", 0)),
        "ideas_final": int(final.get("ideas", 0)),
        "top_idea": float(final.get("top_idea", 0)),
        "dims_final": int(final.get("dims", 0)),
        "n_catastrophes": n_cat,
        "time_sec": round(elapsed, 1),
        "styles_final": final.get("styles", {}),
        "beliefs_final": final.get("beliefs", []),
        # Планировщик-специфичные метрики (0 если v3.0)
        "plan_wins": int(final.get("plan_wins", 0)),
        "plan_fails": int(final.get("plan_fails", 0)),
        "plan_win_rate": float(final.get("plan_win_rate", 0)),
        "mean_horizon": float(final.get("mean_horizon", 0)),
    }
    return summary


def _aggregate(runs: List[Dict]) -> Dict[str, Dict[str, float]]:
    """
    Агрегируем метрики по списку прогонов: median, std.
    Возвращает dict с метриками → {median, std, min, max}.
    """
    if not runs:
        return {}

    keys = ["ai_peak", "ai_mean", "agents_final", "species_final",
            "ideas_final", "top_idea", "dims_final", "n_catastrophes",
            "time_sec", "plan_wins", "plan_fails", "plan_win_rate",
            "mean_horizon"]

    agg = {}
    for k in keys:
        vals = [r.get(k, 0) for r in runs if not r.get("failed")]
        if not vals:
            continue
        agg[k] = {
            "median": float(np.median(vals)),
            "std": float(np.std(vals)),
            "min": float(np.min(vals)),
            "max": float(np.max(vals)),
        }
    return agg


def _aggregate_styles(runs: List[Dict]) -> Dict[str, float]:
    """Усредняем распределение стилей по прогонам."""
    if not runs:
        return {}
    totals: Dict[str, List[int]] = {}
    for r in runs:
        if r.get("failed"):
            continue
        styles = r.get("styles_final", {})
        for s, c in styles.items():
            totals.setdefault(s, []).append(c)
    # Усредняем
    return {s: float(np.mean(counts)) for s, counts in totals.items()}


# ═══════════════════════════════════════════════════════════════════════════════
#                                __main__
# ═══════════════════════════════════════════════════════════════════════════════
#
# Точка входа: парсим аргументы и запускаем либо одиночный прогон,
# либо ablation.
#
# Примеры использования:
#   python maes_v3_1.py                          — один прогон с defaults
#   python maes_v3_1.py --steps 150 --seed 7     — свои параметры
#   python maes_v3_1.py --ablation               — полный ablation на 5 seeds
#   python maes_v3_1.py --ablation --seeds 1 2 3 — ablation на своих seeds
#   python maes_v3_1.py --no-planner             — запустить БЕЗ A* (= v3.0)
#
# ───────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="MAES v3.1 — Multidimensional Algorithmic Evolution System "
                    "with A* path planning."
    )
    parser.add_argument("--steps", type=int, default=200,
                        help="Number of simulation steps (default: 200)")
    parser.add_argument("--agents", type=int, default=40,
                        help="Initial number of agents (default: 40)")
    parser.add_argument("--seed", type=int, default=42,
                        help="Random seed (default: 42)")
    parser.add_argument("--ablation", action="store_true",
                        help="Run full ablation v3.0 vs v3.1 on multiple seeds")
    parser.add_argument("--seeds", type=int, nargs="+", default=None,
                        help="Seeds for ablation (default: 1 2 3 4 5)")
    parser.add_argument("--no-planner", action="store_true",
                        help="Disable A* planner (revert to v3.0 behavior)")
    args = parser.parse_args()

    if args.ablation:
        # Режим ablation: v3.0 vs v3.1 на 5 сидах
        run_ablation(
            seeds=args.seeds if args.seeds else [1, 2, 3, 4, 5],
            steps=args.steps,
            n_agents=args.agents,
            verbose_runs=False
        )
    else:
        # Одиночный прогон
        cfg = Config(
            steps=args.steps,
            n_agents=args.agents,
            seed=args.seed,
            ablate_planner=args.no_planner
        )
        Env(cfg).run()
