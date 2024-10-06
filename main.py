import tkinter as tk  # Импортируем библиотеку для создания графического интерфейса
import pyautogui  # Импортируем библиотеку для управления мышью и клавиатурой
from pynput import mouse  # Импортируем библиотеку для отслеживания событий мыши
import time  # Импортируем библиотеку для работы со временем


class MacroRecorderApp:
    def __init__(self, master):
        self.master = master  # Сохраняем ссылку на главное окно
        master.title("Макрос Запись и Воспроизведение")  # Устанавливаем заголовок окна

        self.recording = False  # Флаг, указывающий на то, идет ли запись
        self.recorded_actions = []  # Список для хранения записанных действий

        # Кнопка для начала/остановки записи макроса
        self.record_button = tk.Button(master, text="Записать Макрос", command=self.toggle_record)
        self.record_button.pack()  # Размещаем кнопку в окне

        # Кнопка для воспроизведения записанного макроса
        self.play_button = tk.Button(master, text="Воспроизвести Макрос", command=self.play_macro)
        self.play_button.pack()  # Размещаем кнопку в окне

        self.info_label = tk.Label(master, text="")  # Метка для отображения информации пользователю
        self.info_label.pack()  # Размещаем метку в окне

        master.attributes('-topmost', True)  # Устанавливаем окно всегда поверх других окон

    def toggle_record(self):
        """Переключает режим записи макроса."""
        if not self.recording:  # Если запись не идет
            self.recording = True  # Устанавливаем флаг записи в True
            self.record_button.config(text="Стоп Запись")  # Изменяем текст кнопки
            self.recorded_actions = []  # Очищаем список записанных действий
            self.info_label.config(text="Запись макроса начата")  # Информируем пользователя
            self.start_mouse_listener()  # Запускаем слушатель событий мыши
        else:  # Если запись идет
            self.recording = False  # Устанавливаем флаг записи в False
            self.record_button.config(text="Записать Макрос")  # Возвращаем текст кнопки к исходному
            self.info_label.config(text="Запись макроса завершена")  # Информируем пользователя

    def record_mouse_click(self, x, y, button, pressed):
        """Записывает координаты клика мыши."""
        if pressed and self.recording:  # Если нажата кнопка мыши и идет запись
            if not self.is_button_clicked(x, y):  # Проверяем, не нажата ли кнопка интерфейса
                self.recorded_actions.append((x, y, time.time()))  # Сохраняем координаты и время клика

    def start_mouse_listener(self):
        """Запускает слушатель для отслеживания кликов мыши."""
        listener = mouse.Listener(on_click=self.record_mouse_click)  # Создаем слушатель кликов мыши
        listener.start()  # Запускаем слушатель в фоновом режиме

    def play_macro(self):
        """Воспроизводит записанный макрос."""
        if not self.recorded_actions:  # Проверяем, есть ли записанные действия
            self.info_label.config(text="Макрос пуст!")  # Информируем пользователя о пустом макросе
            return

        start_time = self.recorded_actions[0][2]  # Время начала записи макроса
        for click in self.recorded_actions:  # Проходим по всем записанным действиям
            pyautogui.moveTo(click[0], click[1], duration=0.25)  # Двигаем мышь к координатам с задержкой

            pyautogui.click(clicks=1)  # Выполняем одиночный клик мыши

            current_time = click[2]  # Получаем время текущего клика
            delay = current_time - start_time  # Вычисляем задержку между кликами
            start_time = current_time  # Обновляем время начала для следующего клика
            time.sleep(delay)  # Ждем перед следующим действием

    def is_button_clicked(self, x, y):
        """Проверяет, был ли клик внутри кнопок интерфейса."""
        button_coords = [
            (self.record_button.winfo_rootx(), self.record_button.winfo_rooty(),
             self.record_button.winfo_width(), self.record_button.winfo_height()),
            (self.play_button.winfo_rootx(), self.play_button.winfo_rooty(),
             self.play_button.winfo_width(), self.play_button.winfo_height())
        ]

        for bx, by, bw, bh in button_coords:  # Проходим по всем кнопкам интерфейса
            if bx <= x <= bx + bw and by <= y <= by + bh:
                return True  # Если клик внутри кнопки, возвращаем True

        return False  # Если клик вне кнопок, возвращаем False


def main():
    root = tk.Tk()  # Создаем главное окно приложения
    app = MacroRecorderApp(root)  # Инициализируем приложение с главным окном
    root.mainloop()  # Запускаем главный цикл приложения


if __name__ == "__main__":
    main()  # Запускаем функцию main при выполнении скрипта