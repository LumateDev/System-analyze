import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import FancyBboxPatch
import matplotlib.patches as mpatches

def calculate_payoff(stock_level, demand_level, profit_per_box, cost_of_unsold):
    """
    Рассчитывает финансовый результат (прибыль/убыток) для конкретного сценария.
    """
    sold_boxes = min(stock_level, demand_level)
    unsold_boxes = stock_level - sold_boxes
    total_profit = (sold_boxes * profit_per_box) - (unsold_boxes * cost_of_unsold)
    return total_profit

def calculate_emv(payoff_row, probabilities):
    """
    Рассчитывает ожидаемую денежную стоимость (EMV).
    """
    return np.dot(payoff_row, probabilities)

def solve_decision_with_research():
    """
    Решает задачу принятия решений с возможностью дополнительного исследования.
    """
    # --- 1. Исходные данные ---
    profit_per_box = 35.0
    cost_of_unsold = 56.0
    research_cost = 15.0
    
    actions = [11, 12, 13]
    demand_levels = [11, 12, 13]
    
    # Вероятности без исследования (исходные)
    prob_original = [0.45, 0.35, 0.20]
    
    # Вероятности после исследования (уточненные)
    prob_research = [0.40, 0.35, 0.25]

    print("=" * 80)
    print("🔬 АНАЛИЗ РЕШЕНИЯ О ПРОВЕДЕНИИ ДОПОЛНИТЕЛЬНОГО ИССЛЕДОВАНИЯ")
    print("   Задача «Фото КОЛОР»")
    print("=" * 80)
    print(f"\n📌 Экономические параметры:")
    print(f"   • Прибыль с проданного ящика: {profit_per_box} тыс. руб.")
    print(f"   • Убыток с непроданного ящика: {cost_of_unsold} тыс. руб.")
    print(f"   • Стоимость исследования: {research_cost} тыс. руб.")

    # --- 2. Построение платежной матрицы ---
    payoff_matrix = [
        [calculate_payoff(stock, demand, profit_per_box, cost_of_unsold) 
         for demand in demand_levels] 
        for stock in actions
    ]
    
    df_payoff = pd.DataFrame(
        payoff_matrix,
        index=[f"Закупить {a}" for a in actions],
        columns=[f"Спрос {d}" for d in demand_levels]
    )
    
    print("\n" + "─" * 80)
    print("📊 ШАГ 1: Платежная матрица (одинакова для обоих сценариев)")
    print("─" * 80)
    print(df_payoff)

    # --- 3. Расчет EMV БЕЗ исследования ---
    print("\n" + "─" * 80)
    print("📈 ШАГ 2: Анализ ИСХОДНОЙ ситуации (БЕЗ исследования)")
    print("─" * 80)
    print(f"Вероятности спроса: P(11)={prob_original[0]}, P(12)={prob_original[1]}, P(13)={prob_original[2]}")
    print()
    
    emv_original = {}
    for stock, payoff_row in zip(actions, payoff_matrix):
        emv = calculate_emv(payoff_row, prob_original)
        emv_original[stock] = emv
        print(f"   EMV(Закупить {stock}) = {emv:.2f} тыс. руб.")
    
    optimal_original = max(emv_original, key=emv_original.get)
    max_emv_original = emv_original[optimal_original]
    
    print(f"\n   ✅ Оптимально БЕЗ исследования: закупать {optimal_original} ящиков")
    print(f"   💰 Ожидаемая прибыль: {max_emv_original:.2f} тыс. руб.")

    # --- 4. Расчет EMV С исследованием ---
    print("\n" + "─" * 80)
    print("🔬 ШАГ 3: Анализ ситуации С исследованием")
    print("─" * 80)
    print(f"Уточненные вероятности: P(11)={prob_research[0]}, P(12)={prob_research[1]}, P(13)={prob_research[2]}")
    print()
    
    emv_research = {}
    for stock, payoff_row in zip(actions, payoff_matrix):
        emv = calculate_emv(payoff_row, prob_research)
        emv_research[stock] = emv
        print(f"   EMV(Закупить {stock}) = {emv:.2f} тыс. руб.")
    
    optimal_research = max(emv_research, key=emv_research.get)
    max_emv_research = emv_research[optimal_research]
    
    print(f"\n   ✅ Оптимально С исследованием: закупать {optimal_research} ящиков")
    print(f"   💰 Ожидаемая прибыль ДО вычета стоимости: {max_emv_research:.2f} тыс. руб.")
    print(f"   💸 Стоимость исследования: -{research_cost:.2f} тыс. руб.")
    
    net_emv_research = max_emv_research - research_cost
    print(f"   💵 Чистая ожидаемая прибыль: {net_emv_research:.2f} тыс. руб.")

    # --- 5. Итоговое сравнение ---
    print("\n" + "=" * 80)
    print("🎯 ИТОГОВОЕ РЕШЕНИЕ")
    print("=" * 80)
    
    if net_emv_research > max_emv_original:
        advantage = net_emv_research - max_emv_original
        print(f"\n✅ РЕКОМЕНДАЦИЯ: Проводить исследование")
        print(f"   • Чистая выгода от исследования: +{advantage:.2f} тыс. руб.")
        print(f"   • Оптимальная закупка: {optimal_research} ящиков в неделю")
        print(f"   • Ожидаемая прибыль: {net_emv_research:.2f} тыс. руб./неделю")
        final_decision = "Проводить"
        final_action = optimal_research
        final_profit = net_emv_research
    else:
        loss = max_emv_original - net_emv_research
        print(f"\n❌ РЕКОМЕНДАЦИЯ: НЕ проводить исследование")
        print(f"   • Исследование снизит прибыль на: -{loss:.2f} тыс. руб.")
        print(f"   • Оптимальная закупка: {optimal_original} ящиков в неделю")
        print(f"   • Ожидаемая прибыль: {max_emv_original:.2f} тыс. руб./неделю")
        final_decision = "НЕ проводить"
        final_action = optimal_original
        final_profit = max_emv_original
    
    print("\n" + "=" * 80)

    # --- 6. Визуализация ---
    visualize_research_decision(
        df_payoff, 
        actions,
        emv_original, 
        emv_research, 
        prob_original, 
        prob_research,
        max_emv_original,
        net_emv_research,
        research_cost,
        final_decision,
        optimal_original,
        optimal_research
    )

    return {
        'conduct_research': net_emv_research > max_emv_original,
        'optimal_action': final_action,
        'expected_profit': final_profit
    }

def visualize_research_decision(df_payoff, actions, emv_orig, emv_res, 
                                prob_orig, prob_res, max_orig, net_res, 
                                cost, decision, opt_orig, opt_res):
    """
    Создает комплексную визуализацию решения о проведении исследования.
    """
    sns.set_theme(style="whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.25)
    
    # Заголовок (БЕЗ эмодзи)
    fig.suptitle('Анализ решения о проведении дополнительного исследования рынка\n«Фото КОЛОР»', 
                 fontsize=22, weight='bold', y=0.98)

    # --- График 1: Платежная матрица ---
    ax1 = fig.add_subplot(gs[0, :])
    sns.heatmap(df_payoff, ax=ax1, annot=True, fmt=".0f", cmap="RdYlGn", 
                linewidths=2, cbar_kws={'label': 'Прибыль (тыс. руб.)'}, 
                annot_kws={"size": 13, "weight": "bold"})
    ax1.set_title('Платежная матрица (результаты для всех комбинаций)', 
                  fontsize=16, pad=15, weight='bold')
    ax1.tick_params(axis='y', rotation=0, labelsize=12)
    ax1.tick_params(axis='x', labelsize=12)

    # --- График 2: Сравнение EMV без исследования ---
    ax2 = fig.add_subplot(gs[1, 0])
    strategies = [f"Закупить {a}" for a in actions]
    emv_orig_values = list(emv_orig.values())
    colors_orig = ['#FF6B6B' if a != opt_orig else '#4ECDC4' for a in actions]
    
    bars2 = ax2.bar(strategies, emv_orig_values, color=colors_orig, 
                    edgecolor='black', linewidth=2, alpha=0.8)
    ax2.set_title(f'БЕЗ исследования\nВероятности: {prob_orig}', 
                  fontsize=14, weight='bold', pad=10)
    ax2.set_ylabel('EMV (тыс. руб.)', fontsize=12, weight='bold')
    ax2.set_ylim(min(emv_orig_values) * 0.9, max(emv_orig_values) * 1.1)
    ax2.axhline(y=max(emv_orig_values), color='green', linestyle='--', 
                linewidth=2, alpha=0.5, label=f'Максимум: {max(emv_orig_values):.2f}')
    
    for bar, val in zip(bars2, emv_orig_values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', 
                fontsize=12, weight='bold')
    ax2.legend(loc='upper right')
    ax2.grid(axis='y', alpha=0.3)

    # --- График 3: Сравнение EMV с исследованием ---
    ax3 = fig.add_subplot(gs[1, 1])
    emv_res_values = list(emv_res.values())
    colors_res = ['#FF6B6B' if a != opt_res else '#95E1D3' for a in actions]
    
    bars3 = ax3.bar(strategies, emv_res_values, color=colors_res, 
                    edgecolor='black', linewidth=2, alpha=0.8)
    ax3.set_title(f'С исследованием\nВероятности: {prob_res}', 
                  fontsize=14, weight='bold', pad=10)
    ax3.set_ylabel('EMV (тыс. руб.)', fontsize=12, weight='bold')
    ax3.set_ylim(min(emv_res_values) * 0.9, max(emv_res_values) * 1.1)
    ax3.axhline(y=max(emv_res_values), color='blue', linestyle='--', 
                linewidth=2, alpha=0.5, label=f'Максимум: {max(emv_res_values):.2f}')
    
    for bar, val in zip(bars3, emv_res_values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', 
                fontsize=12, weight='bold')
    ax3.legend(loc='upper right')
    ax3.grid(axis='y', alpha=0.3)

    # --- График 4: Итоговое сравнение ---
    ax4 = fig.add_subplot(gs[2, :])
    
    scenarios = ['БЕЗ исследования', 'С исследованием\n(до вычета стоимости)', 
                 'С исследованием\n(чистая прибыль)']
    values = [max_orig, max(emv_res_values), net_res]
    colors_final = ['#4ECDC4', '#95E1D3', '#F38181'] if net_res < max_orig else ['#F38181', '#95E1D3', '#4ECDC4']
    
    bars4 = ax4.bar(scenarios, values, color=colors_final, 
                    edgecolor='black', linewidth=3, alpha=0.85, width=0.6)
    
    # Стрелка показывающая вычет стоимости
    ax4.annotate('', xy=(1.9, net_res), xytext=(1.9, max(emv_res_values)),
                arrowprops=dict(arrowstyle='<->', color='red', lw=3))
    ax4.text(2.15, (net_res + max(emv_res_values))/2, f'-{cost:.0f}\n(стоимость\nисследования)', 
            fontsize=11, color='red', weight='bold', va='center')
    
    ax4.set_title('ИТОГОВОЕ СРАВНЕНИЕ: Проводить ли исследование?', 
                  fontsize=16, weight='bold', pad=15)
    ax4.set_ylabel('Ожидаемая прибыль (тыс. руб.)', fontsize=13, weight='bold')
    ax4.set_ylim(min(values) * 0.85, max(values) * 1.15)
    
    for bar, val in zip(bars4, values):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.2f}', ha='center', va='bottom', 
                fontsize=14, weight='bold', 
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    # Добавляем вердикт (БЕЗ эмодзи)
    verdict_color = 'darkgreen' if net_res > max_orig else 'darkred'
    verdict_symbol = '[V]' if net_res > max_orig else '[X]'
    verdict_text = f"{verdict_symbol} РЕШЕНИЕ: {decision} исследование"
    
    ax4.text(0.5, 0.95, verdict_text, 
            transform=ax4.transAxes, fontsize=16, weight='bold',
            color=verdict_color, ha='center', va='top',
            bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', 
                     edgecolor=verdict_color, linewidth=3))
    
    ax4.grid(axis='y', alpha=0.4)

    plt.savefig('decision_analysis_with_research.png', dpi=300, bbox_inches='tight')
    print("\n📊 Визуализация сохранена в файл 'decision_analysis_with_research.png'")

if __name__ == "__main__":
    result = solve_decision_with_research()