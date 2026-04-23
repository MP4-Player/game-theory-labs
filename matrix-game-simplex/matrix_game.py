from __future__ import annotations
from fractions import Fraction
from typing import List, Optional, Dict, Any
import copy

M: int = 0
N: int = 0


def set_dimensions(m: int, n: int) -> None:
    global M, N
    M, N = m, n


def to_fraction(x) -> Fraction:
    return Fraction(str(x))


def load_matrix(raw: List[List]) -> List[List[Fraction]]:
    m = len(raw)
    if m == 0:
        raise ValueError("Матрица пустая")
    n = len(raw[0])
    for row in raw:
        if len(row) != n:
            raise ValueError("Строки матрицы должны иметь одинаковую длину")
    set_dimensions(m, n)
    return [[to_fraction(raw[i][j]) for j in range(n)] for i in range(m)]


def find_saddle_point(A: List[List[Fraction]]) -> list:
    row_mins = [(min(row), i) for i, row in enumerate(A)]
    alpha_val, alpha_row = max(row_mins, key=lambda x: x[0])

    col_maxs = [(max(A[i][j] for i in range(M)), j) for j in range(N)]
    beta_val, beta_col = min(col_maxs, key=lambda x: x[0])

    if alpha_val == beta_val:
        return True, alpha_val, alpha_row, beta_col
    return False, None, None, None


def search_dominance(A: List[List[Fraction]]) -> list:
    A_work = [row[:] for row in A]
    current_rows = list(range(M))
    current_cols = list(range(N))
    removed_rows = []
    removed_cols = []
    messages = []

    changed = True
    while changed:
        changed = False

        i = 0
        while i < len(A_work):
            dominated = False
            for k in range(len(A_work)):
                if k == i:
                    continue
                if all(A_work[k][j] >= A_work[i][j] for j in range(len(A_work[0]))):
                    dominated = True
                    break
            if dominated:
                orig = current_rows[i]
                removed_rows.append(orig)
                messages.append(f"Строка {orig + 1} доминируема доминантом {current_rows[k] + 1}.")
                del A_work[i]
                del current_rows[i]
                changed = True
            else:
                i += 1

        j = 0
        while j < len(A_work[0]):
            dominated = False
            for l in range(len(A_work[0])):
                if l == j:
                    continue
                if all(A_work[i][l] <= A_work[i][j] for i in range(len(A_work))):
                    dominated = True
                    break
            if dominated:
                orig = current_cols[j]
                removed_cols.append(orig)
                messages.append(f"Столбец {orig + 1} доминируем доминантом {current_cols[l] + 1}.")
                for row in A_work:
                    del row[j]
                del current_cols[j]
                changed = True
            else:
                j += 1

    return A_work, removed_rows, removed_cols, messages


def shift_matrix(A: List[List[Fraction]]) -> list:
    amin = min(x for row in A for x in row)
    K = Fraction(0)
    if amin <= 0:
        K = Fraction(1) - amin
    A_shifted = [[x + K for x in row] for row in A]
    return A_shifted, K


def build(A_shifted: List[List[Fraction]]) -> list:
    m_r = len(A_shifted)
    n_r = len(A_shifted[0])

    T = [[Fraction(0)] * (n_r + 1) for _ in range(m_r + 1)]

    for i in range(m_r):
        for j in range(n_r):
            T[i][j] = A_shifted[i][j]
        T[i][-1] = Fraction(1)   # b = 1

    for j in range(n_r):
        T[m_r][j] = Fraction(-1) # Δ
    T[m_r][-1] = Fraction(0) # b в строке Δ

    basis = [f"u{i}" for i in range(m_r)]
    col_names = [f"y{j+1}" for j in range(n_r)]

    return T, basis, col_names


def run_simplex(
    T: List[List[Fraction]],
    basis: List[str],
    col_names: List[str]
):
    m_r = len(basis)       # количество строк без Δ
    n_r = len(col_names)   # количество столбцов без b

    iterations = []
    iterations.append({
        "tableau": copy.deepcopy(T),
        "basis": basis.copy(),
        "col_names": col_names.copy(),
        "pivot_row": None,
        "pivot_col": None,
        "method": "initial"
    })

    while True:
        delta = T[m_r]
        all_delta_nonneg = all(delta[j] >= 0 for j in range(n_r))
        has_neg_b = any(T[i][-1] < 0 for i in range(m_r))

        if all_delta_nonneg and not has_neg_b:
            break  # оптимум

        if not all_delta_nonneg and has_neg_b:
            raise ValueError("Задача не имеет решения: таблица прямо и двойственно недопустима")

        if all_delta_nonneg and has_neg_b:
            # Двойственный симплекс
            method = "dual"
            pivot_row = None
            most_neg_b = Fraction(0)
            for i in range(m_r):
                if T[i][-1] < most_neg_b:
                    most_neg_b = T[i][-1]
                    pivot_row = i

            pivot_col = None
            min_ratio = None
            for j in range(n_r):
                a = T[pivot_row][j]
                if a < 0:
                    ratio = delta[j] / (-a)
                    if min_ratio is None or ratio < min_ratio:
                        min_ratio = ratio
                        pivot_col = j

            if pivot_col is None:
                raise ValueError("Двойственный симплекс: нет отрицательных элементов в ведущей строке")

        else:
            # Прямой симплекс
            method = "primal"
            pivot_col = None
            most_neg = Fraction(0)
            for j in range(n_r):
                if delta[j] < most_neg:
                    most_neg = delta[j]
                    pivot_col = j

            pivot_row = None
            min_ratio = None
            for i in range(m_r):
                a = T[i][pivot_col]
                if a > 0:
                    ratio = T[i][-1] / a
                    if min_ratio is None or ratio < min_ratio:
                        min_ratio = ratio
                        pivot_row = i

            if pivot_row is None:
                raise ValueError("Прямой симплекс: нет положительных элементов в ведущем столбце")

        pivot_el = T[pivot_row][pivot_col]

        new_T = [[Fraction(0)] * (n_r + 1) for _ in range(m_r + 1)]
        new_T[pivot_row][pivot_col] = Fraction(1) / pivot_el

        for j in range(n_r + 1):
            if j == pivot_col:
                continue
            new_T[pivot_row][j] = T[pivot_row][j] / pivot_el

        for i in range(m_r + 1):
            if i == pivot_row:
                continue
            new_T[i][pivot_col] = -T[i][pivot_col] / pivot_el

        for i in range(m_r + 1):
            if i == pivot_row:
                continue
            for j in range(n_r + 1):
                if j == pivot_col:
                    continue
                new_T[i][j] = (T[i][j] * pivot_el - T[i][pivot_col] * T[pivot_row][j]) / pivot_el

        T = new_T

        old_basis_name = basis[pivot_row]
        basis[pivot_row] = col_names[pivot_col]
        col_names[pivot_col] = old_basis_name

        iterations.append({
            "tableau": copy.deepcopy(T),
            "basis": basis.copy(),
            "col_names": col_names.copy(),
            "pivot_row": pivot_row,
            "pivot_col": pivot_col,
            "method": method
        })

    return T, iterations


def extract_solution(
    T: List[List[Fraction]],
    basis: List[str],
    col_names: List[str],
    K: Fraction
) -> list:
    m_r = len(basis)
    n_r = len(col_names)

    F_max = T[m_r][-1]

    if F_max == 0:
        raise ValueError("Z=0: не удалось найти решение")

    v_shift = Fraction(1) / F_max

    y_red = [Fraction(0)] * n_r
    for i in range(m_r):
        var = basis[i]
        if var.startswith("y"):
            idx = int(var[1:]) - 1
            y_red[idx] = T[i][-1]

    x_red = [Fraction(0)] * m_r
    for j in range(n_r):
        var = col_names[j]
        if var.startswith("u"):
            idx = int(var[1:])
            x_red[idx] = T[m_r][j]

    q_red = [v_shift * yj for yj in y_red]
    p_red = [v_shift * xi for xi in x_red]
    v = v_shift - K

    return p_red, q_red, x_red, y_red, v_shift, v


def solve_matrix_game(A: List[List[Fraction]]) -> Dict[str, Any]:
    # 1. Седловая точка
    saddle_found, saddle_value, saddle_i, saddle_j = find_saddle_point(A)
    if saddle_found:
        p = [Fraction(0)] * M
        q = [Fraction(0)] * N
        p[saddle_i] = Fraction(1)
        q[saddle_j] = Fraction(1)
        return {
            "saddle_point": True,
            "saddle_value": saddle_value,
            "saddle_row": saddle_i,
            "saddle_col": saddle_j,
            "p": p, "q": q, "v": saddle_value,
            "K": Fraction(0),
            "A_shifted": A,
            "x": [Fraction(0)] * M,
            "y": [Fraction(0)] * N,
            "v_shift": saddle_value,
            "tableau": [], "basis": [],
            "iterations": [],
            "removed_rows": [], "removed_cols": [],
            "dominance_messages": [],
        }

    # 2. Редукция
    reduced_A, removed_rows, removed_cols, dom_messages = search_dominance(A)
    if not reduced_A or not reduced_A[0]:
        raise ValueError("После редукции матрица пуста")

    # 3. Сдвиг
    A_shifted, K = shift_matrix(reduced_A)

    # 4. Строим таблицу
    T, basis, col_names = build(A_shifted)

    # 5. Симплекс
    T, iterations = run_simplex(T, basis, col_names)

    # 6. Извлекаем решение
    p_red, q_red, x_red, y_red, v_shift, v = extract_solution(T, basis, col_names, K)

    # 7. Восстанавливаем полные векторы
    p_full = [Fraction(0)] * M
    q_full = [Fraction(0)] * N
    kept_rows = [i for i in range(M) if i not in removed_rows]
    kept_cols = [j for j in range(N) if j not in removed_cols]
    for idx, orig_row in enumerate(kept_rows):
        p_full[orig_row] = p_red[idx]
    for idx, orig_col in enumerate(kept_cols):
        q_full[orig_col] = q_red[idx]

    return {
        "saddle_point": False,
        "removed_rows": removed_rows,
        "removed_cols": removed_cols,
        "dominance_messages": dom_messages,
        "reduced_matrix": reduced_A,
        "K": K,
        "A_shifted": A_shifted,
        "x": x_red,
        "y": y_red,
        "p": p_full,
        "q": q_full,
        "v_shift": v_shift,
        "v": v,
        "tableau": T,
        "basis": basis,
        "iterations": iterations,
    }