
import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal

num_obj = [2]
den_obj = [3, 4, 1]

Kp = 2.0
Ki = 0.5
Kd = 0.5

num_reg = [Kd, Kp, Ki]
den_reg = [1, 0]

num_open = np.polymul(num_reg, num_obj)
den_open = np.polymul(den_reg, den_obj)

den_closed = np.polyadd(den_open, num_open)

W_closed = signal.TransferFunction(
    num_open,
    den_closed
)

t, y = signal.step(W_closed, N=500)

y_set = 1.0
y_max = np.max(y)

overshoot = max(0, (y_max - y_set) / y_set * 100)

static_error = abs(y_set - y[-1])

outside = np.where(
    np.abs(y - y_set) > 0.05 * y_set
)[0]

if len(outside) == 0:
    settling_time = 0
elif outside[-1] == len(t) - 1:
    settling_time = None
else:
    settling_time = t[outside[-1] + 1]

print("Результати моделювання:")
print(f"Максимальне значення: {y_max:.4f}")
print(f"Перерегулювання: {overshoot:.2f}%")
print(f"Статична похибка: {static_error:.4f}")

if settling_time is not None:
    print(f"Час регулювання: {settling_time:.4f} секунд")
else:
    print("Час регулювання: не досягнуто в межах моделювання")

plt.figure(figsize=(9, 5))

plt.plot(
    t, y,
    'b-',
    linewidth=2,
    label='Вихід АСУ y(t)'
)

plt.axhline(
    1.0,
    color='r',
    linestyle='--',
    label='Задане значення R(t)=1'
)

plt.axhline(
    1.05,
    color='g',
    linestyle=':',
    label='Верхня межа +5%'
)

plt.axhline(
    0.95,
    color='g',
    linestyle=':',
    label='Нижня межа -5%'
)

plt.title('Перехідна характеристика системи регулювання')
plt.xlabel('Час (секунди)')
plt.ylabel('Амплітуда')

plt.grid(True, linestyle=':', linewidth=0.7)
plt.legend()
plt.tight_layout()
plt.show()
