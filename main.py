import sqlite3
conn = sqlite3.connect('tasks.db')

def create_task(conn, title, description, category_id):
    """
    Создает новую задачу в базе данных.
    """
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO tasks (title, description, category_id)
    VALUES (?, ?, ?)
    """, (title, description, category_id))
    conn.commit()



def get_task(conn):
    'Выводим все задачи'
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM tasks
    ''')
    tasks  = cursor.fetchall()
    
    for task in tasks:
        print(*task, sep=': ')
    
def get_completed(conn):
    'Выводим выполненые задачи'
    cursor = conn.cursor()
    cursor.execute('''
    SELECT * FROM tasks 
    WHERE completed = 1 ''',)

    tasks = cursor.fetchall()

    for task in tasks:
        print(*task, sep=': ')


def get_sorted_task(conn, us_choice):
    'Выводим задачи в отсортированном порядке'
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT * FROM tasks 
    ORDER BY {us_choice} ASC
    ''')

    tasks = cursor.fetchall()

    for task in tasks:
        print(*task, sep=': ')


def update_task(conn, task_id,  title, description, category_id, completed):
    'Обновляем информацию о выполнении задачи'

    cursor = conn.cursor()
    cursor.execute("""UPDATE tasks SET title = ?, description = ?, category_id = ?, completed = ?, updated_at = CURRENT_TIMESTAMP
    WHERE id = ? """, (title, description, category_id, completed, task_id))

    conn.commit()


def completed(conn, task_id):
    'Меняем информацию о выполнении задачи'

    cursor = conn.cursor()
    cursor.execute('''UPDATE tasks SET completed = 1, updated_at = CURRENT_TIMESTAMP
    WHERE id = ?''', (task_id,))

    conn.commit()



def delete_task(conn, task_id):
    'Удаляем задачу'

    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM tasks WHERE id = ?
    """, (task_id,))

    conn.commit()
    tasks = cursor.fetchall()

    return tasks


def delete_from_category(conn, category_id):
    'Удаляем задачи по категориям'

    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM tasks 
    WHERE category_id = ?
    ''', (category_id,))

    conn.commit()


def select_from_category(conn, category_id):
    'Выбираем по категории'

    cursor = conn.cursor()
    cursor.execute(''' 
    SELECT * FROM tasks 
    WHERE category_id = ? 
    ''',(category_id,))
    
    conn.commit()
    tasks = cursor.fetchall()

    for task in tasks:
        print(*task, sep=': ')

    
def choice(conn):

    user_choice = input('''
    Какие действия вы хотите произвести с задачами? 
    (Добавить, Изменить, Удалить, Показать) / (выход)
    Ответ: ''').lower()

    while user_choice != 'выход':

        if user_choice == 'добавить':
            print()
            create_task(conn,
                        title=input('Ввидите тему задачи: '),
                        description=input('Ввидите описание задачи: '),
                        category_id=int(input('''
            Ввидите уровень важности у задачи: 
            1) 1 = срочно
            2) 2 = чуть позже 
            3) 3 = оставить на потом)
            Ответ: ''')))

            print('Задача добавлена')

        elif user_choice == 'изменить':
            change_choice = input('\nВы хотите изменить информацию о задачи или отметить ее как выполненую ? (и/в): ').lower()
            if change_choice == 'и':
                update_task(conn,
                task_id=int(input('Ввидите ID задачи: ')),
                title=input('Ввидите новую тему задачи: '),
                description=input('Ввидите новое описание задачи: '),
                category_id=int(input('''
            Ввидите уровень важности у задачи: 
            1) 1 = срочно
            2) 2 = чуть позже 
            3) 3 = оставить на потом)
            Ответ: ''')),
                completed= 0)       
                print('Задача изменена ')
            
            elif change_choice == 'в':
                completed(conn, task_id=int(input('Ввидите ID задачи: ')))
                print('\nЗадача изменена')

        elif user_choice == 'удалить':
            
            print('\nВы можете удалить либо по ID, либо все задачи из какой-либо категории важности', )

            us_ch = int(input('''
            Выберите:
            1) 1 = по ID задачи
            2) 2 = по категории важности
            Ответ: '''))

            if us_ch == 1:
                delete_task(conn, task_id=int(input('Для удаления ввидите номер столца: ')))
                print('Задача удалена')
            
            elif us_ch == 2:
                delete_from_category(conn, category_id=int(input('''
            Задачи какой категории вы хотите удалить ?
            1) 1 = срочные
            2) 2 = чуть позже 
            3) 3 = оставили на потом)
            Ответ: ''')))
                
            print('Задачи данной категории удалены')

        elif user_choice == 'показать':
            us_ch = input('\nВы хотите увидеть полный список / отсортированный ?: (п/с): ').lower()
            
            if us_ch == 'п':
                print('\nВот полный список ваших дел: ')
                get_task(conn)
                   
            elif us_ch == 'с':

                us_ch_print = int(input('''
                Вы хотите вывести весь список в отсортировонном порядке по:
                1) 1 = по номеру столбца
                2) 2 = по залоголовку
                3) 3 = по описанию задачи
                4) 4 = уровню важности
                5) 5 = по уровню выполнения
                6) 6 = по дате
                7) 7 = по последнему изменению
                8) 8 = вывести только выполненые задачи
                Ответ: '''))

                if us_ch_print == 1:
                    print('Вот полный список ваших дел: ')
                    get_task(conn)

                elif us_ch_print == 2:
                    print('Вот отсортированный по залоговку список ваших дел')
                    get_sorted_task(conn, us_choice='title')

                elif us_ch_print == 3:
                    print('Вот отсортированный по описанию список ваших дел')
                    get_sorted_task(conn, us_choice='description')

                elif us_ch_print == 4:
                    print('Вот отсортированный список ваших дел важности') 
                    get_sorted_task(conn, us_choice='category_id')
                
                elif us_ch_print == 5:
                    print('Вот отсортированный список ваших дел по уровню выполнения') 
                    get_sorted_task(conn, us_choice='completed')
                
                elif us_ch_print == 6:
                    print('Вот отсортированный список ваших дел по дате') 
                    get_sorted_task(conn, us_choice='created_at')
                
                elif us_ch_print == 7:
                    print('Вот отсортированный список ваших дел по последнему изменению') 
                    get_sorted_task(conn, us_choice='updated_at')
                
                elif us_ch_print == 8:
                    print('\n Вот все выполненые задачи:')
                    get_completed(conn)

                else:
                    print('Такого выбора не было, попробуте снова')

        else:
            print('''
            К сожалению, такого действия нет, попробуйте снова
            ''')

        user_choice = input('''
    Какие действия вы хотите произвести с задачами? 
    (Добавить, Изменить, Удалить, Показать)
    Ответ: ''').lower()



choice(conn)
print('Работа выполнена')

conn.close()




