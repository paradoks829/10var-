'''
Создать файл записей, в котором хранится информация о дисциплинах, читаемых на
факультете: название, с какого семестра читается, продолжительность курса (в семестрах),
общее количество часов, вид отчётности (зачёт, экзамен), читающая курс кафедра
Разработать и реализовать программу "Учебный план", которая считывает исходную
информацию и позволяет на основе неё создавать следующие отчёты:
1 Полный список всех дисциплин, который будет отсортирован следующему ключу: с
какого семестра читается (по возрастанию) + читающая кафедра (по возрастанию) +
общее количество часов (по убыванию).
2 Список всех дисциплин с заданным видом отчётности, отсортированный по
следующему ключу: продолжительность курса (по возрастанию) + общее
количество часов (по убыванию).
3 Список всех дисциплин с общим количеством часов от N1 до N2, отсортированный
по следующему ключу: читающая кафедра (по возрастанию) + общее количество
часов 9по убыванию).
Создать базу дисциплин, включающую не менее 25 записей и на основе неё сформировать
все указанные списки. База должна содержать такие записи, чтобы во всех списках явно
прослеживался заданный вид сортировки по всем ключам. Для сортировки записей
использовать сортировку бинарными вставками.
'''

from sort import binary_insertion_sort

def load_database():
    """Загрузка базы данных из файла"""
    disciplines = []
    try:
        with open('database.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(';')
                    if len(parts) == 7:
                        discipline = {
                            'id': int(parts[0]),
                            'name': parts[1],
                            'department': parts[2],
                            'start_semester': int(parts[3]),
                            'duration': int(parts[4]),
                            'total_hours': int(parts[5]),
                            'assessment': parts[6]
                        }
                        disciplines.append(discipline)
        print(f"Загружено {len(disciplines)} записей")
    except FileNotFoundError:
        print("Файл database.txt не найден")
    return disciplines

def save_database(disciplines):
    """Сохранение базы данных в файл"""
    try:
        with open('database.txt', 'w', encoding='utf-8') as file:
            for disc in disciplines:
                line = f"{disc['id']};{disc['name']};{disc['department']};"
                line += f"{disc['start_semester']};{disc['duration']};"
                line += f"{disc['total_hours']};{disc['assessment']}\n"
                file.write(line)
    except:
        print("Ошибка сохранения")

def display_disciplines(disciplines, title=""):
    """Отображение списка дисциплин"""
    if title:
        print(f"\n{title}")
    print("=" * 90)
    print(f"{'ID':<4} {'Название':<25} {'Кафедра':<20} {'Сем':<4} {'Длит':<5} {'Часы':<6} {'Отчёт':<8}")
    print("-" * 90)
    
    for disc in disciplines:
        print(f"{disc['id']:<4} {disc['name']:<25} {disc['department']:<20} "
              f"{disc['start_semester']:<4} {disc['duration']:<5} "
              f"{disc['total_hours']:<6} {disc['assessment']:<8}")
    print("=" * 90)
    print(f"Всего дисциплин: {len(disciplines)}")

def add_discipline(disciplines):
    """Добавление новой дисциплины"""
    print("\n=== Добавление новой дисциплины ===")
    
    # Находим максимальный ID
    max_id = 0
    for disc in disciplines:
        if disc['id'] > max_id:
            max_id = disc['id']
    
    new_id = max_id + 1
    
    name = input("Название: ").strip()
    while not name:
        print("Название не может быть пустым")
        name = input("Название: ").strip()
    
    department = input("Кафедра: ").strip()
    while not department:
        print("Кафедра не может быть пустой")
        department = input("Кафедра: ").strip()
    
    # Ввод числовых значений
    start_semester = 0
    while start_semester < 1 or start_semester > 8:
        try:
            start_semester = int(input("Начальный семестр (1-8): "))
        except:
            print("Введите число от 1 до 8")
    
    duration = 0
    while duration < 1 or duration > 8:
        try:
            duration = int(input("Длительность (1-8): "))
        except:
            print("Введите число от 1 до 8")
    
    total_hours = 0
    while total_hours <= 0:
        try:
            total_hours = int(input("Количество часов: "))
        except:
            print("Введите положительное число")
    
    assessment = ""
    while assessment not in ["зачёт", "экзамен"]:
        assessment = input("Отчётность (зачёт/экзамен): ").strip().lower()
    
    # Создаем новую дисциплину
    new_discipline = {
        'id': new_id,
        'name': name,
        'department': department,
        'start_semester': start_semester,
        'duration': duration,
        'total_hours': total_hours,
        'assessment': assessment
    }
    
    disciplines.append(new_discipline)
    save_database(disciplines)
    print(f"Дисциплина добавлена с ID {new_id}")
    
    return disciplines

def delete_discipline(disciplines):
    """Удаление дисциплины"""
    print("\n=== Удаление дисциплины ===")
    display_disciplines(disciplines, "Текущий список:")
    
    try:
        disc_id = int(input("\nВведите ID для удаления: "))
        
        # Ищем дисциплину
        found = False
        for i in range(len(disciplines)):
            if disciplines[i]['id'] == disc_id:
                name = disciplines[i]['name']
                del disciplines[i]
                save_database(disciplines)
                print(f"Дисциплина '{name}' удалена")
                found = True
                break
        
        if not found:
            print(f"Дисциплина с ID {disc_id} не найдена")
    except:
        print("Ошибка ввода")
    
    return disciplines

def edit_discipline(disciplines):
    """Редактирование дисциплины"""
    print("\n=== Редактирование дисциплины ===")
    display_disciplines(disciplines, "Текущий список:")
    
    try:
        disc_id = int(input("\nВведите ID для редактирования: "))
        
        # Ищем дисциплину
        for disc in disciplines:
            if disc['id'] == disc_id:
                print(f"\nРедактирование: {disc['name']}")
                print("1. Название")
                print("2. Кафедра")
                print("3. Начало семестра")
                print("4. Длительность")
                print("5. Количество часов")
                print("6. Отчётность")
                
                choice = input("Что изменить? (1-6): ").strip()
                
                if choice == '1':
                    name = input("Новое название: ").strip()
                    if name:
                        disc['name'] = name
                
                elif choice == '2':
                    department = input("Новая кафедра: ").strip()
                    if department:
                        disc['department'] = department
                
                elif choice == '3':
                    try:
                        start = int(input("Новый семестр (1-8): "))
                        if 1 <= start <= 8:
                            disc['start_semester'] = start
                    except:
                        print("Ошибка ввода")
                
                elif choice == '4':
                    try:
                        duration = int(input("Новая длительность (1-8): "))
                        if 1 <= duration <= 8:
                            disc['duration'] = duration
                    except:
                        print("Ошибка ввода")
                
                elif choice == '5':
                    try:
                        hours = int(input("Новое количество часов: "))
                        if hours > 0:
                            disc['total_hours'] = hours
                    except:
                        print("Ошибка ввода")
                
                elif choice == '6':
                    assessment = input("Новая отчётность (зачёт/экзамен): ").strip().lower()
                    if assessment in ["зачёт", "экзамен"]:
                        disc['assessment'] = assessment
                
                save_database(disciplines)
                print("Изменения сохранены")
                break
        else:
            print(f"Дисциплина с ID {disc_id} не найдена")
    except:
        print("Ошибка ввода")
    
    return disciplines

def report_1(disciplines):
    """Отчёт 1: Полный список"""
    print("\n=== ОТЧЁТ №1 ===")
    print("Сортировка: семестр(по возрастанию) + кафедра(по возрастанию) + часы(по убыванию)")
    
    sorted_data = binary_insertion_sort(disciplines, 1)
    display_disciplines(sorted_data, "Результат:")

def report_2(disciplines):
    """Отчёт 2: По виду отчётности"""
    print("\n=== ОТЧЁТ №2 ===")
    print("Сортировка: длительность(по возрастанию) + часы(по убыванию)")
    
    assessment = ""
    while assessment not in ["зачёт", "экзамен"]:
        assessment = input("Введите вид отчётности (зачёт/экзамен): ").strip().lower()
    
    # Фильтруем по отчётности
    filtered = []
    for disc in disciplines:
        if disc['assessment'] == assessment:
            filtered.append(disc)
    
    sorted_data = binary_insertion_sort(filtered, 2)
    display_disciplines(sorted_data, f"Дисциплины с отчётностью '{assessment}':")

def report_3(disciplines):
    """Отчёт 3: По количеству часов"""
    print("\n=== ОТЧЁТ №3 ===")
    print("Сортировка: кафедра(по возрастанию) + часы(по убыванию)")
    
    n1 = 0
    n2 = 0
    
    while n1 <= 0:
        try:
            n1 = int(input("Минимальное количество часов (N1): "))
        except:
            print("Введите число")
    
    while n2 < n1:
        try:
            n2 = int(input("Максимальное количество часов (N2): "))
        except:
            print("Введите число")
    
    # Фильтруем по часам
    filtered = []
    for disc in disciplines:
        if n1 <= disc['total_hours'] <= n2:
            filtered.append(disc)
    
    sorted_data = binary_insertion_sort(filtered, 3)
    display_disciplines(sorted_data, f"Дисциплины с часами от {n1} до {n2}:")

def main():
    """Главная функция"""
    print("=" * 60)
    print("ПРОГРАММА 'УЧЕБНЫЙ ПЛАН'")
    print("=" * 60)
    
    # Загрузка данных
    disciplines = load_database()
    
    while True:
        print("\n" + "=" * 40)
        print("ГЛАВНОЕ МЕНЮ")
        print("=" * 40)
        print("1. Показать все дисциплины")
        print("2. Добавить дисциплину")
        print("3. Удалить дисциплину")
        print("4. Редактировать дисциплину")
        print("5. Отчёт 1 (семестр(по возрастанию) кафедра(по возрастанию) часы(по убыванию))")
        print("6. Отчёт 2 (по отчётности)")
        print("7. Отчёт 3 (по часам)")
        print("0. Выход")
        print("-" * 40)
        
        choice = input("Выберите действие: ").strip()
        
        if choice == '0':
            print("Выход из программы")
            break
        
        elif choice == '1':
            display_disciplines(disciplines, "Все дисциплины:")
        
        elif choice == '2':
            disciplines = add_discipline(disciplines)
        
        elif choice == '3':
            disciplines = delete_discipline(disciplines)
        
        elif choice == '4':
            disciplines = edit_discipline(disciplines)
        
        elif choice == '5':
            report_1(disciplines)
        
        elif choice == '6':
            report_2(disciplines)
        
        elif choice == '7':
            report_3(disciplines)
        
        else:
            print("Неверный выбор")
        

if __name__ == "__main__":
    main()