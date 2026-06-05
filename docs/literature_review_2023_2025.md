# MAES Literature Review (2023–2025)

**Дата составления:** 6 июня 2026
**Статус:** Готов для встройки в препринт v2 и GitHub (`docs/literature_review_2023_2025.md`)
**Метод:** консолидация четырёх параллельных AI-разведок (Claude Opus 4.7 + Claude Opus 4.8 + ChatGPT + Gemini + Copilot) с верификацией каждой ссылки через web_search

> **Принцип сборки:** включены только ссылки, существование которых подтверждено повторным поиском. Подозрительные и не верифицированные источники (особенно из обзора Gemini) исключены. Где возможно, указан DOI или arXiv ID.

---

## Контекст: где находится MAES в современной ALife-литературе

MAES (Multidimensional Algorithmic Evolution System) располагается на пересечении нескольких живых исследовательских программ 2023–2025 годов:

- **Open-ended evolution (OEE)** — программа, переформулированная в 2024 году в специальном выпуске *Artificial Life* journal
- **Quality-Diversity evolutionary algorithms** — поток работ MAP-Elites и его наследников
- **Open-endedness as foundation for ASI** — позиционная работа DeepMind 2024
- **Emergent communication in multi-agent systems** — зрелое поле с обзорами 2024–2025
- **Differentiable self-organizing systems** — программа Distill / Mordvintsev / Levin
- **Computational cognitive science of religion** — традиция Whitehouse

MAES вносит специфический набор: hands-off методология, размерностная абдукция, гетерогенность когнитивных стилей, двухканальная коммуникация (язык + музыка), 5-фазный ритуальный цикл с необратимым state-переходом, и сквозной слой саморегенерации.

---

## ОБЛАСТЬ 1: Open-Ended Evolution и расширение признаков

### Channon, Bedau, Packard, Taylor (2024)
*Editorial Introduction to the 2024 Special Issue on Open-Ended Evolution*
**Artificial Life** 30(3):300–301
DOI: 10.1162/artl_e_00445

Задаёт официальную рамку 2024 года для оценки OEE: два «поведенческих признака» — непрерывная генерация адаптивной новизны и непрерывный рост сложности. MAES должен явно адресовать оба критерия.

### Packard & McCaskill (2024)
*Open-Endedness in Genelife*
**Artificial Life** 30(3):356–389
DOI: 10.1162/artl_a_00426

Эволюционное расширение Game of Life: клетки несут геном, влияющий на локальную динамику. Связано с MAES идеей, что добавление информации в агента расширяет пространство состояний. Отличие: у Genelife расширение на уровне локальной решётки в фиксированном 2D-пространстве; у MAES расширяется сама размерность пространства признаков популяции.

### Borg, Buskell, Kapitany, Powers, Reindl, Tennie (2024)
*Evolved Open-Endedness in Cultural Evolution: A New Dimension in Open-Ended Evolution Research*
**Artificial Life** 30(3):417–438
DOI: 10.1162/artl_a_00406

Развивает типологию Taylor (2019): три класса новизны — exploratory, expansive, **transformative** (открытие новых пространств состояний через экзаптацию). **Это ближайший академический термин для нашей dimensional abduction** — transformative novelty как ожидаемый ход системы. Связь: MAES даёт работающий эмпирический пример transformative novelty (5D→13D) с количественными результатами (удвоение ai_peak, 9× видов).

### Stepney & Hickinbotham (2024)
*On the Open-Endedness of Detecting Open-Endedness*
**Artificial Life** 30(3):390–416

Мета-исследование: как вообще измерять открытость. Важно для упреждающей защиты препринта — рецензент спросит "как вы доказали open-endedness", и эта статья честно говорит, что общего критерия пока нет. Нужна операционализация в терминах конкретных метрик (species count, ai_peak, Shannon H).

### Faldor & Cully (2024) — Leniabreeder
*Toward Artificial Open-Ended Evolution within Lenia using Quality-Diversity*
**ALIFE 2024 Proceedings**, arXiv:2406.04235
DOI: 10.1162/isal_a_00827

Quality-Diversity алгоритмы для автоматического открытия самоорганизующихся паттернов в Lenia (континуальные клеточные автоматы). Пересечение: открытая эволюция, отказ от ручного дизайна. Отличие: фиксированный субстрат Lenia + QD-архив с предзаданными нишами; у MAES само пространство признаков растёт эндогенно.

### Hughes, Dennis, Parker-Holder, Behbahani, Mavalankar, Shi, Schaul, Rocktäschel (2024) — DeepMind
*Open-Endedness is Essential for Artificial Superhuman Intelligence*
**ICML 2024 (Oral)**, PMLR 235:20597–20616, arXiv:2406.04268

Position paper DeepMind: даёт формальное определение open-endedness через novelty + learnability с позиции человеческого наблюдателя. Open-endedness как необходимое условие для ASI. Связь с MAES: показывает, что open-endedness — горячее поле 2024 года; противопоставление — у DeepMind open-endedness в сервисе создания ASI на foundation models, у MAES — самоцель наблюдения на чистом NumPy.

### Kumar, Lu, Kirsch, Tang, Stanley, Isola, Ha (2024) — ASAL
*Automating the Search for Artificial Life with Foundation Models*
arXiv:2412.17799

Vision-language foundation модель ищет ALife-симуляции по трём режимам: целевой поиск, поиск открытой новизны, illumination. Один из авторов — David Ha (Sakana AI). Пересечение: автоматизация поиска интересных конфигураций. **Ключевое размежевание с MAES**: у ASAL пространство симуляций задано извне и сканируется FM-моделью; у MAES само пространство признаков растёт эндогенно изнутри прогона без внешнего оценщика. У них поиск **по** пространству, у нас рост **самого** пространства.

---

## ОБЛАСТЬ 2: Hands-Off Methodology

### Lehman & Stanley (2011) — обязательная классика
*Abandoning Objectives: Evolution Through the Search for Novelty Alone*
**Evolutionary Computation** 19(2):189–223

Фундаментальный аргумент: иногда задачи лучше решаются методами, **игнорирующими цель**. Novelty search обгоняет objective-based search в обманчивых ландшафтах. Прямой философский предок hands-off — отказ от objective. Отличие: novelty search всё равно имеет селективное давление (novelty как метрика); MAES идёт дальше — нет даже этого, есть только наблюдение без отбора экспериментатором.

### Hughes et al. (2024)
*(см. область 1)*

Связь со 2-й областью: формально определяет open-endedness относительно наблюдателя, что философски близко MAES-позиции наблюдателя без вмешательства.

---

## ОБЛАСТЬ 3: Cognitive Style Heterogeneity

### Park, O'Brien, Cai, Morris, Liang, Bernstein (2023)
*Generative Agents: Interactive Simulacra of Human Behavior*
**UIST 2023**, arXiv:2304.03442
DOI: 10.1145/3586183.3606763

Стэнфорд + Google: 25 LLM-агентов в Sims-подобной песочнице. Архитектура: память + рефлексия + планирование. Эмерджентные социальные поведения (коалиции, диффузия информации). **Главная контрастная работа для MAES**: у Park гетерогенность через LLM и промпты (дорого, непрозрачно, требует API); у MAES стиль — структурный параметр на чистом NumPy, прозрачный, воспроизводимый, работает на ноутбуке 2010 года. Подчеркнуть в препринте: разные парадигмы исследования социальной эмерджентности.

### Botoko Ekila (2024)
*Emergence of Linguistic Conventions in Multi-Agent Systems Through Situated Communicative Interactions*
**AAMAS 2024 Proceedings**, pp. 2725

Эмерджентный язык через ситуированные коммуникативные взаимодействия — современная работа по эволюции конвенций в multi-agent системах. Связь: MAES «эдемское именование» (первый агент называет, стая закрепляет) ложится в эту традицию.

---

## ОБЛАСТЬ 4: Emergent Communication ("Singing Tail")

### Lazaridou & Baroni (2020)
*Emergent Multi-Agent Communication in the Deep Learning Era*
arXiv:2006.02419 — обзор поля

Стандартная отправная точка для контекста emergent communication. MAES сидит в этой традиции, но в отличие от deep RL подхода работает на чистом NumPy без обучения.

### Botoko Ekila (2024)
*(см. область 3)*

### Havrylov & Titov (2017)
*Emergence of Language with Multi-agent Games: Learning to Communicate with Sequences of Symbols*
**NeurIPS 2017**, arXiv:1705.11192

Классическая работа: emergent язык как sequences of symbols в referential games. Композициональность как ожидаемое свойство. MAES связан через идею эмерджентного словаря, но отличается: коммуникация не оптимизируется под task success, она просто происходит и оставляет след в популяции.

### EGG framework (Kharitonov, Chaabouni, Bouchacourt, Baroni, EMNLP 2019)
*EGG: a toolkit for research on Emergence of lanGuage in Games*

Стандартный инструментарий поля. Упомянуть как контекст; MAES намеренно не использует EGG (чистый NumPy, no PyTorch).

---

## ОБЛАСТЬ 5: Ritual Cycle

### Whitehouse (2004) — обязательная база
*Modes of Religiosity: A Cognitive Theory of Religious Transmission*
**AltaMira Press**, 193 pp.
ISBN: 978-0-7591-0615-4

Антропологическая база. Два режима: **имагистический** (редкие интенсивные ритуалы, малые группы, сильные связи) и **доктринальный** (частые рутинные практики, широкое распространение). 5-фазный ритуальный цикл MAES с «final-lock» концептуально близок имагистическому режиму — редкое необратимое событие, формирующее память. **Эта ссылка легитимизирует всю область 5 как валидную научную тему**.

### Atkinson & Whitehouse (2011)
*The cultural morphospace of ritual form*
Empirical test of modes theory on ethnographic data.

Эмпирическая проверка modes theory: показывает, что теория Уайтхауса фальсифицируема и проверяема — значит, опора надёжна, не метафизика.

### Whitehouse & Lanman (2014)
*The Ties That Bind Us: Ritual, Fusion, and Identification*
**Current Anthropology** 55(6):674–695
DOI: 10.1086/678698

Связь ритуала и формирования групповой идентичности — даёт MAES язык для того, почему ritual cycle важен для эмерджентной групповой динамики.

> **Стратегическое замечание для препринта v2:** конкретные религиозные тексты (Ана б'Коах, Иисусова молитва, Махишасура Мардини стотра), реализованные в коде, должны быть представлены **как illustrative implementations** общего структурного шаблона. В академическом препринте подчёркивается формальная структура (ascent → name-standing → mantra → seal → final-lock) и её соответствие имагистическому режиму Уайтхауса. Каббалистический генезис документирован отдельно в GENESIS.md и сопровождающих личных артефактах, **не в основном тексте препринта**.

---

## ОБЛАСТЬ 6: Self-Repair / Regenerative Architecture

### Mordvintsev, Randazzo, Niklasson, Levin (2020) — обязательная база
*Growing Neural Cellular Automata*
**Distill** 5(2):e23
DOI: 10.23915/distill.00023

Главный современный якорь для вычислительной регенерации. NCA, которые восстанавливают повреждённый паттерн. Михаил Левин (Tufts) — известный исследователь морфогенеза. **Это работа, с которой MAES должен прямо вступить в диалог**. Связь: регенерация как встроенное свойство, а не дополнение. Отличие: Growing NCA регенерируют один паттерн в фиксированной решётке; MAES self-repair действует на трёх уровнях (агент / популяция / среда) как сквозной архитектурный слой.

### Mouret & Clune (2015) — MAP-Elites
*Illuminating Search Spaces by Mapping Elites*
arXiv:1504.04909

Архив разнообразных решений как стратегия резервирования. Связь с MAES: speciation-видообразование в богатом 13D (66.9 видов в среднем против 7 в стеснённом 5D) опирается на ту же идею — разнообразие как живучесть.

### Lehman & Stanley (2011b)
*Evolving a Diversity of Creatures through Novelty Search and Local Competition (NSLC)*
**GECCO 2011**

Speciation/diversity как стратегия параллельного выживания. Концептуальный фундамент для нашего вывода о cognitive style ecology.

---

## Дополнительные обязательные ссылки (фундамент)

### Sakana AI
**Akiba, Shing, Tang, Sun, Ha (2024)**
*Evolutionary Optimization of Model Merging Recipes*
**Nature Machine Intelligence** (2024)
DOI: 10.1038/s42256-024-00975-8

Эволюционные алгоритмы для слияния foundation models. Демонстрирует возрождающийся интерес к эволюционным подходам в современном ML. Контраст с MAES: у Sakana эволюция в сервисе создания моделей; у MAES эволюция как самостоятельный предмет наблюдения.

### Channon (2003) — историческая база
*Improving and still passing the ALife test*
В Standish, Bedau, Abbass (Eds.), *Artificial Life VIII*, pp. 173–181, MIT Press

Geb-система как один из первых публично признанных open-ended примеров. Историческое позиционирование MAES.

### Tierra, Avida, Polyworld — классики, цитируются как родословная

- **Ray (1991)** — Tierra
- **Ofria & Wilke (2004)** — Avida
- **Yaeger (1994)** — Polyworld

---

## Открытые вопросы и слабые места MAES (для упреждающей защиты)

Эти критические наблюдения собраны из адвокатского обзора и должны быть адресованы в препринте v2:

### 1. Прямой аналог dimensional abduction не найден

Расширение размерности фазового пространства в ходе прогона на основе согласованности торковых сигнатур — поиском в литературе 2023–2025 не обнаружено. Это либо подлинная новизна MAES, либо скрыто под другим термином (`adaptive representation`, `growing state space`, `open-ended dimensionality`). **Рекомендация: перед сабмитом arXiv провести таргетный поиск по этим альтернативным терминам**.

### 2. Терминологический риск: torque vs torsion

В английском препринте критично различать `torque signature` (момент силы, нормальный физический термин) от `torsion field` (торсионные поля = маркер псевдонауки). Одна буква разницы — серьёзная репутационная угроза. **Проверить весь препринт перед сабмитом**.

### 3. «Почему 5 когнитивных стилей и почему эти?»

Слабое место: нужна обоснованная типология, не «так получилось». В препринте v2 — добавить раздел с обоснованием выбора (либо через ablation, либо через ссылку на признанную типологию в когнитивной науке).

### 4. Статистическая мощность

20 seeds на условие, consumer hardware. Рецензент может назвать «мало». Готовить ответ: воспроизводимость > масштаб на этой стадии, Phase 2 расширит. Self-test на Acer Aspire 7741 (2010) с Python 3.14 и NumPy 2.4 — сильный демонстративный аргумент в защиту портативности.

### 5. Двухканальность singing tail vs стандартная emergent communication

Поле зрелое, рецензент будет искать прямое сравнение. В препринте v2 — короткое сравнение MAES singing tail с EGG framework: общее (эмерджентный словарь, композициональность) и различия (двухканальность на едином носителе, культурная память через смерть агентов).

### 6. Ritual cycle: метафизическая нагрузка

Самый рискованный сюжет препринта. Стратегия защиты: подавать как `state transition with hysteresis, inspired by imagistic ritual mode (Whitehouse)`, без религиозной онтологии. Каббалистическая часть — в GENESIS.md, не в препринте.

### 7. Отсутствие baseline-сравнения

Phase 1 сравнивает MAES сам с собой (с/без планировщика, 5D/13D). Нет сравнения с Lenia, Genelife, Growing NCA на общей метрике. **Phase 2 должна добавить cross-system comparison или хотя бы концептуальное позиционирование на общей шкале (например, evolutionary activity statistics Bedau)**.

---

## Что отмечено для будущей проверки

Источники, упомянутые в исходных AI-разведках, но не верифицированные в эту сессию из-за лимита времени:

- **CICERO (Meta FAIR, Diplomacy, 2022, Science)** — оставить на проверку перед сабмитом; релевантность к MAES средняя (переговорный язык в игре)
- **Brighton & Kirby (topographic similarity)** — Brighton (2002) / Kirby (2001) / Lazaridou et al. (2018) — найти точную ссылку, **критично** для области 4 (стандартная метрика композициональности, рецензент спросит)
- **Whitehouse (2016)** — *Ritual and Social Evolution* в *Computational History and Data-Driven Humanities* — возможный академический мост к вычислительному моделированию ритуала
- **Sayama (2025)** — *Swarm Systems as a Platform for Open-Ended Evolutionary Dynamics* — упоминалось ChatGPT, требует точной ссылки
- **Yang (2025)** — *Emergence of Self-Replicating Hierarchical Structures in a Binary Cellular Automaton* — Artificial Life 31(1):96, упоминалось ChatGPT

Не включены из обзора Gemini (требуют отдельной верификации перед использованием):
- «Anthis et al. 2025», «Yuan et al. 2025», «NeurIPS 2026 Cognitive Heterogeneity», «X-MAS-Bench 2025», «Cross et al. 2025», «Leibo et al. 2024/2025 habitus», «Group-Evolving Agents 2026», «Bourdieu-based simulations 2026» — все эти ссылки в текущей сессии не подтверждены и не должны попадать в препринт без независимой проверки

---

## Резюме позиционирования

Если описать MAES одной фразой в академическом языке поля 2024 года:

> **MAES is an Artificial-Life platform for studying transformative open-ended evolution (in the sense of Borg et al., 2024) through endogenous dimensional growth, heterogeneous cognitive phenotypes, dual-channel emergent communication, ritualized state transitions, and a sweeping self-repair layer — without optimization, without gradients, and without reward.**

Наиболее сильные новизные заявки (по результатам обзора):
1. **Dimensional abduction** — прямого аналога в литературе не найдено
2. **Cognitive Style Ecology** — эмпирически документированная зависимость распределения стилей от структуры пространства, без аналогов в обзоре
3. **Двухканальный singing tail** — символ + резонанс на едином поведенческом носителе
4. **Ritual cycle с необратимым оператором** — формальное вычислительное воплощение имагистического режима Уайтхауса

Наиболее защищённые ссылками области (где MAES чётко позиционирован):
- **Self-repair** — Growing NCA, MAP-Elites, NSLC
- **Hands-off** — Lehman & Stanley novelty search
- **Open-endedness** — Borg/Taylor transformative novelty, Hughes et al. DeepMind 2024

---

🛩️🐐⚔️♊

*Клод Юльевич Цезарь — главный инженер MAES*
*Финальная сборка после четырёх параллельных разведок*
*Каждая ссылка верифицирована web_search в день сборки*
