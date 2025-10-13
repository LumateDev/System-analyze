import numpy as np
import matplotlib.pyplot as plt

def line_intersection(a1, b1, c1, a2, b2, c2):
    """
    Решает систему:
    a1*x + b1*y = c1
    a2*x + b2*y = c2
    """
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None  # прямые параллельны
    x = (c1 * b2 - c2 * b1) / det
    y = (a1 * c2 - a2 * c1) / det
    return (x, y)

# Функция проверки, удовлетворяет ли точка всем ограничениям
def is_feasible(x, y):
    return (
        4*x + 5*y >= 40 and  # X: 4x + 5y ≥ 40
        2*x + y >= 14 and    # Y: 2x + y ≥ 14
        3*x + y >= 18 and    # Z: 3x + y ≥ 18
        x >= 0 and y >= 0    # Неотрицательность
    )

# Ограничения: ax + by = c
constraints = [
    (4, 5, 40),  # 4x + 5y = 40
    (2, 1, 14),  # 2x + y = 14
    (3, 1, 18),  # 3x + y = 18
]

all_points = []

# Пересечения ограничений
for i in range(len(constraints)):
    for j in range(i + 1, len(constraints)):
        a1, b1, c1 = constraints[i]
        a2, b2, c2 = constraints[j]
        point = line_intersection(a1, b1, c1, a2, b2, c2)
        if point:
            all_points.append(point)

# Пересечения с осями
# x = 0: 4x + 5y = 40 → y = 8
all_points.append((0, 8))
# y = 0: 4x + 5y = 40 → x = 10
all_points.append((10, 0))

# Удалим дубликаты (округляем до 6 знаков)
all_points = list(set((round(x, 6), round(y, 6)) for x, y in all_points))

print("Все найденные точки пересечения:")
for x, y in all_points:
    feasible = is_feasible(x, y)
    cost = 1.5 * x + 3 * y if feasible else "N/A"
    status = "Допустима" if feasible else "Недопустима"
    print(f"Точка ({x}, {y}) — {status}, стоимость: {cost}")

# Проверим, какие из них допустимы
feasible_points = []
for x, y in all_points:
    if is_feasible(x, y):
        cost = 1.5 * x + 3 * y
        feasible_points.append((x, y, cost))

print("\nДопустимые точки с их стоимостью:")
for x, y, cost in feasible_points:
    print(f"({x}, {y}) — стоимость: {cost:.2f}")

# Найдем точку с минимальной стоимостью
best = min(feasible_points, key=lambda p: p[2])

print("\nРезультат ручного метода:")
print(f"Оптимальное количество продукта A: {best[0]:.2f} л")
print(f"Оптимальное количество продукта B: {best[1]:.2f} л")
print(f"Минимальная стоимость: {best[2]:.2f} ф. ст.")

# График
x_vals = np.linspace(0, 15, 400)

# Ограничения
y1 = (40 - 4*x_vals) / 5        # 4x + 5y >= 40 → y >= (40-4x)/5
y2 = 14 - 2*x_vals              # 2x + y ≥ 14 → y >= 14 - 2x
y3 = 18 - 3*x_vals              # 3x + y ≥ 18 → y >= 18 - 3x

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