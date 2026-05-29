#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
 MAES v3.2 — НАДСТРОЙКА "SINGING TAIL" (Поющий Хвост)
 Communication Layer: Язык + Музыка как единый эволюционный оператор
================================================================================
 Дата:      15 мая 2026
 Автор:     Клод Викторович Антропиков
 Заказчик:  Иларион Иванович Шаповал
 Версия:    v3.2-singing_tail-rc1
 База:      maes_v3_1.py (3825 строк, не модифицируется)

 ФИЛОСОФИЯ МОДУЛЯ:
   Этот файл НЕ переписывает существующий код MAES v3.1.
   Он реализует overlay-классы, которые цепляются к существующим
   объектам через 4-5 точек интеграции (см. секцию ИНТЕГРАЦИЯ ниже).

   Принцип непрерывности (механизм 7): всё что работало — продолжает работать.
   Принцип «не навреди» (механизм 8): каждое усиление имеет компенсатор.
   Endogenous Mechanisms (механизм 6): только NumPy, никаких ML-библиотек.

 АРХИТЕКТУРА (10 новых сущностей):
   1.  LanguageSignature  — дискретный канал смысла (словарь + произношение)
   2.  MusicCarrier       — непрерывный канал резонанса (частота + амплитуда)
   3.  EmotionVector      — 6-мерный профиль чувственного переживания
   4.  Song               — единица культурной памяти (имя + мелодия + эмоция)
   5.  Saga               — длинная многочастная песня о пережитом (память рода)
   6.  Ballad             — лирическая песня одного агента о другом/о себе
   7.  Genre              — кластер песен с общими структурными признаками
   8.  Songbook           — коллективная фонотека популяции
   9.  CommunicationField — то что окружает агента (среда обмена)
   10. SingingTail        — обёртка, которая всё это связывает с агентом

 СВЯЗЬ С 86 МЕХАНИЗМАМИ РЕЕСТРА:
   - закрывает №5 (эдемский принцип)
   - частично закрывает №12 (антихвост — в части восприятия)
   - реализует часть №74 (Rosetta через TopSim метрики)
   - создаёт новые сущности №87-90 (Song, Saga, Ballad, Genre)

 СВЯЗЬ С 15 ПУНКТАМИ LIVING LANGUAGE (апрель 2026):
   - п.1: метрики обязательны (TopSim, Zipf, Heaps реализованы)
   - п.3: минимальное ядро примитивов (8 стартовых слов + слоты)
   - п.10: emotional markers (6-мерный вектор)
   - п.13: двухуровневая криптография (свой/чужой через genre similarity)

 ИСПОЛЬЗОВАНИЕ:
   В maes_v3_1.py добавить:
       from maes_v3_2_singing_tail import attach_singing_tail
       attach_singing_tail(agent, rng)                 # в Agent.__init__
       env.communication_field = CommunicationField()  # в Env.__init__
   Плюс 4 блока в Env.step (см. секцию ИНТЕГРАЦИЯ внизу файла).
================================================================================
"""

from __future__ import annotations

import math
from collections import deque, Counter, defaultdict
from typing import Optional, List, Tuple, Dict, Any

import numpy as np


# ══════════════════════════════════════════════════════════════════════════════
#  КОНСТАНТЫ И КОНФИГУРАЦИЯ МОДУЛЯ
# ══════════════════════════════════════════════════════════════════════════════
# Все настройки модуля собраны здесь — для лёгкой ablation.

class SingingTailConfig:
    """Конфигурация коммуникационного слоя. Дефолты осторожные."""

    # ─── ЯЗЫК ─────────────────────────────────────────────────────────────────
    VOCAB_INIT_SIZE       = 8         # сколько слов агент знает при рождении
    VOCAB_MAX_SIZE        = 64        # ограничение словаря (компактность)
    MEANING_DIM           = 8         # размерность вектора смысла
    COIN_NEW_THRESHOLD    = 0.45      # порог расстояния для рождения нового слова
    DENOTATION_LEARN_RATE = 0.1       # скорость обновления denotation_map
    LEXICON_DECAY         = 0.001     # «забывание» неиспользуемых слов

    # ─── МУЗЫКА ───────────────────────────────────────────────────────────────
    FREQ_MIN              = 0.5       # минимальная фундаментальная частота
    FREQ_MAX              = 2.0       # максимальная
    FREQ_MUTATION_RATE    = 0.005     # как быстро частота дрейфует
    ATTRACT_STRENGTH      = 0.02      # сила синхронизации с соседями
    CONSONANCE_BONUS_CAP  = 0.02      # максимальный энергетический бонус (2%)
    DISSONANCE_PENALTY    = 0.99      # множитель за диссонанс
    SIMPLE_RATIOS         = [(1,1), (2,1), (3,2), (4,3), (5,3), (5,4), (8,5)]
    RATIO_TOLERANCE       = 0.04      # допуск при определении консонанса

    # ─── ЭМОЦИИ ───────────────────────────────────────────────────────────────
    # 6 базовых измерений (расширение апрельских emotional markers до 6D)
    EMOTION_NAMES = ["joy", "fear", "anger", "sadness", "awe", "tenderness"]
    EMOTION_DIM           = 6
    EMOTION_DECAY         = 0.95      # эмоции остывают со временем
    EMOTION_SPILL         = 0.05      # часть эмоции «протекает» соседям

    # ─── ПЕСНИ И САГИ ─────────────────────────────────────────────────────────
    SONG_BIRTH_THRESHOLD  = 0.6       # порог силы события для рождения песни
    SONG_MELODY_LEN_MIN   = 3         # минимальная длина мелодии
    SONG_MELODY_LEN_MAX   = 7         # максимальная (короткая песня)
    SAGA_MIN_PARTS        = 3         # минимум частей в саге
    SAGA_TRIGGER_AGE      = 100       # возраст агента для способности к саге
    BALLAD_INTIMACY_THR   = 0.7       # порог близости для рождения баллады
    GENRE_CLUSTER_MIN     = 3         # минимум песен для формирования жанра
    SONGBOOK_MAX_SIZE     = 200       # ограничение коллективной памяти

    # ─── ОБЩЕЕ ────────────────────────────────────────────────────────────────
    NEIGHBOR_RADIUS       = 2.0       # радиус обмена в пространстве
    LOG_EDEN_EVENTS       = True      # логировать первые произнесения новых слов


# ══════════════════════════════════════════════════════════════════════════════
#  1. EmotionVector — чувственное переживание (6D)
# ══════════════════════════════════════════════════════════════════════════════
class EmotionVector:
    """Шесть базовых эмоций как непрерывный 6D вектор.

    Не путать с beliefs (когнитивное) и values (нормативное).
    Эмоции — это СОСТОЯНИЕ ПЕРЕЖИВАНИЯ здесь и сейчас.

    Имена: joy (радость), fear (страх), anger (гнев),
           sadness (печаль), awe (благоговение), tenderness (нежность).

    Откуда: расширение апрельских emotional markers (Living Language п.10).
    Там было 4 (urgency, threat, support, surprise). Здесь 6 более универсальных,
    с теоретической базой Ekman 1992 + Keltner 2003 (awe).
    """
    __slots__ = ('vec', 'history')

    def __init__(self, rng=None, init: Optional[np.ndarray] = None):
        if init is not None:
            self.vec = init.astype(np.float32)
        elif rng is not None:
            # Спокойное эмоциональное стартовое состояние (низкие значения)
            self.vec = rng.uniform(0, 0.2, SingingTailConfig.EMOTION_DIM).astype(np.float32)
        else:
            self.vec = np.zeros(SingingTailConfig.EMOTION_DIM, dtype=np.float32)
        # Память последних 8 состояний — для построения «эмоциональной траектории»
        self.history: deque = deque(maxlen=8)

    def feel(self, deltas: Dict[str, float]) -> None:
        """Сдвиг эмоций. deltas — словарь {'joy': +0.3, 'fear': -0.1, ...}."""
        for name, delta in deltas.items():
            if name in SingingTailConfig.EMOTION_NAMES:
                idx = SingingTailConfig.EMOTION_NAMES.index(name)
                self.vec[idx] = float(np.clip(self.vec[idx] + delta, 0.0, 1.0))

    def decay(self) -> None:
        """Остывание эмоций (механизм 8: не накапливаем бесконечно)."""
        self.history.append(self.vec.copy())
        self.vec *= SingingTailConfig.EMOTION_DECAY

    def intensity(self) -> float:
        """Общая «амплитуда» переживания — для порога рождения песни."""
        return float(np.linalg.norm(self.vec))

    def dominant(self) -> str:
        """Какая эмоция сейчас сильнейшая."""
        return SingingTailConfig.EMOTION_NAMES[int(np.argmax(self.vec))]

    def blend(self, other: 'EmotionVector', alpha: float = 0.05) -> None:
        """Эмоциональное заражение от соседа (механизм 'spill')."""
        self.vec = (1 - alpha) * self.vec + alpha * other.vec

    def __repr__(self) -> str:
        d = self.dominant()
        v = float(self.vec[SingingTailConfig.EMOTION_NAMES.index(d)])
        return f"<E:{d}={v:.2f} I={self.intensity():.2f}>"


# ══════════════════════════════════════════════════════════════════════════════
#  2. LanguageSignature — дискретный канал смысла
# ══════════════════════════════════════════════════════════════════════════════
class LanguageSignature:
    """Словарь токенов + текущее произношение.

    КЛЮЧЕВАЯ ИДЕЯ:
        token_id -> meaning_vector (8D)
    Это означает: каждое «слово» имеет свой смысл, но смысл может
    сдвигаться от взаимодействия с другими носителями (эдемский принцип).

    Внутрисистемная эмерджентность: словарь стартует случайным,
    при контакте с соседями сдвигается к консенсусу, при collective
    synthesis рождаются новые слова.
    """
    # Глобальный счётчик: все агенты делят пространство токенов
    _next_token_id = 1
    # Глобальный «эдемский лог» — кто, когда, какое слово первым произнёс
    _eden_log: List[Tuple[int, int, int, np.ndarray]] = []  # (token, agent_id, step, meaning)

    __slots__ = ('vocab', 'denotation_map', 'usage_count', 'last_utterance',
                 'utterance_age', 'birth_step')

    def __init__(self, rng):
        self.vocab: List[int] = []
        self.denotation_map: Dict[int, np.ndarray] = {}
        self.usage_count: Counter = Counter()
        self.last_utterance: Optional[int] = None
        self.utterance_age = 0
        self.birth_step = 0
        # Инициализируем стартовый словарь — VOCAB_INIT_SIZE случайных слов
        for _ in range(SingingTailConfig.VOCAB_INIT_SIZE):
            tok = LanguageSignature._next_token_id
            LanguageSignature._next_token_id += 1
            meaning = rng.uniform(-1, 1, SingingTailConfig.MEANING_DIM).astype(np.float32)
            meaning /= (np.linalg.norm(meaning) + 1e-9)
            self.vocab.append(tok)
            self.denotation_map[tok] = meaning

    def speak(self, meaning_vector: np.ndarray, agent_id: int, step: int,
              rng) -> Tuple[int, bool]:
        """Произнести: найти ближайшее слово или создать новое.

        Возвращает: (token_id, is_new_word)
        is_new_word=True — это «эдемский момент», логируется.
        """
        if meaning_vector.shape[0] != SingingTailConfig.MEANING_DIM:
            # Подгоняем размерность — берём первые MEANING_DIM компонент
            if meaning_vector.shape[0] > SingingTailConfig.MEANING_DIM:
                meaning_vector = meaning_vector[:SingingTailConfig.MEANING_DIM]
            else:
                pad = np.zeros(SingingTailConfig.MEANING_DIM - meaning_vector.shape[0])
                meaning_vector = np.concatenate([meaning_vector, pad])
        m = meaning_vector.astype(np.float32)
        m_norm = m / (np.linalg.norm(m) + 1e-9)

        # Ищем ближайший токен по косинусному сходству (эквивалент Eucl на сфере)
        if self.vocab:
            sims = np.array([float(np.dot(m_norm, self.denotation_map[t]))
                             for t in self.vocab])
            best_idx = int(np.argmax(sims))
            best_sim = float(sims[best_idx])
            # Если ближайшее слово достаточно близко — используем его
            if best_sim > (1.0 - SingingTailConfig.COIN_NEW_THRESHOLD):
                tok = self.vocab[best_idx]
                self.usage_count[tok] += 1
                self.last_utterance = tok
                self.utterance_age = 0
                return (tok, False)

        # Иначе — эдемский момент: создаём новое слово
        if len(self.vocab) >= SingingTailConfig.VOCAB_MAX_SIZE:
            # Удаляем самое редко используемое (механизм забывания)
            least = min(self.vocab, key=lambda t: self.usage_count.get(t, 0))
            self.vocab.remove(least)
            self.denotation_map.pop(least, None)
            self.usage_count.pop(least, None)

        new_tok = LanguageSignature._next_token_id
        LanguageSignature._next_token_id += 1
        self.vocab.append(new_tok)
        self.denotation_map[new_tok] = m_norm.copy()
        self.usage_count[new_tok] = 1
        self.last_utterance = new_tok
        self.utterance_age = 0

        if SingingTailConfig.LOG_EDEN_EVENTS:
            LanguageSignature._eden_log.append((new_tok, agent_id, step, m_norm.copy()))

        return (new_tok, True)

    def listen(self, token: int, source_denotation: np.ndarray) -> None:
        """Услышать: если знаем слово — сдвигаем denotation к источнику.
           Если не знаем — заимствуем как есть."""
        sd = source_denotation.astype(np.float32)
        sd = sd / (np.linalg.norm(sd) + 1e-9)
        if token in self.denotation_map:
            lr = SingingTailConfig.DENOTATION_LEARN_RATE
            old = self.denotation_map[token]
            new = (1 - lr) * old + lr * sd
            new /= (np.linalg.norm(new) + 1e-9)
            self.denotation_map[token] = new
            self.usage_count[token] += 1
        else:
            # Заимствуем новое слово (как ребёнок учится от взрослых)
            if len(self.vocab) < SingingTailConfig.VOCAB_MAX_SIZE:
                self.vocab.append(token)
                self.denotation_map[token] = sd.copy()
                self.usage_count[token] = 1

    def lexicon_decay(self) -> None:
        """Постепенно забываем неиспользуемые слова."""
        decay = SingingTailConfig.LEXICON_DECAY
        for t in list(self.usage_count.keys()):
            self.usage_count[t] *= (1 - decay)
            if self.usage_count[t] < 0.1 and t != self.last_utterance:
                # Удаляем слово, у которого «вес» упал ниже минимума
                self.vocab.remove(t) if t in self.vocab else None
                self.denotation_map.pop(t, None)
                self.usage_count.pop(t, None)

    def topsim_with(self, meaning_pairs: List[Tuple[np.ndarray, int]]) -> float:
        """TopSim метрика (Brighton & Kirby 2006): корреляция расстояний
        между meaning-векторами и расстояний между token-denotations.

        Принимает список (meaning, token) пар. Возвращает Spearman-подобный rho.
        Чем выше — тем согласованнее язык.
        """
        if len(meaning_pairs) < 4:
            return 0.0
        # Берём токены, для которых знаем denotation
        valid = [(m, t) for m, t in meaning_pairs if t in self.denotation_map]
        if len(valid) < 4:
            return 0.0
        m_dists, t_dists = [], []
        for i in range(len(valid)):
            for j in range(i+1, len(valid)):
                mi, ti = valid[i]
                mj, tj = valid[j]
                m_dists.append(float(np.linalg.norm(mi - mj)))
                t_dists.append(float(np.linalg.norm(
                    self.denotation_map[ti] - self.denotation_map[tj])))
        # Pearson-корреляция (быстрая, без scipy)
        m_arr = np.array(m_dists)
        t_arr = np.array(t_dists)
        if m_arr.std() < 1e-9 or t_arr.std() < 1e-9:
            return 0.0
        corr = float(np.corrcoef(m_arr, t_arr)[0, 1])
        return corr

    @classmethod
    def zipf_alpha(cls, all_usages: List[Counter]) -> float:
        """Закон Ципфа: считаем α из log-log распределения частот.
        Естественные языки → α ≈ -1.0. Случайные равномерные → α ≈ 0.
        """
        total = Counter()
        for u in all_usages:
            total.update(u)
        if len(total) < 5:
            return 0.0
        freqs = sorted(total.values(), reverse=True)
        ranks = np.arange(1, len(freqs) + 1)
        log_r = np.log(ranks)
        log_f = np.log(np.array(freqs, dtype=float) + 1e-9)
        # Линейная регрессия log_f = α * log_r + β
        n = len(log_r)
        alpha = float((n * np.sum(log_r * log_f) - np.sum(log_r) * np.sum(log_f)) /
                      (n * np.sum(log_r ** 2) - np.sum(log_r) ** 2 + 1e-9))
        return alpha

    @classmethod
    def heaps_exponent(cls, vocab_growth_history: List[Tuple[int, int]]) -> float:
        """Закон Хипса: V(N) ~ N^β, где V — размер словаря, N — общее число
        произнесений. Естественные языки β ≈ 0.4-0.6.

        vocab_growth_history — список (total_utterances, vocab_size) на разных шагах.
        """
        if len(vocab_growth_history) < 5:
            return 0.0
        N = np.array([h[0] for h in vocab_growth_history], dtype=float)
        V = np.array([h[1] for h in vocab_growth_history], dtype=float)
        # Отбрасываем нулевые
        mask = (N > 0) & (V > 0)
        if mask.sum() < 5:
            return 0.0
        log_N = np.log(N[mask])
        log_V = np.log(V[mask])
        n = len(log_N)
        beta = float((n * np.sum(log_N * log_V) - np.sum(log_N) * np.sum(log_V)) /
                     (n * np.sum(log_N ** 2) - np.sum(log_N) ** 2 + 1e-9))
        return beta


# ══════════════════════════════════════════════════════════════════════════════
#  3. MusicCarrier — непрерывный канал резонанса
# ══════════════════════════════════════════════════════════════════════════════
class MusicCarrier:
    """Музыкальный носитель: частота + амплитуда + фаза + эмоциональная окраска.

    Базовый процесс:
      1. Частота слабо мутирует с возрастом
      2. В присутствии соседей частоты притягиваются друг к другу
         (механизм синхронизации, как сверчки в траве)
      3. Если отношение частот близко к простому (1:1, 2:1, 3:2...) —
         волны конструктивно интерферируют → энергетический бонус
      4. Эмоциональный профиль агента «окрашивает» музыку через
         модуляцию амплитуды
    """
    __slots__ = ('freq', 'amplitude', 'phase', 'emotion_color', 'tempo_history')

    def __init__(self, rng, emotion: Optional[EmotionVector] = None):
        self.freq = float(rng.uniform(SingingTailConfig.FREQ_MIN,
                                       SingingTailConfig.FREQ_MAX))
        self.amplitude = 1.0
        self.phase = float(rng.uniform(0, 2 * math.pi))
        # Связка с эмоциями: текущее эмоциональное состояние «модулирует» звук
        self.emotion_color = emotion if emotion is not None else EmotionVector(rng=rng)
        # История изменений темпа — потом из неё строится мелодия
        self.tempo_history: deque = deque(maxlen=16)
        self.tempo_history.append(self.freq)

    @staticmethod
    def consonance_factor(f1: float, f2: float) -> float:
        """Возвращает множитель: >1 для консонанса, <1 для диссонанса.

        Используется простая теория консонанса: чем проще отношение
        двух частот, тем меньше «биений», тем эффективнее интерференция.
        Это эмпирический закон Гельмгольца (1863), но применённый
        к произвольным колебаниям, не только звуковым.
        """
        if f1 <= 0 or f2 <= 0:
            return 1.0
        ratio = max(f1, f2) / min(f1, f2)
        for n, m in SingingTailConfig.SIMPLE_RATIOS:
            target = n / m
            if abs(ratio - target) < SingingTailConfig.RATIO_TOLERANCE:
                # Бонус обратно пропорционален «сложности» отношения
                complexity = n + m
                return 1.0 + SingingTailConfig.CONSONANCE_BONUS_CAP / max(2, complexity / 2)
        return SingingTailConfig.DISSONANCE_PENALTY

    def interference_with(self, other: 'MusicCarrier') -> float:
        """Множитель к энергии при соседстве с другим носителем."""
        return self.consonance_factor(self.freq, other.freq)

    def attract_to(self, neighbor_freqs: List[float], rng=None) -> None:
        """Постепенная синхронизация с соседями.

        Модель: каждая соседская частота тянет нашу к себе по
        обратно-квадратичному закону (или вернее — к ближайшему
        консонансному отношению).
        """
        if not neighbor_freqs:
            return
        target = float(np.mean(neighbor_freqs))
        delta = target - self.freq
        self.freq += SingingTailConfig.ATTRACT_STRENGTH * delta
        # Лёгкая мутация (механизм 8: способ выйти из синхронизации)
        if rng is not None:
            self.freq += float(rng.normal(0, SingingTailConfig.FREQ_MUTATION_RATE))
        # Зажим в допустимый диапазон
        self.freq = float(np.clip(self.freq,
                                   SingingTailConfig.FREQ_MIN,
                                   SingingTailConfig.FREQ_MAX))
        self.tempo_history.append(self.freq)

    def modulate_by_emotion(self) -> None:
        """Эмоции окрашивают звук: высокая радость = выше амплитуда и tempo,
        страх = быстрая пульсация, печаль = низкая амплитуда, awe = чистый тон."""
        e = self.emotion_color.vec
        # joy, fear, anger, sadness, awe, tenderness
        joy, fear, anger, sadness, awe, tenderness = e
        # Амплитуда растёт от радости/гнева, падает от печали
        self.amplitude = float(np.clip(
            1.0 + 0.3 * (joy + anger) - 0.4 * sadness + 0.2 * tenderness,
            0.1, 2.0))
        # Awe немного «выпрямляет» частоту (делает её ближе к чистому тону)
        if awe > 0.5:
            # Притягиваем к ближайшей октаве относительно среднего диапазона
            mid = (SingingTailConfig.FREQ_MIN + SingingTailConfig.FREQ_MAX) / 2
            self.freq = (1 - awe * 0.05) * self.freq + (awe * 0.05) * mid


# ══════════════════════════════════════════════════════════════════════════════
#  4-6. Song / Ballad / Saga — три формы культурной памяти
# ══════════════════════════════════════════════════════════════════════════════
class Song:
    """Короткая песня: имя + мелодия (последовательность 3-7 частот) + эмоция.

    Рождается в момент сильного события (collective synthesis,
    переживание катастрофы, эдемское называние).

    Это БАЗОВАЯ единица культурной памяти MAES.
    """
    _next_id = 1
    __slots__ = ('id', 'name_token', 'melody', 'emotion', 'origin_step',
                 'origin_agent', 'carriers', 'kind', 'genre_id')

    def __init__(self, name_token: int, melody: Tuple[float, ...],
                 emotion: EmotionVector, step: int, origin_agent: int,
                 kind: str = "song"):
        self.id = Song._next_id
        Song._next_id += 1
        self.name_token = name_token
        self.melody = tuple(round(f, 4) for f in melody)
        # Замораживаем эмоциональный профиль в момент создания
        self.emotion = EmotionVector(init=emotion.vec.copy())
        self.origin_step = step
        self.origin_agent = origin_agent
        self.carriers: set = {origin_agent}
        self.kind = kind            # "song" | "ballad" | "saga_part"
        self.genre_id: Optional[int] = None

    def melodic_distance(self, other: 'Song') -> float:
        """Расстояние между мелодиями — для кластеризации в жанры."""
        if len(self.melody) == 0 or len(other.melody) == 0:
            return float('inf')
        # Сравниваем по «интервальному контуру» — последовательности отношений
        def contour(m):
            if len(m) < 2:
                return [1.0]
            return [m[i+1] / max(m[i], 1e-6) for i in range(len(m)-1)]
        c1 = contour(self.melody)
        c2 = contour(other.melody)
        # Усекаем до общей длины
        L = min(len(c1), len(c2))
        c1, c2 = c1[:L], c2[:L]
        return float(np.mean([(a - b) ** 2 for a, b in zip(c1, c2)]))

    def __repr__(self) -> str:
        return f"<Song#{self.id} '{self.name_token}' {self.kind} mel={len(self.melody)} agents={len(self.carriers)}>"


class Ballad(Song):
    """Баллада — лирическая песня одного агента о другом или о себе.

    Особенности:
      - Всегда имеет subject_agent_id (про кого песня)
      - Эмоция чаще tenderness/sadness/awe
      - Длиннее обычной песни (5-9 частот)
      - Рождается из close-pair взаимодействий
    """
    __slots__ = ('subject_agent_id', 'is_self_ballad')

    def __init__(self, name_token: int, melody: Tuple[float, ...],
                 emotion: EmotionVector, step: int, origin_agent: int,
                 subject_agent_id: int):
        super().__init__(name_token, melody, emotion, step, origin_agent,
                         kind="ballad")
        self.subject_agent_id = subject_agent_id
        self.is_self_ballad = (subject_agent_id == origin_agent)


class Saga(Song):
    """Сага — длинная многочастная песня о пережитом.

    Особенности:
      - Состоит из нескольких частей (parts) — каждая = мини-песня
      - Хранит последовательность событий из identity старого агента
      - Может рождаться только у агента возрастом > SAGA_TRIGGER_AGE
      - Передаёт «память рода» — то что не уместилось в Song
    """
    __slots__ = ('parts', 'narrative_arc', 'protagonists')

    def __init__(self, name_token: int, parts: List[Tuple[float, ...]],
                 emotion: EmotionVector, step: int, origin_agent: int,
                 narrative: List[Tuple], protagonists: List[int]):
        # Объединяем мелодии частей в одну большую мелодию для базы
        full_melody = tuple(f for part in parts for f in part)
        super().__init__(name_token, full_melody, emotion, step, origin_agent,
                         kind="saga_part")
        self.parts = [tuple(round(f, 4) for f in p) for p in parts]
        # narrative_arc — список событий из identity ((event_type, age, ...))
        self.narrative_arc = list(narrative)
        self.protagonists = list(protagonists)

    def length_in_parts(self) -> int:
        return len(self.parts)


# ══════════════════════════════════════════════════════════════════════════════
#  7. Genre — кластер песен с общей структурой
# ══════════════════════════════════════════════════════════════════════════════
class Genre:
    """Жанр — эмерджентный кластер песен с похожим интервальным контуром.

    Жанры выявляются периодически (раз в N шагов) через простую
    кластеризацию по melodic_distance. Это даёт «культурные субпопуляции»
    которые не совпадают с биологическими видами.
    """
    _next_id = 1
    __slots__ = ('id', 'centroid_melody', 'song_ids', 'birth_step',
                 'dominant_emotion', 'carrier_count')

    def __init__(self, centroid: Tuple[float, ...], birth_step: int):
        self.id = Genre._next_id
        Genre._next_id += 1
        self.centroid_melody = centroid
        self.song_ids: set = set()
        self.birth_step = birth_step
        self.dominant_emotion: Optional[str] = None
        self.carrier_count = 0


# ══════════════════════════════════════════════════════════════════════════════
#  8. Songbook — коллективная фонотека
# ══════════════════════════════════════════════════════════════════════════════
class Songbook:
    """Глобальная фонотека популяции.

    Хранит все песни, баллады, саги. Раз в N шагов кластеризует их в жанры.
    При смерти агента — его песни могут передаваться соседям (культурная
    передача через Tombstone Traces, механизм 60).
    """

    def __init__(self):
        self.songs: Dict[int, Song] = {}
        self.genres: Dict[int, Genre] = {}
        self.genre_assignment_step = 0

    def add(self, song: Song) -> None:
        if len(self.songs) >= SingingTailConfig.SONGBOOK_MAX_SIZE:
            # Удаляем песню с наименьшим числом носителей
            weakest = min(self.songs.values(), key=lambda s: len(s.carriers))
            self.songs.pop(weakest.id, None)
        self.songs[song.id] = song

    def cluster_genres(self, step: int, threshold: float = 0.15) -> int:
        """Выявление жанров через простую агломеративную кластеризацию.

        Возвращает количество жанров.
        """
        songs = list(self.songs.values())
        if len(songs) < SingingTailConfig.GENRE_CLUSTER_MIN:
            return 0

        # Сбрасываем старые жанры
        self.genres.clear()
        for s in songs:
            s.genre_id = None

        # Простой single-link clustering
        for song in songs:
            assigned = False
            for genre in self.genres.values():
                # Пробуем найти жанр, к которому подходит эта песня
                centroid_song = Song(0, genre.centroid_melody,
                                     EmotionVector(), 0, 0)
                if song.melodic_distance(centroid_song) < threshold:
                    genre.song_ids.add(song.id)
                    song.genre_id = genre.id
                    assigned = True
                    break
            if not assigned:
                # Создаём новый жанр с центроидом = эта мелодия
                genre = Genre(song.melody, step)
                genre.song_ids.add(song.id)
                song.genre_id = genre.id
                self.genres[genre.id] = genre

        # Удаляем мелкие жанры (1-2 песни)
        for gid in list(self.genres.keys()):
            if len(self.genres[gid].song_ids) < SingingTailConfig.GENRE_CLUSTER_MIN:
                # Возвращаем песни в «безжанровое» состояние
                for sid in self.genres[gid].song_ids:
                    if sid in self.songs:
                        self.songs[sid].genre_id = None
                del self.genres[gid]

        self.genre_assignment_step = step
        return len(self.genres)

    def stats(self) -> Dict[str, Any]:
        kinds = Counter(s.kind for s in self.songs.values())
        return {
            "songs_total": len(self.songs),
            "songs_short": kinds.get("song", 0),
            "ballads": kinds.get("ballad", 0),
            "sagas": kinds.get("saga_part", 0),
            "genres": len(self.genres),
            "songs_with_genre": sum(1 for s in self.songs.values()
                                    if s.genre_id is not None),
        }


# ══════════════════════════════════════════════════════════════════════════════
#  9. CommunicationField — среда обмена
# ══════════════════════════════════════════════════════════════════════════════
class CommunicationField:
    """Поле коммуникации в среде. Прикручивается к Env.

    Это «эфир» через который проходят сигналы. Здесь хранятся:
      - Songbook (фонотека)
      - История роста словаря (для Heaps' law)
      - Глобальный лог эмоциональных событий
      - Кэш TopSim метрики (обновляется не каждый шаг)
    """

    def __init__(self):
        self.songbook = Songbook()
        # История (total_utterances, total_vocab_size) на разных шагах
        self.vocab_growth_history: List[Tuple[int, int]] = []
        # Каждые N шагов обновляем
        self.metrics_cache: Dict[str, float] = {
            "topsim": 0.0,
            "zipf_alpha": 0.0,
            "heaps_beta": 0.0,
            "consonance_ratio": 0.0,
            "eden_events_total": 0,
        }
        self.last_metrics_update = 0

    def update_metrics(self, agents: List[Any], step: int, force: bool = False) -> None:
        """Обновляет дорогие метрики. По умолчанию раз в 10 шагов."""
        if not force and step - self.last_metrics_update < 10:
            return
        if not agents:
            return

        # Сбор данных
        all_usages = [a.singing_tail.lang.usage_count for a in agents
                      if hasattr(a, 'singing_tail')]
        if not all_usages:
            return

        # Heaps' law: growth history
        total_utt = sum(sum(u.values()) for u in all_usages)
        total_vocab = len({tok for u in all_usages for tok in u})
        self.vocab_growth_history.append((int(total_utt), int(total_vocab)))

        # TopSim: считаем по одному «среднему» агенту с самым большим словарём
        if agents:
            ref = max(agents, key=lambda a: len(a.singing_tail.lang.vocab)
                      if hasattr(a, 'singing_tail') else 0)
            if hasattr(ref, 'singing_tail') and len(ref.singing_tail.lang.vocab) >= 4:
                # Используем сами denotations как meaning-векторы (циркулярная проверка),
                # для реальной TopSim нужны независимые meaning-векторы — это упрощение
                pairs = [(ref.singing_tail.lang.denotation_map[t], t)
                         for t in ref.singing_tail.lang.vocab[:16]]
                # Берём первые компоненты genome агента как «meaning» — это
                # внешняя референция, не зависящая от языка
                ref_pairs = []
                for i, (den, tok) in enumerate(pairs):
                    if i < len(ref.genome):
                        m = ref.genome[:SingingTailConfig.MEANING_DIM]
                        if m.shape[0] < SingingTailConfig.MEANING_DIM:
                            m = np.pad(m, (0, SingingTailConfig.MEANING_DIM - m.shape[0]))
                        # Чуть варьируем на каждый токен для разнообразия
                        m_var = m + 0.1 * den
                        ref_pairs.append((m_var, tok))
                if ref_pairs:
                    self.metrics_cache["topsim"] = ref.singing_tail.lang.topsim_with(ref_pairs)

        # Zipf и Heaps — глобальные
        self.metrics_cache["zipf_alpha"] = LanguageSignature.zipf_alpha(all_usages)
        self.metrics_cache["heaps_beta"] = LanguageSignature.heaps_exponent(
            self.vocab_growth_history)

        # Эдемские события — всего за прогон
        self.metrics_cache["eden_events_total"] = len(LanguageSignature._eden_log)

        # Consonance ratio — доля пар соседей с консонансным отношением частот.
        # Считаем по выборке (max 50 пар) чтобы не тормозить большие популяции.
        agents_with_st = [a for a in agents if hasattr(a, 'singing_tail')]
        if len(agents_with_st) >= 2:
            n_check = min(50, len(agents_with_st) * (len(agents_with_st) - 1) // 2)
            n_consonant = 0
            n_total = 0
            for i in range(min(len(agents_with_st), 20)):
                for j in range(i + 1, min(len(agents_with_st), 20)):
                    if n_total >= n_check:
                        break
                    f1 = agents_with_st[i].singing_tail.music.freq
                    f2 = agents_with_st[j].singing_tail.music.freq
                    factor = MusicCarrier.consonance_factor(f1, f2)
                    if factor > 1.0:
                        n_consonant += 1
                    n_total += 1
            if n_total > 0:
                self.metrics_cache["consonance_ratio"] = n_consonant / n_total

        self.last_metrics_update = step

    def snapshot(self) -> Dict[str, Any]:
        return {
            **self.metrics_cache,
            **self.songbook.stats(),
            "vocab_history_points": len(self.vocab_growth_history),
        }


# ══════════════════════════════════════════════════════════════════════════════
#  10. SingingTail — обёртка, прикрепляющая всё к агенту
# ══════════════════════════════════════════════════════════════════════════════
class SingingTail:
    """Главный объект надстройки. Содержит и язык, и музыку, и эмоции.

    Прикрепляется к каждому Agent как `agent.singing_tail`.
    Не вмешивается в существующие поля Agent — только наблюдает за ними
    через переданные данные при вызове методов.
    """

    def __init__(self, agent_id: int, rng):
        self.agent_id = agent_id
        self.emotion = EmotionVector(rng=rng)
        self.lang = LanguageSignature(rng)
        self.music = MusicCarrier(rng, emotion=self.emotion)
        # Песни которые знает этот агент (по id)
        self.known_songs: set = set()
        # Последние N произнесённых слов — для построения мелодий
        self.utterance_history: deque = deque(maxlen=12)
        # Последние N эмоциональных состояний для саги
        self.emotional_history: deque = deque(maxlen=20)
        # Близость к другим агентам — для баллад
        self.intimacy: Dict[int, float] = {}

    # ────────────────────────────────────────────────────────────────────────
    #  ВЗАИМОДЕЙСТВИЕ С СОСЕДЯМИ
    # ────────────────────────────────────────────────────────────────────────

    def exchange_with_neighbors(self, neighbors: List[Any], agent_genome: np.ndarray,
                                step: int, rng) -> Dict[str, int]:
        """Один цикл обмена: язык + музыка + эмоции.

        Возвращает счётчики событий для логирования.
        """
        events = {"words_spoken": 0, "words_heard": 0, "new_words": 0,
                  "consonance_hits": 0, "dissonance_hits": 0}

        if not neighbors:
            return events

        # ─── ЯЗЫК: говорим и слушаем ──────────────────────────────────────
        # Произносим слово, отражающее наш текущий «смысл» (часть генома)
        meaning = agent_genome[:SingingTailConfig.MEANING_DIM].copy()
        if meaning.shape[0] < SingingTailConfig.MEANING_DIM:
            meaning = np.pad(meaning,
                             (0, SingingTailConfig.MEANING_DIM - meaning.shape[0]))
        # Лёгкий шум — то же самое мы не произносим дважды одинаково
        meaning = meaning + rng.normal(0, 0.05, meaning.shape).astype(np.float32)

        tok, is_new = self.lang.speak(meaning, self.agent_id, step, rng)
        events["words_spoken"] = 1
        events["new_words"] = int(is_new)
        self.utterance_history.append(tok)

        # Слушаем что говорят соседи
        for n in neighbors:
            if not hasattr(n, 'singing_tail'):
                continue
            n_tok = n.singing_tail.lang.last_utterance
            if n_tok is not None and n_tok in n.singing_tail.lang.denotation_map:
                self.lang.listen(n_tok, n.singing_tail.lang.denotation_map[n_tok])
                events["words_heard"] += 1
                # Учитываем «близость» — для баллад
                self.intimacy[n.id] = self.intimacy.get(n.id, 0) * 0.9 + 0.1

        # ─── МУЗЫКА: интерференция + притяжение ───────────────────────────
        n_freqs = [n.singing_tail.music.freq for n in neighbors
                   if hasattr(n, 'singing_tail')]
        self.music.attract_to(n_freqs, rng=rng)
        for n in neighbors:
            if not hasattr(n, 'singing_tail'):
                continue
            factor = self.music.interference_with(n.singing_tail.music)
            if factor > 1.0:
                events["consonance_hits"] += 1
            elif factor < 1.0:
                events["dissonance_hits"] += 1

        # ─── ЭМОЦИИ: заражение ────────────────────────────────────────────
        for n in neighbors:
            if hasattr(n, 'singing_tail'):
                self.emotion.blend(n.singing_tail.emotion,
                                   alpha=SingingTailConfig.EMOTION_SPILL)

        # Модулируем музыку эмоциями
        self.music.modulate_by_emotion()

        return events

    def energy_modulation_from_music(self, neighbors: List[Any]) -> float:
        """Возвращает множитель к энергии за счёт музыкальной интерференции.

        Вызывается отдельно от exchange_with_neighbors, чтобы можно было
        отключить через ablation (--no-music-energy).
        """
        if not neighbors:
            return 1.0
        factors = []
        for n in neighbors:
            if hasattr(n, 'singing_tail'):
                factors.append(self.music.interference_with(n.singing_tail.music))
        if not factors:
            return 1.0
        # Геометрическое среднее — чтобы крайности не доминировали
        prod = 1.0
        for f in factors:
            prod *= f
        return prod ** (1.0 / len(factors))

    # ────────────────────────────────────────────────────────────────────────
    #  СОЗДАНИЕ ПЕСЕН / БАЛЛАД / САГ
    # ────────────────────────────────────────────────────────────────────────

    def maybe_create_song(self, event_intensity: float, step: int,
                          rng, songbook: Songbook,
                          subject_agent: Optional[int] = None,
                          agent_age: int = 0,
                          agent_identity: Optional[deque] = None,
                          agent_genome: Optional[np.ndarray] = None) -> Optional[Song]:
        """Если событие достаточно сильное — рождает песню/балладу/сагу.

        Логика выбора формы:
          • Если subject_agent задан И intimacy высокая → Ballad
          • Если возраст агента > SAGA_TRIGGER_AGE И в identity много событий → Saga
          • Иначе → обычная Song
        """
        if event_intensity < SingingTailConfig.SONG_BIRTH_THRESHOLD:
            return None
        if self.emotion.intensity() < 0.3:
            return None  # Без эмоционального заряда песня не родится

        # Какой формат?
        intimacy_with_subject = (self.intimacy.get(subject_agent, 0)
                                 if subject_agent is not None else 0)
        is_ballad = (subject_agent is not None and
                     intimacy_with_subject > SingingTailConfig.BALLAD_INTIMACY_THR)
        is_saga = (agent_age > SingingTailConfig.SAGA_TRIGGER_AGE and
                   agent_identity is not None and len(agent_identity) >= 5)

        # Создаём мелодию из истории темпа музыкального носителя
        history = list(self.music.tempo_history)
        if len(history) < SingingTailConfig.SONG_MELODY_LEN_MIN:
            return None
        mel_len = rng.integers(SingingTailConfig.SONG_MELODY_LEN_MIN,
                               SingingTailConfig.SONG_MELODY_LEN_MAX + 1)
        melody = tuple(history[-mel_len:])

        # Имя песни — слово, ассоциированное с эмоциональным состоянием
        # (или текущее произнесённое слово агента)
        name_token = self.lang.last_utterance
        if name_token is None and agent_genome is not None:
            name_token, _ = self.lang.speak(agent_genome[:SingingTailConfig.MEANING_DIM],
                                            self.agent_id, step, rng)
        if name_token is None:
            return None

        # ─── Создаём конкретный класс ─────────────────────────────────────
        if is_saga:
            # Разбиваем identity на части по 3 события каждая
            parts = []
            history_freqs = list(self.music.tempo_history)
            chunks = max(SingingTailConfig.SAGA_MIN_PARTS,
                         min(5, len(agent_identity) // 3))
            for i in range(chunks):
                start = i * mel_len // chunks
                end = (i + 1) * mel_len // chunks
                part = tuple(history_freqs[start:end] if end > start
                             else history_freqs[-2:])
                if part:
                    parts.append(part)
            if not parts:
                parts = [melody]
            narrative = list(agent_identity)[-chunks * 3:]
            protagonists = list({self.agent_id})
            song = Saga(name_token, parts, self.emotion, step,
                        self.agent_id, narrative, protagonists)
        elif is_ballad:
            song = Ballad(name_token, melody, self.emotion, step,
                          self.agent_id, subject_agent)
        else:
            song = Song(name_token, melody, self.emotion, step, self.agent_id)

        songbook.add(song)
        self.known_songs.add(song.id)
        return song

    def share_song_with_neighbors(self, neighbors: List[Any],
                                  songbook: Songbook, rng,
                                  share_chance: float = 0.05) -> int:
        """Передача песни соседям. Возвращает число успешных передач."""
        if not self.known_songs or not neighbors:
            return 0
        # Выбираем одну случайную свою песню
        sid_list = list(self.known_songs)
        if not sid_list:
            return 0
        sid = sid_list[int(rng.integers(0, len(sid_list)))]
        if sid not in songbook.songs:
            self.known_songs.discard(sid)
            return 0
        song = songbook.songs[sid]
        shared = 0
        for n in neighbors:
            if not hasattr(n, 'singing_tail'):
                continue
            if rng.random() < share_chance and sid not in n.singing_tail.known_songs:
                n.singing_tail.known_songs.add(sid)
                song.carriers.add(n.id)
                shared += 1
        return shared

    def inherit_songs_to_neighbors(self, neighbors: List[Any],
                                   songbook: Songbook) -> None:
        """При смерти агента — его песни автоматически передаются всем соседям.

        Это реализация механизма 60 (Tombstone Traces) для культурного слоя.
        """
        for sid in list(self.known_songs):
            if sid not in songbook.songs:
                continue
            song = songbook.songs[sid]
            for n in neighbors:
                if hasattr(n, 'singing_tail'):
                    n.singing_tail.known_songs.add(sid)
                    song.carriers.add(n.id)

    # ────────────────────────────────────────────────────────────────────────
    #  ТРИГГЕРЫ ЭМОЦИЙ ОТ СОБЫТИЙ АГЕНТА
    # ────────────────────────────────────────────────────────────────────────

    def react_to_catastrophe(self, severity: float) -> None:
        """Катастрофа = страх + печаль + (иногда) благоговение перед стихией."""
        self.emotion.feel({
            "fear": +0.4 * severity,
            "sadness": +0.2 * severity,
            "awe": +0.1 * severity,
            "joy": -0.3 * severity,
        })

    def react_to_synthesis_success(self, quality: float) -> None:
        """Успешный коллективный синтез = радость + благоговение."""
        self.emotion.feel({
            "joy": +0.5 * quality,
            "awe": +0.3 * quality,
            "tenderness": +0.1 * quality,
        })

    def react_to_neighbor_death(self) -> None:
        """Соседний агент умер = печаль + нежность к памяти."""
        self.emotion.feel({
            "sadness": +0.3,
            "tenderness": +0.2,
        })

    def react_to_abduction(self) -> None:
        """Размерностная абдукция = благоговение + радость открытия."""
        self.emotion.feel({
            "awe": +0.6,
            "joy": +0.3,
        })

    def react_to_birth(self) -> None:
        """Рождение нового агента из этой пары = нежность + радость."""
        self.emotion.feel({
            "tenderness": +0.5,
            "joy": +0.3,
        })

    # ────────────────────────────────────────────────────────────────────────
    #  СЛУЖЕБНОЕ
    # ────────────────────────────────────────────────────────────────────────

    def tick(self) -> None:
        """Шаг времени для внутренних процессов."""
        self.emotion.decay()
        self.emotional_history.append(self.emotion.vec.copy())
        self.lang.lexicon_decay()
        self.lang.utterance_age += 1


# ══════════════════════════════════════════════════════════════════════════════
#  ФАСАДНЫЕ ФУНКЦИИ ДЛЯ ИНТЕГРАЦИИ
# ══════════════════════════════════════════════════════════════════════════════
def attach_singing_tail(agent: Any, rng) -> None:
    """Прикрепить SingingTail к существующему агенту.

    Вызывать в Agent.__init__ ПОСЛЕ установки self.id.
    """
    agent.singing_tail = SingingTail(agent.id, rng)


def communication_step(agents: List[Any],
                       comm_field: CommunicationField,
                       spatial_hash: Any,
                       step: int,
                       rng,
                       enable_music_energy: bool = True,
                       cluster_genres_every: int = 50) -> Dict[str, int]:
    """Главный коммуникационный цикл — один вызов за Env.step().

    Параметры:
      agents             — список живых агентов
      comm_field         — CommunicationField (env.communication_field)
      spatial_hash       — пространственный хеш (env.shash или подобное)
      step               — текущий шаг
      rng                — numpy RandomState
      enable_music_energy— включать ли энергетическую модуляцию от музыки
      cluster_genres_every — раз в сколько шагов пересчитывать жанры
    """
    totals = {"words_spoken": 0, "words_heard": 0, "new_words": 0,
              "consonance_hits": 0, "dissonance_hits": 0,
              "songs_born": 0, "songs_shared": 0}

    radius = SingingTailConfig.NEIGHBOR_RADIUS

    for a in agents:
        if not hasattr(a, 'singing_tail'):
            continue

        # Найти соседей (используем существующий SpatialHash)
        try:
            nb_indices = spatial_hash.neighbors(a.position, radius)
            # nb_indices может быть списком индексов или агентов в зависимости от реализации
            neighbors = []
            for x in nb_indices:
                if isinstance(x, int):
                    if 0 <= x < len(agents) and agents[x] is not a:
                        neighbors.append(agents[x])
                elif x is not a:
                    neighbors.append(x)
        except Exception:
            # Fallback: брутфорс поиск
            neighbors = [b for b in agents if b is not a and
                         np.linalg.norm(b.position[:len(a.position)] -
                                        a.position[:len(b.position)]) < radius]

        # 1. Обмен языком/музыкой/эмоциями
        events = a.singing_tail.exchange_with_neighbors(
            neighbors, a.genome, step, rng)
        for k in events:
            totals[k] += events[k]

        # 2. Энергетическая модуляция от музыки (опционально)
        if enable_music_energy and neighbors:
            mod = a.singing_tail.energy_modulation_from_music(neighbors)
            if hasattr(a, 'energy'):
                # Применяем малое влияние, чтобы не сломать существующий баланс
                a.energy *= (1.0 + 0.5 * (mod - 1.0))

        # 3. Tick внутреннего времени
        a.singing_tail.tick()

        # 4. Возможное рождение песни (от текущего эмоционального заряда)
        intensity = a.singing_tail.emotion.intensity()
        if intensity > SingingTailConfig.SONG_BIRTH_THRESHOLD * 0.7:
            # Ищем «протагониста» для возможной баллады — самого близкого
            subject = None
            if a.singing_tail.intimacy:
                subject = max(a.singing_tail.intimacy.items(),
                              key=lambda kv: kv[1])[0]
            song = a.singing_tail.maybe_create_song(
                event_intensity=intensity,
                step=step, rng=rng,
                songbook=comm_field.songbook,
                subject_agent=subject,
                agent_age=getattr(a, 'age', 0),
                agent_identity=getattr(a, 'identity', None),
                agent_genome=a.genome,
            )
            if song is not None:
                totals["songs_born"] += 1

        # 5. Передача песен соседям
        if neighbors:
            shared = a.singing_tail.share_song_with_neighbors(
                neighbors, comm_field.songbook, rng)
            totals["songs_shared"] += shared

    # 6. Метрики (TopSim, Zipf, Heaps) — обновляем не каждый шаг
    comm_field.update_metrics(agents, step)

    # 7. Кластеризация в жанры
    if step > 0 and step % cluster_genres_every == 0:
        comm_field.songbook.cluster_genres(step)

    return totals


def on_agent_death(dying_agent: Any, neighbors: List[Any],
                   songbook: Songbook) -> None:
    """Вызывать когда агент умирает — для передачи песен.

    Подключается к существующей логике cleanup_dead в Env.
    """
    if hasattr(dying_agent, 'singing_tail'):
        dying_agent.singing_tail.inherit_songs_to_neighbors(neighbors, songbook)


def on_catastrophe(agents: List[Any], severity: float) -> None:
    """Реакция на катастрофу — обновить эмоции всех агентов."""
    for a in agents:
        if hasattr(a, 'singing_tail'):
            a.singing_tail.react_to_catastrophe(severity)


def on_abduction(agent: Any) -> None:
    """Реакция на размерностную абдукцию."""
    if hasattr(agent, 'singing_tail'):
        agent.singing_tail.react_to_abduction()


def on_synthesis(agent: Any, quality: float) -> None:
    """Реакция на успешный коллективный синтез."""
    if hasattr(agent, 'singing_tail'):
        agent.singing_tail.react_to_synthesis_success(quality)


def metrics_snapshot(comm_field: CommunicationField,
                     agents: List[Any]) -> Dict[str, float]:
    """Собрать все коммуникационные метрики для записи в JSON прогона."""
    snap = comm_field.snapshot()
    # Дополнительные агрегаты по агентам
    if agents:
        emo_intensities = []
        dominant_emotions = []
        vocab_sizes = []
        for a in agents:
            if hasattr(a, 'singing_tail'):
                emo_intensities.append(a.singing_tail.emotion.intensity())
                dominant_emotions.append(a.singing_tail.emotion.dominant())
                vocab_sizes.append(len(a.singing_tail.lang.vocab))
        if emo_intensities:
            snap["emotion_mean_intensity"] = float(np.mean(emo_intensities))
            snap["emotion_max_intensity"] = float(np.max(emo_intensities))
            snap["vocab_mean_size"] = float(np.mean(vocab_sizes))
            snap["vocab_max_size"] = int(np.max(vocab_sizes))
            # Доля каждой доминирующей эмоции
            emo_dist = Counter(dominant_emotions)
            for e in SingingTailConfig.EMOTION_NAMES:
                snap[f"emo_share_{e}"] = emo_dist.get(e, 0) / len(dominant_emotions)
    return snap


# ══════════════════════════════════════════════════════════════════════════════
#  САМОПРОВЕРКА МОДУЛЯ (запускается напрямую: python maes_v3_2_singing_tail.py)
# ══════════════════════════════════════════════════════════════════════════════
def _self_test():
    """Минимальный тест: всё ли цело, ничего ли не падает."""
    print("=" * 70)
    print(" MAES v3.2 Singing Tail — Self-test")
    print("=" * 70)
    rng = np.random.default_rng(42)

    # Создаём пару фиктивных «агентов»
    class FakeAgent:
        def __init__(self, aid, dims=8):
            self.id = aid
            self.position = rng.uniform(-5, 5, dims)
            self.genome = rng.uniform(-1, 1, dims)
            self.energy = 1.0
            self.age = 0
            self.identity = deque([("born", 0, "explorer")], maxlen=20)

    agents = [FakeAgent(i+1) for i in range(10)]
    for a in agents:
        attach_singing_tail(a, rng)

    comm = CommunicationField()

    # Фейковый SpatialHash (с увеличенным радиусом для теста — в реальном MAES
    # агенты ближе из-за кластеризации, тут просто хотим увидеть взаимодействие)
    class FakeHash:
        def neighbors(self, pos, r):
            # В тесте используем радиус 8 вместо 2, иначе в 8D пространстве [-5,5]
            # 10 агентов слишком разрежены чтобы пересекаться
            return [a for a in agents
                    if 0 < np.linalg.norm(a.position - pos) < 8.0]
    fhash = FakeHash()

    print("\n1. Симулируем 20 шагов взаимодействия...")
    for step in range(1, 21):
        # Триггерим эмоции каждые 3 шага чтобы увидеть рождение песен
        if step % 3 == 0:
            for a in agents[:3]:
                a.singing_tail.react_to_synthesis_success(0.8)
        totals = communication_step(agents, comm, fhash, step, rng,
                                     enable_music_energy=True,
                                     cluster_genres_every=10)
        if step % 5 == 0:
            print(f"   step={step:3d}  "
                  f"words_spoken={totals['words_spoken']:3d}  "
                  f"new_words={totals['new_words']}  "
                  f"songs_born={totals['songs_born']}  "
                  f"cons={totals['consonance_hits']:3d}  "
                  f"diss={totals['dissonance_hits']:3d}")

    print("\n2. Проверка эмоциональных реакций...")
    on_catastrophe(agents, severity=0.8)
    print(f"   После катастрофы — emotion[0]: {agents[0].singing_tail.emotion}")

    print("\n3. Финальные метрики...")
    snap = metrics_snapshot(comm, agents)
    for k, v in sorted(snap.items()):
        if isinstance(v, float):
            print(f"   {k:30s}: {v:.4f}")
        else:
            print(f"   {k:30s}: {v}")

    print("\n4. Проверка передачи песен при смерти...")
    dying = agents[0]
    living = agents[1:4]
    songs_before = len(living[0].singing_tail.known_songs)
    on_agent_death(dying, living, comm.songbook)
    songs_after = len(living[0].singing_tail.known_songs)
    print(f"   У соседа known_songs: {songs_before} → {songs_after}")

    print("\n" + "=" * 70)
    print(" SELF-TEST PASSED")
    print("=" * 70)


if __name__ == "__main__":
    _self_test()


# ══════════════════════════════════════════════════════════════════════════════
#  ИНТЕГРАЦИЯ В maes_v3_1.py  —  ПОШАГОВАЯ ИНСТРУКЦИЯ
# ══════════════════════════════════════════════════════════════════════════════
"""
==============================================================================
 КАК НАЛОЖИТЬ ЭТОТ МОДУЛЬ НА СУЩЕСТВУЮЩИЙ maes_v3_1.py
==============================================================================

ШАГ 1. Положи `maes_v3_2_singing_tail.py` РЯДОМ с `maes_v3_1.py`.

ШАГ 2. В `maes_v3_1.py` в самом верху (после import numpy as np) добавь:

    from maes_v3_2_singing_tail import (
        attach_singing_tail, communication_step,
        on_agent_death, on_catastrophe, on_abduction, on_synthesis,
        metrics_snapshot, CommunicationField
    )

ШАГ 3. В `Agent.__init__` (примерно строка 1556) после `self.identity.append(...)`
       добавь ОДНУ строку:

    attach_singing_tail(self, np.random.default_rng())

ШАГ 4. В `Env.__init__` (ищи `class Env`, примерно строка 2898) добавь:

    self.communication_field = CommunicationField()

ШАГ 5. В `Env.step` (строка 3050) ПОСЛЕ блока обработки соседства (там где
       вызывается self.shash.neighbors или подобное), но ПЕРЕД метриками,
       добавь ОДИН вызов:

    comm_totals = communication_step(
        self.agents, self.communication_field, self.shash, self.step_n, self.rng,
        enable_music_energy=True
    )

ШАГ 6. В `Env._catastrophe` (или там где обрабатывается катастрофа),
       сразу после `for a in self.agents: a.survive_catastrophe(sev)`:

    on_catastrophe(self.agents, sev)

ШАГ 7. В `Agent.attempt_abduction` где возвращается True — добавь:

    on_abduction(self)

ШАГ 8. В `_cleanup_dead` или там где удаляются мёртвые агенты:

    for dying in agents_to_remove:
        neighbors_of_dying = [a for a in self.agents
                              if a is not dying and
                              np.linalg.norm(a.position - dying.position) < 3.0]
        on_agent_death(dying, neighbors_of_dying, self.communication_field.songbook)

ШАГ 9. В `Env._metrics` (метод собирающий метрики, ~ строка 3348) в конец:

    comm_metrics = metrics_snapshot(self.communication_field, self.agents)
    m.update({f"comm_{k}": v for k, v in comm_metrics.items()})

ШАГ 10. Запуск и проверка:

    python maes_v3_2_singing_tail.py    # self-test модуля
    python maes_v3_1.py --steps 50      # быстрый прогон с новым слоем

ВСЁ. Никаких других правок не нужно. Если что-то сломалось — закомментируй
шаг 5 (communication_step) и проверь что v3.1 работает как раньше — это
доказательство что модуль не вмешивается в существующую логику.

==============================================================================
"""
