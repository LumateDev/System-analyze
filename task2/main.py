import numpy as np
from scipy.optimize import linprog

def solve_transportation_problem():
    """
    Решает несбалансированную транспортную задачу, приводя ее к сбалансированному виду
    и используя метод линейного программирования.
    """
    # --- 1. Исходные данные ---
    supply = np.array([20, 30, 40, 20])
    demand = np.array([40, 40, 20])
    costs = np.array([
        [2, 3, 4],
        [1, 2, 3],
        [4, 1, 2],
        [3, 1, 1]
    ])

    num_suppliers = len(supply)
    num_consumers_orig = len(demand)

    print("--- Исходные данные ---")
    print(f"Мощности поставщиков (A): {supply}")
    print(f"Мощности потребителей (B): {demand}")
    print("Матрица стоимостей (C):\n", costs)
    print("-" * 25)

    # --- 2. Проверка и балансировка задачи ---
    total_supply = np.sum(supply)
    total_demand = np.sum(demand)

    print(f"Общее предложение: {total_supply}")
    print(f"Общий спрос: {total_demand}\n")
    
    is_fictitious_consumer = False
    if total_supply > total_demand:
        print("Задача несбалансированная (предложение > спрос).")
        fictitious_demand = total_supply - total_demand
        demand = np.append(demand, fictitious_demand)
        costs = np.c_[costs, np.zeros(num_suppliers)]
        is_fictitious_consumer = True
        print(f"Добавлен фиктивный потребитель со спросом: {fictitious_demand}")
        print("Стоимости перевозок к нему равны 0.\n")
    elif total_demand > total_supply:
        print("Задача несбалансированная (спрос > предложение).")
        fictitious_supply = total_demand - total_supply
        supply = np.append(supply, fictitious_supply)
        costs = np.r_[costs, np.zeros((1, num_consumers_orig))]
        print(f"Добавлен фиктивный поставщик с предложением: {fictitious_supply}\n")

    num_suppliers_balanced = len(supply)
    num_consumers_balanced = len(demand)

    print("--- Сбалансированная задача ---")
    print(f"Новые мощности потребителей (B'): {demand}")
    print("Новая матрица стоимостей (C'):\n", costs)
    print("-" * 25)

    # --- 3. Формулировка задачи для scipy.optimize.linprog ---
    c = costs.flatten()
    b_eq = np.concatenate([supply, demand])
    
    A_eq = []
    # Ограничения по поставщикам
    for i in range(num_suppliers_balanced):
        row = np.zeros(num_suppliers_balanced * num_consumers_balanced)
        row[i * num_consumers_balanced : (i + 1) * num_consumers_balanced] = 1
        A_eq.append(row)

    # Ограничения по потребителям
    for j in range(num_consumers_balanced):
        col = np.zeros(num_suppliers_balanced * num_consumers_balanced)
        col[j::num_consumers_balanced] = 1
        A_eq.append(col)

    A_eq = np.array(A_eq)
    bounds = (0, None)

    # --- 4. Решение ---
    print("Решение задачи методом линейного программирования...")
    result = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method='highs')

    # --- 5. Вывод результатов ---
    if result.success:
        shipping_plan = result.x.reshape((num_suppliers_balanced, num_consumers_balanced))
        total_cost = result.fun

        print("\n--- РЕЗУЛЬТАТЫ ---")
        print("\nОптимальный план перевозок (матрица X):")
        
        # Форматированный вывод таблицы
        header_parts = [f"Потребитель {j+1:<2}" for j in range(num_consumers_orig)]
        if is_fictitious_consumer:
            header_parts.append("Фиктивный")
        
        header = "          |" + "|".join([f"{part:^14}" for part in header_parts])
        print(header)
        print("-" * len(header))
        for i in range(num_suppliers_balanced):
            row_str = f"Поставщик {i+1:<2} |"
            for val in shipping_plan[i]:
                # Используем .0f для округления до целого, abs() чтобы убрать "-0.0"
                row_str += f" {abs(val):^13.0f}|"
            print(row_str)

        print("\n\nИнтерпретация:")
        for i in range(num_suppliers_balanced):
            for j in range(num_consumers_balanced):
                if shipping_plan[i, j] > 0.001: # Используем порог для точности
                    if is_fictitious_consumer and j == num_consumers_balanced - 1:
                        print(f"  - У поставщика {i+1} на складе остается {shipping_plan[i, j]:.0f} ед. товара.")
                    else:
                        print(f"  - От поставщика {i+1} к потребителю {j+1} везти {shipping_plan[i, j]:.0f} ед.")
        
        print(f"\n✅ Минимальная общая стоимость перевозок: {total_cost:.2f}")
    else:
        print("\n❌ Не удалось найти оптимальное решение.")
        print(f"Статус: {result.message}")

if __name__ == "__main__":
    solve_transportation_problem()