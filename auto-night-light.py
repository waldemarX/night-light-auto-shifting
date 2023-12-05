import time
import pyautogui
import pydirectinput
import subprocess
import os
import tkinter as tk
from datetime import datetime, timedelta


def show_warning_dialog():
    """
    Окно предупреждения.
    """
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.title('Warning')
    root.configure(bg='#00FF00')
    font = ('Arial', 14)
    label = tk.Label(root,
                     text='Prepare for change night light param.',
                     font=font)
    label.pack(pady=10)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 500
    window_height = 150
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
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
    pydirectinput.press('right', presses=change_value)
    pyautogui.hotkey('alt', 'f4')


def set_start_settings(start_value: int):
    """
    Установка начального значения.
    """
    last_value = read_file()
    if start_value == last_value:
        print('Last value was the same, no need to change start value')
        time.sleep(1.5)
        return
    print('Setting start value...')
    open_night_light_window()
    if last_value > start_value:
        pydirectinput.press('left', presses=(last_value - start_value))
    else:
        pydirectinput.press('right', presses=(start_value - last_value))
    pyautogui.hotkey('alt', 'f4')
    write_file(start_value)


def set_start_values() -> int:
    """
    Установка начальных параметров.
    """
    while True:
        try:
            start_value = int(input('Set start value: '))
            change_value = int(input('Set change value: '))
            period = int(input('Set period (minutes): '))
            break
        except ValueError:
            print('Invalid input. Please enter a valid integer.')
    os.system('cls')
    return start_value, change_value, period


def read_file() -> int:
    """
    Чтение файла.
    """
    try:
        with open('last-value.txt', 'r') as file:
            value = file.read()
            return int(value) if value else 0
    except (FileNotFoundError, ValueError):
        return 0


def write_file(current_value):
    """
    Запись в файл.
    """
    with open('last-value.txt', 'w') as file:
        file.write(f'{current_value}')


def get_time_now():
    """
    Текущее время
    """
    return datetime.now().strftime("%H:%M")


def get_time_next(period):
    """
    Время следующего изменения
    """
    return (datetime.now() + timedelta(minutes=period)).strftime("%H:%M")


def check_and_change(current_value: int, change_value: int, period: int):
    """
    Изменение значения
    """
    while True:
        os.system('cls')
        print(f'Current value -> {current_value}\n'
              f'Change value -> {change_value}\n'
              f'Value change every {period} minutes\n'
              f'Last update -> {get_time_now()}\n'
              f'Next update -> {get_time_next(period)}\n')
        print('Waiting for next change...')
        time.sleep(60 * period)
        os.system('cls')
        print('Setting new value...')
        set_night_light_temperature(change_value)
        current_value += change_value
        write_file(current_value)


def main():
    print(f'Last value was -> {read_file()}\n')
    start_value, change_value, period = set_start_values()
    set_start_settings(start_value)
    check_and_change(start_value, change_value, period)


if __name__ == "__main__":
    main()
