import numpy as np
import matplotlib.pyplot as plt

# Гипотетическое значение Pi = 4
pi_4 = 4.0
pi_std = np.pi
def circle_perimeter_pi_4(radius):
    return 8 * radius

def circle_area_pi_4(radius):
    """Площадь 'круга Pi=4'."""
    return 4 * radius**2

def square_perimeter(side):
    """Периметр квадрата."""
    return 4 * side

def square_area(side):
    """Площадь квадрата."""
    return side**2

def get_circle_points(radius, center_x=0, center_y=0, n_points=300, pi_value=np.pi):
    """Возвращает координаты точек для построения круга (или 'круга Pi=4') с заданным центром."""
    theta = np.linspace(0, 2 * pi_value, n_points)
    x = radius * np.cos(theta) + center_x
    y = radius * np.sin(theta) + center_y
    return x, y
    
    

def plot_shapes_equal_perimeter_centered(perimeter_value):
    """Строит квадрат и 'круг Pi=4' с равным периметром и общим центром."""
    side_square = perimeter_value / 4
    radius_circle_pi_4 = perimeter_value / 8
    center_x, center_y = 0, 0 # Общий центр в начале координат
    
    area_square = square_area(side_square)
    area_circle_4 = circle_area_pi_4(radius_circle_pi_4)
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    
    # Квадрат с центром
    x_square, y_square = get_square_points_centered(side_square, center_x, center_y)
    ax.plot(x_square, y_square, label=f'Квадрат', color='blue')
    
    # 'Круг Pi=4' с центром
    x_circle_4, y_circle_4 = get_circle_points(radius_circle_pi_4, center_x, center_y, pi_value=pi_4)
    ax.plot(x_circle_4, y_circle_4, label=f"'Круг Pi=4'", color='red')
    
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(f'Квадрат и "Круг Pi=4" с равным периметром = {perimeter_value:.2f}, Центры совпадают')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    
    # Вывод площадей на график
    textstr = '\n'.join((
        f'Площадь квадрата: {area_square:.2f}',
        f'Площадь "Круга Pi=4": {area_circle_4:.2f}',
        f'Периметр общий: {perimeter_value:.2f}',
        f'Радиус "Круга Pi=4": {radius_circle_pi_4:.2f}',
        f'Сторона квадрата: {side_square:.2f}'
    ))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)
    
    plt.show()

def plot_shapes_equal_area_centered(area_value):
    """Строит квадрат и 'круг Pi=4' с равной площадью и общим центром."""
    side_square = np.sqrt(area_value)
    radius_circle_pi_4 = np.sqrt(area_value / 4)
    center_x, center_y = 0, 0 # Общий центр в начале координат
    
    perimeter_square = square_perimeter(side_square)
    perimeter_circle_4 = circle_perimeter_pi_4(radius_circle_pi_4)
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    
    # Квадрат с центром
    x_square, y_square = get_square_points_centered(side_square, center_x, center_y)
    ax.plot(x_square, y_square, label=f'Квадрат', color='blue')
    
    # 'Круг Pi=4' с центром
    x_circle_4, y_circle_4 = get_circle_points(radius_circle_pi_4, center_x, center_y, pi_value=pi_4)
    ax.plot(x_circle_4, y_circle_4, label=f"'Круг Pi=4'", color='red')
    
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(f'Квадрат и "Круг Pi=4" с равной площадью = {area_value:.2f}, Центры совпадают')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.legend()
    
    # Вывод периметров и размеров на график
    textstr = '\n'.join((
        f'Периметр квадрата: {perimeter_square:.2f}',
        f'Периметр "Круга Pi=4": {perimeter_circle_4:.2f}',
        f'Площадь общая: {area_value:.2f}',
        f'Радиус "Круга Pi=4": {radius_circle_pi_4:.2f}',
        f'Сторона квадрата: {side_square:.2f}'
    ))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=props)
    plt.show()
def get_square_points_centered(side, center_x=0, center_y=0):
    half_side = side / 2
    points = [
        (center_x - half_side, center_y - half_side),
        (center_x + half_side, center_y - half_side),
        (center_x + half_side, center_y + half_side),
        (center_x - half_side, center_y + half_side),
        (center_x - half_side, center_y - half_side)
    ]
    x_coords, y_coords = zip(*points)
    return x_coords, y_coords
    
    # --- Функция для построения искаженной полярной сетки ---

def get_distorted_polar_grid(max_radius, n_circles=5, n_rays=16, distortion_factor=2.0):
    radii = np.linspace(0, max_radius, n_circles)
    theta = np.linspace(0, 2 * np.pi, n_rays, endpoint=False)
    
    x_lines = []
    y_lines = []
    
    for r in radii:
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        x_lines.append(x)
        y_lines.append(y)
    
    distorted_theta = np.linspace(0, distortion_factor * np.pi, n_rays, endpoint=False)
    for t in distorted_theta:
        x = radii * np.cos(t)
        y = radii * np.sin(t)
        x_lines.append(x)
        y_lines.append(y)
    
    return x_lines, y_lines
    

def plot_distorted_grid_visualization_with_square():
    """Визуализация искаженной полярной сетки и круга + квадрата."""
    max_radius = 6
    distortion_factor_pi4 = 4.0 / np.pi #  Масштаб искажения для Pi=4
    
    x_grid_distorted, y_grid_distorted = get_distorted_polar_grid(max_radius, distortion_factor=distortion_factor_pi4)
    x_grid_euclidean, y_grid_euclidean = get_distorted_polar_grid(max_radius, distortion_factor=2.0) # Евклидова сетка
    
    radius_circle = 4 # Радиус кругов для примера
    perimeter_circle_pi4 = circle_perimeter_pi_4(radius_circle) # Периметр "круга Pi=4"
    side_square_pi4_perimeter = perimeter_circle_pi4 / 4 # Сторона квадрата с таким же периметром в Pi=4
    perimeter_euclidean_circle = 2 * np.pi * radius_circle # Периметр евклидова круга
    side_square_euclidean_perimeter = perimeter_euclidean_circle / 4 # Сторона евклидова квадрата с таким же периметром
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 7)) # Два подграфика рядом
    
    # Подграфик 1: Искаженная "Pi=4" сетка
    ax1 = axes[0]
    for x_line, y_line in zip(x_grid_distorted, y_grid_distorted):
        ax1.plot(x_line, y_line, color='gray', linewidth=0.5) # Рисуем искаженную сетку
    
    # 'Круг Pi=4' на искаженной сетке
    x_circle_pi4, y_circle_pi4 = get_circle_points(radius_circle, pi_value=pi_4)
    ax1.plot(x_circle_pi4, y_circle_pi4, color='red', linewidth=2, label="'Круг Pi=4'") # Красный круг
    
    # Квадрат (Pi=4, равный периметр кругу Pi=4) на искаженной сетке
    x_square_pi4, y_square_pi4 = get_square_points_centered(side_square_pi4_perimeter)
    ax1.plot(x_square_pi4, y_square_pi4, color='green', linestyle='--', linewidth=2, label="Квадрат (Pi=4, ~периметр)") # Зеленый пунктир
    
    ax1.set_aspect('equal', adjustable='box')
    ax1.set_title('Искаженная "Pi=4" Полярная Сетка, "Круг Pi=4" и Квадрат', fontsize=12)
    ax1.legend()
    ax1.set_xlim([-max_radius*1.2, max_radius*1.2])
    ax1.set_ylim([-max_radius*1.2, max_radius*1.2])
    
    
    # Подграфик 2: Евклидова сетка для сравнения
    ax2 = axes[1]
    for x_line, y_line in zip(x_grid_euclidean, y_grid_euclidean):
        ax2.plot(x_line, y_line, color='gray', linewidth=0.5) # Рисуем евклидову сетку
    
    # Евклидов круг на евклидовой сетке
    x_circle_std, y_circle_std = get_circle_points(radius_circle, pi_value=np.pi)
    ax2.plot(x_circle_std, y_circle_std, color='blue', linewidth=2, label="Евклидов Круг") # Синий круг
    
    # Евклидов квадрат (равный периметр евклидову кругу) на евклидовой сетке
    x_square_std, y_square_std = get_square_points_centered(side_square_euclidean_perimeter)
    ax2.plot(x_square_std, y_square_std, color='purple', linestyle='--', linewidth=2, label="Евклидов Квадрат (~периметр)") # Фиолетовый пунктир
    
    ax2.set_aspect('equal', adjustable='box')
    ax2.set_title('Евклидова Полярная Сетка, Евклидов Круг и Квадрат', fontsize=12)
    ax2.legend()
    ax2.set_xlim([-max_radius*1.2, max_radius*1.2])
    ax2.set_ylim([-max_radius*1.2, max_radius*1.2])
    
    
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    plot_distorted_grid_visualization_with_square()