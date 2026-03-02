import pymysql as db
import string
from random import choice

def get_db_connection():
    return db.connect(
        host='localhost',
        user='root',
        port=3306,
        password='zhbr3407',
        charset='utf8mb4',
        db='coursework',
        cursorclass=db.cursors.DictCursor
    )

def object_exists(connection, table, column, value):

    with connection.cursor() as cursor:
        sql = f"SELECT 1 FROM `{table}` WHERE `{column}` = %s LIMIT 1"
        cursor.execute(sql, (value,))
        return cursor.fetchone() is not None

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Роли` ("
        "`id_роли` INT NOT NULL, "
        "`Название` VARCHAR(45) NOT NULL, "
        "PRIMARY KEY (`id_роли`))"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Пользователи` ("
        "`UserId` VARCHAR(50) NOT NULL, "
        "`Логин` VARCHAR(50) NOT NULL, "
        "`id_роли` INT NOT NULL, "
        "`Пароль` VARCHAR(255) NOT NULL, "
        "`Заблокированный` BOOLEAN NOT NULL DEFAULT FALSE,"
        "PRIMARY KEY (`UserId`), "
        "INDEX `idx_роль` (`id_роли` ASC), "
        "CONSTRAINT `fk_пользователи_роли` "
        "FOREIGN KEY (`id_роли`) REFERENCES `Роли` (`id_роли`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Типы_контактов` ("
        "`id_типа_контакта` INT NOT NULL, "
        "`Название` VARCHAR(45) NOT NULL, "
        "PRIMARY KEY (`id_типа_контакта`))"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Студенты` ("
        "`UserId` VARCHAR(50) NOT NULL, "
        "`Фамилия` VARCHAR(45) NOT NULL, "
        "`Имя` VARCHAR(45) NOT NULL, "
        "`Отчество` VARCHAR(45), "
        "`Страна` VARCHAR(45) NOT NULL, "
        "`Возраст` INT NOT NULL, "
        "`Фото` LONGBLOB, "
        "PRIMARY KEY (`UserId`), "
        "CONSTRAINT `fk_студенты_пользователи` "
        "FOREIGN KEY (`UserId`) REFERENCES `Пользователи` (`UserId`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Преподаватели` ("
        "`UserId` VARCHAR(50) NOT NULL, "
        "`Фамилия` VARCHAR(45) NOT NULL, "
        "`Имя` VARCHAR(45) NOT NULL, "
        "`Отчество` VARCHAR(45), "
        "`Страна` VARCHAR(45) NOT NULL, "
        "`Образование` LONGBLOB, "
        "`Описание` VARCHAR(1000) NOT NULL, "
        "`Фото` LONGBLOB, "
        "PRIMARY KEY (`UserId`), "
        "CONSTRAINT `fk_преподаватели_пользователи` "
        "FOREIGN KEY (`UserId`) REFERENCES `Пользователи` (`UserId`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Администраторы` ("
        "`UserId` VARCHAR(50) NOT NULL, "
        "PRIMARY KEY (`UserId`), "
        "CONSTRAINT `fk_администраторы_пользователи` "
        "FOREIGN KEY (`UserId`) REFERENCES `Пользователи` (`UserId`))"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Контакты_студентов` ("
        "`id_записи` INT NOT NULL AUTO_INCREMENT, "
        "`id_типа_контакта` INT NOT NULL, "
        "`UserId` VARCHAR(50) NOT NULL, "
        "`Значение` VARCHAR(45) NOT NULL, "
        "PRIMARY KEY (`id_записи`), "
        "CONSTRAINT `fk_контакты_студентов` "
        "FOREIGN KEY (`UserId`) REFERENCES `Студенты` (`UserId`) "
        "ON DELETE CASCADE ON UPDATE CASCADE, "
        "CONSTRAINT `fk_типы_контактов_студенты` "
        "FOREIGN KEY (`id_типа_контакта`) REFERENCES `Типы_контактов` (`id_типа_контакта`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Контакты_преподавателей` ("
        "`id_записи` INT NOT NULL AUTO_INCREMENT, "
        "`id_типа_контакта` INT NOT NULL, "
        "`UserId` VARCHAR(50) NOT NULL, "
        "`Значение` VARCHAR(45) NOT NULL, "
        "PRIMARY KEY (`id_записи`), "
        "CONSTRAINT `fk_контакты_преподавателей` "
        "FOREIGN KEY (`UserId`) REFERENCES `Преподаватели` (`UserId`) "
        "ON DELETE CASCADE ON UPDATE CASCADE, "
        "CONSTRAINT `fk_типы_контактов_преподаватели` "
        "FOREIGN KEY (`id_типа_контакта`) REFERENCES `Типы_контактов` (`id_типа_контакта`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Языки` ("
        "`id_языка` INT NOT NULL, "
        "`Название` VARCHAR(45) NOT NULL UNIQUE, "
        "PRIMARY KEY (`id_языка`))"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Курсы` ("
        "`id_курса` INT NOT NULL, "
        "`Название` VARCHAR(200) NOT NULL, "
        "`id_языка` INT NOT NULL, "
        "`Описание` VARCHAR(2000) NOT NULL, "
        "`UserId` VARCHAR(50) NOT NULL, "
        "PRIMARY KEY (`id_курса`), "
        "INDEX `idx_язык` (`id_языка` ASC), "
        "CONSTRAINT `fk_курсы_языки` "
        "FOREIGN KEY (`id_языка`) REFERENCES `Языки` (`id_языка`) "
        "ON DELETE CASCADE ON UPDATE CASCADE, "
        "CONSTRAINT `fk_курсы_создатель` "
        "FOREIGN KEY (`UserId`) REFERENCES `Преподаватели` (`UserId`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Уровни` ("
        "`id_уровня` INT NOT NULL, "
        "`Название` VARCHAR(45) NOT NULL, "
        "`id_языка` INT NOT NULL, "
        "`Описание` VARCHAR(200) NOT NULL, "
        "PRIMARY KEY (`id_уровня`), "
        "INDEX `idx_язык` (`id_языка` ASC), "
        "CONSTRAINT `fk_уровни_языки` "
        "FOREIGN KEY (`id_языка`) REFERENCES `Языки` (`id_языка`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Занятия` ("
        "`id_занятия` INT NOT NULL, "
        "`id_курса` INT NOT NULL, "
        "`Описание` VARCHAR(1000) NOT NULL, "
        "`id_преподавателя` VARCHAR(50) NOT NULL, "
        "`Дата` DATE NOT NULL, "
        "`Время_начала` TIME NOT NULL, "
        "`Время_окончания` TIME NOT NULL, "
        "PRIMARY KEY (`id_занятия`), "
        "INDEX `idx_курс` (`id_курса` ASC), "
        "INDEX `idx_преподаватель` (`id_преподавателя` ASC), "
        "CONSTRAINT `fk_занятия_курсы` "
        "FOREIGN KEY (`id_курса`) REFERENCES `Курсы` (`id_курса`) "
        "ON DELETE CASCADE ON UPDATE CASCADE, "
        "CONSTRAINT `fk_занятия_преподаватели` "
        "FOREIGN KEY (`id_преподавателя`) REFERENCES `Преподаватели` (`UserId`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Языки_преподавателей` ("
        "`id_записи` INT NOT NULL AUTO_INCREMENT, "
        "`id_языка` INT NOT NULL, "
        "`UserId` VARCHAR(50) NOT NULL, "
        "`id_уровня` INT NOT NULL, "
        "PRIMARY KEY (`id_записи`), "
        "INDEX `idx_преподаватель` (`UserId` ASC), "
        "INDEX `idx_уровень` (`id_уровня` ASC), "
        "CONSTRAINT `fk_языки_преподавателей_языки` "
        "FOREIGN KEY (`id_языка`) REFERENCES `Языки` (`id_языка`) "
        "ON DELETE CASCADE ON UPDATE CASCADE, "
        "CONSTRAINT `fk_языки_преподавателей_преподаватели` "
        "FOREIGN KEY (`UserId`) REFERENCES `Преподаватели` (`UserId`) "
        "ON DELETE CASCADE ON UPDATE CASCADE, "
        "CONSTRAINT `fk_языки_преподавателей_уровни` "
        "FOREIGN KEY (`id_уровня`) REFERENCES `Уровни` (`id_уровня`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Студенты_на_занятиях` ("
        "`id_записи` INT NOT NULL AUTO_INCREMENT, "
        "`id_занятия` INT NOT NULL, "
        "`UserId` VARCHAR(50) NOT NULL, "
        "PRIMARY KEY (`id_записи`), " 
        "INDEX `idx_студент` (`UserId` ASC), "
        "CONSTRAINT `fk_студенты_занятия` "
        "FOREIGN KEY (`UserId`) REFERENCES `Студенты` (`UserId`) "
        "ON DELETE CASCADE ON UPDATE CASCADE, "
        "CONSTRAINT `fk_занятия_студенты` "
        "FOREIGN KEY (`id_занятия`) REFERENCES `Занятия` (`id_занятия`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Преподаватели_на_курсах` ("
        "`id_записи` INT NOT NULL AUTO_INCREMENT, "
        "`id_курса` INT NOT NULL, "
        "`UserId` VARCHAR(50) NOT NULL, "
        "PRIMARY KEY (`id_записи`), "
        "INDEX `idx_преподаватель` (`UserId` ASC), "
        "CONSTRAINT `fk_курсы_преподаватели` "
        "FOREIGN KEY (`UserId`) REFERENCES `Преподаватели` (`UserId`) "
        "ON DELETE CASCADE ON UPDATE CASCADE, "
        "CONSTRAINT `fk_преподаватели_курсы` "
        "FOREIGN KEY (`id_курса`) REFERENCES `Курсы` (`id_курса`) "
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Студенты_На_Курсах` ("
        "`id_записи` INT NOT NULL AUTO_INCREMENT, "
        "`id_курса` INT NOT NULL,"
        "`UserId` VARCHAR(50) NOT NULL,"
        "PRIMARY KEY (`id_записи`),"
        "INDEX `idx_студент` (`UserId` ASC),"
        "CONSTRAINT `fk_курсы_студенты`"
        "FOREIGN KEY (`UserId`) REFERENCES `Студенты` (`UserId`)"
        "ON DELETE CASCADE ON UPDATE CASCADE,"
        "CONSTRAINT `fk_студенты_курсы`"
        "FOREIGN KEY (`id_курса`) REFERENCES `Курсы` (`id_курса`)"
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Оценки` ("
        "`Номер_записи` INT NOT NULL,"
        "`UserId` VARCHAR(50) NOT NULL,"
        "`id_курса` INT NOT NULL,"
        "`Оценка` INT NOT NULL,"
        "`Максимальный_балл` INT NOT NULL,"
        "`Дата` DATE NOT NULL,"
        "`Описание` VARCHAR(200) NOT NULL,"
        "PRIMARY KEY (`Номер_записи`),"
        "CONSTRAINT `fk_оценки_студенты`"
        "FOREIGN KEY (`UserId`) REFERENCES `Студенты` (`UserId`)"
        "ON DELETE CASCADE ON UPDATE CASCADE,"
        "CONSTRAINT `fk_оценки_курсы`"
        "FOREIGN KEY (`id_курса`) REFERENCES `Курсы` (`id_курса`)"
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Уведомления` ("
        "`Номер_записи` INT NOT NULL,"
        "`UserId` VARCHAR(50) NOT NULL,"
        "`Дата` DATE NOT NULL,"
        "`Тема` VARCHAR(20) NOT NULL,"
        "`Содержание` VARCHAR(200) NOT NULL,"
        "`Прочитано` BOOLEAN NOT NULL DEFAULT FALSE,"
        "PRIMARY KEY (`Номер_записи`),"
        "CONSTRAINT `fk_уведомление_пользователи`"
        "FOREIGN KEY (`UserId`) REFERENCES `Пользователи` (`UserId`)"
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `Заявки` ("
        "`Номер_заявки` INT NOT NULL,"
        "`UserId` VARCHAR(50) NOT NULL,"
        "`id_курса` INT NOT NULL, "
        "`Содержание` VARCHAR(200) NOT NULL,"
        "PRIMARY KEY (`Номер_заявки`),"
        "CONSTRAINT `fk_заявка_студент`"
        "FOREIGN KEY (`UserId`) REFERENCES `Студенты` (`UserId`)"
        "ON DELETE CASCADE ON UPDATE CASCADE,"
        "CONSTRAINT `fk_заявка_курс`"
        "FOREIGN KEY (`id_курса`) REFERENCES `Курсы` (`id_курса`)"
        "ON DELETE CASCADE ON UPDATE CASCADE)"
    )

    if not object_exists(conn, 'Роли', 'Название', 'Администратор'):
        Role = (1, 'Администратор')
        cursor.execute("""INSERT INTO Роли (id_роли, Название)
                          VALUES (%s, %s)""", Role)
    if not object_exists(conn, 'Роли', 'Название', 'Преподаватель'):
        Role = (2, 'Преподаватель')
        cursor.execute("""INSERT INTO Роли (id_роли, Название)
                          VALUES (%s, %s)""", Role)
    if not object_exists(conn, 'Роли', 'Название', 'Студент'):
        Role = (3, 'Студент')
        cursor.execute("""INSERT INTO Роли (id_роли, Название)
                          VALUES (%s, %s)""", Role)

    if not object_exists(conn, 'Пользователи', 'Логин', 'Main_admin'):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(choice(characters) for i in range(10))
        userId = ''.join(choice(characters) for i in range(6))
        Admin = (userId, 'Main_admin', 1, password)
        cursor.execute("""INSERT INTO Пользователи (UserId, Логин, id_роли, Пароль)
                          VALUES (%s, %s, %s, %s)""", Admin)
        cursor.execute("""INSERT INTO Администраторы (UserId) VALUES (%s)""", (userId, ))
        f = open('password.txt', 'w')
        f.write(password)
        f.close()

    conn.commit()

    cursor.close()
    conn.close()

init_db()