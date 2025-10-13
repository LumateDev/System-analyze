import numpy as np
import matplotlib.pyplot as plt

# Функция проверки, удовлетворяет ли точка всем ограничениям
def is_feasible(x, y):
    return (
        4*x + 5*y >= 40 and  # X: 4x + 5y ≥ 40
        2*x + y >= 14 and    # Y: 2x + y ≥ 14
        3*x + y >= 18 and    # Z: 3x + y ≥ 18
        x >= 0 and y >= 0    # Неотрицательность
    )

# Найдем точки пересечения ограничений
# 1. 4x + 5y = 40 и 2x + y = 14
# Из второго: y = 14 - 2x
# Подставим в первое: 4x + 5(14 - 2x) = 40 → -6x = -30 → x = 5, y = 4
point1 = (5, 4)

# 2. 2x + y = 14 и 3x + y = 18
# Вычтем: x = 4 → y = 14 - 8 = 6
point2 = (4, 6)

# 3. 4x + 5y = 40 и 3x + y = 18
# Из второго: y = 18 - 3x
# Подставим в первое: 4x + 5(18 - 3x) = 40 → -11x = -50 → x = 50/11, y = 48/11
x3 = 50 / 11
y3 = 48 / 11
point3 = (x3, y3)

# 4. Пересечение с осями (x=0, y=0)
# x = 0: 5y = 40 → y = 8 → (0, 8) → проверим
point4 = (0, 8)
# y = 0: 4x = 40 → x = 10 → (10, 0) → проверим
point5 = (10, 0)

# Соберем все точки
all_points = [point1, point2, point3, point4, point5]

# Проверим, какие из них допустимы
feasible_points = []
for x, y in all_points:
    if is_feasible(x, y):
        cost = 1.5 * x + 3 * y  # Целевая функция: 1.5x + 3y
        feasible_points.append((x, y, cost))

# Найдем точку с минимальной стоимостью
best = min(feasible_points, key=lambda p: p[2])

print("Результат ручного метода:")
print(f"Оптимальное количество продукта A: {best[0]:.2f} л")
print(f"Оптимальное количество продукта B: {best[1]:.2f} л")
print(f"Минимальная стоимость: {best[2]:.2f} ф. ст.")

# График
x_vals = np.linspace(0, 15, 400)

# Ограничения
y1 = (40 - 4*x_vals) / 5        # 4x + 5y >= 40 → y >= (40-4x)/5
y2 = 14 - 2*x_vals              # 2x + y >= 14 → y >= 14 - 2x
y3 = 18 - 3*x_vals              # 3x + y >= 18 → y >= 18 - 3x

plt.figure(figsize=(10, 8))

# Построим ограничения
plt.plot(x_vals, y1, 'r-', label='4x + 5y ≥ 40')
plt.plot(x_vals, y2, 'g-', label='2x + y ≥ 14')
plt.plot(x_vals, y3, 'b-', label='3x + y ≥ 18')

# Заштрихуем область допустимых решений
y_max = np.maximum(np.maximum(y1, y2), y3)
plt.fill_between(x_vals, y_max, 20, color='gray', alpha=0.3, label='Допустимая область')

# Отметим все допустимые точки
for x, y, cost in feasible_points:
    plt.plot(x, y, 'bo', markersize=8, label=f'({x:.2f}, {y:.2f})')

# Отметим оптимальную точку
plt.plot(best[0], best[1], 'ro', markersize=12, label=f'Оптимум ({best[0]:.2f}, {best[1]:.2f})')

plt.xlim(0, 15)
plt.ylim(0, 20)
plt.xlabel('Продукт A (л)')
plt.ylabel('Продукт B (л)')
plt.title('Область допустимых решений и оптимальное решение')
plt.legend()
plt.grid(True)
plt.show()