from fractions import Fraction
import matrix_game as mg
from matrix_game import load_matrix, solve_matrix_game
from matrix_game import load_matrix, solve_matrix_game


def print_result(result: dict) -> None:
    print(f"\n=== Матрица {mg.M}x{mg.N} ===")

    if result["dominance_messages"]:
        print("\n-- Доминирование --")
        for msg in result["dominance_messages"]:
            print(" ", msg)

    if result["saddle_point"]:
        print(f"\nСедловая точка: строка {result['saddle_row'] + 1}, столбец {result['saddle_col'] + 1}")
        print(f"Цена игры v = {result['v']}")
        print(f"p = {result['p']}")
        print(f"q = {result['q']}")
        return

    print(f"\nУдалённые строки: {[r + 1 for r in result['removed_rows']]}")
    print(f"Удалённые столбцы: {[c + 1 for c in result['removed_cols']]}")
    print(f"Сдвиг K = {result['K']}")
    print(f"\nЦена игры v = {result['v']}")
    print(f"p (полная) = {result['p']}")
    print(f"q (полная) = {result['q']}")

    print(f"\nИтераций симплекса: {len(result['iterations']) - 1}")
    for step in result["iterations"]:
        if step["method"] == "initial":
            print("  [начальная таблица]")
        else:
            print(f"  [{step['method']}] строка={step['row']}, столбец={step['col']}")


def main() -> None:
    # Матрица задаётся как list[list[int|float|str]] — load_matrix приведёт к Fraction
    raw = [
        [3, -1,  2],
        [1,  4, -2],
        [-2, 3,  1],
    ]

    A = load_matrix(raw)   # -> list[list[Fraction]], устанавливает M, N
    result = solve_matrix_game(A)
    print_result(result)


if __name__ == "__main__":
    main()
