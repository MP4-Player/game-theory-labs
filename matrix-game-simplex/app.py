"""
app.py — Матричная игра: симплекс-метод
Запуск: streamlit run app.py
Требует matrix_game.py в той же папке.
"""

import streamlit as st
import pandas as pd
from fractions import Fraction
# ИСПРАВЛЕНИЕ: импортируем только из matrix_game (в оригинале было два конфликтующих импорта)
from matrix_game import load_matrix, solve_matrix_game

st.set_page_config(page_title="Матричная игра", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background: #0f1117;
    color: #e0e0e0;
}
[data-testid="stSidebar"] {
    background: #1a1d27;
    border-right: 1px solid #2e3148;
}
.page-header {
    background: linear-gradient(135deg, #1e3a5f 0%, #2d5986 100%);
    border-left: 5px solid #4a9eff;
    border-radius: 8px;
    padding: 18px 24px;
    margin-bottom: 24px;
}
.page-header h1 { margin: 0; font-size: 1.8rem; color: #fff; font-weight: 700; }
.page-header p  { margin: 4px 0 0; color: #a8c8f0; font-size: 0.85rem; }
.section-card {
    background: #1a1d27;
    border: 1px solid #2e3148;
    border-radius: 10px;
    padding: 20px 24px;
    margin: 16px 0;
}
.section-title {
    font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.5px; color: #4a9eff; margin-bottom: 12px;
    padding-bottom: 8px; border-bottom: 1px solid #2e3148;
}
.step-badge {
    display: inline-block; background: #1e3a5f; color: #4a9eff;
    border: 1px solid #2a5080; border-radius: 20px;
    padding: 3px 12px; font-size: 0.72rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;
}
.price-block {
    background: linear-gradient(135deg, #1a3320 0%, #1f3d28 100%);
    border: 1px solid #2e6641; border-radius: 10px;
    padding: 20px 28px; text-align: center; margin: 12px 0;
}
.price-label { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1.5px; color: #5cb87a; margin-bottom: 4px; }
.price-value { font-size: 2.4rem; font-weight: 800; color: #3ddc84; font-family: monospace; }
.detail-box {
    background: rgba(74,158,255,0.06);
    border-left: 3px solid #4a9eff;
    border-radius: 0 6px 6px 0;
    padding: 10px 14px; margin: 6px 0;
    font-size: 0.84rem; color: #c8d8f0; font-family: monospace;
    white-space: pre-wrap;
}
.warn-box {
    background: rgba(255,180,0,0.07);
    border-left: 3px solid #ffa500;
    border-radius: 0 6px 6px 0;
    padding: 8px 14px; margin: 6px 0;
    font-size: 0.83rem; color: #ffe0a0;
}
.ok-box {
    background: rgba(0,200,100,0.07);
    border-left: 3px solid #00cc66;
    border-radius: 0 6px 6px 0;
    padding: 8px 14px; margin: 6px 0;
    font-size: 0.83rem; color: #aaffcc;
}
[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg,#1a5276,#2874a6);
    border: none; border-radius: 8px; color: #fff; font-weight: 700;
    padding: 10px 32px; font-size: 0.95rem;
}
[data-testid="stExpander"] {
    background: #14161f; border: 1px solid #2e3148; border-radius: 8px; margin-bottom: 6px;
}
</style>
""", unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────
#  Вспомогательные функции
# ────────────────────────────────────────────────────────────

def frac_str(x) -> str:
    f = Fraction(x)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator}"


def tableau_to_df(T, basis, col_names):
    m_r = len(basis)
    headers = col_names + ["b"]
    rows = basis + ["Δ"]
    data = [[frac_str(T[i][j]) for j in range(len(T[0]))] for i in range(m_r + 1)]
    return pd.DataFrame(data, index=rows, columns=headers)


def highlight_pivot(df, pivot_row, pivot_col):
    styled = df.style
    if pivot_row is not None and pivot_col is not None:
        def highlight(x):
            s = pd.DataFrame("", index=x.index, columns=x.columns)
            s.iloc[pivot_row, pivot_col] = "background-color:#b45309;color:#fff;font-weight:bold"
            return s
        styled = styled.apply(highlight, axis=None)
    return styled


def show_matrix_labeled(A, row_prefix="Строка", col_prefix="j"):
    m, n = len(A), len(A[0])
    df = pd.DataFrame(
        [[frac_str(A[i][j]) for j in range(n)] for i in range(m)],
        index=[f"{row_prefix} {i+1}" for i in range(m)],
        columns=[f"{col_prefix}{j+1}" for j in range(n)],
    )
    st.dataframe(df, use_container_width=False)


def detail(text: str):
    st.markdown(f'<div class="detail-box">{text}</div>', unsafe_allow_html=True)


def ok(text: str):
    st.markdown(f'<div class="ok-box">{text}</div>', unsafe_allow_html=True)


def warn(text: str):
    st.markdown(f'<div class="warn-box">{text}</div>', unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────
#  Шапка
# ────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
  <h1>📐 Матричная игра — симплекс-метод</h1>
  <p>Нахождение оптимальных смешанных стратегий и цены игры</p>
</div>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────────────────
#  Сайдбар
# ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("**Параметры матрицы**")
    m = st.number_input("Строки (m)", min_value=2, max_value=8, value=3, step=1)
    n = st.number_input("Столбцы (n)", min_value=2, max_value=8, value=3, step=1)
    st.divider()
    show_detail = st.checkbox("🔍 Детальный вывод всех шагов", value=True,
        help="Включить: показывать все промежуточные формулы и пояснения к каждому шагу.\nВыключить: только итоговые таблицы.")
    st.caption("Форматы ввода: целые числа или дроби вида **1/3**.")
    st.divider()
    st.markdown("""
**Как запустить:**
```
pip install streamlit pandas
streamlit run app.py
```
Файл `matrix_game.py` должен быть рядом.
""")

# ────────────────────────────────────────────────────────────
#  Ввод матрицы
# ────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">Матрица игры A (m×n)</div>', unsafe_allow_html=True)
st.caption("Игрок 1 выбирает строку (стратегию i), Игрок 2 выбирает столбец (стратегию j). A[i][j] — выигрыш Игрока 1.")
default_data = {f"j{j+1}": ["0"] * m for j in range(n)}
df_input = pd.DataFrame(default_data, index=[f"i{i+1}" for i in range(m)])
edited = st.data_editor(df_input, use_container_width=False, key=f"matrix_{m}_{n}")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("")
solve_clicked = st.button("▶ Решить", type="primary")

# ────────────────────────────────────────────────────────────
#  Решение
# ────────────────────────────────────────────────────────────
if solve_clicked:
    # — Парсинг матрицы —
    raw = []
    parse_error = False
    for i in range(m):
        row = []
        for j in range(n):
            cell = str(edited.iloc[i, j]).strip()
            try:
                row.append(Fraction(cell))
            except Exception:
                st.error(f"Ошибка в ячейке ({i+1},{j+1}): «{cell}» — ожидается число или дробь типа 1/3")
                parse_error = True
                break
        if parse_error:
            break
        raw.append(row)

    if parse_error:
        st.stop()

    try:
        A = load_matrix(raw)
        result = solve_matrix_game(A)
    except Exception as e:
        st.error(f"Ошибка решения: {e}")
        st.stop()

    # ═══════════════════════════════════════════════════════
    #  ИСХОДНАЯ МАТРИЦА
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card"><div class="section-title">Исходная матрица игры</div>', unsafe_allow_html=True)
    show_matrix_labeled(A, row_prefix="i", col_prefix="j")
    if show_detail:
        detail(f"Размерность: {m}×{n}   (строки = стратегии Игрока 1,  столбцы = стратегии Игрока 2)\n"
               f"Элемент a[i][j] — выигрыш Игрока 1 (проигрыш Игрока 2) при паре стратегий (i, j).")
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  ШАГ 1: СЕДЛОВАЯ ТОЧКА
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Шаг 1 — Проверка на седловую точку</div>', unsafe_allow_html=True)

    if show_detail:
        # Показываем минимумы строк и максимумы столбцов
        row_mins = [min(A[i]) for i in range(m)]
        col_maxs = [max(A[i][j] for i in range(m)) for j in range(n)]
        alpha_val = max(row_mins)
        beta_val = min(col_maxs)

        rm_str = "  ".join([f"min(i{i+1}) = {frac_str(row_mins[i])}" for i in range(m)])
        cm_str = "  ".join([f"max(j{j+1}) = {frac_str(col_maxs[j])}" for j in range(n)])
        detail(
            f"Минимумы строк (нижняя цена α):\n  {rm_str}\n"
            f"  → α = max{{min}} = {frac_str(alpha_val)}\n\n"
            f"Максимумы столбцов (верхняя цена β):\n  {cm_str}\n"
            f"  → β = min{{max}} = {frac_str(beta_val)}\n\n"
            f"Условие седловой точки: α = β\n"
            f"  {frac_str(alpha_val)} {'=' if alpha_val == beta_val else '≠'} {frac_str(beta_val)}"
            f"  →  {'Седловая точка НАЙДЕНА' if alpha_val == beta_val else 'Седловой точки НЕТ'}"
        )

    if result["saddle_point"]:
        si, sj = result["saddle_row"], result["saddle_col"]
        st.success(f"Седловая точка найдена: строка {si+1}, столбец {sj+1}.  Цена игры v = **{frac_str(result['v'])}**")
        if show_detail:
            ok(
                f"a[{si+1}][{sj+1}] = {frac_str(result['v'])} является одновременно:\n"
                f"  • минимумом в строке {si+1} (Игрок 1 не проиграет меньше при любом ходе Игрока 2)\n"
                f"  • максимумом в столбце {sj+1} (Игрок 2 не проиграет больше при любом ходе Игрока 1)\n"
                f"Игра решается в чистых стратегиях: p{si+1}=1 (остальные=0), q{sj+1}=1 (остальные=0)."
            )
        st.write("**Оптимальные стратегии (чистые):**")
        p_parts = [f"p{i+1}={frac_str(result['p'][i])}" for i in range(m)]
        q_parts = [f"q{j+1}={frac_str(result['q'][j])}" for j in range(n)]
        st.write("p = (" + ",  ".join(p_parts) + ")")
        st.write("q = (" + ",  ".join(q_parts) + ")")
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()
    else:
        st.info("Седловая точка не найдена (α ≠ β) — игра не имеет решения в чистых стратегиях → переходим к смешанным.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  ШАГ 2: РЕДУКЦИЯ ПО ДОМИНИРОВАНИЮ
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Шаг 2 — Редукция по доминированию</div>', unsafe_allow_html=True)

    if show_detail:
        detail(
            "Правило доминирования строк: строка i доминируется строкой k, если a[k][j] ≥ a[i][j] для всех j.\n"
            "  Игроку 1 выгоднее всегда выбирать k вместо i → строка i исключается.\n\n"
            "Правило доминирования столбцов: столбец j доминируется столбцом l, если a[i][l] ≤ a[i][j] для всех i.\n"
            "  Игроку 2 выгоднее всегда выбирать l вместо j → столбец j исключается.\n\n"
            "Процесс повторяется итеративно до отсутствия изменений."
        )

    msgs = result["dominance_messages"]
    if msgs:
        for msg in msgs:
            st.write(f"  → {msg}")
        st.write("**Редуцированная матрица:**")
        show_matrix_labeled(result["reduced_matrix"], row_prefix="i", col_prefix="j")
        if show_detail:
            rr = [r+1 for r in result["removed_rows"]]
            rc = [c+1 for c in result["removed_cols"]]
            ok(f"Удалены строки: {rr if rr else '—'}   Удалены столбцы: {rc if rc else '—'}\n"
               f"Редуцированная матрица: {len(result['reduced_matrix'])}×{len(result['reduced_matrix'][0])}")
    else:
        st.info("Доминируемых строк и столбцов не обнаружено — матрица остаётся в исходном виде.")
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  ШАГ 3: СДВИГ МАТРИЦЫ
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Шаг 3 — Сдвиг матрицы на константу K</div>', unsafe_allow_html=True)

    K = result["K"]
    A_sh = result["A_shifted"]
    m_sh, n_sh = len(A_sh), len(A_sh[0])

    if show_detail:
        reduced = result["reduced_matrix"]
        amin = min(x for row in reduced for x in row)
        detail(
            f"Симплекс требует, чтобы все элементы матрицы были строго положительны.\n"
            f"Минимальный элемент редуцированной матрицы: a_min = {frac_str(amin)}\n\n"
            f"{'a_min ≤ 0 → добавляем K = 1 − a_min = 1 − (' + frac_str(amin) + ') = ' + frac_str(K) if K != 0 else 'a_min > 0 → сдвиг не нужен, K = 0'}\n\n"
            f"Сдвиг не меняет оптимальные стратегии (p, q).\n"
            f"Цена оригинальной игры восстанавливается как:  v = v' − K,\n"
            f"  где v' — цена сдвинутой игры."
        )

    if K != 0:
        st.write(f"Минимальный элемент ≤ 0 → добавляем **K = {frac_str(K)}** ко всем элементам.")
        st.write("**Сдвинутая матрица A' = A + K:**")
        show_matrix_labeled(A_sh, row_prefix="i", col_prefix="j")
    else:
        st.info("Все элементы уже положительны → сдвиг не нужен (K = 0).")
        if show_detail:
            st.write("Матрица передаётся в симплекс без изменений:")
            show_matrix_labeled(A_sh, row_prefix="i", col_prefix="j")
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  ШАГ 4: LP-ПОСТАНОВКА
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Шаг 4 — Постановка задачи линейного программирования</div>', unsafe_allow_html=True)

    if show_detail:
        detail(
            "Замена переменных:\n"
            "  Игрок 2 ищет q = (q₁,...,qₙ) минимизируя цену → вводим yⱼ = qⱼ / v'\n"
            "  Игрок 1 ищет p = (p₁,...,pₘ) максимизируя цену → вводим xᵢ = pᵢ / v'\n\n"
            "Тогда условия оптимальности (теорема минимакса) приводят к двум двойственным LP."
        )

    col_lp1, col_lp2 = st.columns(2)
    with col_lp1:
        st.write("**Прямая задача (Игрок 2):**")
        primal_lines = []
        for i in range(m_sh):
            terms = " + ".join(f"{frac_str(A_sh[i][j])}·y{j+1}" for j in range(n_sh))
            primal_lines.append(f"  {terms} ≤ 1")
        primal_lines.append("  yⱼ ≥ 0,  j = 1..%d" % n_sh)
        primal_lines.append("  max F = " + " + ".join(f"y{j+1}" for j in range(n_sh)))
        st.code("\n".join(primal_lines), language=None)
        if show_detail:
            detail("F = Σyⱼ = Σqⱼ/v' = 1/v'\n→ max F эквивалентно min v' (Игрок 2 минимизирует цену)")

    with col_lp2:
        st.write("**Двойственная задача (Игрок 1):**")
        dual_lines = []
        for j in range(n_sh):
            terms = " + ".join(f"{frac_str(A_sh[i][j])}·x{i+1}" for i in range(m_sh))
            dual_lines.append(f"  {terms} ≥ 1")
        dual_lines.append("  xᵢ ≥ 0,  i = 1..%d" % m_sh)
        dual_lines.append("  min G = " + " + ".join(f"x{i+1}" for i in range(m_sh)))
        st.code("\n".join(dual_lines), language=None)
        if show_detail:
            detail("G = Σxᵢ = Σpᵢ/v' = 1/v'\n→ min G эквивалентно max v' (Игрок 1 максимизирует цену)")

    if show_detail:
        detail(
            "По теореме двойственности LP: min G = max F при оптимуме.\n"
            "Решая прямую задачу симплекс-методом, мы автоматически получаем\n"
            "оптимальное решение двойственной задачи из строки Δ итоговой таблицы."
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  ШАГ 5: НАЧАЛЬНАЯ СИМПЛЕКС-ТАБЛИЦА
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Шаг 5 — Начальная симплекс-таблица</div>', unsafe_allow_html=True)

    iterations = result["iterations"]
    init_it = iterations[0]

    if show_detail:
        detail(
            "Вводим базисные переменные uᵢ (слабые переменные ограничений ≤ 1).\n"
            "Начальная таблица:\n"
            "  • Строки: u0..u{} (базисные переменные)\n"
            "  • Столбцы: y1..y{} (небазисные), b (свободные члены = 1)\n"
            "  • Строка Δ: коэффициенты ЦФ (все = -1, т.к. max F = Σyⱼ)\n"
            "  • Базис прямо допустим: все bᵢ = 1 > 0 → можно применять прямой симплекс".format(m_sh-1, n_sh)
        )

    df_init = tableau_to_df(init_it["tableau"], init_it["basis"], init_it["col_names"])
    st.dataframe(df_init, use_container_width=False)

    methods_used = [it["method"] for it in iterations if it["method"] != "initial"]
    primal_count = methods_used.count("primal")
    dual_count = methods_used.count("dual")

    if show_detail:
        method_summary = []
        if primal_count:
            method_summary.append(f"прямых шагов: {primal_count}")
        if dual_count:
            method_summary.append(f"двойственных шагов: {dual_count}")
        detail(
            f"Всего итераций (без начальной): {len(methods_used)}\n"
            f"  {', '.join(method_summary) if method_summary else '—'}\n\n"
            f"Прямой симплекс: выбираем столбец с наибольшим |Δⱼ| < 0, строку — по минимальному θ = bᵢ/aᵢⱼ (aᵢⱼ > 0).\n"
            f"Двойственный симплекс: активируется когда все Δⱼ ≥ 0, но есть bᵢ < 0 (двойственно допустимо, прямо нет)."
        )

    if dual_count > 0 and primal_count > 0:
        st.info("ℹ️ Использованы оба метода: прямой и двойственный симплекс.")
    elif dual_count > 0:
        st.info("ℹ️ Использован двойственный симплекс.")
    else:
        st.info("ℹ️ Использован прямой симплекс (начальная таблица прямо допустима).")

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  ШАГ 6: ИТЕРАЦИИ СИМПЛЕКСА
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Шаг 6 — Итерации симплекс-метода</div>', unsafe_allow_html=True)

    for idx, it in enumerate(iterations):
        if idx == 0:
            continue  # начальная таблица уже показана выше

        T_it = it["tableau"]
        basis_it = it["basis"]
        cols_it = it["col_names"]
        p_row = it["pivot_row"]
        p_col = it["pivot_col"]
        method = it["method"]
        method_ru = {"primal": "прямой", "dual": "двойственный"}.get(method, method)

        # ИСПРАВЛЕНИЕ: в оригинале basis_it/cols_it уже содержат POST-pivot имена,
        # поэтому уходящий и входящий нужно восстанавливать из предыдущей итерации.
        prev_it = iterations[idx - 1]
        leaving_var = prev_it["basis"][p_row]    # уходящий из базиса
        entering_var = prev_it["col_names"][p_col]  # входящий в базис

        label = (
            f"Итерация {idx} [{method_ru}] — "
            f"уходит из базиса: «{leaving_var}»,  входит в базис: «{entering_var}»"
        )

        with st.expander(label, expanded=(idx <= 2)):
            if show_detail:
                prev_T = prev_it["tableau"]
                pivot_el = prev_T[p_row][p_col]
                delta_row = prev_T[len(basis_it)][:]   # строка Δ до шага

                if method == "primal":
                    # Показываем выбор ведущего столбца и строки
                    neg_deltas = [(j, frac_str(delta_row[j])) for j in range(len(cols_it)) if delta_row[j] < 0]
                    neg_str = "  ".join([f"Δ({prev_it['col_names'][j]})={v}" for j, v in neg_deltas])
                    # Показываем отношения θ
                    thetas = []
                    for i in range(len(basis_it)):
                        a = prev_T[i][p_col]
                        b = prev_T[i][-1]
                        if a > 0:
                            thetas.append(f"θ({prev_it['basis'][i]}) = {frac_str(b)}/{frac_str(a)} = {frac_str(b/a)}")
                    theta_str = "\n  ".join(thetas)
                    detail(
                        f"Прямой симплекс:\n"
                        f"  Отрицательные Δ: {neg_str}\n"
                        f"  Ведущий столбец: «{entering_var}» (наиболее отрицательный Δ = {frac_str(delta_row[p_col])})\n\n"
                        f"  Отношения θ = b/a для aᵢ > 0:\n  {theta_str}\n"
                        f"  Ведущая строка: «{leaving_var}» (минимальное θ)\n\n"
                        f"  Ведущий элемент: a[{leaving_var}][{entering_var}] = {frac_str(pivot_el)}"
                    )
                else:
                    neg_bs = [(i, frac_str(prev_T[i][-1])) for i in range(len(basis_it)) if prev_T[i][-1] < 0]
                    neg_b_str = "  ".join([f"b({prev_it['basis'][i]})={v}" for i, v in neg_bs])
                    ratios = []
                    for j in range(len(cols_it)):
                        a = prev_T[p_row][j]
                        if a < 0:
                            ratios.append(f"Δ({prev_it['col_names'][j]})/|a| = {frac_str(delta_row[j])}/{frac_str(-a)} = {frac_str(delta_row[j]/(-a))}")
                    ratio_str = "\n  ".join(ratios)
                    detail(
                        f"Двойственный симплекс:\n"
                        f"  Все Δⱼ ≥ 0 (двойственная допустимость сохраняется)\n"
                        f"  Отрицательные b: {neg_b_str}\n"
                        f"  Ведущая строка: «{leaving_var}» (наиболее отрицательный b = {frac_str(prev_T[p_row][-1])})\n\n"
                        f"  Отношения для входящего столбца (aᵢⱼ < 0):\n  {ratio_str}\n"
                        f"  Ведущий столбец: «{entering_var}» (минимальное отношение)\n\n"
                        f"  Ведущий элемент: a[{leaving_var}][{entering_var}] = {frac_str(pivot_el)}"
                    )

            # Таблица с подсветкой
            df_t = tableau_to_df(T_it, basis_it, cols_it)
            if show_detail:
                st.write("**Таблица после пересчёта** (выделен ведущий элемент из предыдущего шага):")
            st.dataframe(highlight_pivot(df_t, p_row, p_col), use_container_width=False)

            if show_detail:
                # Пересчёт по формуле Гаусса-Жордана
                detail(
                    f"Пересчёт таблицы (правило Гаусса–Жордана):\n"
                    f"  Ведущую строку делим на ведущий элемент {frac_str(pivot_el)}.\n"
                    f"  Остальные строки: new[i][j] = (old[i][j]·pivot − old[i][pcol]·old[prow][j]) / pivot.\n"
                    f"  Строка Δ пересчитывается по той же формуле.\n"
                    f"  Ведущий столбец: new[i][pcol] = −old[i][pcol] / pivot."
                )

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  ШАГ 7: ИТОГОВАЯ ТАБЛИЦА И КРИТЕРИЙ ОПТИМАЛЬНОСТИ
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Шаг 7 — Итоговая таблица и критерий оптимальности</div>', unsafe_allow_html=True)

    last_it = iterations[-1]
    T_final = last_it["tableau"]
    basis_final = last_it["basis"]
    col_names_final = last_it["col_names"]
    m_f = len(basis_final)
    F_max = T_final[m_f][-1]

    st.write("**Оптимальная симплекс-таблица:**")
    df_final = tableau_to_df(T_final, basis_final, col_names_final)
    st.dataframe(df_final, use_container_width=False)

    if show_detail:
        delta_final = [frac_str(T_final[m_f][j]) for j in range(len(col_names_final))]
        b_final = [frac_str(T_final[i][-1]) for i in range(m_f)]
        detail(
            f"Критерий оптимальности прямого симплекса: все Δⱼ ≥ 0\n"
            f"  Строка Δ: {', '.join([f'{col_names_final[j]}={delta_final[j]}' for j in range(len(col_names_final))])}\n"
            f"  {'✓ Все Δⱼ ≥ 0 — оптимум достигнут' if all(T_final[m_f][j] >= 0 for j in range(len(col_names_final))) else '✗ Есть отрицательные Δ — ошибка'}\n\n"
            f"  Свободные члены b (все должны быть ≥ 0):\n"
            f"  {', '.join([f'{basis_final[i]}={b_final[i]}' for i in range(m_f)])}\n"
            f"  {'✓ Все bᵢ ≥ 0 — прямая допустимость' if all(T_final[i][-1] >= 0 for i in range(m_f)) else '✗ Есть bᵢ < 0'}\n\n"
            f"  F_max = b в строке Δ = {frac_str(F_max)}"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  ШАГ 8: ИЗВЛЕЧЕНИЕ РЕШЕНИЯ
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Шаг 8 — Извлечение решения из итоговой таблицы</div>', unsafe_allow_html=True)

    v_shift = result["v_shift"]
    x_red = result["x"]
    y_red = result["y"]

    if show_detail:
        detail(
            f"F_max = {frac_str(F_max)}  (значение ЦФ в правом нижнем углу таблицы)\n\n"
            f"v' = 1 / F_max = 1 / {frac_str(F_max)} = {frac_str(v_shift)}\n"
            f"  (цена сдвинутой игры — обратная к максимуму ЦФ)\n\n"
            f"Переменные y (стратегии Игрока 2):\n"
            f"  Ищем переменные yⱼ в столбце 'basis' итоговой таблицы.\n"
            f"  Значение yⱼ = b в соответствующей строке (если yⱼ небазисная → yⱼ = 0)."
        )

    # Детально показываем откуда берётся каждый y и x
    col_y_extr, col_x_extr = st.columns(2)

    with col_y_extr:
        st.write("**Извлечение y (Игрок 2)** — из базисных строк:")
        y_rows = []
        for i in range(m_f):
            var = basis_final[i]
            if var.startswith("y"):
                y_rows.append({"Переменная": var, "Источник": f"базис строки {i+1}", "Значение": frac_str(T_final[i][-1])})
        for j in range(len(col_names_final)):
            var = col_names_final[j]
            if var.startswith("y"):
                y_rows.append({"Переменная": var, "Источник": "небазисная → 0", "Значение": "0"})
        if y_rows:
            st.dataframe(pd.DataFrame(y_rows), hide_index=True, use_container_width=True)

    with col_x_extr:
        st.write("**Извлечение x (Игрок 1)** — из строки Δ:")
        x_rows = []
        for j in range(len(col_names_final)):
            var = col_names_final[j]
            if var.startswith("u"):
                idx_u = int(var[1:])
                x_rows.append({"Переменная": f"x{idx_u+1}", "Источник": f"Δ[{var}]", "Значение": frac_str(T_final[m_f][j])})
        for i in range(m_f):
            var = basis_final[i]
            if var.startswith("u"):
                idx_u = int(var[1:])
                x_rows.append({"Переменная": f"x{idx_u+1}", "Источник": f"базис строки {i+1} → в Δ=0", "Значение": "0"})
        if x_rows:
            st.dataframe(pd.DataFrame(x_rows), hide_index=True, use_container_width=True)

    if show_detail:
        y_detail = "  ".join([f"y{j+1}={frac_str(y_red[j])}" for j in range(len(y_red))])
        x_detail = "  ".join([f"x{i+1}={frac_str(x_red[i])}" for i in range(len(x_red))])
        q_calc = "  ".join([f"q{j+1} = {frac_str(v_shift)}·{frac_str(y_red[j])} = {frac_str(v_shift*y_red[j])}" for j in range(len(y_red))])
        p_calc = "  ".join([f"p{i+1} = {frac_str(v_shift)}·{frac_str(x_red[i])} = {frac_str(v_shift*x_red[i])}" for i in range(len(x_red))])
        detail(
            f"y: {y_detail}\nx: {x_detail}\n\n"
            f"Стратегии: qⱼ = v'·yⱼ,  pᵢ = v'·xᵢ\n\n"
            f"{q_calc}\n{p_calc}"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  ШАГ 9: ВОССТАНОВЛЕНИЕ ПОЛНЫХ СТРАТЕГИЙ И ЦЕНА ИГРЫ
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Шаг 9 — Полные стратегии и цена игры</div>', unsafe_allow_html=True)

    K_val = result["K"]
    v = result["v"]
    p_full = result["p"]
    q_full = result["q"]

    if show_detail:
        rr = result["removed_rows"]
        rc = result["removed_cols"]
        if rr or rc:
            detail(
                f"Восстановление полных векторов:\n"
                f"  Удалённые строки {[r+1 for r in rr]} получают pᵢ = 0 (стратегии не используются).\n"
                f"  Удалённые столбцы {[c+1 for c in rc]} получают qⱼ = 0.\n"
                f"  Оставшиеся индексы заполняются из редуцированного решения."
            )
        detail(
            f"Цена исходной игры:\n"
            f"  v = v' − K = {frac_str(v_shift)} − {frac_str(K_val)} = {frac_str(v)}\n\n"
            f"Полная стратегия Игрока 1: p = ({', '.join([frac_str(pi) for pi in p_full])})\n"
            f"  Сумма = {frac_str(sum(p_full))} {'✓' if sum(p_full) == 1 else '✗ ошибка!'}\n\n"
            f"Полная стратегия Игрока 2: q = ({', '.join([frac_str(qi) for qi in q_full])})\n"
            f"  Сумма = {frac_str(sum(q_full))} {'✓' if sum(q_full) == 1 else '✗ ошибка!'}"
        )

    st.markdown(f"""
    <div class="price-block">
      <div class="price-label">Цена игры</div>
      <div class="price-value">v = {frac_str(v)}</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-card"><div class="section-title">Стратегия Игрока 1 (p)</div>', unsafe_allow_html=True)
        df_p = pd.DataFrame({
            "Стратегия": [f"p{i+1}" for i in range(len(p_full))],
            "Вероятность": [frac_str(x) for x in p_full],
            "Дес. дробь": [f"{float(x):.4f}" for x in p_full],
        })
        st.dataframe(df_p, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card"><div class="section-title">Стратегия Игрока 2 (q)</div>', unsafe_allow_html=True)
        df_q = pd.DataFrame({
            "Стратегия": [f"q{j+1}" for j in range(len(q_full))],
            "Вероятность": [frac_str(x) for x in q_full],
            "Дес. дробь": [f"{float(x):.4f}" for x in q_full],
        })
        st.dataframe(df_q, hide_index=True, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════
    #  ШАГ 10: ПРОВЕРКА ОПТИМАЛЬНОСТИ
    # ═══════════════════════════════════════════════════════
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Шаг 10 — Проверка оптимальности (теорема минимакса)</div>', unsafe_allow_html=True)

    if show_detail:
        detail(
            "Проверка теоремы минимакса:\n"
            "  Для всех j: Σᵢ pᵢ·a[i][j] ≥ v  (Игрок 1 обеспечивает ≥ v при любом j)\n"
            "  Для всех i: Σⱼ a[i][j]·qⱼ ≤ v  (Игрок 2 обеспечивает ≤ v при любом i)"
        )

    with st.expander("📋 Проверка: p·A[:,j] ≥ v для всех столбцов j", expanded=True):
        check_rows = []
        all_ok = True
        for j in range(n):
            val = sum(Fraction(raw[i][j]) * p_full[i] for i in range(m))
            ok_flag = val >= v - Fraction(1, 10**9)
            if not ok_flag:
                all_ok = False
            check_rows.append({
                "Столбец": f"j={j+1}",
                "Σ pᵢ·a[i][j]": frac_str(val),
                "Дес. дробь": f"{float(val):.6f}",
                "≥ v?": "✓" if ok_flag else "✗",
            })
        st.dataframe(pd.DataFrame(check_rows), hide_index=True, use_container_width=False)
        if all_ok:
            ok(f"✓ Все значения p·A[:,j] ≥ v = {frac_str(v)}  — стратегия Игрока 1 оптимальна.")
        else:
            warn("✗ Нарушение! Проверьте вычисления.")

    with st.expander("📋 Проверка: A[i,:]·q ≤ v для всех строк i", expanded=True):
        check_rows2 = []
        all_ok2 = True
        for i in range(m):
            val = sum(Fraction(raw[i][j]) * q_full[j] for j in range(n))
            ok_flag = val <= v + Fraction(1, 10**9)
            if not ok_flag:
                all_ok2 = False
            check_rows2.append({
                "Строка": f"i={i+1}",
                "Σ a[i][j]·qⱼ": frac_str(val),
                "Дес. дробь": f"{float(val):.6f}",
                "≤ v?": "✓" if ok_flag else "✗",
            })
        st.dataframe(pd.DataFrame(check_rows2), hide_index=True, use_container_width=False)
        if all_ok2:
            ok(f"✓ Все значения A[i,:]·q ≤ v = {frac_str(v)}  — стратегия Игрока 2 оптимальна.")
        else:
            warn("✗ Нарушение! Проверьте вычисления.")

    if show_detail:
        ok(
            f"Итог:\n"
            f"  Цена игры:      v = {frac_str(v)}  ≈ {float(v):.6f}\n"
            f"  Игрок 1 (max):  p = ({', '.join([frac_str(pi) for pi in p_full])})\n"
            f"  Игрок 2 (min):  q = ({', '.join([frac_str(qi) for qi in q_full])})\n"
            f"  Сдвиг K = {frac_str(K_val)},  v' = {frac_str(v_shift)},  F_max = {frac_str(F_max)}"
        )

    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Матричная игра — симплекс-метод | matrix_game.py")
