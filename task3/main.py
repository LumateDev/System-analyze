import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_payoff(stock_level, demand_level, profit_per_box, cost_of_unsold):
    """
    Рассчитывает финансовый результат (прибыль/убыток) для конкретного сценария.
    """
    sold_boxes = min(stock_level, demand_level)
    unsold_boxes = stock_level - sold_boxes
    total_profit = (sold_boxes * profit_per_box) - (unsold_boxes * cost_of_unsold)
    return total_profit

def solve_and_visualize_decision_problem():
    """
    Решает задачу принятия решений и визуализирует результаты.
    """
    # --- 1. Исходные данные ---
    profit_per_box = 35.0
    cost_of_unsold = 56.0
    actions = [11, 12, 13]
    demand_levels = [11, 12, 13]
    probabilities = [0.45, 0.35, 0.20]

    print("--- Анализ задачи «Фото КОЛОР» ---")
    print(f"Прибыль с проданного ящика: {profit_per_box} тыс. руб.")
    print(f"Убыток с непроданного ящика: {cost_of_unsold} тыс. руб.\n")

    # --- 2. Построение платежной матрицы ---
    payoff_matrix = [[calculate_payoff(stock, demand, profit_per_box, cost_of_unsold) for demand in demand_levels] for stock in actions]
    
    df_payoff = pd.DataFrame(
        payoff_matrix,
        index=[f"Закупить {a}" for a in actions],
        columns=[f"Спрос {d} (P={p})" for d, p in zip(demand_levels, probabilities)]
    )
    print("--- 1. Платежная матрица (финансовые исходы, тыс. руб.) ---")
    print(df_payoff)
    print("\n")

    # --- 3. Расчет EMV ---
    emv_results = {stock: np.dot(payoff_row, probabilities) for stock, payoff_row in zip(actions, payoff_matrix)}
    
    print("--- 2. Расчет ожидаемой денежной стоимости (EMV) ---")
    for stock, emv in emv_results.items():
        print(f"EMV(Закупить {stock}) = {emv:.2f} тыс. руб.")
    
    optimal_action = max(emv_results, key=emv_results.get)
    max_emv = emv_results[optimal_action]

    print("\n--- 3. Вывод и рекомендация ---")
    print(f"✅ Оптимальная стратегия: еженедельно закупать {optimal_action} ящиков.")
    print(f"   Максимальная ожидаемая прибыль (EMV) составляет {max_emv:.2f} тыс. рублей.")

    # --- 4. Визуализация ---
    
    # Настройка стилей и шрифтов для корректного отображения кириллицы
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans'] # Шрифт, поддерживающий кириллицу
    
    # Создаем фигуру с двумя под-графиками
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle('Визуальный анализ задачи о закупках «Фото КОЛОР»', fontsize=20, weight='bold')

    # График 1: Тепловая карта платежной матрицы
    sns.heatmap(df_payoff, ax=axes[0], annot=True, fmt=".0f", cmap="viridis", linewidths=.5, annot_kws={"size": 14})
    axes[0].set_title('Платежная матрица (Прибыль, тыс. руб.)', fontsize=16)
    axes[0].tick_params(axis='y', rotation=0)

    # График 2: Сравнение EMV для разных стратегий
    strategies = [f"Закупить {a}" for a in actions]
    emv_values = list(emv_results.values())
    
    # Цвета для баров: выделяем оптимальную стратегию
    colors = ['skyblue' if val < max_emv else 'salmon' for val in emv_values]
    
    bars = sns.barplot(x=strategies, y=emv_values, ax=axes[1], palette=colors, hue=strategies, legend=False)
    axes[1].set_title('Сравнение стратегий по ожидаемой прибыли (EMV)', fontsize=16)
    axes[1].set_ylabel('Ожидаемая прибыль (EMV), тыс. руб.', fontsize=12)
    axes[1].set_xlabel('Стратегия', fontsize=12)
    
    # Добавляем значения над барами
    for bar in bars.patches:
        axes[1].annotate(f'{bar.get_height():.2f}',
                       (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                       ha='center', va='bottom',
                       size=14, xytext=(0, 5),
                       textcoords='offset points')

    # Сохраняем результат в файл
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig('decision_analysis.png')
    
    print("\n📊 Визуализация сохранена в файл 'decision_analysis.png'")


if __name__ == "__main__":
    solve_and_visualize_decision_problem()