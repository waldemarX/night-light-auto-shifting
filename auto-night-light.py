import time
import pyautogui
import pydirectinput
import subprocess
import os
import tkinter as tk
from datetime import datetime


def show_warning_dialog():
    """
    Окно предупреждения.
    """
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.title('Предупреждение')
    root.configure(bg='#00FF00')
    font = ('Arial', 14)
    label = tk.Label(root,
                     text='Сейчас будет изменен параметр ночного света.',
                     font=font)
    label.pack(pady=10)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 500
    window_height = 150
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    # Закрытие окна через 2 секунды
    root.after(2000, root.destroy)
    root.mainloop()


def open_night_light_window():
    """
    Открытие параметров ночного света.
    """
    subprocess.run(['control', 'desk.cpl'])
    time.sleep(1)
    pyautogui.hotkey('shift', 'tab')
    pyautogui.press(['tab', 'enter'])
    time.sleep(0.5)
    pyautogui.press(['tab', 'tab'])


def set_night_light_temperature(change_value: int):
    """
    Установка значения температуры.
    """
    show_warning_dialog()
    open_night_light_window()
    # Изменение температуры
    pydirectinput.press('right', presses=change_value)
    # Закрытие окна
    pyautogui.hotkey('alt', 'f4')


def set_start_settings(start_value: int):
    """
    Установка начального значения.
    """
    with open('last-value.txt', 'r') as file:
        last_value = file.read()
    last_value = int(last_value)
    print('Setting starting value...')
    open_night_light_window()
    pydirectinput.press('left', presses=last_value)
    pydirectinput.press('right', presses=start_value)
    pyautogui.hotkey('alt', 'f4')


def set_start_values() -> int:
    """
    Установка начальных параметров.
    """
    start_value: int = int(input('Set start value: '))
    change_value: int = int(input('Set change value: '))
    current_time: int = datetime.now().hour
    os.system('cls')
    return start_value, current_time, change_value


def check_and_change(check_time: int, current_value: int, change_value: int):
    """
    Изменение значения раз в час.
    """
    while True:
        current_hour = datetime.now().hour
        if current_hour > check_time:
            os.system('cls')
            print('Setting new value...')
            check_time = current_hour
            set_night_light_temperature(change_value)
            current_value += 5
            # Запись текущего значения
            with open('last-value.txt', 'w') as file:
                file.write(f'{current_value}')
        os.system('cls')
        print(f'\nCurrent value -> {current_value}\n'
              f'Next change in {60 - datetime.now().minute} minutes')
        # Проверка каждые 60 секунд
        time.sleep(60)


def main():
    """
    Основная функция.
    """
    start_value, current_time, change_value = set_start_values()
    set_start_settings(start_value)
    check_and_change(current_time, start_value, change_value)


if __name__ == "__main__":
    main()
