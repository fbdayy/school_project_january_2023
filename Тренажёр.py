# This Python file uses the following encoding: utf-8
# --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# Импорт специфичных системе функций и нужных классов
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
# Импорт возможности загрузки пользовательского интерфейса
from PyQt5 import uic
# Импорт прочих вспомогательных функций
from random import randint, choice
from math import log


# Класс, отвечающий за меню (главное окно)
class Main(QMainWindow):
    # Инициализация
    def __init__(self):
        # Инициализация родительского класса QMainWindow
        super(Main, self).__init__()
        # Загрузка пользовательского интерфейса
        uic.loadUi('Main.ui', self)
        # Подключение кнопки к функции открытия окна генератора
        self.pushButton.clicked.connect(self.open_generator)

    # Открытие окна генератора
    def open_generator(self):
        # Получение выбранного типа задания
        task_type = self.comboBox.currentText()
        # Открытие генератора с параметром для выбранного типа задания
        if task_type[0] == 'К':
            self.generator_window = Generator(1)
            self.generator_window.show()
        if task_type[0] == 'С':
            self.generator_window = Generator(2)
            self.generator_window.show()
        elif task_type[0] == 'Н':
            self.generator_window = Generator(3)
            self.generator_window.show()
        elif task_type[0] == 'П':
            self.generator_window = Generator(4)
            self.generator_window.show()
        elif task_type[0] == 'N':
            self.generator_window = Generator(5)
            self.generator_window.show()
        # Скрытие окна без его окончательного закрытия
        self.hide()

    # Отслеживание нажатия клавиш
    def keyPressEvent(self, event):
        if event.key() == 16777220:
            # Нажатие кнопки, если enter
            self.pushButton.click()
            # Закрыть окно, если нажата клавиша esc
        elif event.key() == 16777216:
            self.close()

    # Отслеживание закрытия окна
    def closeEvent(self, event):
        # Правила хорошего тона :)
        print('Хорошего дня')
        event.accept()


# Класс, отвечающий за окно генерации задания
class Generator(QWidget):
    def __init__(self, asktype):
        super(Generator, self).__init__()
        uic.loadUi('Generator.ui', self)
        self.pushButton.clicked.connect(self.generation)
        # lineEdit - строка ввода, label - текстовая метка, pushButton - кнопка
        # isvisible - видимость строки ввода, isgenerated - статус генерации
        # expression - выражение, right_answer - правильный ответ
        # placeholder - текстовая подложка во вводе
        self.lineEdit.hide()
        self.isgenerated = 0
        self.lineEdit.textChanged.connect(self.refresh)
        # Выбор текстовой подложки для ввода параметра в зависимости от задания
        self.asktype = asktype
        if self.asktype == 1:
            self.placeholder = 'Ищем: (0-1); количество слагаемых: (2-3)'
        elif self.asktype == 2:
            self.placeholder = 'Тип задания: (0-1); система: (3, 5, 6, 7, 9)'
        elif self.asktype == 3:
            self.placeholder = 'Тип задания: (0-2); количество слагаемых: (1-3)'
        elif self.asktype == 4:
            self.placeholder = 'Система: (3, 5, 6, 7, 9); количество слагаемых: (2-4)'

    # Генерация
    def generation(self):
        # Обновление текстовой метки
        self.refresh()
        if not self.isgenerated:
            # Действия генератора в зависимости от выбранного типа
            # (в соответствии с их порядком в меню)
            if self.asktype == 1:
                # Присвоение переменных с учётом параметра
                text = self.lineEdit.text().strip().replace(' ', '')
                if text.isdigit() and text in ['02', '03', '12', '13']:
                    parameter = int(text[0])
                    count_summand = int(text[1])
                else:
                    parameter = randint(0, 1)
                    count_summand = randint(2, 3)
                self.expression = self.generation_numbers(count_summand)
                signs = list()
                task_word = [['нулей', '0'], ['единиц', '1']]
                for i in range(count_summand):
                    signs.append(choice(['-', '+']))
                if '-' not in signs:
                    signs[randint(0, (len(signs) - 1))] = '-'
                while count_summand != 0:
                    sign = signs[::-1][count_summand - 1]
                    self.expression += (' ' + sign + ' ' + self.generation_numbers(count_summand, sign, self.expression))
                    count_summand -= 1
                self.label.setText('Сколько {} в записи двоичного числа данного выражения:\n{}?'.format(task_word[parameter][0], self.expression))
                self.right_answer = str(self.count_number_in(bin(eval(self.expression))[2:], task_word[parameter][1]))
                self.generation_changes()
            elif self.asktype == 2:
                text = self.lineEdit.text().strip().replace(' ', '')
                if text.isdigit() and text in ['03', '05', '06', '07', '09', '13', '15', '16', '17', '19']:
                    parameter = int(text[0])
                    number_system = int(text[1])
                else:
                    parameter = randint(0, 1)
                    number_system = choice([3, 5, 6, 7, 9])
                front_power = randint(1, 3)
                back_power = randint(20, 250)
                self.expression = '{} * {}**{}'.format(randint(2, 150), number_system ** front_power, back_power // front_power)
                signs = [choice(['+', '-'])]
                if signs[0] == '+':
                    signs.append('-')
                elif parameter == 1:
                    signs[0] = '+'
                    signs.append('-')
                else:
                    signs.append(choice(['+', '-']))
                if signs[0] == '-':
                    if back_power == 20:
                        power_next = (20 // front_power) - 1
                    else:
                        power_next = randint(19 // front_power, (back_power - front_power) // front_power)
                    front_power = randint(1, 3)
                    if eval(self.expression) // number_system ** power_next < 150:
                        self.expression += ' {} {} * {}**{}'.format(signs[0], randint(2, eval(self.expression) // number_system ** power_next),
                                                             number_system ** front_power, power_next // front_power)
                    else:
                        self.expression += ' {} {} * {}**{}'.format(signs[0],randint(2, 150), number_system ** front_power,
                                                             power_next // front_power)
                else:
                    self.expression += ' {} {} * {}**{}'.format(signs[0], randint(2, 150), number_system ** front_power,
                                                         randint(20, 250) // front_power)
                self.expression += ' {} {}'.format(signs[1], randint(10, 1000))
                if parameter == 0:
                    self.label.setText('Чему равна {} в данном выражении в {}-ой системе счисления:\n{}?'.
                          format(choice(['cумма цифр', 'cумма разрядов']), number_system, self.expression))
                    self.right_answer = str(self.sum_numbers_in(self.convert_to(eval(self.expression), number_system)))
                else:
                    self.label.setText('Сколько нулей в записи данного выражения в {}-ой системе:\n{}?'.format(number_system, self.expression))
                    self.right_answer = str(self.count_number_in(self.convert_to(eval(self.expression), number_system), '0'))
                self.generation_changes()
            elif self.asktype == 3:
                text = self.lineEdit.text().strip().replace(' ', '')
                if text.isdigit() and text in ['01', '02', '03', '11', '12', '13', '21', '22', '23']:
                    parameter = int(text[0])
                    count_summand = int(text[1])
                else:
                    parameter = randint(0, 2)
                    count_summand = randint(1, 3)
                number_system = choice(['2', '4'])
                task = ['Сколько цифр', 'Какая первая цифра', 'Сколько различных цифр']
                task_word = {4: 'четверичной', 8: 'восьмеричной', 16: 'шестнадцатеричной'}
                if number_system == '2':
                    task_number_system = choice([4, 8, 16])
                else:
                    task_number_system = 16
                power_now = randint(100, 500)
                self.expression = '{}**{}'.format(number_system, power_now)
                for i in range(count_summand):
                    sign = choice(['+', '-'])
                    if sign == '-' and parameter != 1:
                        power_next = randint(power_now - 5, power_now - 1)
                    else:
                        power_next = randint(power_now - 5, power_now + 5)
                        sign = '+'
                    self.expression += ' {} {}**{}'.format(sign, number_system, power_next)
                self.label.setText('{} в {} записи данного выражения:\n{}?'.format(task[parameter], task_word[task_number_system], self.expression))
                if parameter == 0:
                    self.right_answer = str(len(self.convert_to(eval(self.expression), task_number_system)))
                elif parameter == 1:
                    self.right_answer = str(self.convert_to(eval(self.expression), task_number_system)[0])
                else:
                    set_digits = set()
                    for i in self.convert_to(eval(self.expression), task_number_system):
                        set_digits.add(i)
                    self.right_answer = str(len(set_digits))
                self.generation_changes()
            elif self.asktype == 4:
                text = self.lineEdit.text().strip().replace(' ', '')
                if text.isdigit() and text in ['32', '52', '62', '72', '92', '33', '53', '63', '73', '93', '34', '54', '64', '74', '94']:
                    number_system = int(text[0])
                    count_summand = int(text[1])
                else:
                    number_system = choice([3, 5, 6, 7, 9])
                    count_summand = randint(2, 4)
                front_power = randint(1, 3)
                self.expression = '{} * {}**{}'.format(randint(2, 150), number_system ** front_power, randint(20, 250) // front_power)
                signs = list()
                for i in range(count_summand):
                    signs.append(choice(['-', '+']))
                if '-' not in signs:
                    signs[randint(0, (len(signs) - 1))] = '-'
                if '+' not in signs:
                    signs[randint(0, (len(signs) - 1))] = '+'
                while count_summand != 0:
                    sign = signs[::-1][count_summand - 1]
                    self.expression += (' ' + sign + ' ' + self.generation_numbers(count_summand, sign, self.expression, number_system))
                    count_summand -= 1
                self.label.setText('Сколько {} в записи данного выражения в {}-ой системе:\n{}?'.format(number_system - 1, number_system, self.expression))
                self.right_answer = str(self.count_number_in(self.convert_to(eval(self.expression), number_system), str(number_system - 1)))
                self.generation_changes()
            elif self.asktype == 5:
                number_system = randint(3, 9)
                power_now = randint(10, 100)
                self.expression = 'N**{}'.format(power_now)
                expression_back = number_system ** power_now
                signs = [choice(['+', '-'])]
                if signs[0] == '+':
                    signs.append('-')
                else:
                    signs.append(choice(['+', '-']))
                if signs[0] == '-':
                    if power_now == 10:
                        power_next = 9
                    else:
                        power_next = randint(9, power_now - 1)
                    if expression_back // number_system ** power_next < 100:
                        multiprocessing = randint(2, (expression_back // number_system ** power_next) - 1)
                        expression_back = eval('{}{}{}'.format(expression_back,
                                                               signs[0], randint(2, multiprocessing * number_system ** power_next)))
                        self.expression += ' {} {} * N**{}'.format(signs[0], multiprocessing, power_next)
                    else:
                        multiprocessing = randint(2, 100)
                        expression_back = eval('{}{}{}'.format(expression_back,
                                                               signs[0], multiprocessing * number_system ** power_next))
                        self.expression += ' {} {} * N**{}'.format(signs[0], multiprocessing, power_next)
                else:
                    power_next = randint(10, 100)
                    multiprocessing = randint(2, 100)
                    expression_back = eval('{}{}{}'.format(expression_back,
                                                               signs[0], multiprocessing * number_system ** power_next))
                    self.expression += ' {} {} * N**{}'.format(signs[0], multiprocessing, power_next)
                summand = randint(50, 1000)
                self.expression += ' {} {}'.format(signs[1], summand)
                expression_back = eval('{}{}{}'.format(expression_back, signs[1], summand))
                self.label.setText('Значение данного арифметического выражения записали в системе счисления с основанием N:\n' +
                                   self.expression + '\nОпределите основание системы счисления, если известно, что сумма разрядов в числе, \n' +
                                   'представленном в этой системе счисления, равна ' + str(self.sum_numbers_in(self.convert_to(expression_back, number_system))))
                self.right_answer = str(number_system)
                self.generation_changes()
        else:
            # Восстановление изначального вида окна генерации
            if self.check_answer(self.lineEdit.text().strip(), self.right_answer):
                self.isgenerated = 0
                self.pushButton.setText('Сгенерировать')
                self.lineEdit.hide()
                self.label.setText('Сгенерируйте задание случайно\n или введите ключ генерации')
                self.lineEdit.clear()
                self.setWindowTitle('Генератор задания')

    # Генерация подходящих чисел
    def generation_numbers(self, count_summand, sign=False, expression=False, number_system=2):
        if count_summand == 1:
            if eval(expression) <= 2000 and sign == '-':
                return str(randint(1, eval(expression) - 1))
            else:
                return str(randint(1, 2000))
        else:
            front_power = randint(1, 3)
            if expression:
                if log(eval(expression), number_system) // front_power <= 1:
                    front_power = 1
            if sign == '-' and log(eval(expression), number_system) // front_power <= 2000:
                return '{}**{}'.format(str(number_system ** front_power),
                                       str(randint(1, int(log(eval(expression), number_system)) // front_power) - 1))
            else:
                return '{}**{}'.format(str(number_system**front_power), str(randint(2, 2000 // front_power)))

    # Перевод чисел между системами
    def convert_to(self, number, base):
        digits = '0123456789abcdefghijklmnopqrstuvwxyz'
        result = ''
        if number < 0:
            number *= -1
        while number > 0:
            result = digits[number % base] + result
            number //= base
        return result

    # Сумма цифр числа
    def sum_numbers_in(self, expression):
        sm = 0
        for i in expression:
            sm += int(i)
        return sm

    # Частота цифры в числе
    def count_number_in(self, expression, number):
        count = 0
        for i in expression:
            if i == number:
                count += 1
        return count

    # Проверка правильности ответа
    def check_answer(self, user_answer, right_answer):
        if user_answer != right_answer:
            self.label.setText(self.label.text() + '\nНеверный ответ')
            return 0
        else:
            return 1

    # Отслежка касания мыши
    def mousePressEvent(self, event):
        # Исключение лишних случаев
        if (event.x() > 20 or event.y() > 20) and not self.lineEdit.isVisible():
            return None
        # Сделать видимой строку ввода
        if not self.lineEdit.isVisible() and self.asktype != 5:
            self.lineEdit.setPlaceholderText(self.placeholder)
            self.lineEdit.show()
            self.lineEdit.setFocus()
        # Очистить и скрыть её
        elif self.lineEdit.isVisible() and not self.isgenerated:
            self.lineEdit.clear()
            self.lineEdit.hide()
        # Просто очистить
        elif self.lineEdit.isVisible() and self.isgenerated:
            self.lineEdit.clear()

    def keyPressEvent(self, event):
        self.refresh()
        if event.key() == 16777220:
            self.pushButton.click()
        elif event.key() == 16777216:
            if not self.isgenerated:
                self.close()
            # Возврат к генерации, если нажат esc, а пример уже сгенерирован
            else:
                self.isgenerated = 0
                self.pushButton.setText('Сгенерировать')
                self.lineEdit.hide()
                self.label.setText('Сгенерируйте задание случайно\n или введите ключ генерации')
                self.lineEdit.clear()
                self.setWindowTitle('Генератор задания')
        # Автоматическая фокусировка
        elif event.text() and self.isgenerated and self.asktype != 5:
            self.lineEdit.show()
            self.lineEdit.setPlaceholderText(self.placeholder)
            self.lineEdit.setFocus()
            self.lineEdit.setText(event.text())

    def closeEvent(self, event):
        # Открытие главного окна при закрытии генератора
        self.main_window = Main()
        self.main_window.show()
        event.accept()

    def refresh(self):
        # Декоративная обрезка надписи "Неверный ответ" при редактировании ввода
        text = self.lineEdit.text().lower().replace(' ', '')
        if not self.isgenerated:
            return None
        if text != 'ответ' and text != 'answer':
            if self.label.text().split('\n')[-1] == 'Неверный ответ':
                self.label.setText('\n'.join(self.label.text().split('\n')[0:-1]))
        # Получение правильного ответа
        else:
            self.lineEdit.setText(self.right_answer)

    # Установка стандартного вида сразу после генерации
    def generation_changes(self):
        self.isgenerated = 1
        self.lineEdit.clear()
        self.setWindowTitle('Задание')
        self.lineEdit.setFocus()
        self.pushButton.setText('Отправить')
        self.lineEdit.show()
        self.lineEdit.setPlaceholderText('Решение')

# Привязка и запуск главного окна
app = QApplication(sys.argv)
ex = Main()
ex.show()
app.exec()
