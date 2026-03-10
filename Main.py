from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QWidget
import traceback

from connection import *
from applogic import *
import string

class Program_Ui:
    # ==============================
    # Exception handling
    # ==============================
    def check_registration(self):
        try:
            self.textEdit_login_reg.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.comboBox_roles.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.textEdit_password_reg.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.textEdit_surname.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.textEdit_name.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.comboBox_country.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.textEdit_age.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            self.addFile_education.setStyleSheet("QPushButton {background-color: #cccccc; border: none; color: #808080}")
            self.textEdit_description.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
            check = False
            if self.textEdit_login_reg.text() == '':
                check = True
                self.textEdit_login_reg.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid red; border-radius: 8px;")

            if self.comboBox_roles.currentIndex() == 0:
                check = True
                self.comboBox_roles.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid red; border-radius: 8px;")

            if self.textEdit_password_reg.text() == '':
                check = True
                self.textEdit_password_reg.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid red; border-radius: 8px;")

            if self.textEdit_surname.text() == '':
                check = True
                self.textEdit_surname.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid red; border-radius: 8px;")

            if self.textEdit_name.text() == '':
                check = True
                self.textEdit_name.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid red; border-radius: 8px;")

            if self.comboBox_country.currentIndex() == 0:
                check = True
                self.comboBox_country.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid red; border-radius: 8px;")

            if self.textEdit_age.text() == '' and self.comboBox_roles.currentIndex() == 1:
                check = True
                self.textEdit_age.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid red; border-radius: 8px;")

            if self.textEdit_education.text() == '' and self.comboBox_roles.currentIndex() == 2:
                check = True
                self.addFile_education.setStyleSheet("QPushButton {background-color: #cccccc; border: 2px solid red; border-radius: 8px; color: #808080}")

            if self.textEdit_description.toPlainText() == '' and self.comboBox_roles.currentIndex() == 2:
                check = True
                self.textEdit_description.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0); border: 2px solid red; border-radius: 8px;")

            if check:
                QtWidgets.QMessageBox.critical(None, "Ошибка", f"Выделенные поля должны быть заполнены")
            elif self.textEdit_password_reg.text().strip() != self.textEdit_repeat_password.text().strip():
                self.textEdit_password_reg.setStyleSheet("border: 2px solid red; border-radius: 8px;")
                self.textEdit_repeat_password.setStyleSheet("border: 2px solid red; border-radius: 8px;")
                QtWidgets.QMessageBox.critical(None, "Ошибка", f"Пароли не совпадают")
            else:
                self.add_user()
                self.add_image.setStyleSheet("QPushButton {background-color: #cccccc; border: none; color: #808080}")
                self.avatar_registration.hide()
                self.avatar_registration.clear()
                self.textEdit_login_reg.clear()
                self.comboBox_roles.setCurrentIndex(0)
                self.textEdit_password_reg.clear()
                self.textEdit_repeat_password.clear()
                self.textEdit_surname.clear()
                self.textEdit_name.clear()
                self.textEdit_patronum.clear()
                self.comboBox_country.clear()
                self.textEdit_age.clear()
                self.textEdit_education.clear()
                self.textEdit_description.clear()
                self.addFile_education.setEnabled(True)
                if self.current_role_id == 2:
                    self.table_of_language_registration.show()
                    self.label_language_registration.show()
                    self.pushButton_add_language_registration.show()
                    self.pushButton_edit_language_registration.show()
                    self.pushButton_delete_language_registration.show()
                else:
                    self.table_of_language_registration.hide()
                    self.label_language_registration.hide()
                    self.pushButton_add_language_registration.hide()
                    self.pushButton_edit_language_registration.hide()
                    self.pushButton_delete_language_registration.hide()
                self.switch_forms(self.frame_registration, self.frame_language_contacts)
        except Exception as e:
            print(e)

    # ==============================
    # CRUD methods
    # ==============================

    def add_contact_at_table(self):
        try:
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Добавление контакта")
            dialog.setFixedSize(350, 180)
            layout = QtWidgets.QVBoxLayout(dialog)

            types = list(fetch_all('select * from Типы_контактов'))
            combo = QtWidgets.QComboBox()
            combo.addItems(['']+[i[1] for i in types])
            placeholders = ['']+[i[2] for i in types]

            line_edit = QtWidgets.QLineEdit()

            combo.currentIndexChanged.connect(lambda: line_edit.setPlaceholderText(placeholders[combo.currentIndex()]))

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok |
                QtWidgets.QDialogButtonBox.StandardButton.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)

            layout.addWidget(QtWidgets.QLabel("Тип контакта:"))
            layout.addWidget(combo)
            layout.addWidget(QtWidgets.QLabel("Значение:"))
            layout.addWidget(line_edit)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                contact_type = combo.currentText()
                contact_value = line_edit.text().strip()

                if not contact_value:
                    QtWidgets.QMessageBox.warning(None, "Ошибка", "Поле ввода не может быть пустым!")
                    return

                table = self.table_of_contacts_registration
                row_idx = table.rowCount()
                table.insertRow(row_idx)


                item_type = QtWidgets.QTableWidgetItem(contact_type)
                item_value = QtWidgets.QTableWidgetItem(contact_value)

                self._font(item_type, 18)
                self._font(item_value, 18)

                item_type.setFlags(item_type.flags() & ~Qt.ItemFlag.ItemIsEditable)
                item_value.setFlags(item_value.flags() & ~Qt.ItemFlag.ItemIsEditable)

                table.setItem(row_idx, 0, item_type)
                table.setItem(row_idx, 1, item_value)

        except Exception as e:
            print(f"Ошибка в add_contact_and_sync: {e}")
            traceback.print_exc()

    def edit_contact_at_table(self):
        try:
            table = self.table_of_contacts_registration
            selected_row = table.currentRow()

            if selected_row == -1:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите контакт для редактирования!")
                return

            current_type = table.item(selected_row, 0).text()
            current_value = table.item(selected_row, 1).text()

            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Редактирование контакта")
            dialog.setFixedSize(350, 180)
            layout = QtWidgets.QVBoxLayout(dialog)

            types_data = fetch_all('select * from Типы_контактов', ())
            combo = QtWidgets.QComboBox()

            type_names = [str(i[1]) for i in types_data] if types_data else []
            placeholders = [str(i[2]) for i in types_data] if types_data else []

            combo.addItems(type_names)

            if current_type in type_names:
                combo.setCurrentText(current_type)

            line_edit = QtWidgets.QLineEdit()
            line_edit.setText(current_value)
            self._font(line_edit, 12)
            self._font(combo, 12)

            def update_placeholder():
                idx = combo.currentIndex()
                if idx >= 0:
                    line_edit.setPlaceholderText(placeholders[idx])

            combo.currentIndexChanged.connect(update_placeholder)
            update_placeholder()

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok |
                QtWidgets.QDialogButtonBox.StandardButton.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)

            layout.addWidget(QtWidgets.QLabel("Тип контакта:"))
            layout.addWidget(combo)
            layout.addWidget(QtWidgets.QLabel("Значение:"))
            layout.addWidget(line_edit)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                new_type = combo.currentText()
                new_value = line_edit.text().strip()

                if not new_value:
                    QtWidgets.QMessageBox.warning(None, "Ошибка", "Поле ввода не может быть пустым!")
                    return

                item_type = table.item(selected_row, 0)
                item_value = table.item(selected_row, 1)

                item_type.setText(new_type)
                item_value.setText(new_value)

                QtWidgets.QMessageBox.information(None, "Успех", "Контакт изменен!")

        except Exception as e:
            print(f"Ошибка в edit_contact_at_table: {e}")
            traceback.print_exc()

    def delete_contact_from_table(self):
        try:
            table = self.table_of_contacts_registration
            selected_row = table.currentRow()

            if selected_row == -1:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите строку для удаления!")
                return

            confirm = QtWidgets.QMessageBox.question(
                None, "Подтверждение", "Вы уверены, что хотите удалить этот контакт?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )

            if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                table.removeRow(selected_row)

        except Exception as e:
            print(f"Ошибка при удалении строки: {e}")
            traceback.print_exc()

    def add_language_at_table(self):
        try:
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Добавление языка")
            dialog.setFixedSize(350, 220)
            layout = QtWidgets.QVBoxLayout(dialog)

            all_langs = fetch_all('SELECT id_языка, Название FROM Языки', ())
            all_levels = fetch_all('SELECT id_уровня, Название, id_языка FROM Уровни', ())

            combo_lang = QtWidgets.QComboBox()
            combo_lang.addItems([''] + [str(i[1]) for i in all_langs])

            combo_level = QtWidgets.QComboBox()
            self._font(combo_lang, 12)
            self._font(combo_level, 12)

            def update_levels():
                combo_level.clear()
                lang_name = combo_lang.currentText()
                if not lang_name: return

                lang_id = next((i[0] for i in all_langs if i[1] == lang_name), None)
                filtered_levels = [i[1] for i in all_levels if i[2] == lang_id]
                combo_level.addItems(filtered_levels)

            combo_lang.currentIndexChanged.connect(update_levels)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)

            layout.addWidget(QtWidgets.QLabel("Выберите язык:"))
            layout.addWidget(combo_lang)
            layout.addWidget(QtWidgets.QLabel("Выберите уровень:"))
            layout.addWidget(combo_level)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                lang = combo_lang.currentText()
                level = combo_level.currentText()

                if not lang or not level:
                    QtWidgets.QMessageBox.warning(None, "Ошибка", "Все поля должны быть заполнены!")
                    return

                table = self.table_of_language_registration
                row_idx = table.rowCount()
                table.insertRow(row_idx)

                item_lang = QtWidgets.QTableWidgetItem(lang)
                item_level = QtWidgets.QTableWidgetItem(level)

                for item in [item_lang, item_level]:
                    self._font(item, 18)
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)

                table.setItem(row_idx, 0, item_lang)
                table.setItem(row_idx, 1, item_level)

        except Exception as e:
            print(f"Ошибка в add_language_at_table: {e}")
            traceback.print_exc()

    def edit_language_at_table(self):
        try:
            table = self.table_of_language_registration
            selected_row = table.currentRow()
            if selected_row == -1:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите строку!")
                return

            current_lang = table.item(selected_row, 0).text()
            current_level = table.item(selected_row, 1).text()

            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Редактирование языка")
            dialog.setFixedSize(350, 220)
            layout = QtWidgets.QVBoxLayout(dialog)

            all_langs = fetch_all('SELECT id_языка, Название FROM Языки', ())
            all_levels = fetch_all('SELECT id_уровня, Название, id_языка FROM Уровни', ())

            combo_lang = QtWidgets.QComboBox()
            combo_lang.addItems([str(i[1]) for i in all_langs])
            combo_level = QtWidgets.QComboBox()

            def update_levels():
                combo_level.clear()
                lang_id = next((i[0] for i in all_langs if i[1] == combo_lang.currentText()), None)
                combo_level.addItems([i[1] for i in all_levels if i[2] == lang_id])

            combo_lang.currentIndexChanged.connect(update_levels)
            combo_lang.setCurrentText(current_lang)
            update_levels()
            combo_level.setCurrentText(current_level)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)

            layout.addWidget(QtWidgets.QLabel("Язык:"))
            layout.addWidget(combo_lang)
            layout.addWidget(QtWidgets.QLabel("Уровень:"))
            layout.addWidget(combo_level)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                table.item(selected_row, 0).setText(combo_lang.currentText())
                table.item(selected_row, 1).setText(combo_level.currentText())

        except Exception as e:
            print(f"Ошибка в edit_language_at_table: {e}")
            traceback.print_exc()

    def delete_language_from_table(self):
        try:
            table = self.table_of_language_registration
            selected_row = table.currentRow()
            if selected_row == -1:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите строку!")
                return

            if QtWidgets.QMessageBox.question(None, "Удаление", "Удалить выбранный язык?",
                                              QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No) == QtWidgets.QMessageBox.StandardButton.Yes:
                table.removeRow(selected_row)
        except Exception as e:
            print(f"Ошибка при удалении языка: {e}")

    def add_contact_edit(self):
        try:
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Добавить контакт")
            dialog.setFixedSize(350, 180)
            layout = QtWidgets.QVBoxLayout(dialog)

            types_data = fetch_all('SELECT * FROM Типы_контактов')
            combo = QtWidgets.QComboBox()
            combo.addItems([str(i[1]) for i in types_data])
            placeholders = [str(i[2]) for i in types_data]

            line_edit = QtWidgets.QLineEdit()
            self._font(line_edit, 12)
            self._font(combo, 12)

            combo.currentIndexChanged.connect(lambda: line_edit.setPlaceholderText(placeholders[combo.currentIndex()]))
            if placeholders: line_edit.setPlaceholderText(placeholders[0])

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)

            layout.addWidget(QtWidgets.QLabel("Тип контакта:"))
            layout.addWidget(combo)
            layout.addWidget(QtWidgets.QLabel("Значение:"))
            layout.addWidget(line_edit)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                val = line_edit.text().strip()
                if not val:
                    QtWidgets.QMessageBox.warning(None, "Ошибка", "Значение не может быть пустым!")
                    return

                new_id = get_new_id("Контакты", "id_контакта")
                data = {
                    "id_контакта": new_id,
                    "UserId": self.current_user_id,
                    "Тип": combo.currentText(),
                    "Значение": val
                }
                insert_row("Контакты", data)

                reload_table(self.table_of_contacts_editing,
                             "SELECT id_контакта, Тип, Значение FROM Контакты WHERE UserId = %s",
                             values=(self.current_user_id,))
        except Exception as e:
            print(f"Ошибка добавления контакта: {e}")

    def edit_contact_edit(self):
        try:
            table = self.table_of_contacts_editing
            pk = self.get_selected_pk(table)
            if pk is None:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите контакт!")
                return

            row = table.currentRow()
            current_type = table.item(row, 1).text()
            current_val = table.item(row, 2).text()

            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Редактирование контакта")
            dialog.setFixedSize(350, 180)
            layout = QtWidgets.QVBoxLayout(dialog)

            types_data = fetch_all('SELECT * FROM Типы_контактов')
            combo = QtWidgets.QComboBox()
            type_names = [str(i[1]) for i in types_data]
            combo.addItems(type_names)
            combo.setCurrentText(current_type)

            line_edit = QtWidgets.QLineEdit(current_val)
            self._font(line_edit, 12)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)

            layout.addWidget(QtWidgets.QLabel("Тип:"))
            layout.addWidget(combo)
            layout.addWidget(QtWidgets.QLabel("Значение:"))
            layout.addWidget(line_edit)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                new_val = line_edit.text().strip()
                if not new_val: return

                update_row("Контакты", pk, {"Тип": combo.currentText(), "Значение": new_val}, "id_контакта")
                reload_table(table, "SELECT id_контакта, Тип, Значение FROM Контакты WHERE UserId = %s",
                             values=(self.current_user_id,))
        except Exception as e:
            print(f"Ошибка редактирования: {e}")

    def delete_contact_edit(self):
        try:
            table = self.table_of_contacts_editing
            # Получаем PK (id_контакта) выделенной строки
            pk = self.get_selected_pk(table)

            if pk is None:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите контакт для удаления!")
                return

            confirm = QtWidgets.QMessageBox.question(
                None, "Подтверждение", "Вы уверены, что хотите удалить этот контакт?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )

            if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                delete_row("Контакты", "id_контакта", pk)

                reload_table(table,
                             "SELECT id_контакта, Тип, Значение FROM Контакты WHERE UserId = %s",
                             values=(self.current_user_id,))

                QtWidgets.QMessageBox.information(None, "Успех", "Контакт удален!")

        except Exception as e:
            print(f"Ошибка при удалении контакта: {e}")
            traceback.print_exc()

    def add_language_edit(self):
        try:
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Добавить язык")
            dialog.setFixedSize(350, 220)
            layout = QtWidgets.QVBoxLayout(dialog)

            all_langs = fetch_all('SELECT id_языка, Название FROM Языки')
            all_levels = fetch_all('SELECT id_уровня, Название, id_языка FROM Уровни')

            combo_lang = QtWidgets.QComboBox()
            combo_lang.addItems([str(i[1]) for i in all_langs])
            combo_level = QtWidgets.QComboBox()
            self._font(combo_lang, 12)
            self._font(combo_level, 12)

            def update_levels():
                combo_level.clear()
                lang_id = next((i[0] for i in all_langs if i[1] == combo_lang.currentText()), None)
                combo_level.addItems([i[1] for i in all_levels if i[2] == lang_id])

            combo_lang.currentIndexChanged.connect(update_levels)
            update_levels()

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)

            layout.addWidget(QtWidgets.QLabel("Язык:"))
            layout.addWidget(combo_lang)
            layout.addWidget(QtWidgets.QLabel("Уровень:"))
            layout.addWidget(combo_level)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                new_id = get_new_id("Языки_преподавателей", "id_записи")
                data = {
                    "id_записи": new_id,
                    "UserId": self.current_user_id,
                    "id_языка": next(i[0] for i in all_langs if i[1] == combo_lang.currentText()),
                    "id_уровня": next(i[0] for i in all_levels if i[1] == combo_level.currentText())
                }
                insert_row("Языки_преподавателей", data)

                reload_table(self.table_of_language_editing,
                             "SELECT yp.id_записи, y.Название, u.Название FROM Языки_преподавателей yp JOIN Языки y ON yp.id_языка = y.id_языка JOIN Уровни u ON yp.id_уровня = u.id_уровня WHERE yp.UserId = %s",
                             values=(self.current_user_id,))
        except Exception as e:
            print(f"Ошибка: {e}")

    def edit_language_edit(self):
        try:
            pk = self.get_selected_pk(self.table_of_language_editing)
            if pk is None:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите язык из списка")
                return

            new_level, ok = QtWidgets.QInputDialog.getItem(None, "Редактирование", "Новый уровень:",
                                                           ["A1", "A2", "B1", "B2", "C1", "C2", "Native"], 0, False)
            if ok:
                update_row("Языки", {"Уровень": new_level}, "id_языка", pk)
                reload_table(self.table_of_language_editing,
                             "SELECT id_языка, Название, Уровень FROM Языки WHERE UserId = %s",
                             ("Название", "Уровень"), (self.current_user_id,))
        except Exception as e:
            print(f"Ошибка редактирования языка: {e}")

    def delete_language_edit(self):
        try:
            pk = self.get_selected_pk(self.table_of_language_editing)
            if pk is None: return

            if QtWidgets.QMessageBox.question(None, "Удаление",
                                              "Удалить этот язык?") == QtWidgets.QMessageBox.StandardButton.Yes:
                delete_row("Языки_преподавателей", "id_записи", pk)
                reload_table(self.table_of_language_editing,
                             "SELECT yp.id_записи, y.Название, u.Название FROM Языки_преподавателей yp JOIN Языки y ON yp.id_языка = y.id_языка JOIN Уровни u ON yp.id_уровня = u.id_уровня WHERE yp.UserId = %s",
                             values=(self.current_user_id,))
        except Exception as e:
            print(f"Ошибка удаления: {e}")

    def save_tables_data_to_db(self):
        try:
            contact_table = "Контакты_преподавателей" if self.current_role_id == 2 else "Контакты_студентов"

            table_contacts = self.table_of_contacts_registration
            for row in range(table_contacts.rowCount()):
                type_name = table_contacts.item(row, 0).text()
                contact_value = table_contacts.item(row, 1).text()

                type_res = fetch_all("SELECT id_типа_контакта FROM Типы_контактов WHERE Название = %s", (type_name,))

                if not type_res:
                    print(f"Ошибка: Тип контакта '{type_name}' не найден в БД!")
                    continue

                type_id = type_res[0][0]

                new_contact_id = get_new_id(contact_table, "id_записи")
                contact_data = {
                    "id_записи": new_contact_id,
                    "UserId": self.current_user_id,
                    "id_типа_контакта": type_id,
                    "Значение": contact_value
                }

                insert_row(contact_table, contact_data)

            if self.current_role_id == 2:
                table_langs = self.table_of_language_registration
                for row in range(table_langs.rowCount()):
                    lang_name = table_langs.item(row, 0).text()
                    level_name = table_langs.item(row, 1).text()

                    lang_res = fetch_all("SELECT id_языка FROM Языки WHERE Название = %s", (lang_name,))
                    level_res = fetch_all("SELECT id_уровня FROM Уровни WHERE Название = %s", (level_name,))

                    if lang_res and level_res:
                        lang_id = lang_res[0][0]
                        level_id = level_res[0][0]

                        new_lang_rec_id = get_new_id("Языки_преподавателей", "id_записи")
                        lang_data = {
                            "id_записи": new_lang_rec_id,
                            "UserId": self.current_user_id,
                            "id_языка": lang_id,
                            "id_уровня": level_id
                        }
                        insert_row("Языки_преподавателей", lang_data)

            self.enter()

        except Exception as e:
            print(f"Ошибка при сохранении данных таблиц: {e}")
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Ошибка", f"Не удалось сохранить дополнительные данные: {e}")

    def send_course_application(self):
        try:
            course_id = self.get_selected_pk(self.table_of_courses)
            check_role = 'Студенты_На_Курсах' if self.current_role_id == 3 else 'Преподаватели_на_курсах'
            if fetch_all(f"SELECT * FROM {check_role} WHERE id_курса = %s and UserId = %s", (course_id, self.current_user_id)):
                QtWidgets.QMessageBox.critical(None, "Ошибка", f"Пользователь состоит на данном курсе")
                return
            course_name = fetch_cell(table_name='Курсы', column='Название', primary_key='id_курса', value=course_id)
            text, ok = QtWidgets.QInputDialog.getMultiLineText(
                None,
                "Подача заявки",
                f"Напишите сообщение преподавателю курса '{course_name}':"
            )
            role = 'Преподаватели' if self.current_role_id==2 else 'Студенты'
            user = fetch_one(table_name=role, column='UserId', value=self.current_user_id)
            if ok and text:
                req_id = get_new_id("Заявки", "Номер_заявки")
                req_data = {
                    "Номер_заявки": req_id,
                    "UserId": self.current_user_id,
                    "id_курса": course_id,
                    "Содержание": text
                }
                insert_row("Заявки", req_data)
                teachers = fetch_all(
                    "SELECT UserId FROM Преподаватели_на_курсах WHERE id_курса = %s",
                    (course_id,)
                )
                if teachers:
                    import datetime
                    today = datetime.date.today()
                    for teacher_row in teachers:
                        teacher_id = teacher_row[0]
                        notif_id = get_new_id("Уведомления", "Номер_записи")

                        notif_data = {
                            "Номер_записи": notif_id,
                            "UserId": teacher_id,
                            "Дата": today,
                            "Тема": f"Заявка от пользователя {user[1]} {user[2]} {user[3]}",
                            "Содержание": text,
                        }
                        insert_row("Уведомления", notif_data)
                QtWidgets.QMessageBox.information(None, "Успех", "Заявка отправлена!")
        except Exception as e:
            print(f"Ошибка при подаче заявки: {e}")
            traceback.print_exc()

    def approve_application(self, request_pk):
        try:
            request = fetch_one(table_name='Заявки', column='Номер_заявки', value=request_pk)
            role = fetch_cell("Пользователи", "id_роли", request[1], "UserId")

            target_table = "Студенты_На_Курсах" if role == 3 else "Преподаватели_На_Курсах"

            link_data = {
                "id_курса": request[2],
                "UserId": request[1]
            }
            insert_row(target_table, link_data)

            import datetime
            today = datetime.date.today()

            course_name = fetch_cell(table_name='Курсы', column='Название', value=request[2], primary_key='id_курса')

            notif_id = get_new_id("Уведомления", "Номер_записи")
            notif_data = {
                "Номер_записи": notif_id,
                "UserId": request[1],
                "Дата": today,
                "Тема": f"Одобрение заявки на {course_name}",
                "Содержание": f"Ваша заявка на курс '{course_name}' была одобрена. Вы зачислены.",
            }
            insert_row("Уведомления", notif_data)
            delete_row("Заявки", request_pk, "Номер_заявки")

            QtWidgets.QMessageBox.information(None, "Успех", "Пользователь принят на курс.")

        except Exception as e:
            print(f"Ошибка при одобрении: {e}")
            traceback.print_exc()

    def reject_application(self, request_pk):
        try:
            request = fetch_one(table_name='Заявки', column='Номер_заявки', value=request_pk)
            course_name = fetch_cell(table_name='Курсы', column='Название', value=request[2],
                                     primary_key='id_курса')

            reason, ok = QtWidgets.QInputDialog.getMultiLineText(
                None,
                "Отклонение заявки",
                f"Укажите причину отказа для заявки на курс '{course_name}':"
            )

            if ok:
                import datetime
                today = datetime.date.today()

                if not reason.strip():
                    reason = "Причина не указана преподавателем."

                notif_id = get_new_id("Уведомления", "Номер_записи")
                notif_data = {
                    "Номер_записи": notif_id,
                    "UserId": request[1],
                    "Дата": today,
                    "Тема": f"Отклонение заявки на {course_name}",
                    "Содержание": f"Ваша заявка на курс '{course_name}' была отклонена.\n\nПричина: {reason}",
                }
                insert_row("Уведомления", notif_data)

                delete_row("Заявки", request_pk, "Номер_заявки")

                QtWidgets.QMessageBox.information(None, "Готово", "Заявка успешно отклонена, пользователь уведомлен.")

        except Exception as e:
            print(f"Ошибка при отклонении: {e}")
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Ошибка", f"Не удалось отклонить заявку: {e}")

    def open_application_dialog(self, table):
        try:
            application_id = self.get_selected_pk(table)

            if application_id is None:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Пожалуйста, выберите заявку в таблице!")
                return

            query = """
                    SELECT з.Содержание,
                           COALESCE(с.Фамилия, пр.Фамилия) as Fam,
                           COALESCE(с.Имя, пр.Имя)         as Nam,
                           з.UserId, \
                           з.id_курса
                    FROM Заявки з
                             LEFT JOIN Студенты с ON з.UserId = с.UserId
                             LEFT JOIN Преподаватели пр ON з.UserId = пр.UserId
                    WHERE з.Номер_заявки = %s \
                    """
            data = fetch_all(query, (application_id,))
            if not data:
                return

            content, fam, nam, applicant_id, course_id = data[0]

            self.app_decision_dialog = QtWidgets.QDialog()
            self.app_decision_dialog.setWindowTitle(f"Заявка №{application_id}")
            self.app_decision_dialog.setFixedSize(450, 400)
            layout = QtWidgets.QVBoxLayout(self.app_decision_dialog)

            info_label = QtWidgets.QLabel(f"<b>Отправитель:</b> {fam} {nam}<br><b>ID пользователя:</b> {applicant_id}")
            self._font(info_label, 12)

            text_browser = QtWidgets.QTextBrowser()
            text_browser.setText(content)
            self._font(text_browser, 12)

            btn_layout = QtWidgets.QHBoxLayout()

            btn_accept = QtWidgets.QPushButton("Принять")
            btn_accept.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; height: 40px;")
            btn_accept.clicked.connect(lambda: self.approve_application(application_id))

            btn_reject = QtWidgets.QPushButton("Отклонить")
            btn_reject.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; height: 40px;")
            btn_reject.clicked.connect(lambda: self.reject_application(application_id))

            btn_layout.addWidget(btn_accept)
            btn_layout.addWidget(btn_reject)

            layout.addWidget(info_label)
            layout.addWidget(QtWidgets.QLabel("<b>Текст заявки:</b>"))
            layout.addWidget(text_browser)
            layout.addLayout(btn_layout)

            self.app_decision_dialog.exec()

        except Exception as e:
            print(f"Ошибка при открытии окна заявки: {e}")
            traceback.print_exc()

    def open_profile(self, tableWidget, frame):
        try:
            self.observed_user_id = self.get_selected_pk(tableWidget)
            role = fetch_cell(table_name="Пользователи", column="id_роли", value=self.observed_user_id, primary_key="UserId")
            if role == 3:
                self.output_age.show()
                self.output_description.hide()
                self.pushButtonDownloadEducation.hide()
                self.label_age_output.show()
                self.label_description_output.hide()
                self.label_education_output.hide()
                self.table_of_language_view_profile.hide()
                self.label_language_output.hide()
            if role == 2:
                self.output_age.hide()
                self.output_description.show()
                self.pushButtonDownloadEducation.show()
                self.label_age_output.hide()
                self.label_description_output.show()
                self.label_education_output.show()
                self.table_of_language_view_profile.show()
                self.label_language_output.show()

            table_role = "Преподаватели" if role == 2 else "Студенты"
            contacts_table_role = "Контакты_преподавателей" if role == 2 else "Контакты_студентов"

            surname = fetch_cell(table_name=table_role, column="Фамилия", primary_key="UserId",
                                 value=self.observed_user_id)
            name = fetch_cell(table_name=table_role, column="Имя", primary_key="UserId", value=self.observed_user_id)
            patronim = fetch_cell(table_name=table_role, column="Отчество", primary_key="UserId",
                                  value=self.observed_user_id)
            value = (surname + ' ' + name + ' ' + patronim) if patronim else (surname + ' ' + name)

            reload_table(self.table_of_contacts_view_profile, f'select cu.id_записи, c.Название, cu.Значение from {contacts_table_role} cu join Типы_контактов c on cu.id_типа_контакта = c.id_типа_контакта where cu.UserId = %s', columns=('Тип', 'Значение'), values=(self.observed_user_id, ))

            self.output_FIO.clear()
            self.output_FIO.setText(value)

            reload_image(image_widget=self.avatar_view_profile, table_name=table_role, column="Фото",
                         primary_key="UserId",
                         key_value=self.observed_user_id)

            reload_line(line_widget=self.output_roles, table_name="Роли", column="Название",
                        primary_key="id_роли", key_value=role)

            current_country_id = fetch_cell(table_role, 'Страна', self.observed_user_id, 'UserId')

            reload_line(line_widget=self.output_country, table_name='Страны', column="Название",
                        primary_key="id_страны",
                        key_value=current_country_id)

            if role == 3:
                reload_line(line_widget=self.output_age, table_name="Студенты", column="Возраст",
                            primary_key="UserId", key_value=self.observed_user_id)
            if role == 2:
                reload_table(self.table_of_language_view_profile,
                             """SELECT 
                                            Языки.Название AS Язык, 
                                            Уровни.Название AS Уровень,
                                            Уровни.Описание AS Описание_уровня
                                        FROM Языки_преподавателей
                                        JOIN Языки ON Языки_преподавателей.id_языка = Языки.id_языка
                                        JOIN Уровни ON Языки_преподавателей.id_уровня = Уровни.id_уровня
                                        WHERE Языки_преподавателей.UserId = %s;""",
                             columns=('Язык', 'Уровень'), values=(self.observed_user_id,))
                reload_line(line_widget=self.output_description, table_name="Преподаватели", column="Описание",
                            primary_key="UserId", key_value=self.observed_user_id)

            self.switch_forms(frame, self.frame_view_profile)
        except Exception as e:
            print(e)
            traceback.print_exc()

    def open_course_info(self, table_widget):
        try:
            self.observed_course_id = self.get_selected_pk(table_widget)
            if self.observed_course_id is None:
                return
            course_data = fetch_one("Курсы", "id_курса", self.observed_course_id)

            if course_data:

                c_id, name, lang_id, description, teacher_id = course_data

                self.textEdit_course_name.setText(str(name))
                self.textEdit_course_description.setText(str(description))
                lang_name = fetch_cell("Языки", "Название", lang_id, "id_языка")
                self.textEdit_course_language.setText(str(lang_name))
                self.tabWidget_course.setCurrentIndex(0)
                self.switch_forms(self.frame_main, self.frame_course)
                self.course_tables()
                if fetch_all('select * from Преподаватели_на_курсах where id_курса=%s and UserId=%s', (c_id, self.current_user_id)) is not None:
                    self.pushButton_leave_the_course_main_course.setVisible(True)
                    self.pushButton_leave_the_course_main_course.setGeometry(860, 250, 291, 61)
                    self.pushButton_back_to_main_from_main_course.setGeometry(860, 340, 291, 61)
                    self.pushButton_edit_course.setVisible(True)
                    self.pushButton_edit_course.setGeometry(860, 430, 291, 61)


                    self.tabWidget_course.addTab(self.tab_application, "")
                    self.tabWidget_course.setTabText(self.tabWidget_course.indexOf(self.tab_application), "Заявки")
                    self.tabWidget_course.setStyleSheet("""
                                                                         QTabBar::tab {
                                                                                width: """ + str(
                        1200 / self.tabWidget_course.count()) + """; 
                                                                                height: 50;
                                                                                background: rgb(85, 0, 0);
                                                                                color: white;
                                                                         }
                                                                         QTabBar::tab:selected {
                                                                             background: rgb(65, 0, 0);
                                                                             border-bottom-color: #202020;
                                                                         }""")
                    self.pushButtonExcludeStudent.show()
                    self.pushButtonMarks.setGeometry(860, 160, 291, 61)
                    self.pushButtonObserveProfile.setGeometry(860, 250, 291, 61)
                    self.pushButton_back_to_main_from_students.setGeometry(860, 340, 291, 61)

                elif fetch_all('select * from Студенты_На_Курсах where id_курса=%s and UserId=%s', (c_id, self.current_user_id)) is not None:
                    self.pushButton_leave_the_course_main_course.setVisible(True)
                    self.pushButton_leave_the_course_main_course.setGeometry(860, 250, 291, 61)
                    self.pushButton_back_to_main_from_main_course.setGeometry(860, 340, 291, 61)
                    self.pushButton_edit_course.setVisible(False)

                    self.pushButtonExcludeStudent.hide()
                    self.pushButtonMarks.setGeometry(860, 70, 291, 61)
                    self.pushButtonObserveProfile.setGeometry(860, 160, 291, 61)
                    self.pushButton_back_to_main_from_students.setGeometry(860, 250, 291, 61)
                else:
                    self.pushButton_leave_the_course_main_course.setVisible(True)
                    self.pushButton_edit_course.setVisible(False)
                    self.pushButton_back_to_main_from_main_course.setVisible(True)
                    self.pushButton_back_to_main_from_main_course.setGeometry(860, 250, 291, 61)

                    self.pushButtonExcludeStudent.hide()
                    self.pushButtonMarks.setGeometry(860, 70, 291, 61)
                    self.pushButtonObserveProfile.setGeometry(860, 160, 291, 61)
                    self.pushButton_back_to_main_from_students.setGeometry(860, 250, 291, 61)

        except Exception as e:
            print(f"Ошибка при открытии курса: {e}")
            traceback.print_exc()

    def course_tables(self):
        try:
            reload_table(self.table_of_students_course, "SELECT s.UserId, CONCAT_WS(' ', s.Фамилия, s.Имя, s.Отчество) AS `ФИО Студента`, c.Название, s.Возраст FROM Студенты s JOIN Студенты_На_Курсах snk ON s.UserId = snk.UserId JOIN Страны c ON s.Страна = c.id_страны WHERE snk.id_курса = %s;", values=(self.observed_course_id,))
            reload_table(self.table_of_teachers_course,"SELECT p.UserId, CONCAT_WS(' ', p.Фамилия, p.Имя, p.Отчество) AS `ФИО Преподавателя`, c.Название FROM Преподаватели p JOIN Преподаватели_на_курсах pnk ON p.UserId = pnk.UserId JOIN Страны c ON p.Страна = c.id_страны WHERE pnk.id_курса = %s;",values=(self.observed_course_id,))
            reload_table(self.teacher_application_list, "SELECT з.`Номер_заявки`, пр.`Фамилия`, пр.`Имя`, з.`Содержание` FROM `Заявки` з JOIN `Преподаватели` пр ON з.`UserId` = пр.`UserId` JOIN `Пользователи` п ON з.`UserId` = п.`UserId` JOIN `Роли` р ON п.`id_роли` = р.`id_роли` WHERE р.`Название` = 'Преподаватель' AND з.`id_курса` = %s;", values=(self.observed_course_id,))
            reload_table(self.student_application_list, "SELECT з.`Номер_заявки`, с.`Фамилия`, с.`Имя`, з.`Содержание` FROM `Заявки` з JOIN `Студенты` с ON з.`UserId` = с.`UserId` JOIN `Пользователи` п ON з.`UserId` = п.`UserId` JOIN `Роли` р ON п.`id_роли` = р.`id_роли` WHERE р.`Название` = 'Студент' AND з.`id_курса` = %s;", values=(self.observed_course_id,))
        except Exception as e:
            print(e)
            traceback.print_exc()

    def close_course_info(self):
        self.observed_course_id = None
        self.main_tables()
        self.switch_forms(self.frame_course, self.frame_main)

    def leave_course(self, from_info=False):
        try:
            if from_info:
                course_id = self.observed_course_id
            else:
                course_id = self.get_selected_pk(self.table_of_my_courses)
                if course_id is None:
                    QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите курс!")
                    return
            is_teacher = (self.current_role_id == 2)

            if is_teacher:
                course_data = fetch_one("Курсы", "id_курса", course_id)
                if not course_data: return
                owner_id = course_data[4]

                if owner_id == self.current_user_id:
                    other_teachers = fetch_all(
                        "SELECT UserId, Фамилия, Имя FROM Преподаватели WHERE UserId != %s",
                        (self.current_user_id,)
                    )

                    if other_teachers:
                        self.show_transfer_control_dialog(course_id, other_teachers)
                    else:
                        confirm = QtWidgets.QMessageBox.question(None, "Удаление",
                                                                 "Вы единственный преподаватель. Курс будет удален. Продолжить?")
                        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                            delete_row("Курсы", "id_курса", course_id)
                else:

                    execute_query("DELETE FROM Преподаватели_на_курсах WHERE id_курса = %s AND UserId = %s",
                                  (course_id, self.current_user_id))

            else:
                confirm = QtWidgets.QMessageBox.question(None, "Выход", "Вы уверены, что хотите покинуть курс?")
                if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                    execute_query("DELETE FROM Студенты_На_Курсах WHERE id_курса = %s AND UserId = %s",
                                  (course_id, self.current_user_id))
                    execute_query("DELETE FROM Оценки WHERE id_курса = %s AND UserId = %s", (course_id, self.current_user_id))

            QtWidgets.QMessageBox.information(None, "Успех", "Операция завершена")
            self.course_tables()
            self.close_course_info()


        except Exception as e:
            print(f"Ошибка: {e}")
            traceback.print_exc()

    def show_transfer_control_dialog(self, course_id, other_teachers):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Передача курса")
        layout = QtWidgets.QVBoxLayout(dialog)

        combo = QtWidgets.QComboBox()
        teacher_map = {f"{t[1]} {t[2]}": t[0] for t in other_teachers}
        combo.addItems(teacher_map.keys())

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout.addWidget(QtWidgets.QLabel("Выберите нового владельца курса:"))
        layout.addWidget(combo)
        layout.addWidget(buttons)

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            new_owner_id = teacher_map[combo.currentText()]
            update_row("Курсы", course_id, {"id_создателя": new_owner_id}, "id_курса")


    def get_level_data(self, existing_name="", existing_desc=""):
        try:
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Данные уровня")
            dialog.setFixedSize(400, 300)

            name_edit = QtWidgets.QLineEdit()
            name_edit.setPlaceholderText("Название")
            name_edit.setText(existing_name)

            desc_edit = QtWidgets.QTextEdit()
            desc_edit.setPlaceholderText("Описание")
            desc_edit.setText(existing_desc)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok |
                QtWidgets.QDialogButtonBox.StandardButton.Cancel
            )

            layout = QtWidgets.QVBoxLayout(dialog)
            layout.addWidget(QtWidgets.QLabel("Название уровня:"))
            layout.addWidget(name_edit)
            layout.addWidget(QtWidgets.QLabel("Описание:"))
            layout.addWidget(desc_edit)
            layout.addWidget(buttons)

            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)

            if dialog.exec():
                return {
                    "Название": name_edit.text(),
                    "Описание": desc_edit.toPlainText()
                }
            return None
        except Exception as e:
            print(f"Ошибка диалога: {e}")
            return None

    def add_level(self, model):
        try:
            new_level_data = self.get_level_data()

            if new_level_data and new_level_data["Название"].strip():
                item_name = QtGui.QStandardItem(new_level_data["Название"].strip())
                item_desc = QtGui.QStandardItem(new_level_data["Описание"].strip())

                model.appendRow([item_name, item_desc])

        except Exception as e:
            print(f"Ошибка при добавлении уровня: {e}")
            traceback.print_exc()

    def edit_level(self, tableView, model):
        try:
            current_index = tableView.currentIndex()

            if not current_index.isValid():
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите уровень для изменения.")
                return

            row = current_index.row()

            current_name_item = model.item(row, 0)
            current_desc_item = model.item(row, 1)

            current_name = current_name_item.text() if current_name_item else ""
            current_desc = current_desc_item.text() if current_desc_item else ""

            updated_data = self.get_level_data(existing_name=current_name, existing_desc=current_desc)

            if updated_data and updated_data["Название"]:
                model.item(row, 0).setText(updated_data["Название"])
                model.item(row, 1).setText(updated_data["Описание"])

        except Exception as e:
            print(f"Ошибка при изменении уровня: {e}")
            traceback.print_exc()

    def delete_level(self, tableView, model):
        try:
            current_index = tableView.currentIndex()

            if not current_index.isValid():
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите уровень для удаления.")
                return

            row = current_index.row()

            reply = QtWidgets.QMessageBox.question(
                None, 'Подтверждение',
                "Вы уверены, что хотите удалить этот уровень?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.No
            )

            if reply == QtWidgets.QMessageBox.StandardButton.Yes:
                model.removeRow(row)


        except Exception as e:
            print(f"Ошибка при удалении уровня: {e}")
            traceback.print_exc()

    def prepare_add_language(self):
        self.current_language_id = None
        self.textEdit_language_name.clear()
        self.table_of_levels_model.setRowCount(0)

        self.pushButton_save_language.setText("Добавить")
        if hasattr(self, 'pushButton_delete_language'):
            self.pushButton_delete_language.hide()

        self.switch_forms(self.frame_main, self.frame_language)

    def open_language_info(self, source_table):
        try:
            lang_id = self.get_selected_pk(source_table)
            if lang_id is None:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите язык из списка!")
                return

            self.current_language_id = lang_id

            lang_data = fetch_all("SELECT Название FROM Языки WHERE id_языка = %s", (lang_id,))
            if lang_data:
                self.textEdit_language_name.setText(str(lang_data[0][0]))

            levels_data = fetch_all("SELECT Название FROM Уровни WHERE id_языка = %s", (lang_id,))

            self.table_of_levels_model.clear()
            self.table_of_levels_model.setHorizontalHeaderLabels(["Название уровня"])

            if levels_data:
                for row in levels_data:
                    item = QtGui.QStandardItem(str(row[0]))
                    self.table_of_levels_model.appendRow(item)

            self.pushButton_delete_language.show()
            self.pushButton_save_language.setText("Сохранить")

            self.frame_language.show()
            self.frame_language.raise_()

        except Exception as e:
            print(f"Ошибка при загрузке языка: {e}")
            traceback.print_exc()

    def save_language_logic(self):
        name = self.textEdit_language_name.text()
        if not name:
            QtWidgets.QMessageBox.warning(None, "Ошибка", "Введите название языка!")
            return

        try:
            if self.current_language_id:
                update_row("Языки", self.current_language_id, {"Название": name}, "id_языка")
                lang_id = self.current_language_id

                conn = get_db_connection()
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM Уровни WHERE id_языка = %s", (lang_id,))
                conn.commit()
                conn.close()
            else:
                lang_id = get_new_id("Языки", "id_языка")
                insert_row("Языки", {"id_языка": lang_id, "Название": name})

            for row in range(self.table_of_levels_model.rowCount()):
                lvl_name = self.table_of_levels_model.item(row, 0).text()
                lvl_desc = self.table_of_levels_model.item(row, 1).text() if self.table_of_levels_model.item(row,
                                                                                                             1) else ""

                lvl_id = get_new_id("Уровни", "id_уровня")
                insert_row("Уровни", {
                    "id_уровня": lvl_id,
                    "Название": lvl_name,
                    "id_языка": lang_id,
                    "Описание": lvl_desc
                })

            QtWidgets.QMessageBox.information(None, "Успех", "Данные о языке сохранены!")
            self.frame_language.hide()

        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            traceback.print_exc()

    def delete_current_language(self):
        if not self.current_language_id:
            return

        confirm = QtWidgets.QMessageBox.question(None, "Подтверждение", "Удалить этот язык и все его уровни?")
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                delete_row("Языки", self.current_language_id, "id_языка")

                self.frame_language.hide()
                QtWidgets.QMessageBox.information(None, "Удалено", "Язык удален.")
            except Exception as e:
                print(f"Ошибка удаления: {e}")

    def ban_selected_user(self, table_widget):
        try:
            user_id = self.get_selected_pk(table_widget)

            if user_id is None:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Пожалуйста, выберите пользователя из списка.")
                return
            user_name = table_widget.item(table_widget.currentRow(), 1).text()

            confirm = QtWidgets.QMessageBox.question(
                None,
                "Подтверждение",
                f"Вы уверены, что хотите заблокировать пользователя: {user_name} (ID: {user_id})?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )

            if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                update_row('Пользователи', user_id, {'Заблокированный': 1}, 'UserId')


                QtWidgets.QMessageBox.information(None, "Успех", f"Пользователь {user_name} заблокирован.")

                self.main_tables()

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Ошибка", f"{e}")
            traceback.print_exc()

    def unban_selected_user(self):
        try:
            user_id = self.get_selected_pk(self.table_of_banned)

            if user_id is None:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Пожалуйста, выберите пользователя из списка.")
                return
            user_name = self.table_of_banned.item(self.table_of_banned.currentRow(), 1).text()

            confirm = QtWidgets.QMessageBox.question(
                None,
                "Подтверждение",
                f"Вы уверены, что хотите разблокировать пользователя: {user_name} (ID: {user_id})?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )

            if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                update_row('Пользователи', user_id, {'Заблокированный': 0}, 'UserId')


                QtWidgets.QMessageBox.information(None, "Успех", f"Пользователь {user_name} Разблокирован.")

                self.users_tables()

        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Ошибка", f"{e}")
            traceback.print_exc()

    def delete_user(self):
        try:
            user_id = self.get_selected_pk(self.table_of_banned)

            if not user_id:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите пользователя для полного удаления")
                return

            confirm = QtWidgets.QMessageBox.question(
                None, "Удаление аккаунта",
                f"Вы действительно хотите БЕЗВОЗВРАТНО удалить учетную запись {user_id} и все связанные данные?",
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )

            if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
                role_id = fetch_cell("Пользователи", "id_роли", user_id, "UserId")

                queries = []

                queries.append(("DELETE FROM Заблокированные WHERE UserId = %s", (user_id,)))

                if role_id == 3:
                    queries.append(("DELETE FROM Контакты_студентов WHERE UserId = %s", (user_id,)))
                    queries.append(("DELETE FROM Студенты_На_Курсах WHERE UserId = %s", (user_id,)))
                    queries.append(("DELETE FROM Студенты WHERE UserId = %s", (user_id,)))
                elif role_id == 2:
                    queries.append(("DELETE FROM Контакты_преподавателей WHERE UserId = %s", (user_id,)))
                    queries.append(("DELETE FROM Языки_преподавателей WHERE UserId = %s", (user_id,)))
                    queries.append(("DELETE FROM Преподаватели WHERE UserId = %s", (user_id,)))

                queries.append(("DELETE FROM Уведомления WHERE UserId = %s", (user_id,)))
                queries.append(("DELETE FROM Заявки WHERE UserId = %s", (user_id,)))

                queries.append(("DELETE FROM Пользователи WHERE UserId = %s", (user_id,)))

                success = True
                for q, v in queries:
                    if not execute_query(q, v):
                        success = False
                        break

                if success:
                    QtWidgets.QMessageBox.information(None, "Успех", f"Пользователь {user_id} полностью удален")
                    self.main_tables()
                else:
                    QtWidgets.QMessageBox.critical(None, "Ошибка", "Произошла ошибка при удалении из одной из таблиц")

        except Exception as e:
            print(f"Ошибка при полном удалении пользователя: {e}")
            traceback.print_exc()

    def add_lesson(self):
        try:
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Добавить занятие")
            dialog.setMinimumSize(400, 500)
            layout = QtWidgets.QVBoxLayout(dialog)

            time_start = QtWidgets.QTimeEdit()
            time_end = QtWidgets.QTimeEdit()
            desc_edit = QtWidgets.QLineEdit()

            for w in [time_start, time_end, desc_edit]:
                self._font(w, 11)

            layout.addWidget(QtWidgets.QLabel("Время начала:"))
            layout.addWidget(time_start)
            layout.addWidget(QtWidgets.QLabel("Время окончания:"))
            layout.addWidget(time_end)
            layout.addWidget(QtWidgets.QLabel("Описание (тема):"))
            layout.addWidget(desc_edit)

            layout.addWidget(QtWidgets.QLabel("Выберите студентов:"))

            select_all_cb = QtWidgets.QCheckBox("Выбрать всех")
            layout.addWidget(select_all_cb)

            student_list = QtWidgets.QListWidget()
            layout.addWidget(student_list)

            # Используем fetch_all для получения данных
            query_students = f"""
                SELECT s.UserId, CONCAT(s.Фамилия, ' ', s.Имя, IFNULL(CONCAT(' ', s.Отчество), '')) AS ФИО 
                FROM Студенты s 
                JOIN Студенты_На_Курсах snk ON s.UserId = snk.UserId 
                WHERE snk.id_курса = %s
            """
            students = fetch_all(query_students, (self.observed_course_id,))

            if students:
                for s_id, s_name in students:
                    item = QtWidgets.QListWidgetItem(s_name)
                    item.setData(QtCore.Qt.ItemDataRole.UserRole, s_id)
                    item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)
                    item.setCheckState(QtCore.Qt.CheckState.Unchecked)
                    student_list.addItem(item)

            def toggle_all(state):
                check_state = QtCore.Qt.CheckState.Checked if state else QtCore.Qt.CheckState.Unchecked
                for i in range(student_list.count()):
                    student_list.item(i).setCheckState(check_state)

            select_all_cb.stateChanged.connect(toggle_all)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                new_lesson_id = get_new_id("Занятия", "id_занятия")
                lesson_data = {
                    "id_занятия": new_lesson_id,
                    "id_курса": self.observed_course_id,
                    "Описание": desc_edit.text() or "Без описания",
                    "id_преподавателя": self.current_user_id,
                    "Дата": self.observed_schedule_date,
                    "Время_начала": time_start.time().toString("HH:mm:ss"),
                    "Время_окончания": time_end.time().toString("HH:mm:ss")
                }
                insert_row("Занятия", lesson_data)

                selected_count = 0
                for i in range(student_list.count()):
                    item = student_list.item(i)
                    if item.checkState() == QtCore.Qt.CheckState.Checked:
                        student_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
                        record_id = get_new_id('Студенты_на_занятиях', 'id_записи')
                        attendance_data = {
                            "id_записи": record_id,
                            "id_занятия": new_lesson_id,
                            "UserId": student_id
                        }
                        insert_row("Студенты_на_занятиях", attendance_data)
                        selected_count += 1

                QtWidgets.QMessageBox.information(None, "Успех",
                                                  f"Занятие добавлено! Назначено студентов: {selected_count}")
        except Exception as e:
            traceback.print_exc()

    def edit_lesson(self):
        try:
            lesson_id = self.get_selected_pk(self.table_of_schedule)
            if lesson_id is None:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите занятие для изменения!")
                return

            lesson = fetch_one("Занятия", "id_занятия", lesson_id)
            if not lesson: return

            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Изменить занятие")
            dialog.setMinimumSize(400, 550)
            layout = QtWidgets.QVBoxLayout(dialog)

            time_start = QtWidgets.QTimeEdit()
            time_end = QtWidgets.QTimeEdit()
            desc_edit = QtWidgets.QLineEdit()

            t_s = lesson[5]
            t_e = lesson[6]
            if hasattr(t_s, 'seconds'):
                time_start.setTime(QtCore.QTime(t_s.seconds // 3600, (t_s.seconds // 60) % 60))
                time_end.setTime(QtCore.QTime(t_e.seconds // 3600, (t_e.seconds // 60) % 60))

            desc_edit.setText(lesson[2])

            layout.addWidget(QtWidgets.QLabel("Время начала:"))
            layout.addWidget(time_start)
            layout.addWidget(QtWidgets.QLabel("Время окончания:"))
            layout.addWidget(time_end)
            layout.addWidget(QtWidgets.QLabel("Описание (тема):"))
            layout.addWidget(desc_edit)

            layout.addWidget(QtWidgets.QLabel("Студенты на занятии:"))

            select_all_cb = QtWidgets.QCheckBox("Выбрать всех")
            layout.addWidget(select_all_cb)

            student_list = QtWidgets.QListWidget()
            layout.addWidget(student_list)

            # 1. Получаем список всех студентов курса через fetch_all
            query_all = f"""
                SELECT s.UserId, CONCAT(s.Фамилия, ' ', s.Имя, IFNULL(CONCAT(' ', s.Отчество), '')) AS ФИО 
                FROM Студенты s 
                JOIN Студенты_На_Курсах snk ON s.UserId = snk.UserId 
                WHERE snk.id_курса = %s
            """
            all_students = fetch_all(query_all, (self.observed_course_id,))

            # 2. Получаем ID тех, кто уже записан на это занятие
            query_current = "SELECT UserId FROM Студенты_на_занятиях WHERE id_занятия = %s"
            current_attendance = fetch_all(query_current, (lesson_id,))

            present_student_ids = {row[0] for row in current_attendance} if current_attendance else set()

            if all_students:
                for s_id, s_name in all_students:
                    item = QtWidgets.QListWidgetItem(s_name)
                    item.setData(QtCore.Qt.ItemDataRole.UserRole, s_id)
                    item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsUserCheckable)

                    if s_id in present_student_ids:
                        item.setCheckState(QtCore.Qt.CheckState.Checked)
                    else:
                        item.setCheckState(QtCore.Qt.CheckState.Unchecked)

                    student_list.addItem(item)

            select_all_cb.stateChanged.connect(lambda state: [
                student_list.item(i).setCheckState(
                    QtCore.Qt.CheckState.Checked if state else QtCore.Qt.CheckState.Unchecked)
                for i in range(student_list.count())
            ])

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                update_data = {
                    "Описание": desc_edit.text() or "Без описания",
                    "Время_начала": time_start.time().toString("HH:mm:ss"),
                    "Время_окончания": time_end.time().toString("HH:mm:ss")
                }
                update_row("Занятия", lesson_id, update_data, "id_занятия")

                # Для удаления записей используем execute_query (он делает commit)
                execute_query("DELETE FROM Студенты_на_занятиях WHERE id_занятия = %s", (lesson_id,))

                for i in range(student_list.count()):
                    item = student_list.item(i)
                    if item.checkState() == QtCore.Qt.CheckState.Checked:
                        student_id = item.data(QtCore.Qt.ItemDataRole.UserRole)
                        record_id = get_new_id('Студенты_на_занятиях', 'id_записи')
                        attendance_data = {
                            "id_записи": record_id,
                            "id_занятия": lesson_id,
                            "UserId": student_id
                        }
                        insert_row("Студенты_на_занятиях", attendance_data)

                QtWidgets.QMessageBox.information(None, "Успех", "Данные занятия и список студентов обновлены!")
        except Exception as e:
            traceback.print_exc()

    def delete_lesson(self):
        try:
            lesson_id = self.get_selected_pk(self.table_of_schedule)
            if lesson_id is None:
                QtWidgets.QMessageBox.warning(None, "Ошибка", "Выберите занятие для удаления!")
                return

            if QtWidgets.QMessageBox.question(None, "Удаление",
                                              "Удалить это занятие?") == QtWidgets.QMessageBox.StandardButton.Yes:
                delete_row("Занятия", lesson_id, "id_занятия")
        except Exception as e:
            traceback.print_exc()

    # ==============================
    # Helper methods
    # ==============================

    def check_unread_notifications(self):
        try:
            if not hasattr(self, 'current_user_id') or not self.current_user_id:
                return

            query = "SELECT COUNT(*) FROM Уведомления WHERE UserId = %s AND Прочитано = 0"
            result = fetch_all(query, (self.current_user_id,))
            unread_count = result[0][0] if result else 0

            tab_index = self.tabWidget_main.indexOf(self.tab_notification)

            if tab_index != -1:
                if unread_count > 0:
                    self.tabWidget_main.setTabText(tab_index, f"Уведомления ({unread_count})")
                else:
                    self.tabWidget_main.setTabText(tab_index, "Уведомления")

        except Exception as e:
            import traceback
            print(f"Ошибка обновления счетчика уведомлений: {e}")
            traceback.print_exc()

    def check_upcoming_lessons(self):
        try:
            import datetime
            now = datetime.datetime.now()
            today = now.date()

            lessons = fetch_all(
                "SELECT id_занятия, id_курса, Описание, id_преподавателя, Время_начала "
                "FROM Занятия WHERE Дата = %s",
                (today,)
            )

            if not lessons:
                return

            for lesson in lessons:
                lesson_id, course_id, description, teacher_id, time_start_td = lesson

                start_dt = datetime.datetime.combine(today, datetime.time.min) + time_start_td
                time_diff = (start_dt - now).total_seconds()

                course_name = fetch_cell('Курсы', 'Название', course_id, 'id_курса')

                students = fetch_all("SELECT UserId FROM Студенты_На_Курсах WHERE id_курса = %s", (course_id,))
                student_ids = [s[0] for s in students] if students else []

                users_to_notify = [teacher_id] + student_ids

                notifications_to_send = []

                if time_diff > 0:
                    notifications_to_send.append({
                        "subject": f"[{lesson_id}] Занятие сегодня: {course_name}",
                        "content": f"Напоминаем, что сегодня состоится занятие по курсу '{course_name}'.\nТема: {description}\nВремя начала: {start_dt.strftime('%H:%M')}."
                    })

                if 0 < time_diff <= 3600:
                    notifications_to_send.append({
                        "subject": f"[{lesson_id}] Занятие через час: {course_name}",
                        "content": f"Занятие по курсу '{course_name}' начнется всего через час!\nТема: {description}\nВремя начала: {start_dt.strftime('%H:%M')}."
                    })

                if -900 <= time_diff <= 0:
                    notifications_to_send.append({
                        "subject": f"[{lesson_id}] Занятие началось: {course_name}",
                        "content": f"Занятие по курсу '{course_name}' началось!\nТема: {description}"
                    })

                for notif in notifications_to_send:
                    for uid in users_to_notify:
                        exists = fetch_all(
                            "SELECT 1 FROM Уведомления WHERE UserId = %s AND Дата = %s AND Тема = %s",
                            (uid, today, notif["subject"])
                        )

                        if not exists:
                            notif_id = get_new_id("Уведомления", "Номер_записи")
                            notif_data = {
                                "Номер_записи": notif_id,
                                "UserId": uid,
                                "Дата": today,
                                "Тема": notif["subject"],
                                "Содержание": notif["content"],
                                "Прочитано": 0
                            }
                            insert_row("Уведомления", notif_data)

                            if hasattr(self, 'current_user_id') and self.current_user_id == uid:
                                self.update_active_notifications_tab()

        except Exception as e:
            import traceback
            print(f"Ошибка в фоновом таймере уведомлений: {e}")
            traceback.print_exc()

    def update_active_notifications_tab(self):
        try:
            if hasattr(self, 'unchecked_notification_list') and hasattr(self,
                                                                        'current_user_id') and self.current_user_id is not None:
                reload_table(self.unchecked_notification_list,
                             "SELECT Номер_записи, Тема, Дата FROM `Уведомления` WHERE `UserId` = %s AND `Прочитано` = 0 ORDER BY `Дата` DESC;",
                             ("Тема", "Дата"), (self.current_user_id,))
                self.check_unread_notifications()
        except Exception:
            pass

    def manage_schedule_for_date(self, qdate):
        try:
            date_str = qdate.toString("yyyy-MM-dd")
            self.observed_schedule_date = date_str

            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle(f"Расписание на {qdate.toString('dd.MM.yyyy')}")
            dialog.setFixedSize(700, 450)
            layout = QtWidgets.QVBoxLayout(dialog)

            self.table_of_schedule = QtWidgets.QTableWidget()
            self.table_of_schedule.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
            layout.addWidget(self.table_of_schedule)

            def reload_schedule():
                query = """
                        SELECT з.id_занятия, \
                               з.Время_начала, \
                               з.Время_окончания, \
                               з.Описание,
                               CONCAT(п.Фамилия, ' ', п.Имя) AS Преподаватель
                        FROM Занятия з
                                 JOIN Преподаватели п ON з.id_преподавателя = п.UserId
                        WHERE з.id_курса = %s \
                          AND з.Дата = %s
                        ORDER BY з.Время_начала; \
                        """
                reload_table(self.table_of_schedule, query, ("Начало", "Конец", "Описание", "Преподаватель"),
                             (self.observed_course_id, date_str))
                self.table_of_schedule.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

            reload_schedule()
            if self.current_role_id == 2:
                btn_layout = QtWidgets.QHBoxLayout()

                btn_add = QtWidgets.QPushButton("Добавить")
                btn_edit = QtWidgets.QPushButton("Изменить")
                btn_delete = QtWidgets.QPushButton("Удалить")

                for btn in [btn_add, btn_edit, btn_delete]:
                    self._font(btn, 14)
                    btn.setStyleSheet("background-color: rgb(85, 0, 0); color: white; padding: 5px;")
                    btn_layout.addWidget(btn)

                layout.addLayout(btn_layout)

                btn_add.clicked.connect(
                    lambda: (self.add_lesson(), reload_schedule(), self.update_calendar_highlights()))
                btn_edit.clicked.connect(lambda: (self.edit_lesson(), reload_schedule()))
                btn_delete.clicked.connect(
                    lambda: (self.delete_lesson(), reload_schedule(), self.update_calendar_highlights()))

            btn_close = QtWidgets.QPushButton("Закрыть")
            self._font(btn_close, 14)
            btn_close.clicked.connect(dialog.accept)
            layout.addWidget(btn_close)

            dialog.exec()

        except Exception as e:
            print(f"Ошибка открытия расписания: {e}")
            traceback.print_exc()

    def update_calendar_highlights(self):
        try:
            default_format = QtGui.QTextCharFormat()
            self.schedule_calendar.setDateTextFormat(QtCore.QDate(), default_format)

            if not self.observed_course_id:
                return

            query = "SELECT DISTINCT Дата FROM Занятия WHERE id_курса = %s"
            dates = fetch_all(query, (self.observed_course_id,))

            if not dates: return

            highlight_format = QtGui.QTextCharFormat()
            highlight_format.setBackground(QtGui.QColor(255, 200, 200))
            highlight_format.setForeground(QtGui.QColor(85, 0, 0))
            highlight_format.setFontWeight(QtGui.QFont.Weight.Bold)

            for row in dates:
                date_obj = row[0]
                qdate = QtCore.QDate(date_obj.year, date_obj.month, date_obj.day)
                self.schedule_calendar.setDateTextFormat(qdate, highlight_format)

        except Exception as e:
            print(f"Ошибка подсветки календаря: {e}")
            traceback.print_exc()

    def observe_marks(self):
        self.switch_forms(self.frame_course, self.frame_mark)
        self.observed_marks_user = self.get_selected_pk(self.table_of_students_course)
        reload_table(table_widget=self.table_of_marks,
                     query="SELECT Номер_записи, Оценка, Максимальный_балл, Дата, Описание  FROM `Оценки` WHERE `UserId` = %s AND `id_курса` = %s ORDER BY `Дата` DESC;",
                     columns=('Оценка', 'Максимальный балл', 'Дата', 'Описание'), values=(self.observed_marks_user, self.observed_course_id))
        if fetch_all('Select * From Преподаватели_на_курсах WHERE UserID = %s And id_курса = %', self.current_user_id, self.observed_course_id):
            self.pushButtonAddMark.show()
            self.pushButtonEditMark.show()
            self.pushButtonDeleteMark.show()
        else:
            self.pushButtonAddMark.hide()
            self.pushButtonEditMark.hide()
            self.pushButtonDeleteMark.hide()

    def add_mark(self):
        try:
            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Выставить оценку")
            dialog.setFixedSize(350, 320)
            layout = QtWidgets.QVBoxLayout(dialog)

            spin_mark = QtWidgets.QSpinBox()
            spin_mark.setRange(0, 100)

            spin_max = QtWidgets.QSpinBox()
            spin_max.setRange(1, 100)
            spin_max.setValue(100)

            date_edit = QtWidgets.QDateEdit()
            date_edit.setCalendarPopup(True)
            date_edit.setDate(QtCore.QDate.currentDate())
            date_edit.setMaximumDate(QtCore.QDate.currentDate())

            line_desc = QtWidgets.QLineEdit()

            for w in [spin_mark, spin_max, date_edit, line_desc]:
                self._font(w, 12)

            layout.addWidget(QtWidgets.QLabel("Оценка:"))
            layout.addWidget(spin_mark)
            layout.addWidget(QtWidgets.QLabel("Максимальный балл:"))
            layout.addWidget(spin_max)
            layout.addWidget(QtWidgets.QLabel("Дата получения:"))
            layout.addWidget(date_edit)
            layout.addWidget(QtWidgets.QLabel("Описание:"))
            layout.addWidget(line_desc)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)

            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                new_id = get_new_id("Оценки", "Номер_записи")

                selected_date = date_edit.date().toString("yyyy-MM-dd")

                data = {
                    "Номер_записи": new_id,
                    "UserId": self.observed_marks_user,
                    "id_курса": self.observed_course_id,
                    "Оценка": spin_mark.value(),
                    "Максимальный_балл": spin_max.value(),
                    "Дата": selected_date,
                    "Описание": line_desc.text().strip() or "Без описания"
                }

                insert_row("Оценки", data)

                reload_table(
                    table_widget=self.table_of_marks,
                    query="""SELECT Номер_записи, Оценка, Максимальный_балл, Дата, Описание
                             FROM `Оценки`
                             WHERE `UserId` = %s
                               AND `id_курса` = %s
                             ORDER BY `Дата` DESC;""",
                    columns=('Оценка', 'Максимальный балл', 'Дата', 'Описание'),
                    values=(self.observed_marks_user, self.observed_course_id)
                )
        except Exception as e:
            print(f"Ошибка добавления: {e}")
            traceback.print_exc()

    def edit_mark(self):
        try:
            selected_row = self.table_of_marks.currentRow()
            if selected_row == -1:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите оценку для редактирования!")
                return

            item_mark = self.table_of_marks.item(selected_row, 0)
            mark_id = item_mark.data(QtCore.Qt.ItemDataRole.UserRole)

            current_value = item_mark.text()
            current_desc = self.table_of_marks.item(selected_row, 3).text()

            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle("Редактирование оценки")
            dialog.setFixedSize(350, 200)
            layout = QtWidgets.QVBoxLayout(dialog)

            spin_mark = QtWidgets.QSpinBox()
            spin_mark.setRange(0, 100)
            spin_mark.setValue(int(current_value))

            line_desc = QtWidgets.QLineEdit()
            line_desc.setText(current_desc)

            self._font(spin_mark, 12)
            self._font(line_desc, 12)

            layout.addWidget(QtWidgets.QLabel("Оценка:"))
            layout.addWidget(spin_mark)
            layout.addWidget(QtWidgets.QLabel("Описание:"))
            layout.addWidget(line_desc)

            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.StandardButton.Ok |
                QtWidgets.QDialogButtonBox.StandardButton.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
                new_mark = spin_mark.value()
                new_desc = line_desc.text().strip()

                updated_values = {
                    "Оценка": new_mark,
                    "Описание": new_desc
                }

                update_row(
                    table="Оценки",
                    record_id=mark_id,
                    values=updated_values,
                    primary_key="Номер_записи"
                )

                item_mark.setText(str(new_mark))
                self.table_of_marks.item(selected_row, 3).setText(new_desc)

                QtWidgets.QMessageBox.information(None, "Успех", "Оценка успешно обновлена!")

        except Exception as e:
            print(f"Ошибка в edit_mark: {e}")
            traceback.print_exc()

    def delete_mark(self):
        try:
            selected_row = self.table_of_marks.currentRow()
            if selected_row == -1:
                QtWidgets.QMessageBox.warning(None, "Ошибка", "Выберите строку!")
                return

            mark_id = self.table_of_marks.item(selected_row, 0).data(QtCore.Qt.ItemDataRole.UserRole)

            if QtWidgets.QMessageBox.question(None, "Удаление",
                                              "Удалить оценку?") == QtWidgets.QMessageBox.StandardButton.Yes:
                delete_row("Оценки", mark_id, "Номер_записи")
                self.table_of_marks.removeRow(selected_row)
                reload_table(table_widget=self.table_of_marks,
                             query="SELECT Номер_записи, Оценка, Максимальный_балл, Дата, Описание  FROM `Оценки` WHERE `UserId` = %s AND `id_курса` = %s ORDER BY `Дата` DESC;",
                             columns=('Оценка', 'Максимальный балл', 'Дата', 'Описание'),
                             values=(self.observed_marks_user, self.observed_course_id))
        except Exception as e:
            print(f"Ошибка удаления: {e}")

    def download_file(self):
        try:
            user_id = self.observed_user_id
            result = fetch_one(table_name='Преподаватели', column='UserId', value=user_id)

            if result:
                file_blob = result[5]
                default_name = result[1]
                file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
                    None, "Сохранить файл", default_name, "Документы (*.txt)"
                )

                if file_path:
                    with open(file_path, 'wb') as file:
                        file.write(file_blob)
                    QtWidgets.QMessageBox.information(None, "Успех", "Файл успешно сохранен!")
            else:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Файл (BLOB) отсутствует для этой записи.")

        except Exception as e:
            print(f"Ошибка при скачивании: {e}")
            traceback.print_exc()

    def get_selected_pk(self, table_widget):
        current_index = table_widget.currentIndex()

        if not current_index.isValid():
            return None

        row = current_index.row()
        item = table_widget.item(row, 0)

        if item:
            return item.data(Qt.ItemDataRole.UserRole)

        return None

    def on_combo_changed(self, index):
        if index == 0:
            self.textEdit_age.hide()
            self.textEdit_description.hide()
            self.textEdit_education.hide()
            self.textEdit_education.setText("")
            self.addFile_education.setEnabled(False)
            self.reg_education_name = None
            self.addFile_education.hide()
            self.label_age.hide()
            self.label_description.hide()
            self.label_education.hide()
        if index == 1:
            self.textEdit_age.show()
            self.textEdit_description.hide()
            self.textEdit_education.hide()
            self.textEdit_education.setText("")
            self.addFile_education.setEnabled(False)
            self.reg_education_name = None
            self.addFile_education.hide()
            self.label_age.show()
            self.label_description.hide()
            self.label_education.hide()
        if index == 2:
            self.textEdit_age.hide()
            self.textEdit_description.show()
            self.textEdit_education.hide()
            self.addFile_education.setEnabled(True)
            self.addFile_education.show()
            self.label_age.hide()
            self.label_description.show()
            self.label_education.show()

    def _font(self, object, size: int):
        font = QtGui.QFont()
        font.setFamily("BabyPop (Kerning sherbackoffale")
        font.setPointSize(size)
        object.setFont(font)
        return font

    def open_image(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Выбрать фотографию",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp)"
        )

        if file_name:
            return file_name
        else:
            return None

    def open_file(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Выбрать файл",
            "",
            "Документы PDF (*.pdf)"
        )

        if file_name:
            self.textEdit_education.show()
            self.addFile_education.setStyleSheet("""
                QPushButton {
                background-color: transparent;
                border: none;
                color: transparent;
            }
            """)
            self.textEdit_education.setText(file_name)
            self.reg_education_name = file_name

    def open_file_edit(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Выбрать файл",
            "",
            "Документы PDF (*.pdf)"
        )

        if file_name:
            self.textEdit_education_edit.show()
            self.addFile_education_edit.setStyleSheet("""
                QPushButton {
                background-color: transparent;
                border: none;
                color: transparent;
            }
            """)
            self.textEdit_education_edit.setText(file_name)
            self.edit_education_name = file_name

    def set_name_image(self, label, btn):
        try:
            file_path = self.open_image()
            if not file_path:
                return
            pixmap = QtGui.QPixmap(file_path)
            if pixmap.isNull():
                raise ValueError("Invalid image file")
            scaled_pixmap = pixmap.scaled(
                label.width(),
                label.height(),
                QtCore.Qt.AspectRatioMode.KeepAspectRatio,
                QtCore.Qt.TransformationMode.SmoothTransformation
            )
            label.setPixmap(scaled_pixmap)
            btn.setStyleSheet("""
                QPushButton {
                background-color: transparent;
                border: none;
                color: transparent;
            }
            """)
            label.show()
            self.add_image_name = file_path
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Ошибка", f"Не удалось загрузить изображение:\n{e}")
            traceback.print_exc()

    def switch_forms(self, first=None, second=None):
        try:
            if first is None:
                if hasattr(self, "_current_frame") and self._current_frame:
                    self._current_frame.hide()
                    second.show()
                return
            if second is None:
                if hasattr(self, "_previous_frame") and self._previous_frame:
                    first.hide()
                    self._previous_frame.show()
                return
            self._previous_frame = first
            self._current_frame = second
            first.hide()
            second.show()

        except Exception:
            traceback.print_exc()

    def open_notification(self, table):
        try:
            notification_id = self.get_selected_pk(table)

            if notification_id is None:
                QtWidgets.QMessageBox.warning(None, "Внимание", "Выберите уведомление для чтения!")
                return
            query = "SELECT Тема, Дата, Содержание FROM Уведомления WHERE Номер_записи = %s"
            result = fetch_all(query, (notification_id,))

            if not result:
                QtWidgets.QMessageBox.error(None, "Ошибка", "Не удалось найти данные уведомления в базе.")
                return

            topic, date_sent, content = result[0]

            dialog = QtWidgets.QDialog()
            dialog.setWindowTitle(f"Просмотр уведомления")
            dialog.setFixedSize(450, 350)
            layout = QtWidgets.QVBoxLayout(dialog)

            header_label = QtWidgets.QLabel(f"<b>Тема:</b> {topic}<br><b>Дата:</b> {date_sent}")
            self._font(header_label, 12)

            content_area = QtWidgets.QTextEdit()
            content_area.setPlainText(content)
            content_area.setReadOnly(True)
            self._font(content_area, 12)

            btn_close = QtWidgets.QPushButton("Ок")
            btn_close.clicked.connect(dialog.accept)
            self._font(btn_close, 12)

            layout.addWidget(header_label)
            layout.addWidget(content_area)
            layout.addWidget(btn_close)

            update_row(
                table="Уведомления",
                record_id=notification_id,
                values={"Прочитано": 1},
                primary_key="Номер_записи"
            )

            reload_table(self.unchecked_notification_list,
                         "SELECT Номер_записи, Тема, Дата FROM `Уведомления` WHERE `UserId` = %s AND `Прочитано` = 0 ORDER BY `Дата` DESC;",
                         ("Тема", "Дата"), (self.current_user_id,))
            reload_table(self.checked_notification_list,
                         "SELECT Номер_записи, Тема, Дата FROM `Уведомления` WHERE `UserId` = %s AND `Прочитано` = 1 ORDER BY `Дата` DESC;",
                         ("Тема", "Дата"), (self.current_user_id,))

            self.check_unread_notifications()
            dialog.exec()

        except Exception as e:
            print(f"Ошибка при открытии уведомления: {e}")
            traceback.print_exc()

    def enter(self):
        try:
            if self.current_role_id != 1:
                self.tabWidget_main.addTab(self.tab_account, "")
                self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_account), "Личный кабинет")

            self.tabWidget_main.addTab(self.tab_course, "")
            self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_course), "Курсы")

            match self.current_role_id:
                case 1:
                    self.tabWidget_main.addTab(self.tab_users, "")
                    self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_users), "Пользователи")

                    self.tabWidget_main.addTab(self.tab_language, "")
                    self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_language), "Языки")

                    self.pushButtonJoin.setVisible(False)
                    self.pushButtonObserve.setGeometry(860, 70, 291, 61)
                    self.pushButtonDeleteCourse.setGeometry(860, 160, 291, 61)
                case 2:
                    self.tabWidget_main.addTab(self.tab_my_course, "")
                    self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_my_course), "Мои курсы")
                    self.pushButtonJoin.setVisible(True)
                    self.pushButtonObserve.setGeometry(860, 160, 291, 61)
                    self.pushButtonDeleteCourse.setGeometry(860, 240, 291, 61)
                    self.label_age_profile_output.hide()
                    self.output_age_profile.hide()
                case 3:
                    self.tabWidget_main.addTab(self.tab_my_course, "")
                    self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_my_course), "Мои курсы")

                    self.tabWidget_main.addTab(self.tab_my_marks, "")
                    self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_my_marks),
                                                   "Личная успеваемость")
                    self.pushButtonJoin.setVisible(True)
                    self.pushButtonObserve.setGeometry(860, 160, 291, 61)
                    self.pushButtonDeleteCourse.setGeometry(860, 240, 291, 61)
                    self.label_age_profile_output.show()
                    self.output_age_profile.show()

            self.tabWidget_main.addTab(self.tab_notification, "")
            self.tabWidget_main.setTabText(self.tabWidget_main.indexOf(self.tab_notification), "Уведомления")

            self.tabWidget_main.setStyleSheet("""
                                                         QTabBar::tab {
                                                                width: """ + str(1200 / self.tabWidget_main.count()) + """; 
                                                                height: 50;
                                                                background: rgb(85, 0, 0);
                                                                color: white;
                                                         }
                                                         QTabBar::tab:selected {
                                                             background: rgb(65, 0, 0);
                                                             border-bottom-color: #202020;
                                                         }""")
            if self.current_role_id != 1:
                role = "Преподаватели" if self.current_role_id == 2 else "Студенты"
                reload_image(image_widget=self.avatar, table_name=role, column="Фото", primary_key="UserId",
                             key_value=self.current_user_id)

                reload_line(line_widget=self.output_login_profile, table_name="Пользователи", column="Логин",
                            primary_key="UserId", key_value=self.current_user_id)

                reload_line(line_widget=self.output_roles_profile, table_name="Роли", column="Название",
                            primary_key="id_роли", key_value=self.current_role_id)

                current_country_id = fetch_cell(role, 'Страна', self.current_user_id, 'UserId')

                reload_line(line_widget=self.output_country_profile, table_name='Страны', column="Название", primary_key="id_страны",
                             key_value=current_country_id)
                if self.current_role_id == 3:
                    reload_line(line_widget=self.output_age_profile, table_name="Студенты", column="Возраст", primary_key="UserId", key_value=self.current_user_id)
                    self.pushButtonAdd.hide()
                    self.pushButtonExclude.setGeometry(860, 160, 291, 61)
                surname = fetch_cell(table_name=role, column="Фамилия", primary_key="UserId",
                                     value=self.current_user_id)
                name = fetch_cell(table_name=role, column="Имя", primary_key="UserId", value=self.current_user_id)
                patronim = fetch_cell(table_name=role, column="Отчество", primary_key="UserId",
                                      value=self.current_user_id)
                value = (surname + ' ' + name + ' ' + patronim) if patronim else (surname + ' ' + name)
                self.output_name_profile.clear()
                self.output_name_profile.setText(value)
            self.switch_forms(second=self.frame_main)
            self.check_unread_notifications()
        except Exception as e:
            traceback.print_exc()
            print(e)

    def main_tables(self):
        reload_table(self.table_of_courses,
                     "SELECT Курсы.id_курса, Курсы.Название AS Название_курса, Языки.Название AS Название_языка FROM Курсы JOIN Языки ON Курсы.id_языка = Языки.id_языка",
                     ("Название", "Язык"))
        reload_table(self.unchecked_notification_list,
                     "SELECT Номер_записи, Тема, Дата FROM `Уведомления` WHERE `UserId` = %s AND `Прочитано` = 0 ORDER BY `Дата` DESC;",
                     ("Тема", "Дата"), (self.current_user_id, ))
        reload_table(self.checked_notification_list,
                     "SELECT Номер_записи, Тема, Дата FROM `Уведомления` WHERE `UserId` = %s AND `Прочитано` = 1 ORDER BY `Дата` DESC;",
                     ("Тема", "Дата"), (self.current_user_id,))
        if self.current_role_id == 1:
            reload_table(self.table_of_language,
                        "SELECT id_языка, Название FROM Языки", ("Название", ))
            self.users_tables()
        if self.current_role_id == 3:
            reload_table(self.table_of_my_courses,
                     "SELECT Курсы.id_курса, Курсы.Название AS Название_курса, Языки.Название AS Название_языка FROM Курсы JOIN Языки ON Курсы.id_языка = Языки.id_языка JOIN Студенты_На_Курсах ON Курсы.id_курса = Студенты_На_Курсах.id_курса WHERE Студенты_На_Курсах.UserId = %s;",
                     ("Название", "Язык"), values=(self.current_user_id,))
            self.load_profile_marks()
        elif self.current_role_id == 2:
            reload_table(self.table_of_my_courses,
                         "SELECT Курсы.id_курса, Курсы.Название AS Название_курса, Языки.Название AS Название_языка FROM Курсы JOIN Языки ON Курсы.id_языка = Языки.id_языка JOIN Преподаватели_на_курсах ON Курсы.id_курса = Преподаватели_на_курсах.id_курса WHERE Преподаватели_на_курсах.UserId = %s;",
                         ("Название", "Язык"), values=(self.current_user_id,))
            reload_table(self.table_of_profile,
                         "SELECT Курсы.id_курса, Курсы.Название AS Название_курса, Языки.Название AS Название_языка FROM Курсы JOIN Языки ON Курсы.id_языка = Языки.id_языка JOIN Преподаватели_на_курсах ON Курсы.id_курса = Преподаватели_на_курсах.id_курса WHERE Преподаватели_на_курсах.UserId = %s;",
                         ("Название", "Язык"), values=(self.current_user_id,))
        self.check_unread_notifications()

    def exit_profile(self):
        self.tabWidget_main.clear()
        self.current_user_id = None
        self.current_role_id = None
        self.current_login = None
        self.switch_forms(self.frame_main, self.frame_authorization)

    def add_user(self):
        if self.add_image_name:
            with open(self.add_image_name, 'rb') as f:
                image_blob = f.read()
        else:
            with open("image/i.jpg", 'rb') as f:
                image_blob = f.read()
        self.add_image_name = None
        if self.reg_education_name:
            with open(self.reg_education_name, 'rb') as g:
                file_blob = g.read()
        else:
            file_blob = None
        self.reg_education_name = None
        characters = string.ascii_letters + string.digits

        self.current_user_id = ''.join(choice(characters) for i in range(5))
        self.current_role_id = 2 if (self.comboBox_roles.currentText() == 'Преподаватель') else 3
        self.current_login = self.textEdit_login_reg.text()

        user_data = {
            "UserId": self.current_user_id,
            "Логин": self.current_login,
            "id_роли": self.current_role_id,
            "Пароль": self.textEdit_password_reg.text().strip()
        }
        insert_row('Пользователи', user_data)
        if self.current_role_id == 3:
            student_data = {
            "UserId": self.current_user_id,
            "Фамилия": self.textEdit_surname.text(),
            "Имя": self.textEdit_name.text(),
            "Отчество": self.textEdit_patronum.text(),
            "Страна": self.comboBox_country.currentIndex()-1,
            "Возраст": int(self.textEdit_age.text()),
            "Фото": image_blob
            }
            insert_row("Студенты", student_data)
        elif self.current_role_id == 2:
            teacher_data = {
            "UserId": self.current_user_id,
            "Фамилия": self.textEdit_surname.text(),
            "Имя": self.textEdit_name.text(),
            "Отчество": self.textEdit_patronum.text(),
            "Страна": self.comboBox_country.currentIndex()-1,
            "Образование": file_blob,
            "Описание": self.textEdit_description.toPlainText(),
            "Фото": image_blob
            }
            insert_row("Преподаватели", teacher_data)

    def to_edit_form(self):
        try:
            if self.current_role_id == 3:
                self.textEdit_age_edit.show()
                self.textEdit_description_edit.hide()
                self.textEdit_education_edit.hide()
                self.textEdit_education_edit.setText("")
                self.edit_education_name = None
                self.label_age_edit.show()
                self.label_description_edit.hide()
                self.label_education_edit.hide()
            if self.current_role_id == 2:
                self.textEdit_age_edit.hide()
                self.textEdit_description_edit.show()
                self.textEdit_education_edit.hide()
                self.label_age_edit.hide()
                self.edit_education_name = None
                self.addFile_education_edit.show()
                self.label_description.show()
                self.label_education_edit.show()

            if self.current_role_id != 1:
                self.add_image_edit.setStyleSheet("""
                                QPushButton {
                                background-color: transparent;
                                border: none;
                                color: transparent;
                            }
                            """)
                role = "Преподаватели" if self.current_role_id == 2 else "Студенты"
                reload_image(image_widget=self.avatar_editing, table_name=role, column="Фото", primary_key="UserId",
                             key_value=self.current_user_id)

                reload_line(line_widget=self.textEdit_login_edit, table_name="Пользователи", column="Логин",
                            primary_key="UserId", key_value=self.current_user_id)

                reload_line(line_widget=self.textEdit_password_edit, table_name="Пользователи", column="Пароль",
                            primary_key="UserId", key_value=self.current_user_id)

                reload_line(line_widget=self.textEdit_surname_edit, table_name=role, column="Фамилия",
                            primary_key="UserId", key_value=self.current_user_id)

                reload_line(line_widget=self.textEdit_name_edit, table_name=role, column="Имя",
                            primary_key="UserId", key_value=self.current_user_id)

                reload_line(line_widget=self.textEdit_patronum_edit, table_name=role, column="Отчество",
                            primary_key="UserId", key_value=self.current_user_id)

                self.comboBox_country_edit.clear()
                self.comboBox_country_edit.addItems([i[0] for i in fetch_all('SELECT Название from Страны')])
                self.comboBox_country_edit.setCurrentIndex(int(fetch_cell(role, 'Страна', self.current_user_id, "UserId")))
                if self.current_role_id == 3:
                    reload_line(line_widget=self.textEdit_age_edit, table_name="Студенты", column="Возраст",
                                primary_key="UserId", key_value=self.current_user_id)
                if self.current_role_id == 2:
                    reload_line(line_widget=self.textEdit_description_edit, table_name="Преподаватели", column="Описание",
                                primary_key="UserId", key_value=self.current_user_id)
            self.switch_forms(self.frame_main, self.frame_editing)
        except Exception as e:
            print(e)
            traceback.print_exc()

    def edit_user(self):
        try:
            if self.add_image_name:
                with open(self.add_image_name, 'rb') as f:
                    image_blob = f.read()
            else:
                image_blob = fetch_cell(table_name=("Преподаватели" if self.current_role_id == 2 else "Студенты"),
                                        column="Фото", value=self.current_user_id, primary_key="UserId")
            if self.edit_education_name:
                with open(self.edit_education_name, 'rb') as g:
                    file_blob = g.read()
            elif self.current_role_id == 2:
                file_blob = fetch_cell(table_name="Преподаватели", column="Образование", value=self.current_user_id,
                                       primary_key="UserId")
            user_data = {
                "Логин": self.textEdit_login_edit.text(),
                "Пароль": self.textEdit_password_edit.text()
            }
            update_row('Пользователи', self.current_user_id, user_data, 'UserId')
            if self.current_role_id == 3:
                student_data = {
                    "Фамилия": self.textEdit_surname_edit.text(),
                    "Имя": self.textEdit_name_edit.text(),
                    "Отчество": self.textEdit_patronum_edit.text(),
                    "Страна": self.comboBox_country_edit.currentIndex(),
                    "Возраст": int(self.textEdit_age_edit.text()),
                    "Фото": image_blob
                }
                update_row("Студенты", self.current_user_id, student_data, 'UserId')
            elif self.current_role_id == 2:
                teacher_data = {
                    "Фамилия": self.textEdit_surname_edit.text(),
                    "Имя": self.textEdit_name_edit.text(),
                    "Отчество": self.textEdit_patronum_edit.text(),
                    "Страна": self.comboBox_country_edit.currentIndex(),
                    "Описание": self.textEdit_description_edit.toPlainText(),
                    "Образование": file_blob,
                    "Фото": image_blob
                }
                update_row("Преподаватели", self.current_user_id, teacher_data, 'UserId')

            if self.current_role_id != 1:
                role = "Преподаватели" if self.current_role_id == 2 else "Студенты"
                reload_image(image_widget=self.avatar, table_name=role, column="Фото", primary_key="UserId",
                             key_value=self.current_user_id)

                reload_line(line_widget=self.output_login_profile, table_name="Пользователи", column="Логин",
                            primary_key="UserId", key_value=self.current_user_id)

                reload_line(line_widget=self.output_roles_profile, table_name="Роли", column="Название",
                            primary_key="id_роли", key_value=self.current_role_id)

                current_country_id = fetch_cell(role, 'Страна', self.current_user_id, 'UserId')

                reload_line(line_widget=self.output_country_profile, table_name='Страны', column="Название",
                            primary_key="id_страны",
                            key_value=current_country_id)
                if self.current_role_id == 3:
                    reload_line(line_widget=self.output_age_profile, table_name="Студенты", column="Возраст",
                                primary_key="UserId", key_value=self.current_user_id)
                surname = fetch_cell(table_name=role, column="Фамилия", primary_key="UserId",
                                     value=self.current_user_id)
                name = fetch_cell(table_name=role, column="Имя", primary_key="UserId", value=self.current_user_id)
                patronim = fetch_cell(table_name=role, column="Отчество", primary_key="UserId",
                                      value=self.current_user_id)
                value = (surname + ' ' + name + ' ' + patronim) if patronim else (surname + ' ' + name)
                self.output_name_profile.clear()
                self.output_name_profile.setText(value)
            role = "Контакты_студентов" if self.current_role_id == 3 else "Контакты_преподавателей"
            reload_table(table_widget=self.table_of_contacts_editing, query=f'SELECT ku.id_записи, tk.Название AS Тип, ku.Значение FROM {role} ku JOIN Типы_контактов tk ON ku.id_типа_контакта = tk.id_типа_контакта WHERE ku.UserId = %s;', values=(self.current_user_id, ))
            if self.current_role_id == 2:
                reload_table(self.table_of_language_editing, 'SELECT yp.id_записи, y.Название AS Язык, u.Название AS Уровень FROM Языки_преподавателей yp JOIN Языки y ON yp.id_языка = y.id_языка JOIN Уровни u ON yp.id_уровня = u.id_уровня WHERE yp.UserId = %s;', values=(self.current_user_id, ))
            else:
                self.table_of_language_editing.hide()
                self.label_language_editing.hide()
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    def add_course(self):
        try:
            course_id = get_new_id("Курсы", "id_курса")
            language = fetch_all('select id_языка from Языки where Название = %s', self.comboBox_language.currentText())[0][0]
            course_data = {
                "id_курса": course_id,
                "Название": self.textEdit_course_name_creation.text(),
                "id_языка": language,
                "Описание": self.textEdit_course_description_creation.toPlainText(),
                "UserId": self.current_user_id,
            }
            insert_row('Курсы', course_data)

            teacher_on_course_data = {
                "id_курса": course_id,
                "UserId": self.current_user_id
            }
            insert_row('Преподаватели_на_курсах', teacher_on_course_data)

            self.main_tables()

            self.switch_forms(self.frame_course_creation, self.frame_main),
            self.tabWidget_main.setCurrentIndex(self.tabWidget_main.indexOf(self.tab_my_course))
        except Exception as e:
            print(e)
            traceback.print_exc()

    def authorize_user(self):
        try:
            login_input = self.textEdit_login_auth.text().strip()
            password_input = self.textEdit_password_auth.text().strip()

            if not login_input or not password_input:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Ошибка",
                    "Введите логин и пароль"
                )
                return
            result = fetch_one("Пользователи", "Логин", login_input)

            if not result:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Ошибка",
                    "Пользователь не найден"
                )
                return
            user_id, login, role_id, db_password, banned = result
            if banned:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Ошибка",
                    "Пользователь заблокирован"
                )
                return
            if password_input != db_password:
                QtWidgets.QMessageBox.warning(
                    None,
                    "Ошибка",
                    "Неверный пароль"
                )
                return
            self.current_user_id = user_id
            self.current_role_id = role_id
            self.current_login = login
            self.enter()
        except Exception as e:
            traceback.print_exc()
            print(e)

    def delete_profile(self):

        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setText("Вы уверены, что хотите удалить профиль?")
        msg.setInformativeText("Это действие необратимо. Все ваши данные, курсы и прогресс будут удалены.")
        msg.setWindowTitle("Подтверждение удаления")
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)

        answer = msg.exec()

        if answer == QtWidgets.QMessageBox.StandardButton.Yes:
            if self.current_role_id == 3:
                delete_row('Студенты', self.current_user_id, 'UserId')
            elif self.current_role_id == 2:
                delete_row('Преподаватели', self.current_user_id, 'UserId')
            delete_row('Пользователи', self.current_user_id, 'UserId')

            self.exit_profile()

            QtWidgets.QMessageBox.information(None, "Успех", "Ваш профиль был успешно удален.")

    def users_tables(self):
        try:
            reload_table(self.table_of_students,
                         "SELECT Студенты.UserId AS UserId, CONCAT(Студенты.Фамилия, ' ', Студенты.Имя, ' ', Студенты.Отчество) AS ФИО, Страны.Название FROM Студенты JOIN Пользователи ON Студенты.UserId = Пользователи.UserId JOIN Страны ON Студенты.Страна = Страны.id_страны WHERE Пользователи.Заблокированный = %s;",
                         ("UserId", "ФИО", "Страна"), values=('0',), show_pk=True)
            reload_table(self.table_of_teachers,
                         "SELECT Преподаватели.UserId AS UserId, CONCAT(Преподаватели.Фамилия, ' ', Преподаватели.Имя, ' ', Преподаватели.Отчество) AS ФИО, Страны.Название FROM Преподаватели JOIN Пользователи ON Преподаватели.UserId = Пользователи.UserId JOIN Страны ON Преподаватели.Страна = Страны.id_страны WHERE Пользователи.Заблокированный = %s;",
                         ("UserId", "ФИО", "Страна"), values=('0',), show_pk=True)
            reload_table(self.table_of_banned,
                         "SELECT p.UserId, CONCAT(s.Фамилия, ' ', s.Имя, IFNULL(CONCAT(' ', s.Отчество), '')) AS ФИО, 'Студент' AS Роль FROM Пользователи p INNER JOIN Студенты s ON p.UserId = s.UserId WHERE p.Заблокированный = TRUE UNION ALL SELECT  p.UserId, CONCAT(t.Фамилия, ' ', t.Имя, IFNULL(CONCAT(' ', t.Отчество), '')) AS ФИО, 'Преподаватель' AS Роль FROM Пользователи p INNER JOIN Преподаватели t ON p.UserId = t.UserId WHERE p.Заблокированный = TRUE;",
                         ("UserId", "ФИО", "Роль"), show_pk=True)
            match self.users_tabs.currentIndex():
                case 0:
                    self.pushButtonBan.setText("Заблокировать")
                    try:
                        self.pushButtonBan.clicked.disconnect()
                    finally:
                        self.pushButtonBan.clicked.connect(lambda: self.ban_selected_user(self.table_of_students))
                    try:
                        self.pushButtonOpenProfile.clicked.disconnect()
                    finally:
                        self.pushButtonOpenProfile.clicked.connect(lambda: self.open_profile(self.table_of_students, self.frame_main))
                    self.pushButtonDeleteUser.hide()
                case 1:
                    self.pushButtonBan.setText("Заблокировать")
                    try:
                        self.pushButtonBan.clicked.disconnect()
                    finally:
                        self.pushButtonBan.clicked.connect(lambda: self.ban_selected_user(self.table_of_teachers))
                    try:
                        self.pushButtonOpenProfile.clicked.disconnect()
                    finally:
                        self.pushButtonOpenProfile.clicked.connect(lambda: self.open_profile(self.table_of_teachers, self.frame_main))
                    self.pushButtonDeleteUser.hide()
                case 2:
                    self.pushButtonBan.setText("Разблокировать")
                    try:
                        self.pushButtonBan.clicked.disconnect()
                    finally:
                        self.pushButtonBan.clicked.connect(lambda: self.unban_selected_user())
                    try:
                        self.pushButtonOpenProfile.clicked.disconnect()
                    finally:
                        self.pushButtonOpenProfile.clicked.connect(lambda: self.open_profile(self.table_of_banned, self.frame_main))
                    self.pushButtonDeleteUser.show()
        except Exception as e:
            print(e)
            traceback.print_exc()

    def generate_marks_report(self):
        try:
            date_start = self.dateEdit_from.date().toString("yyyy-MM-dd")
            date_end = self.dateEdit_to.date().toString("yyyy-MM-dd")
            user_id = self.current_user_id

            if date_start > date_end:
                QtWidgets.QMessageBox.warning(None, "Ошибка", "Дата начала не может быть позже даты окончания.")
                return

            columns_query = """
                            SELECT Дата, row_num \
                            FROM (SELECT Дата, \
                                         ROW_NUMBER() OVER(PARTITION BY id_курса, Дата ORDER BY Номер_записи) as row_num \
                                  FROM Оценки \
                                  WHERE UserId = %s \
                                    AND Дата BETWEEN %s AND %s) as t
                            GROUP BY Дата, row_num
                            ORDER BY Дата, row_num \
                            """
            columns_result = fetch_all(columns_query, (user_id, date_start, date_end))

            if not columns_result:
                QtWidgets.QMessageBox.information(None, "Инфо", "Оценок нет.")
                self.report_of_my_marks.setRowCount(0)
                return

            headers_dates = []
            dynamic_columns = []

            for row in columns_result:
                d_str = str(row[0])
                r_num = row[1]

                headers_dates.append(d_str)

                dynamic_columns.append(
                    f"MAX(CASE WHEN m.Дата = '{d_str}' AND m.rn = {r_num} THEN m.Оценка END)"
                )
                dynamic_columns.append(
                    f"MAX(CASE WHEN m.Дата = '{d_str}' AND m.rn = {r_num} THEN m.Номер_записи END)"
                )

            columns_sql_part = ",\n".join(dynamic_columns)

            final_query = f"""
                SELECT 
                    id_курса,
                    Название,
                    {columns_sql_part},
                    ROUND(AVG((Оценка / Максимальный_балл) * 100), 2)
                FROM (
                    SELECT 
                        c.id_курса, c.Название, m.Оценка, m.Номер_записи, m.Дата, m.Максимальный_балл,
                        ROW_NUMBER() OVER(PARTITION BY m.id_курса, m.Дата ORDER BY m.Номер_записи) as rn
                    FROM Курсы c
                    JOIN Оценки m ON c.id_курса = m.id_курса
                    WHERE m.UserId = %s AND m.Дата BETWEEN %s AND %s
                ) as m
                GROUP BY id_курса, Название
                ORDER BY Название;
            """

            rows = fetch_all(final_query, (user_id, date_start, date_end))

            headers_text = ["Курс"] + headers_dates + ["Ср. %"]
            self.report_of_my_marks.clear()
            self.report_of_my_marks.setColumnCount(len(headers_text))
            self.report_of_my_marks.setHorizontalHeaderLabels(headers_text)
            self.report_of_my_marks.setRowCount(len(rows) if rows else 0)
            for row_idx, row_data in enumerate(rows):
                item_name = QtWidgets.QTableWidgetItem(str(row_data[1]))
                item_name.setFlags(item_name.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self._font(item_name, 18)
                item_name.setData(QtCore.Qt.ItemDataRole.UserRole, row_data[0])
                self.report_of_my_marks.setItem(row_idx, 0, item_name)

                dynamic_data = row_data[2:-1]
                col_idx = 1
                for i in range(0, len(dynamic_data), 2):
                    val = dynamic_data[i]
                    pk = dynamic_data[i + 1]

                    txt = str(val) if val is not None else "-"
                    item = QtWidgets.QTableWidgetItem(txt)
                    if val is not None:
                        item.setData(QtCore.Qt.ItemDataRole.UserRole, pk)

                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self._font(item, 18)
                    item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                    self.report_of_my_marks.setItem(row_idx, col_idx, item)
                    col_idx += 1

                avg_val = row_data[-1]
                item_avg = QtWidgets.QTableWidgetItem(str(avg_val) if avg_val is not None else "")
                item_avg.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self._font(item_avg, 18)
                self.report_of_my_marks.setItem(row_idx, col_idx, item_avg)

            self.report_of_my_marks.resizeColumnsToContents()


        except Exception as e:
            print(f"Ошибка: {e}")
            traceback.print_exc()

    def load_profile_marks(self):
        try:
            import datetime
            import traceback

            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=7)
            user_id = self.current_user_id

            columns_query = """
                            SELECT Дата, row_num \
                            FROM (SELECT Дата, \
                                         ROW_NUMBER() OVER(PARTITION BY id_курса, Дата ORDER BY Номер_записи) as row_num \
                                  FROM Оценки \
                                  WHERE UserId = %s \
                                    AND Дата BETWEEN %s AND %s) as t
                            GROUP BY Дата, row_num
                            ORDER BY Дата, row_num \
                            """
            columns_result = fetch_all(columns_query, (user_id, start_date, end_date))

            if not columns_result:
                self.table_of_profile.clear()
                self.table_of_profile.setRowCount(0)
                self.table_of_profile.setColumnCount(0)
                return

            headers_dates = []
            dynamic_columns = []
            for row in columns_result:
                d_str = str(row[0])
                r_num = row[1]

                headers_dates.append(d_str)

                dynamic_columns.append(
                    f"MAX(CASE WHEN m.Дата = '{d_str}' AND m.rn = {r_num} THEN m.Оценка END)"
                )

            columns_sql = ",\n".join(dynamic_columns)

            query = f"""
                SELECT 
                    id_курса,
                    Название,
                    {columns_sql}
                FROM (
                    SELECT 
                        c.id_курса, c.Название, m.Оценка, m.Дата,
                        ROW_NUMBER() OVER(PARTITION BY m.id_курса, m.Дата ORDER BY m.Номер_записи) as rn
                    FROM Курсы c
                    JOIN Оценки m ON c.id_курса = m.id_курса
                    WHERE m.UserId = %s AND m.Дата BETWEEN %s AND %s
                ) as m
                GROUP BY id_курса, Название
                ORDER BY Название;
            """

            rows = fetch_all(query, (user_id, start_date, end_date))

            headers = ["Курс"] + headers_dates
            self.table_of_profile.clear()
            self.table_of_profile.setColumnCount(len(headers))
            self.table_of_profile.setHorizontalHeaderLabels(headers)
            self.table_of_profile.setRowCount(len(rows) if rows else 0)

            if rows:
                for row_idx, row_data in enumerate(rows):
                    item_name = QtWidgets.QTableWidgetItem(str(row_data[1]))
                    item_name.setFlags(item_name.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                    self._font(item_name, 10)
                    self.table_of_profile.setItem(row_idx, 0, item_name)

                    dynamic_data = row_data[2:]
                    for col_idx, value in enumerate(dynamic_data, start=1):
                        display_value = str(value) if value is not None else "-"
                        item = QtWidgets.QTableWidgetItem(display_value)

                        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
                        self._font(item, 10)

                        self.table_of_profile.setItem(row_idx, col_idx, item)

            self.table_of_profile.resizeColumnsToContents()

        except Exception as e:
            print(f"Ошибка динамической таблицы профиля: {e}")
            traceback.print_exc()

    # ==============================
    # Main setup
    # ==============================
    def setupUi(self, MainWindow):

        self.add_image_name = None
        self.reg_education_name = None
        self.observed_user_id = None

        self._setup_main_window(MainWindow)
        self._setup_central_widget(MainWindow)
        self._setup_authorization_frame()
        self._setup_course_creation_frame()
        self._setup_editing_frame()
        self._setup_main_frame()
        self._setup_view_profile_frame()
        self._setup_marks_frame()
        self._setup_course_frame()
        self._setup_registration_frame()
        self._setup_language_frame()
        self._setup_language_contacts_frame()
        self._setup_language_contacts_editing_frame()

        self._current_frame = self.frame_authorization

        MainWindow.setCentralWidget(self.centralwidget)
        self.tabWidget_main.setCurrentIndex(0)

        self.notification_timer = QtCore.QTimer()
        self.notification_timer.timeout.connect(self.check_upcoming_lessons)
        self.notification_timer.start(60000)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ==============================
    # Window & central widget
    # ==============================
    def _setup_main_window(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("Информационная система для записи на курсы иностранных языков")
        MainWindow.resize(1200, 750)
        MainWindow.setMinimumSize(1200, 750)
        MainWindow.setMaximumSize(1200, 750)

    def _setup_central_widget(self, MainWindow):
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

    # ==============================
    # Authorization screen
    # ==============================
    def _setup_authorization_frame(self):
        self.frame_authorization = QtWidgets.QFrame(self.centralwidget)
        self.frame_authorization.setGeometry(0, 0, 1200, 750)
        self.frame_authorization.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_authorization.setStyleSheet("background-color: #EFE6DE;")
        self.frame_authorization.setObjectName("frame_authorization")

        self._create_auth_labels()
        self._create_auth_inputs()
        self._create_auth_buttons()

    def _create_auth_labels(self):
        self.label_enter = QtWidgets.QLabel("", self.frame_authorization)
        self.label_enter.setGeometry(400, 190, 400, 130)
        self._font(self.label_enter, 100)
        self.label_enter.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_enter.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_enter.setText("ВХОД")

        self.label_login = QtWidgets.QLabel(self.frame_authorization)
        self.label_login.setGeometry(270, 380, 120, 50)
        self._font(self.label_login, 26)
        self.label_login.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_login.setText("Логин")

        self.label_password = QtWidgets.QLabel(self.frame_authorization)
        self.label_password.setGeometry(270, 480, 120, 50)
        self._font(self.label_password, 26)
        self.label_password.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_password.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_password.setText("Пароль")

    def _create_auth_inputs(self):
        self.textEdit_login_auth = QtWidgets.QLineEdit(self.frame_authorization)
        self.textEdit_login_auth.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0)")
        self._font(self.textEdit_login_auth, 20)
        self.textEdit_login_auth.setGeometry(400, 380, 400, 50)

        self.textEdit_password_auth = QtWidgets.QLineEdit(self.frame_authorization)
        self.textEdit_password_auth.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_password_auth, 20)
        self.textEdit_password_auth.setGeometry(400, 480, 400, 50)

    def _create_auth_buttons(self):
        self.pushButton_enter = QtWidgets.QPushButton(self.frame_authorization)
        self.pushButton_enter.setGeometry(489, 600, 222, 74)
        self._font(self.pushButton_enter, 36)
        self.pushButton_enter.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self.pushButton_enter.clicked.connect(self.authorize_user)
        self.pushButton_enter.setText("Войти")

        self.pushButton_registration = QtWidgets.QPushButton(self.frame_authorization)
        self.pushButton_registration.setGeometry(940, 10, 250, 50)
        self.pushButton_registration.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButton_registration, 20)
        def switch_to_registration():
            try:
                self.switch_forms(self.frame_authorization,
                                  self.frame_registration)
                self.comboBox_country.clear()
                self.comboBox_country.addItems(
                    [''] + [i[0] for i in fetch_all('SELECT Название from Страны')])
            except Exception as e:
                traceback.print_exc()
                print(e)

        self.pushButton_registration.clicked.connect(switch_to_registration)
        self.pushButton_registration.setText("Зарегистрироваться")

    # ==============================
    # Language & contacts screen
    # ==============================
    def _setup_language_contacts_frame(self):
        self.frame_language_contacts = QtWidgets.QFrame(self.centralwidget)
        self.frame_language_contacts.setGeometry(0, 0, 1200, 750)
        self.frame_language_contacts.hide()
        self.frame_language_contacts.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_language_contacts.setStyleSheet("background-color: #EFE6DE;")
        self.frame_language_contacts.setObjectName("frame_language_contacts")

        self.label_contacts_registration = QtWidgets.QLabel(self.frame_language_contacts)
        self.label_contacts_registration.setGeometry(100, 30, 170, 30)
        self._font(self.label_contacts_registration, 30)
        self.label_contacts_registration.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_contacts_registration.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_contacts_registration.setText("Контакты")

        self.table_of_contacts_registration = QtWidgets.QTableWidget(self.frame_language_contacts)
        self.table_of_contacts_registration.setGeometry(100, 75, 900, 250)
        self.table_of_contacts_registration.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header_c = self.table_of_contacts_registration.horizontalHeader()
        self.table_of_contacts_registration.verticalHeader().setVisible(False)
        self._font(header_c, 20)
        header_c.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table_of_contacts_registration.setColumnCount(2)
        self.table_of_contacts_registration.setHorizontalHeaderLabels(('Тип', 'Значение'))

        self.pushButton_add_contacts_registration = QtWidgets.QPushButton(self.frame_language_contacts)
        self.pushButton_add_contacts_registration.setGeometry(1030, 95, 50, 50)
        self.pushButton_add_contacts_registration.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(85, 0, 0);
                        border-style: solid;
                        border-width: 2px;
                        border-radius: 25px;
                        border-color: rgb(50, 50, 50);
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: rgb(120, 20, 20);
                    }
                    QPushButton:pressed {
                        background-color: rgb(65, 0, 0);
                    }
                """)
        self._font(self.pushButton_add_contacts_registration, 30)
        self.pushButton_add_contacts_registration.setText("+")
        self.pushButton_add_contacts_registration.clicked.connect(self.add_contact_at_table)

        self.pushButton_edit_contacts_registration = QtWidgets.QPushButton(self.frame_language_contacts)
        self.pushButton_edit_contacts_registration.setGeometry(1030, 165, 50, 50)
        self.pushButton_edit_contacts_registration.setStyleSheet("""
                            QPushButton {
                                background-color: rgb(85, 0, 0);
                                border-style: solid;
                                border-width: 2px;
                                border-radius: 25px;
                                border-color: rgb(50, 50, 50);
                                color: white;
                            }
                            QPushButton:hover {
                                background-color: rgb(120, 20, 20);
                            }
                            QPushButton:pressed {
                                background-color: rgb(65, 0, 0);
                            }
                        """)
        self.pushButton_edit_contacts_registration.setIcon(QtGui.QIcon("image/edit.png"))
        self.pushButton_edit_contacts_registration.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_edit_contacts_registration.clicked.connect(self.edit_contact_at_table)

        self.pushButton_delete_contacts_registration = QtWidgets.QPushButton(self.frame_language_contacts)
        self.pushButton_delete_contacts_registration.setGeometry(1030, 235, 50, 50)
        self.pushButton_delete_contacts_registration.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(85, 0, 0);
                                        border-style: solid;
                                        border-width: 2px;
                                        border-radius: 25px;
                                        border-color: rgb(50, 50, 50);
                                        color: white;
                                    }
                                    QPushButton:hover {
                                        background-color: rgb(120, 20, 20);
                                    }
                                    QPushButton:pressed {
                                        background-color: rgb(65, 0, 0);
                                    }
                                """)
        self.pushButton_delete_contacts_registration.setIcon(QtGui.QIcon("image/delete.png"))
        self.pushButton_delete_contacts_registration.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_delete_contacts_registration.clicked.connect(self.delete_contact_from_table)

        self.label_language_registration = QtWidgets.QLabel(self.frame_language_contacts)
        self.label_language_registration.setGeometry(100, 365, 170, 30)
        self._font(self.label_language_registration, 30)
        self.label_language_registration.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_language_registration.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_language_registration.setText("Языки")

        self.table_of_language_registration = QtWidgets.QTableWidget(self.frame_language_contacts)
        self.table_of_language_registration.setGeometry(100, 400, 900, 250)
        self.table_of_language_registration.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header_l = self.table_of_language_registration.horizontalHeader()
        self.table_of_language_registration.verticalHeader().setVisible(False)
        self._font(header_l, 20)
        header_l.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table_of_language_registration.setColumnCount(2)
        self.table_of_language_registration.setHorizontalHeaderLabels(('Язык', 'Уровень'))

        self.pushButton_add_language_registration = QtWidgets.QPushButton(self.frame_language_contacts)
        self.pushButton_add_language_registration.setGeometry(1030, 420, 50, 50)
        self.pushButton_add_language_registration.setStyleSheet("""
            QPushButton {
                background-color: rgb(85, 0, 0);
                border-style: solid;
                border-width: 2px;
                border-radius: 25px;
                border-color: rgb(50, 50, 50);
                color: white;
            }
            QPushButton:hover {
                background-color: rgb(120, 20, 20);
            }
            QPushButton:pressed {
                background-color: rgb(65, 0, 0);
            }
        """)
        self._font(self.pushButton_add_language_registration, 30)
        self.pushButton_add_language_registration.setText("+")
        self.pushButton_add_language_registration.clicked.connect(self.add_language_at_table)

        self.pushButton_edit_language_registration = QtWidgets.QPushButton(self.frame_language_contacts)
        self.pushButton_edit_language_registration.setGeometry(1030, 490, 50, 50)
        self.pushButton_edit_language_registration.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(85, 0, 0);
                        border-style: solid;
                        border-width: 2px;
                        border-radius: 25px;
                        border-color: rgb(50, 50, 50);
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: rgb(120, 20, 20);
                    }
                    QPushButton:pressed {
                        background-color: rgb(65, 0, 0);
                    }
                """)
        self.pushButton_edit_language_registration.setIcon(QtGui.QIcon("image/edit.png"))
        self.pushButton_edit_language_registration.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_edit_language_registration.clicked.connect(self.edit_language_at_table)

        self.pushButton_delete_language_registration = QtWidgets.QPushButton(self.frame_language_contacts)
        self.pushButton_delete_language_registration.setGeometry(1030, 560, 50, 50)
        self.pushButton_delete_language_registration.setStyleSheet("""
                            QPushButton {
                                background-color: rgb(85, 0, 0);
                                border-style: solid;
                                border-width: 2px;
                                border-radius: 25px;
                                border-color: rgb(50, 50, 50);
                                color: white;
                            }
                            QPushButton:hover {
                                background-color: rgb(120, 20, 20);
                            }
                            QPushButton:pressed {
                                background-color: rgb(65, 0, 0);
                            }
                        """)
        self.pushButton_delete_language_registration.setIcon(QtGui.QIcon("image/delete.png"))
        self.pushButton_delete_language_registration.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_delete_language_registration.clicked.connect(self.delete_language_from_table)

        self.pushButton_acceptence_language_contacts = QtWidgets.QPushButton(self.frame_language_contacts)
        self.pushButton_acceptence_language_contacts.setGeometry(490, 675, 220, 60)
        self.pushButton_acceptence_language_contacts.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButton_acceptence_language_contacts, 30)
        self.pushButton_acceptence_language_contacts.setText("Принять")
        self.pushButton_acceptence_language_contacts.clicked.connect(self.save_tables_data_to_db)

    # ==============================
    # Registration screen
    # ==============================
    def _setup_registration_frame(self):
        self.frame_registration = QtWidgets.QFrame(self.centralwidget)
        self.frame_registration.setGeometry(0, 0, 1200, 750)
        self.frame_registration.hide()
        self.frame_registration.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_registration.setStyleSheet("background-color: #EFE6DE;")
        self.frame_registration.setObjectName("frame_registration")

        self.avatar_registration = QtWidgets.QLabel(self.frame_registration)
        self.avatar_registration.setGeometry(110, 70, 300, 300)
        self.avatar_registration.setScaledContents(True)
        self.avatar_registration.hide()

        self.add_image = QtWidgets.QPushButton(self.frame_registration)
        self.add_image.setGeometry(110, 70, 300, 300)
        self._font(self.add_image, 200)
        self.add_image.setText("+")
        self.add_image.setStyleSheet("QPushButton {background-color: #cccccc; border: none; color: #808080}")
        self.add_image.setObjectName("add_image")
        self.add_image.clicked.connect(lambda: self.set_name_image(self.avatar_registration, self.add_image))

        self.pushButton_acceptence_registration = QtWidgets.QPushButton(self.frame_registration)
        self.pushButton_acceptence_registration.setGeometry(490, 675, 220, 60)
        self.pushButton_acceptence_registration.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButton_acceptence_registration, 30)
        self.pushButton_acceptence_registration.setText("Принять")
        self.pushButton_acceptence_registration.clicked.connect(lambda: self.check_registration())


        self._create_reg_labels()
        self._create_reg_inputs()

    def _create_reg_labels(self):
        self.label_photo = QtWidgets.QLabel(self.frame_registration)
        self.label_photo.setGeometry(130, 30, 95, 30)
        self._font(self.label_photo, 30)
        self.label_photo.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_photo.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_photo.setText("Фото")

        self.label_login = QtWidgets.QLabel("", self.frame_registration)
        self.label_login.setGeometry(620, 50, 160, 50)
        self._font(self.label_login, 30)
        self.label_login.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_login.setText("Логин")

        self.label_role = QtWidgets.QLabel(self.frame_registration)
        self.label_role.setGeometry(620, 136, 160, 50)
        self._font(self.label_role, 30)
        self.label_role.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_role.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_role.setText("Роль")

        self.label_password = QtWidgets.QLabel(self.frame_registration)
        self.label_password.setGeometry(620, 223, 160, 50)
        self._font(self.label_password, 30)
        self.label_password.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_password.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_password.setText("Пароль")

        self.label_password_repeat = QtWidgets.QLabel(self.frame_registration)
        self.label_password_repeat.setGeometry(440, 310, 340, 50)
        self._font(self.label_password_repeat, 30)
        self.label_password_repeat.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_password_repeat.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_password_repeat.setText("Повторите пароль")

        self.label_surname = QtWidgets.QLabel(self.frame_registration)
        self.label_surname.setGeometry(80, 380, 160, 30)
        self._font(self.label_surname, 20)
        self.label_surname.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_surname.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_surname.setText("Фамилия")

        self.label_name = QtWidgets.QLabel(self.frame_registration)
        self.label_name.setGeometry(80, 430, 160, 30)
        self._font(self.label_name, 20)
        self.label_name.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_name.setText("Имя")

        self.label_patronum = QtWidgets.QLabel(self.frame_registration)
        self.label_patronum.setGeometry(80, 480, 160, 30)
        self._font(self.label_patronum, 20)
        self.label_patronum.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_patronum.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_patronum.setText("Отчество")

        self.label_country = QtWidgets.QLabel(self.frame_registration)
        self.label_country.setGeometry(80, 530, 160, 30)
        self._font(self.label_country, 20)
        self.label_country.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_country.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_country.setText("Страна")

        self.label_age = QtWidgets.QLabel(self.frame_registration)
        self.label_age.setGeometry(80, 580, 160, 30)
        self._font(self.label_age, 20)
        self.label_age.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_age.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_age.setText("Возраст")
        self.label_age.hide()

        self.label_education = QtWidgets.QLabel(self.frame_registration)
        self.label_education.setGeometry(80, 630, 160, 30)
        self._font(self.label_education, 20)
        self.label_education.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_education.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_education.setText("Образование")
        self.label_education.hide()

        self.label_description = QtWidgets.QLabel(self.frame_registration)
        self.label_description.setGeometry(450, 380, 145, 50)
        self._font(self.label_description, 25)
        self.label_description.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_description.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_description.setText("Описание")
        self.label_description.hide()

    def _create_reg_inputs(self):
        self.textEdit_login_reg = QtWidgets.QLineEdit(self.frame_registration)
        self.textEdit_login_reg.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_login_reg, 15)
        self.textEdit_login_reg.setGeometry(800, 50, 350, 50)

        self.comboBox_roles = QtWidgets.QComboBox(self.frame_registration)
        self.comboBox_roles.setGeometry(800, 136, 350, 50)
        self._font(self.comboBox_roles, 26)
        self.comboBox_roles.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self.comboBox_roles.addItems(['', 'Студент', 'Преподаватель'])
        self.comboBox_roles.currentIndexChanged.connect(self.on_combo_changed)

        self.textEdit_password_reg = QtWidgets.QLineEdit(self.frame_registration)
        self.textEdit_password_reg.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_password_reg, 15)
        self.textEdit_password_reg.setGeometry(800, 223, 350, 50)

        self.textEdit_repeat_password = QtWidgets.QLineEdit(self.frame_registration)
        self.textEdit_repeat_password.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_repeat_password, 15)
        self.textEdit_repeat_password.setGeometry(800, 310, 350, 50)

        self.textEdit_surname = QtWidgets.QLineEdit(self.frame_registration)
        self.textEdit_surname.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_surname, 15)
        self.textEdit_surname.setGeometry(250, 380, 160, 30)

        self.textEdit_name = QtWidgets.QLineEdit(self.frame_registration)
        self.textEdit_name.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_name, 15)
        self.textEdit_name.setGeometry(250, 430, 160, 30)

        self.textEdit_patronum = QtWidgets.QLineEdit(self.frame_registration)
        self.textEdit_patronum.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_patronum, 15)
        self.textEdit_patronum.setGeometry(250, 480, 160, 30)

        self.comboBox_country = QtWidgets.QComboBox(self.frame_registration)
        self.comboBox_country.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.comboBox_country, 15)
        self.comboBox_country.setGeometry(250, 530, 160, 30)

        self.textEdit_age = QtWidgets.QLineEdit(self.frame_registration)
        self.textEdit_age.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_age, 15)
        self.textEdit_age.setGeometry(250, 580, 160, 30)
        self.textEdit_age.hide()

        self.textEdit_education = QtWidgets.QLineEdit(self.frame_registration)
        self.textEdit_education.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_education, 15)
        self.textEdit_education.setGeometry(250, 630, 160, 30)
        self.textEdit_education.hide()
        self.textEdit_education.setReadOnly(True)

        self.addFile_education = QtWidgets.QPushButton(self.frame_registration)
        self.addFile_education.setStyleSheet("QPushButton {background-color: #cccccc; border: none; color: #808080}")
        self._font(self.addFile_education, 15)
        self.addFile_education.setGeometry(250, 630, 160, 30)
        self.addFile_education.setText("+")
        self.addFile_education.setEnabled(False)
        self.addFile_education.clicked.connect(self.open_file)
        self.addFile_education.hide()

        self.textEdit_description = QtWidgets.QTextEdit(self.frame_registration)
        self.textEdit_description.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_description, 15)
        self.textEdit_description.setGeometry(450, 430, 700, 225)
        self.textEdit_description.hide()

    # ==============================
    # Language & contacts screen
    # ==============================

    def _setup_language_contacts_editing_frame(self):
        self.frame_language_contacts_editing = QtWidgets.QFrame(self.centralwidget)
        self.frame_language_contacts_editing.setGeometry(0, 0, 1200, 750)
        self.frame_language_contacts_editing.hide()
        self.frame_language_contacts_editing.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_language_contacts_editing.setStyleSheet("background-color: #EFE6DE;")
        self.frame_language_contacts_editing.setObjectName("frame_language_contacts")

        self.label_contacts_editing = QtWidgets.QLabel(self.frame_language_contacts_editing)
        self.label_contacts_editing.setGeometry(100, 30, 170, 30)
        self._font(self.label_contacts_editing, 30)
        self.label_contacts_editing.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_contacts_editing.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_contacts_editing.setText("Контакты")

        self.table_of_contacts_editing = QtWidgets.QTableWidget(self.frame_language_contacts_editing)
        self.table_of_contacts_editing.setGeometry(100, 75, 900, 250)
        self.table_of_contacts_editing.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header_c = self.table_of_contacts_editing.horizontalHeader()
        self.table_of_contacts_editing.verticalHeader().setVisible(False)
        self._font(header_c, 20)
        header_c.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.pushButton_add_contacts_editing = QtWidgets.QPushButton(self.frame_language_contacts_editing)
        self.pushButton_add_contacts_editing.setGeometry(1030, 95, 50, 50)
        self.pushButton_add_contacts_editing.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(85, 0, 0);
                        border-style: solid;
                        border-width: 2px;
                        border-radius: 25px;
                        border-color: rgb(50, 50, 50);
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: rgb(120, 20, 20);
                    }
                    QPushButton:pressed {
                        background-color: rgb(65, 0, 0);
                    }
                """)
        self._font(self.pushButton_add_contacts_editing, 30)
        self.pushButton_add_contacts_editing.setText("+")
        self.pushButton_add_contacts_editing.clicked.connect(self.add_contact_edit)

        self.pushButton_edit_contacts_editing = QtWidgets.QPushButton(self.frame_language_contacts_editing)
        self.pushButton_edit_contacts_editing.setGeometry(1030, 165, 50, 50)
        self.pushButton_edit_contacts_editing.setStyleSheet("""
                            QPushButton {
                                background-color: rgb(85, 0, 0);
                                border-style: solid;
                                border-width: 2px;
                                border-radius: 25px;
                                border-color: rgb(50, 50, 50);
                                color: white;
                            }
                            QPushButton:hover {
                                background-color: rgb(120, 20, 20);
                            }
                            QPushButton:pressed {
                                background-color: rgb(65, 0, 0);
                            }
                        """)
        self.pushButton_edit_contacts_editing.setIcon(QtGui.QIcon("image/edit.png"))
        self.pushButton_edit_contacts_editing.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_edit_contacts_editing.clicked.connect(self.edit_contact_edit)

        self.pushButton_delete_contacts_editing = QtWidgets.QPushButton(self.frame_language_contacts_editing)
        self.pushButton_delete_contacts_editing.setGeometry(1030, 235, 50, 50)
        self.pushButton_delete_contacts_editing.setStyleSheet("""
                                    QPushButton {
                                        background-color: rgb(85, 0, 0);
                                        border-style: solid;
                                        border-width: 2px;
                                        border-radius: 25px;
                                        border-color: rgb(50, 50, 50);
                                        color: white;
                                    }
                                    QPushButton:hover {
                                        background-color: rgb(120, 20, 20);
                                    }
                                    QPushButton:pressed {
                                        background-color: rgb(65, 0, 0);
                                    }
                                """)
        self.pushButton_delete_contacts_editing.setIcon(QtGui.QIcon("image/delete.png"))
        self.pushButton_delete_contacts_editing.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_delete_contacts_editing.clicked.connect(self.delete_contact_edit)

        self.label_language_editing = QtWidgets.QLabel(self.frame_language_contacts_editing)
        self.label_language_editing.setGeometry(100, 365, 170, 30)
        self._font(self.label_language_editing, 30)
        self.label_language_editing.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_language_editing.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_language_editing.setText("Языки")

        self.table_of_language_editing = QtWidgets.QTableWidget(self.frame_language_contacts_editing)
        self.table_of_language_editing.setGeometry(100, 400, 900, 250)
        self.table_of_language_editing.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header_l = self.table_of_language_editing.horizontalHeader()
        self.table_of_language_editing.verticalHeader().setVisible(False)
        self._font(header_l, 20)
        header_l.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.pushButton_add_language_editing = QtWidgets.QPushButton(self.frame_language_contacts_editing)
        self.pushButton_add_language_editing.setGeometry(1030, 420, 50, 50)
        self.pushButton_add_language_editing.setStyleSheet("""
            QPushButton {
                background-color: rgb(85, 0, 0);
                border-style: solid;
                border-width: 2px;
                border-radius: 25px;
                border-color: rgb(50, 50, 50);
                color: white;
            }
            QPushButton:hover {
                background-color: rgb(120, 20, 20);
            }
            QPushButton:pressed {
                background-color: rgb(65, 0, 0);
            }
        """)
        self._font(self.pushButton_add_language_editing, 30)
        self.pushButton_add_language_editing.setText("+")
        self.pushButton_add_language_editing.clicked.connect(self.add_language_edit)

        self.pushButton_edit_language_editing = QtWidgets.QPushButton(self.frame_language_contacts_editing)
        self.pushButton_edit_language_editing.setGeometry(1030, 490, 50, 50)
        self.pushButton_edit_language_editing.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(85, 0, 0);
                        border-style: solid;
                        border-width: 2px;
                        border-radius: 25px;
                        border-color: rgb(50, 50, 50);
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: rgb(120, 20, 20);
                    }
                    QPushButton:pressed {
                        background-color: rgb(65, 0, 0);
                    }
                """)
        self.pushButton_edit_language_editing.setIcon(QtGui.QIcon("image/edit.png"))
        self.pushButton_edit_language_editing.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_edit_language_editing.clicked.connect(self.edit_language_edit)

        self.pushButton_delete_language_editing = QtWidgets.QPushButton(self.frame_language_contacts_editing)
        self.pushButton_delete_language_editing.setGeometry(1030, 560, 50, 50)
        self.pushButton_delete_language_editing.setStyleSheet("""
                            QPushButton {
                                background-color: rgb(85, 0, 0);
                                border-style: solid;
                                border-width: 2px;
                                border-radius: 25px;
                                border-color: rgb(50, 50, 50);
                                color: white;
                            }
                            QPushButton:hover {
                                background-color: rgb(120, 20, 20);
                            }
                            QPushButton:pressed {
                                background-color: rgb(65, 0, 0);
                            }
                        """)
        self.pushButton_delete_language_editing.setIcon(QtGui.QIcon("image/delete.png"))
        self.pushButton_delete_language_editing.setIconSize(QtCore.QSize(35, 35))
        self.pushButton_delete_language_editing.clicked.connect(self.delete_language_edit)

        self.pushButton_acceptence_language_contacts_editing = QtWidgets.QPushButton(self.frame_language_contacts_editing)
        self.pushButton_acceptence_language_contacts_editing.setGeometry(490, 675, 220, 60)
        self.pushButton_acceptence_language_contacts_editing.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButton_acceptence_language_contacts_editing, 30)
        self.pushButton_acceptence_language_contacts_editing.setText("Принять")
        self.pushButton_acceptence_language_contacts_editing.clicked.connect(lambda: self.switch_forms(self.frame_language_contacts_editing, self.frame_main))

    # ==============================
    # Editing screen
    # ==============================
    def _setup_editing_frame(self):
        self.frame_editing = QtWidgets.QFrame(self.centralwidget)
        self.frame_editing.setGeometry(0, 0, 1200, 750)
        self.frame_editing.hide()
        self.frame_editing.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_editing.setStyleSheet("background-color: #EFE6DE;")
        self.frame_editing.setObjectName("frame_editing")

        self.avatar_editing = QtWidgets.QLabel(self.frame_editing)
        self.avatar_editing.setGeometry(110, 70, 300, 300)
        self.avatar_editing.setScaledContents(True)
        self.avatar_editing.hide()

        self.add_image_edit = QtWidgets.QPushButton(self.frame_editing)
        self.add_image_edit.setGeometry(110, 70, 300, 300)
        self._font(self.add_image_edit, 200)
        self.add_image_edit.setText("+")
        self.add_image_edit.setStyleSheet("QPushButton {background-color: #cccccc; border: none; color: #808080}")
        self.add_image_edit.setObjectName("add_image_edit")
        self.add_image_edit.clicked.connect(lambda: self.set_name_image(self.avatar_editing, self.add_image_edit))

        self.pushButton_acceptence_editing = QtWidgets.QPushButton(self.frame_editing)
        self.pushButton_acceptence_editing.setGeometry(355, 675, 220, 60)
        self.pushButton_acceptence_editing.setStyleSheet("""
            QPushButton {
                background-color: rgb(85, 0, 0);
                color: white;
                border-radius: 8px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: rgb(120, 20, 20);
            }
            QPushButton:pressed {
                background-color: rgb(65, 0, 0);
            }
            """)
        self._font(self.pushButton_acceptence_editing, 30)
        self.pushButton_acceptence_editing.setText("Принять")
        self.pushButton_acceptence_editing.clicked.connect(lambda: (self.edit_user(), self.switch_forms(self.frame_editing, self.frame_language_contacts_editing)))

        self.pushButton_editing_back_to_main = QtWidgets.QPushButton(self.frame_editing)
        self.pushButton_editing_back_to_main.setGeometry(625, 675, 220, 60)
        self.pushButton_editing_back_to_main.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        border-radius: 8px;
                        padding: 6px;
                    }
                    QPushButton:hover {
                        background-color: rgb(120, 20, 20);
                    }
                    QPushButton:pressed {
                        background-color: rgb(65, 0, 0);
                    }
                    """)
        self._font(self.pushButton_editing_back_to_main, 30)
        self.pushButton_editing_back_to_main.setText("Назад")
        self.pushButton_editing_back_to_main.clicked.connect(lambda: self.switch_forms(self.frame_editing, self.frame_main))

        self._create_edit_labels()
        self._create_edit_inputs()

    def _create_edit_labels(self):
        self.label_photo_edit = QtWidgets.QLabel(self.frame_editing)
        self.label_photo_edit.setGeometry(130, 30, 95, 30)
        self._font(self.label_photo_edit, 30)
        self.label_photo_edit.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_photo_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_photo_edit.setText("Фото")

        self.label_login_edit = QtWidgets.QLabel("", self.frame_editing)
        self.label_login_edit.setGeometry(620, 50, 160, 50)
        self._font(self.label_login_edit, 30)
        self.label_login_edit.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_login_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_login_edit.setText("Логин")

        self.label_password_edit = QtWidgets.QLabel(self.frame_editing)
        self.label_password_edit.setGeometry(620, 120, 160, 50)
        self._font(self.label_password_edit, 30)
        self.label_password_edit.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_password_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_password_edit.setText("Пароль")

        self.label_surname_edit = QtWidgets.QLabel(self.frame_editing)
        self.label_surname_edit.setGeometry(80, 380, 160, 30)
        self._font(self.label_surname_edit, 20)
        self.label_surname_edit.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_surname_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_surname_edit.setText("Фамилия")

        self.label_name_edit = QtWidgets.QLabel(self.frame_editing)
        self.label_name_edit.setGeometry(80, 430, 160, 30)
        self._font(self.label_name_edit, 20)
        self.label_name_edit.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_name_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_name_edit.setText("Имя")

        self.label_patronum_edit = QtWidgets.QLabel(self.frame_editing)
        self.label_patronum_edit.setGeometry(80, 480, 160, 30)
        self._font(self.label_patronum_edit, 20)
        self.label_patronum_edit.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_patronum_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_patronum_edit.setText("Отчество")

        self.label_country_edit = QtWidgets.QLabel(self.frame_editing)
        self.label_country_edit.setGeometry(80, 530, 160, 30)
        self._font(self.label_country_edit, 20)
        self.label_country_edit.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_country_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_country_edit.setText("Страна")

        self.label_age_edit = QtWidgets.QLabel(self.frame_editing)
        self.label_age_edit.setGeometry(80, 580, 160, 30)
        self._font(self.label_age_edit, 20)
        self.label_age_edit.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_age_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_age_edit.setText("Возраст")

        self.label_education_edit = QtWidgets.QLabel(self.frame_editing)
        self.label_education_edit.setGeometry(80, 580, 160, 30)
        self._font(self.label_education_edit, 20)
        self.label_education_edit.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_education_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_education_edit.setText("Образование")

        self.label_description_edit = QtWidgets.QLabel(self.frame_editing)
        self.label_description_edit.setGeometry(450, 380, 145, 50)
        self._font(self.label_description_edit, 25)
        self.label_description_edit.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_description_edit.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_description_edit.setText("Описание")

    def _create_edit_inputs(self):
        self.textEdit_login_edit = QtWidgets.QLineEdit(self.frame_editing)
        self.textEdit_login_edit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_login_edit, 15)
        self.textEdit_login_edit.setGeometry(800, 50, 350, 50)

        self.textEdit_password_edit = QtWidgets.QLineEdit(self.frame_editing)
        self.textEdit_password_edit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_password_edit, 15)
        self.textEdit_password_edit.setGeometry(800, 120, 350, 50)

        self.textEdit_surname_edit = QtWidgets.QLineEdit(self.frame_editing)
        self.textEdit_surname_edit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_surname_edit, 15)
        self.textEdit_surname_edit.setGeometry(250, 380, 160, 30)

        self.textEdit_name_edit = QtWidgets.QLineEdit(self.frame_editing)
        self.textEdit_name_edit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_name_edit, 15)
        self.textEdit_name_edit.setGeometry(250, 430, 160, 30)

        self.textEdit_patronum_edit = QtWidgets.QLineEdit(self.frame_editing)
        self.textEdit_patronum_edit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_patronum_edit, 15)
        self.textEdit_patronum_edit.setGeometry(250, 480, 160, 30)

        self.comboBox_country_edit = QtWidgets.QComboBox(self.frame_editing)
        self.comboBox_country_edit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.comboBox_country_edit, 15)
        self.comboBox_country_edit.setGeometry(250, 530, 160, 30)

        self.textEdit_age_edit = QtWidgets.QLineEdit(self.frame_editing)
        self.textEdit_age_edit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_age_edit, 15)
        self.textEdit_age_edit.setGeometry(250, 580, 160, 30)

        self.textEdit_education_edit = QtWidgets.QLineEdit(self.frame_editing)
        self.textEdit_education_edit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_education_edit, 15)
        self.textEdit_education_edit.setGeometry(250, 580, 160, 30)

        self.addFile_education_edit = QtWidgets.QPushButton(self.frame_editing)
        self.addFile_education_edit.setStyleSheet("QPushButton {background-color: #cccccc; border: none; color: #808080}")
        self._font(self.addFile_education_edit, 15)
        self.addFile_education_edit.setGeometry(250, 580    , 160, 30)
        self.addFile_education_edit.setText("+")
        self.addFile_education_edit.setEnabled(False)
        self.addFile_education_edit.clicked.connect(self.open_file_edit)
        self.addFile_education_edit.hide()

        self.textEdit_description_edit = QtWidgets.QTextEdit(self.frame_editing)
        self.textEdit_description_edit.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_description_edit, 15)
        self.textEdit_description_edit.setGeometry(450, 430, 700, 225)

    # ==============================
    # Main application area
    # ==============================
    def _setup_main_frame(self):
        self.frame_main = QtWidgets.QFrame(self.centralwidget)
        self.frame_main.hide()
        self.frame_main.setGeometry(0, 0, 1200, 750)
        self.frame_main.setStyleSheet("background-color: #EFE6DE;")

        self._setup_main_tabs()

    def _setup_main_tabs(self):
        self.tabWidget_main = QtWidgets.QTabWidget(self.frame_main)
        self.tabWidget_main.setGeometry(0, 0, 1200, 750)
        self._font(self.tabWidget_main, 15)
        self.tabWidget_main.setObjectName("tabWidget_main")

        self._setup_account_tab()
        self._setup_course_tab()
        self._setup_users_tab()
        self._setup_language_tab()
        self._setup_my_course_tab()
        self._setup_my_marks()
        self._setup_notification_tab()

        self.tabWidget_main.currentChanged.connect(self.main_tables)

    def _setup_account_tab(self):
        self.tab_account = QtWidgets.QWidget()

        self.label_photo_profile_output = QtWidgets.QLabel(self.tab_account)
        self.label_photo_profile_output.setGeometry(70, 30, 95, 30)
        self._font(self.label_photo_profile_output, 30)
        self.label_photo_profile_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_photo_profile_output.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_photo_profile_output.setText("Фото")

        self.avatar = QtWidgets.QLabel(self.tab_account)
        self.avatar.setGeometry(70, 70, 300, 300)
        self.avatar.setScaledContents(True)

        self.label_login_output = QtWidgets.QLabel(self.tab_account)
        self.label_login_output.setGeometry(430, 50, 100, 50)
        self._font(self.label_login_output, 20)
        self.label_login_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_login_output.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_login_output.setText("Логин")

        self.label_name_profile_output = QtWidgets.QLabel(self.tab_account)
        self.label_name_profile_output.setGeometry(430, 90, 100, 50)
        self._font(self.label_name_profile_output, 20)
        self.label_name_profile_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_name_profile_output.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_name_profile_output.setText("ФИО")

        self.label_role_profile_output = QtWidgets.QLabel(self.tab_account)
        self.label_role_profile_output.setGeometry(430, 130, 100, 50)
        self._font(self.label_role_profile_output, 20)
        self.label_role_profile_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_role_profile_output.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_role_profile_output.setText("Роль")

        self.label_country_profile_output = QtWidgets.QLabel(self.tab_account)
        self.label_country_profile_output.setGeometry(430, 170, 100, 50)
        self._font(self.label_country_profile_output, 20)
        self.label_country_profile_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_country_profile_output.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_country_profile_output.setText("Страна")

        self.label_age_profile_output = QtWidgets.QLabel(self.tab_account)
        self.label_age_profile_output.setGeometry(430, 210, 100, 50)
        self._font(self.label_age_profile_output, 20)
        self.label_age_profile_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_age_profile_output.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_age_profile_output.setText("Возраст")

        self.output_login_profile = QtWidgets.QLineEdit(self.tab_account)
        self.output_login_profile.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.output_login_profile, 25)
        self.output_login_profile.setGeometry(550, 50, 600, 40)
        self.output_login_profile.setReadOnly(True)

        self.output_name_profile = QtWidgets.QLineEdit(self.tab_account)
        self.output_name_profile.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.output_name_profile, 25)
        self.output_name_profile.setGeometry(550, 90, 600, 40)
        self.output_name_profile.setReadOnly(True)

        self.output_roles_profile = QtWidgets.QLineEdit(self.tab_account)
        self.output_roles_profile.setGeometry(550, 130, 600, 40)
        self._font(self.output_roles_profile, 26)
        self.output_roles_profile.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self.output_roles_profile.setReadOnly(True)

        self.output_country_profile = QtWidgets.QLineEdit(self.tab_account)
        self.output_country_profile.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.output_country_profile, 25)
        self.output_country_profile.setGeometry(550, 170, 600, 40)
        self.output_country_profile.setReadOnly(True)

        self.output_age_profile = QtWidgets.QLineEdit(self.tab_account)
        self.output_age_profile.setGeometry(550, 210, 600, 40)
        self._font(self.output_age_profile, 26)
        self.output_age_profile.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self.output_age_profile.setReadOnly(True)

        self.table_of_profile = QtWidgets.QTableWidget(self.tab_account)
        self.table_of_profile.setGeometry(70, 400, 1075, 225)
        self.table_of_profile.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header = self.table_of_profile.horizontalHeader()
        self.table_of_profile.verticalHeader().setVisible(False)
        self._font(header, 20)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.pushButtonEditProfile = QtWidgets.QPushButton(self.tab_account)
        self.pushButtonEditProfile.setGeometry(300, 635, 200, 40)
        self.pushButtonEditProfile.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButtonEditProfile, 25)
        self.pushButtonEditProfile.setText("Изменить")
        self.pushButtonEditProfile.clicked.connect(lambda: self.to_edit_form())

        self.pushButtonDeleteProfile = QtWidgets.QPushButton(self.tab_account)
        self.pushButtonDeleteProfile.setGeometry(600, 635, 200, 40)
        self.pushButtonDeleteProfile.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButtonDeleteProfile, 25)
        self.pushButtonDeleteProfile.setText("Удалить")
        self.pushButtonDeleteProfile.clicked.connect(self.delete_profile)

    def _setup_course_tab(self):
        self.tab_course = QtWidgets.QWidget()

        self.table_of_courses = QtWidgets.QTableWidget(self.tab_course)
        self.table_of_courses.setGeometry(45, 40, 780, 620)
        self.table_of_courses.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header = self.table_of_courses.horizontalHeader()
        self._font(header, 15)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table_of_courses.verticalHeader().setVisible(False)

        self.pushButtonJoin = QtWidgets.QPushButton(self.tab_course)
        self.pushButtonJoin.setGeometry(860, 70, 291, 61)
        self.pushButtonJoin.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButtonJoin, 28)
        self.pushButtonJoin.setText("Вступить")
        self.pushButtonJoin.clicked.connect(self.send_course_application)

        self.pushButtonObserve = QtWidgets.QPushButton(self.tab_course)
        self.pushButtonObserve.setGeometry(860, 160, 291, 61)
        self.pushButtonObserve.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButtonObserve, 28)
        self.pushButtonObserve.setText("Просмотреть")
        self.pushButtonObserve.clicked.connect(lambda: self.open_course_info(self.table_of_courses))

        self.pushButtonDeleteCourse = QtWidgets.QPushButton(self.tab_course)
        self.pushButtonDeleteCourse.setGeometry(860, 250, 291, 61)
        self.pushButtonDeleteCourse.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButtonDeleteCourse, 28)
        self.pushButtonDeleteCourse.setText("Удалить")

    def _setup_language_tab(self):
        self.tab_language = QtWidgets.QWidget()

        self.table_of_language = QtWidgets.QTableWidget(self.tab_language)
        self.table_of_language.setGeometry(45, 40, 780, 620)

        self.table_of_language.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_of_language.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)

        self.table_of_language.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: black;
                color: black;
            }
            QHeaderView::section {
                background-color: rgb(85, 0, 0);
                color: white;
                font-size: 15px;
                border: 1px solid black;
                padding: 4px;
            }
        """)
        header = self.table_of_language.horizontalHeader()
        self._font(header, 15)
        self.table_of_language.verticalHeader().setVisible(False)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.pushButtonAddLanguage = QtWidgets.QPushButton(self.tab_language)
        self.pushButtonAddLanguage.setGeometry(860, 70, 291, 61)
        self.pushButtonAddLanguage.setStyleSheet("""
        QPushButton { background-color: rgb(85, 0, 0); color: white; border-radius: 8px; }
        QPushButton:hover { background-color: rgb(120, 20, 20); }
        """)
        self._font(self.pushButtonAddLanguage, 28)
        self.pushButtonAddLanguage.setText("Добавить")
        # При нажатии вызываем подготовку пустой формы
        self.pushButtonAddLanguage.clicked.connect(self.prepare_add_language)

        self.pushButtonViewLanguage = QtWidgets.QPushButton(self.tab_language)
        self.pushButtonViewLanguage.setGeometry(860, 160, 291, 61)
        self.pushButtonViewLanguage.setStyleSheet("""
        QPushButton { background-color: rgb(85, 0, 0); color: white; border-radius: 8px; }
        QPushButton:hover { background-color: rgb(120, 20, 20); }
        """)
        self._font(self.pushButtonViewLanguage, 28)
        self.pushButtonViewLanguage.setText("Просмотреть")
        self.pushButtonViewLanguage.clicked.connect(lambda: self.open_language_info(self.table_of_language))

    def _setup_users_tab(self):
        self.tab_users = QtWidgets.QWidget()

        self.users_tabs = QtWidgets.QTabWidget(self.tab_users)
        self.users_tabs.setGeometry(45, 40, 750, 620)
        self._font(self.users_tabs, 20)
        self.users_tabs.setObjectName("users_tabs")

        self.students_tab = QtWidgets.QWidget()
        self.users_tabs.addTab(self.students_tab, "")
        self.users_tabs.setTabText(self.users_tabs.indexOf(self.students_tab),
                                          "Студенты")

        self.teachers_tab = QtWidgets.QWidget()
        self.users_tabs.addTab(self.teachers_tab, "")
        self.users_tabs.setTabText(self.users_tabs.indexOf(self.teachers_tab), "Преподаватели")

        self.banned_tab = QtWidgets.QWidget()
        self.users_tabs.addTab(self.banned_tab, "")
        self.users_tabs.setTabText(self.users_tabs.indexOf(self.banned_tab), "Заблокированные")

        self.users_tabs.setStyleSheet("""
                                                             QTabBar::tab {
                                                                    width: """ + str(750 / self.users_tabs.count()) + """; 
                                                                    height: 50;
                                                                    background: rgb(85, 0, 0);
                                                                    color: white;
                                                             }
                                                             QTabBar::tab:selected {
                                                                 background: rgb(65, 0, 0);
                                                                border-bottom-color: #202020;
                                                             }""")

        self.users_tabs.currentChanged.connect(self.users_tables)

        self.table_of_students = QtWidgets.QTableWidget(self.students_tab)
        self.table_of_students.setGeometry(0, 0, 750, 620)
        self.table_of_students.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header_s = self.table_of_students.horizontalHeader()
        self._font(header_s, 25)
        self._font(self.table_of_students, 25)
        header_s.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table_of_students.verticalHeader().setVisible(False)

        self.table_of_teachers = QtWidgets.QTableWidget(self.teachers_tab)
        self.table_of_teachers.setGeometry(0, 0, 750, 620)
        self.table_of_teachers.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header_t = self.table_of_teachers.horizontalHeader()
        self._font(header_t, 25)
        self._font(self.table_of_teachers, 25)
        header_t.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table_of_teachers.verticalHeader().setVisible(False)

        self.table_of_banned = QtWidgets.QTableWidget(self.banned_tab)
        self.table_of_banned.setGeometry(0, 0, 750, 620)
        self.table_of_banned.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header_b = self.table_of_banned.horizontalHeader()
        self._font(header_b, 25)
        self._font(self.table_of_banned, 20)
        header_b.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        self.table_of_banned.verticalHeader().setVisible(False)

        self.pushButtonOpenProfile = QtWidgets.QPushButton(self.tab_users)
        self.pushButtonOpenProfile.setGeometry(860, 70, 291, 61)
        self.pushButtonOpenProfile.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButtonOpenProfile, 25)
        self.pushButtonOpenProfile.setText("Открыть профиль")
        self.pushButtonOpenProfile.clicked.connect(lambda: self.open_profile(self.table_of_students, self.frame_course))

        self.pushButtonBan = QtWidgets.QPushButton(self.tab_users)
        self.pushButtonBan.setGeometry(860, 160, 291, 61)
        self.pushButtonBan.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButtonBan, 25)
        self.pushButtonBan.setText("Заблокировать")
        self.pushButtonBan.clicked.connect(lambda: self.ban_selected_user(self.table_of_students))

        self.pushButtonDeleteUser = QtWidgets.QPushButton(self.tab_users)
        self.pushButtonDeleteUser.setGeometry(860, 250, 291, 61)
        self.pushButtonDeleteUser.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButtonDeleteUser, 28)
        self.pushButtonDeleteUser.setText("Удалить")
        self.pushButtonDeleteUser.clicked.connect(self.delete_user)

    def _setup_notification_tab(self):
        self.tab_notification = QtWidgets.QWidget()

        self.notification_tabs = QtWidgets.QTabWidget(self.tab_notification)
        self.notification_tabs.setGeometry(45, 40, 800, 600)
        self._font(self.notification_tabs, 22)
        self.notification_tabs.setObjectName("notification_tabs")

        self.notification_unchecked_tab = QtWidgets.QWidget()
        self.notification_tabs.addTab(self.notification_unchecked_tab, "")
        self.notification_tabs.setTabText(self.notification_tabs.indexOf(self.notification_unchecked_tab), "Непрочитано")

        self.notification_checked_tab = QtWidgets.QWidget()
        self.notification_tabs.addTab(self.notification_checked_tab, "")
        self.notification_tabs.setTabText(self.notification_tabs.indexOf(self.notification_checked_tab), "Прочитано")

        self.notification_tabs.setStyleSheet("""
                                                     QTabBar::tab {
                                                            width: """ + str(800 / self.notification_tabs.count()) + """; 
                                                            height: 50;
                                                            background: rgb(85, 0, 0);
                                                            color: white;
                                                     }
                                                     QTabBar::tab:selected {
                                                         background: rgb(65, 0, 0);
                                                         border-bottom-color: #202020;
                                                     }""")

        self.unchecked_notification_list = QtWidgets.QTableWidget(self.notification_unchecked_tab)
        self.unchecked_notification_list.setGeometry(0, 0, 800, 600)
        self._font(self.unchecked_notification_list, 28)
        self.unchecked_notification_list.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header = self.unchecked_notification_list.horizontalHeader()
        self._font(header, 20)
        self.unchecked_notification_list.verticalHeader().setVisible(False)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.checked_notification_list = QtWidgets.QTableWidget(self.notification_checked_tab)
        self.checked_notification_list.setGeometry(0, 0, 800, 600)
        self._font(self.checked_notification_list, 28)
        self.checked_notification_list.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header = self.checked_notification_list.horizontalHeader()
        self._font(header, 20)
        self.checked_notification_list.verticalHeader().setVisible(False)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.pushButtonOpenNotification = QtWidgets.QPushButton(self.tab_notification)
        self.pushButtonOpenNotification.setGeometry(860, 70, 291, 61)
        self.pushButtonOpenNotification.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButtonOpenNotification, 28)
        self.pushButtonOpenNotification.setText("Открыть")
        self.pushButtonOpenNotification.clicked.connect(lambda: self.open_notification(self.unchecked_notification_list))

        self.notification_tabs.currentChanged.connect(lambda: (
            self.pushButtonOpenNotification.disconnect(),
            self.pushButtonOpenNotification.clicked.connect(lambda: self.open_notification(
                self.unchecked_notification_list if self.notification_tabs.currentIndex == 0 else self.checked_notification_list))
        )
                                                      )

        self.pushButtonDeleteNotification = QtWidgets.QPushButton(self.tab_notification)
        self.pushButtonDeleteNotification.setGeometry(860, 160, 291, 61)
        self.pushButtonDeleteNotification.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButtonDeleteNotification, 28)
        self.pushButtonDeleteNotification.setText("Удалить")

    def _setup_my_course_tab(self):
        self.tab_my_course = QtWidgets.QWidget()

        self.table_of_my_courses = QtWidgets.QTableWidget(self.tab_my_course)
        self.table_of_my_courses.setGeometry(45, 40, 780, 620)
        self.table_of_my_courses.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header = self.table_of_my_courses.horizontalHeader()
        self.table_of_my_courses.verticalHeader().setVisible(False)
        self._font(header, 15)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.pushButtonOpenMyCourse = QtWidgets.QPushButton(self.tab_my_course)
        self.pushButtonOpenMyCourse.setGeometry(860, 70, 291, 61)
        self.pushButtonOpenMyCourse.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButtonOpenMyCourse, 28)
        self.pushButtonOpenMyCourse.setText("Открыть")
        self.pushButtonOpenMyCourse.clicked.connect(lambda: self.open_course_info(self.table_of_my_courses))

        self.pushButtonAdd = QtWidgets.QPushButton(self.tab_my_course)
        self.pushButtonAdd.setGeometry(860, 160, 291, 61)
        self.pushButtonAdd.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButtonAdd, 28)
        self.pushButtonAdd.setText("Добавить")
        self.pushButtonAdd.clicked.connect(lambda: (
            self.switch_forms(self.frame_main, self.frame_course_creation),
            self.comboBox_language.clear(),
            self.comboBox_language.addItems([''] + [k[0] for k in fetch_all("select Название from Языки", None)])
        ))

        self.pushButtonExclude = QtWidgets.QPushButton(self.tab_my_course)
        self.pushButtonExclude.setGeometry(860, 250, 291, 61)
        self.pushButtonExclude.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButtonExclude, 28)
        self.pushButtonExclude.setText("Выйти из курса")
        self.pushButtonExclude.clicked.connect(lambda: (self.leave_course()))

    def _setup_my_marks(self):
        self.tab_my_marks = QtWidgets.QWidget()

        self.report_of_my_marks = QtWidgets.QTableWidget(self.tab_my_marks)
        self.report_of_my_marks.setGeometry(50, 80, 1100, 500)
        self.report_of_my_marks.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 14px;
                        padding: 4px;
                    }
                """)
        self.report_of_my_marks.verticalHeader().setVisible(False)
        self._font(self.report_of_my_marks.horizontalHeader(), 20)

        self.label_date_from = QtWidgets.QLabel("C:", self.tab_my_marks)
        self.label_date_from.setGeometry(50, 30, 30, 30)
        self.label_date_from.setStyleSheet("color: rgb(85, 0, 0);")
        self._font(self.label_date_from, 15)

        self.dateEdit_from = QtWidgets.QDateEdit(self.tab_my_marks)
        self.dateEdit_from.setGeometry(90, 30, 150, 30)
        self.dateEdit_from.setCalendarPopup(True)
        self.dateEdit_from.setStyleSheet("background-color: white; color: rgb(85, 0, 0);")
        self.dateEdit_from.setDate(QtCore.QDate.currentDate().addMonths(-1))  # По умолчанию - месяц назад
        self._font(self.dateEdit_from, 12)

        self.label_date_to = QtWidgets.QLabel("По:", self.tab_my_marks)
        self.label_date_to.setGeometry(260, 30, 40, 30)
        self.label_date_to.setStyleSheet("color: rgb(85, 0, 0);")
        self._font(self.label_date_to, 15)

        self.dateEdit_to = QtWidgets.QDateEdit(self.tab_my_marks)
        self.dateEdit_to.setGeometry(310, 30, 150, 30)
        self.dateEdit_to.setCalendarPopup(True)
        self.dateEdit_to.setStyleSheet("background-color: white; color: rgb(85, 0, 0);")
        self.dateEdit_to.setDate(QtCore.QDate.currentDate())
        self._font(self.dateEdit_to, 12)

        self.pushButton_release_report = QtWidgets.QPushButton(self.tab_my_marks)
        self.pushButton_release_report.setGeometry(280, 600, 220, 60)
        self.pushButton_release_report.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButton_release_report, 30)
        self.pushButton_release_report.setText("Вывести")
        self.pushButton_release_report.clicked.connect(self.generate_marks_report)

        self.pushButton_observe_mark = QtWidgets.QPushButton(self.tab_my_marks)
        self.pushButton_observe_mark.setGeometry(700, 600, 220, 60)
        self.pushButton_observe_mark.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButton_observe_mark, 25)
        self.pushButton_observe_mark.setText("Просмотреть")

    # ==============================
    # Course screen
    # ==============================
    def _setup_course_frame(self):
        self.frame_course = QtWidgets.QFrame(self.centralwidget)
        self.frame_course.hide()
        self.frame_course.setGeometry(0, 0, 1200, 750)
        self.frame_course.setStyleSheet("background-color: #EFE6DE;")

        self._setup_course_tabs()

    def _setup_course_tabs(self):
        self.tabWidget_course = QtWidgets.QTabWidget(self.frame_course)
        self.tabWidget_course.setGeometry(0, 0, 1200, 750)
        self._font(self.tabWidget_course, 22)
        self.tabWidget_course.setObjectName("tabWidget_course")

        self._setup_main_course_tab()
        self._setup_students_course_tab()
        self._setup_teacher_course_tab()
        self._setup_schedule_course_tab()
        self._setup_application_course_tab()

        self.tabWidget_course.currentChanged.connect(self.course_tables)

        self.tabWidget_course.setStyleSheet("""
                                                     QTabBar::tab {
                                                            width: """ + str(1200 / self.tabWidget_course.count()) + """; 
                                                            height: 50;
                                                            background: rgb(85, 0, 0);
                                                            color: white;
                                                     }
                                                     QTabBar::tab:selected {
                                                         background: rgb(65, 0, 0);
                                                         border-bottom-color: #202020;
                                                     }""")

    def _setup_main_course_tab(self):
        self.tab_main_course = QtWidgets.QWidget()
        self.tabWidget_course.addTab(self.tab_main_course, "")
        self.tabWidget_course.setTabText(self.tabWidget_course.indexOf(self.tab_main_course), "Общее описание")

        self.label_course_name_view = QtWidgets.QLabel(self.tab_main_course)
        self.label_course_name_view.setStyleSheet("color: rgb(85, 0, 0);")
        self._font(self.label_course_name_view, 20)
        self.label_course_name_view.setGeometry(50, 0, 350, 50)
        self.label_course_name_view.setText('Название')

        self.textEdit_course_name = QtWidgets.QLineEdit(self.tab_main_course)
        self.textEdit_course_name.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_course_name, 20)
        self.textEdit_course_name.setGeometry(50, 50, 350, 50)
        self.textEdit_course_name.setReadOnly(True)

        self.label_course_name_view = QtWidgets.QLabel(self.tab_main_course)
        self.label_course_name_view.setStyleSheet("color: rgb(85, 0, 0);")
        self._font(self.label_course_name_view, 20)
        self.label_course_name_view.setGeometry(50, 100, 350, 50)
        self.label_course_name_view.setText('Язык')

        self.textEdit_course_language = QtWidgets.QLineEdit(self.tab_main_course)
        self.textEdit_course_language.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_course_language, 20)
        self.textEdit_course_language.setGeometry(50, 150, 350, 50)
        self.textEdit_course_language.setReadOnly(True)

        self.label_course_name_view = QtWidgets.QLabel(self.tab_main_course)
        self.label_course_name_view.setStyleSheet("color: rgb(85, 0, 0);")
        self._font(self.label_course_name_view, 20)
        self.label_course_name_view.setGeometry(50, 200, 350, 50)
        self.label_course_name_view.setText('Описание')

        self.textEdit_course_description = QtWidgets.QTextEdit(self.tab_main_course)
        self.textEdit_course_description.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_course_description, 20)
        self.textEdit_course_description.setGeometry(50, 250, 780, 400)
        self.textEdit_course_description.setReadOnly(True)

        self.pushButton_leave_the_course_main_course = QtWidgets.QPushButton(self.tab_main_course)
        self.pushButton_leave_the_course_main_course.setGeometry(860, 250, 291, 61)
        self.pushButton_leave_the_course_main_course.setStyleSheet("""
                                                   QPushButton {
                                                       background-color: rgb(85, 0, 0);
                                                       color: white;
                                                       border-radius: 8px;
                                                       padding: 6px;
                                                   }
                                                   QPushButton:hover {
                                                       background-color: rgb(120, 20, 20);
                                                   }
                                                   QPushButton:pressed {
                                                       background-color: rgb(65, 0, 0);
                                                   }
                                                   """)
        self._font(self.pushButton_leave_the_course_main_course, 20)
        self.pushButton_leave_the_course_main_course.setText("Покинуть курс")
        self.pushButton_leave_the_course_main_course.clicked.connect(lambda: self.leave_course(True))

        self.pushButton_back_to_main_from_main_course = QtWidgets.QPushButton(self.tab_main_course)
        self.pushButton_back_to_main_from_main_course.setGeometry(860, 340, 291, 61)
        self.pushButton_back_to_main_from_main_course.setStyleSheet("""
                                           QPushButton {
                                               background-color: rgb(85, 0, 0);
                                               color: white;
                                               border-radius: 8px;
                                               padding: 6px;
                                           }
                                           QPushButton:hover {
                                               background-color: rgb(120, 20, 20);
                                           }
                                           QPushButton:pressed {
                                               background-color: rgb(65, 0, 0);
                                           }
                                           """)
        self._font(self.pushButton_back_to_main_from_main_course, 20)
        self.pushButton_back_to_main_from_main_course.setText("Назад")
        self.pushButton_back_to_main_from_main_course.clicked.connect(self.close_course_info)

        self.pushButton_edit_course = QtWidgets.QPushButton(self.tab_main_course)
        self.pushButton_edit_course.setGeometry(860, 430, 291, 61)
        self.pushButton_edit_course.setStyleSheet("""
                                                   QPushButton {
                                                       background-color: rgb(85, 0, 0);
                                                       color: white;
                                                       border-radius: 8px;
                                                       padding: 6px;
                                                   }
                                                   QPushButton:hover {
                                                       background-color: rgb(120, 20, 20);
                                                   }
                                                   QPushButton:pressed {
                                                       background-color: rgb(65, 0, 0);
                                                   }
                                                   """)
        self._font(self.pushButton_edit_course, 20)
        self.pushButton_edit_course.setText("Редактировать")

    def _setup_students_course_tab(self):
        self.tab_students_course = QtWidgets.QWidget()

        self.table_of_students_course = QtWidgets.QTableWidget(self.tab_students_course)
        self.table_of_students_course.setGeometry(50, 20, 780, 650)
        self.table_of_students_course.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: black;
                font-size: 12px;
                color: black;
            }
            QTableWidget::item {
                border-right: 1px solid black;
                border-bottom: 1px solid black;
            }
            QTableWidget::item:selected {
                background-color: #f8f8f8;
                color: #000;
            }
            QHeaderView::section {
                background-color: rgb(85, 0, 0);
                color: white;
                font-size: 15px;
                border: 1px solid black;
                padding: 4px;
            }
        """)
        header = self.table_of_students_course.horizontalHeader()
        self.table_of_students_course.verticalHeader().setVisible(False)
        self._font(header, 15)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)


        self.pushButtonExcludeStudent = QtWidgets.QPushButton(self.tab_students_course)
        self.pushButtonExcludeStudent.setGeometry(860, 70, 291, 61)
        self.pushButtonExcludeStudent.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButtonExcludeStudent, 28)
        self.pushButtonExcludeStudent.setText("Исключить")

        self.pushButtonMarks = QtWidgets.QPushButton(self.tab_students_course)
        self.pushButtonMarks.setGeometry(860, 160, 291, 61)
        self.pushButtonMarks.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButtonMarks, 28)
        self.pushButtonMarks.setText("Оценки")
        self.pushButtonMarks.clicked.connect(self.observe_marks)

        self.pushButtonObserveProfile = QtWidgets.QPushButton(self.tab_students_course)
        self.pushButtonObserveProfile.setGeometry(860, 250, 291, 61)
        self.pushButtonObserveProfile.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButtonObserveProfile, 20)
        self.pushButtonObserveProfile.setText("Открыть профиль")
        self.pushButtonObserveProfile.clicked.connect(lambda: self.open_profile(self.table_of_students_course, self.frame_course))

        self.pushButton_back_to_main_from_students = QtWidgets.QPushButton(self.tab_students_course)
        self.pushButton_back_to_main_from_students.setGeometry(860, 340, 291, 61)
        self.pushButton_back_to_main_from_students.setStyleSheet("""
                                   QPushButton {
                                       background-color: rgb(85, 0, 0);
                                       color: white;
                                       border-radius: 8px;
                                       padding: 6px;
                                   }
                                   QPushButton:hover {
                                       background-color: rgb(120, 20, 20);
                                   }
                                   QPushButton:pressed {
                                       background-color: rgb(65, 0, 0);
                                   }
                                   """)
        self._font(self.pushButton_back_to_main_from_students, 20)
        self.pushButton_back_to_main_from_students.setText("Назад")
        self.pushButton_back_to_main_from_students.clicked.connect(self.close_course_info)

        self.tabWidget_course.addTab(self.tab_students_course, "")

        self.tabWidget_course.setTabText(self.tabWidget_course.indexOf(self.tab_students_course), "Студенты")

    def _setup_teacher_course_tab(self):
        self.tab_teacher_course = QtWidgets.QWidget()

        self.table_of_teachers_course = QtWidgets.QTableWidget(self.tab_teacher_course)
        self.table_of_teachers_course.setGeometry(50, 20, 1100, 570)
        self.table_of_teachers_course.setStyleSheet("""
            QTableWidget {
                background-color: white;
                gridline-color: black;
                font-size: 12px;
                color: black;
            }
            QTableWidget::item {
                border-right: 1px solid black;
                border-bottom: 1px solid black;
            }
            QTableWidget::item:selected {
                background-color: #f8f8f8;
                color: #000;
            }
            QHeaderView::section {
                background-color: rgb(85, 0, 0);
                color: white;
                font-size: 15px;
                border: 1px solid black;
                padding: 4px;
            }
        """)
        header = self.table_of_teachers_course.horizontalHeader()
        self._font(header, 15)
        self.table_of_teachers_course.verticalHeader().setVisible(False)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.pushButton_back_to_main_from_teachers = QtWidgets.QPushButton(self.tab_teacher_course)
        self.pushButton_back_to_main_from_teachers.setGeometry(355, 600, 220, 60)
        self.pushButton_back_to_main_from_teachers.setStyleSheet("""
                                           QPushButton {
                                               background-color: rgb(85, 0, 0);
                                               color: white;
                                               border-radius: 8px;
                                               padding: 6px;
                                           }
                                           QPushButton:hover {
                                               background-color: rgb(120, 20, 20);
                                           }
                                           QPushButton:pressed {
                                               background-color: rgb(65, 0, 0);
                                           }
                                           """)
        self._font(self.pushButton_back_to_main_from_teachers, 30)
        self.pushButton_back_to_main_from_teachers.setText("Назад")
        self.pushButton_back_to_main_from_teachers.clicked.connect(self.close_course_info)

        self.pushButton_open_profile_teachers = QtWidgets.QPushButton(self.tab_teacher_course)
        self.pushButton_open_profile_teachers.setGeometry(625, 600, 220, 60)
        self.pushButton_open_profile_teachers.setStyleSheet("""
                                                   QPushButton {
                                                       background-color: rgb(85, 0, 0);
                                                       color: white;
                                                       border-radius: 8px;
                                                       padding: 6px;
                                                   }
                                                   QPushButton:hover {
                                                       background-color: rgb(120, 20, 20);
                                                   }
                                                   QPushButton:pressed {
                                                       background-color: rgb(65, 0, 0);
                                                   }
                                                   """)
        self._font(self.pushButton_open_profile_teachers, 18)
        self.pushButton_open_profile_teachers.setText("Открыть профиль")
        self.pushButton_open_profile_teachers.clicked.connect(lambda: self.open_profile(self.table_of_teachers_course, self.frame_course))

        self.tabWidget_course.addTab(self.tab_teacher_course, "")

        self.tabWidget_course.setTabText(self.tabWidget_course.indexOf(self.tab_teacher_course), "Преподаватели")

    def _setup_schedule_course_tab(self):
        self.tab_schedule_course = QtWidgets.QWidget()

        self.schedule_calendar = QtWidgets.QCalendarWidget(self.tab_schedule_course)
        self.schedule_calendar.setGeometry(45, 40, 780, 620)
        self._font(self.schedule_calendar, 15)
        self.schedule_calendar.setStyleSheet("""
QCalendarWidget {
    background-color: #ffffff;
    border: 1px solid #dcdcdc;
    border-radius: 8px;
}

QCalendarWidget QWidget#qt_calendar_navigationbar {
    background-color: rgb(85, 0, 0);
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
}

QCalendarWidget QToolButton {
    color: white;
    font-weight: bold;
    background-color: transparent;
    border: none;
    margin: 5px;
    padding: 5px;
}

QCalendarWidget QToolButton:hover {
    background-color: rgba(255, 255, 255, 0.2);
    border-radius: 5px;
}

QCalendarWidget QWidget {
    alternate-background-color: #f7f7f7; 
}

QCalendarWidget QAbstractItemView:enabled {
    color: #333;  
    selection-background-color: #4a90e2; 
    selection-color: white;
    outline: 0;
}

QCalendarWidget QAbstractItemView:disabled {
    color: #bbbbbb;
}

QHeaderView {
    background-color: transparent;
}

QCalendarWidget QMenu {
    background-color: #f2e9e1; 
    border: 1px solid #4a0000; 
    color: #4a0000;            
    font-family: "BabyPop";  
    font-size: 14px;
}

QCalendarWidget QMenu::item {
    padding: 5px 20px;
    background-color: transparent;
}

QCalendarWidget QMenu::item:selected {
    background-color: #4a0000; /* Цвет выделения */
    color: #ffffff;            /* Цвет текста при выделении */
}

QCalendarWidget QAbstractItemView {
    background-color: #f2e9e1;
    selection-background-color: #4a0000;
    selection-color: white;
    selection-border: 0px;
}
                """)

        self.schedule_calendar.clicked.connect(self.manage_schedule_for_date)

        self.pushButton_back_to_main_from_schedule = QtWidgets.QPushButton(self.tab_schedule_course)
        self.pushButton_back_to_main_from_schedule.setGeometry(860, 340, 291,
                                                               61)  # Переместил кнопку вправо, как на других вкладках
        self.pushButton_back_to_main_from_schedule.setStyleSheet("""
                    QPushButton { background-color: rgb(85, 0, 0); color: white; border-radius: 8px; padding: 6px; }
                    QPushButton:hover { background-color: rgb(120, 20, 20); }
                    QPushButton:pressed { background-color: rgb(65, 0, 0); }
                """)
        self._font(self.pushButton_back_to_main_from_schedule, 28)
        self.pushButton_back_to_main_from_schedule.setText("Назад")
        self.pushButton_back_to_main_from_schedule.clicked.connect(self.close_course_info)

        self.tabWidget_course.addTab(self.tab_schedule_course, "")
        self.tabWidget_course.setTabText(self.tabWidget_course.indexOf(self.tab_schedule_course), "Расписание")

    def _setup_application_course_tab(self):
        self.tab_application = QtWidgets.QWidget()

        self.application_tabs = QtWidgets.QTabWidget(self.tab_application)
        self.application_tabs.setGeometry(45, 40, 800, 600)
        self._font(self.application_tabs, 22)
        self.application_tabs.setObjectName("application_tabs")

        self.student_application_tab = QtWidgets.QWidget()
        self.application_tabs.addTab(self.student_application_tab, "")
        self.application_tabs.setTabText(self.application_tabs.indexOf(self.student_application_tab), "Студенты")

        self.teacher_application_tab = QtWidgets.QWidget()
        self.application_tabs.addTab(self.teacher_application_tab, "")
        self.application_tabs.setTabText(self.application_tabs.indexOf(self.teacher_application_tab), "Преподаватели")

        self.application_tabs.setStyleSheet("""
                                                     QTabBar::tab {
                                                            width: """ + str(800 / self.application_tabs.count()) + """; 
                                                            height: 50;
                                                            background: rgb(85, 0, 0);
                                                            color: white;
                                                     }
                                                     QTabBar::tab:selected {
                                                         background: rgb(65, 0, 0);
                                                         border-bottom-color: #202020;
                                                     }""")

        self.student_application_list = QtWidgets.QTableWidget(self.student_application_tab)
        self.student_application_list.setGeometry(0, 0, 800, 600)
        self._font(self.student_application_list, 28)
        self.student_application_list.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header = self.student_application_list.horizontalHeader()
        self._font(header, 20)
        self.student_application_list.verticalHeader().setVisible(False)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.teacher_application_list = QtWidgets.QTableWidget(self.teacher_application_tab)
        self.teacher_application_list.setGeometry(0, 0, 800, 600)
        self._font(self.teacher_application_list, 28)
        self.teacher_application_list.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header = self.teacher_application_list.horizontalHeader()
        self._font(header, 20)
        self.teacher_application_list.verticalHeader().setVisible(False)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.pushButton_open_application = QtWidgets.QPushButton(self.tab_application)
        self.pushButton_open_application.setGeometry(860, 70, 291, 61)
        self.pushButton_open_application.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButton_open_application, 28)
        self.pushButton_open_application.setText("Открыть")
        self.pushButton_open_application.clicked.connect(lambda: self.open_application_dialog(self.student_application_list))

        self.application_tabs.currentChanged.connect(lambda:(
            self.course_tables(),
            self.pushButton_open_application.disconnect(),
            self.pushButton_open_application.clicked.connect(lambda: self.open_application_dialog(self.student_application_list if self.application_tabs.currentIndex()==0 else self.teacher_application_list))
        )
                                             )

        self.pushButton_back_to_main_from_application = QtWidgets.QPushButton(self.tab_application)
        self.pushButton_back_to_main_from_application.setGeometry(860, 160, 291, 61)
        self.pushButton_back_to_main_from_application.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButton_back_to_main_from_application, 28)
        self.pushButton_back_to_main_from_application.setText("Назад")
        self.pushButton_back_to_main_from_application.clicked.connect(self.close_course_info)
    # ==============================
    # View profile screen
    # ==============================
    def _setup_view_profile_frame(self):
        self.frame_view_profile = QtWidgets.QFrame(self.centralwidget)
        self.frame_view_profile.hide()
        self.frame_view_profile.setGeometry(0, 0, 1200, 750)
        self.frame_view_profile.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_view_profile.setStyleSheet("background-color: #EFE6DE;")
        self.frame_view_profile.setObjectName("frame_view_profile")

        self.avatar_view_profile = QtWidgets.QLabel(self.frame_view_profile)
        self.avatar_view_profile.setGeometry(110, 70, 300, 300)
        self.avatar_view_profile.setScaledContents(True)

        self.pushButton_back_from_view_profile = QtWidgets.QPushButton(self.frame_view_profile)
        self.pushButton_back_from_view_profile.setGeometry(490, 675, 220, 60)
        self.pushButton_back_from_view_profile.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButton_back_from_view_profile, 30)
        self.pushButton_back_from_view_profile.setText("Назад")
        self.pushButton_back_from_view_profile.clicked.connect(lambda: self.switch_forms(first=self.frame_view_profile))

        self.table_of_contacts_view_profile = QtWidgets.QTableWidget(self.frame_view_profile)
        self.table_of_contacts_view_profile.setGeometry(640, 210, 510, 175)
        self.table_of_contacts_view_profile.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        gridline-color: black;
                        font-size: 12px;
                        color: black;
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        self.table_of_contacts_view_profile.verticalHeader().setVisible(False)
        header_с = self.table_of_contacts_view_profile.horizontalHeader()
        self._font(header_с, 15)
        header_с.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self.table_of_language_view_profile = QtWidgets.QTableWidget(self.frame_view_profile)
        self.table_of_language_view_profile.setGeometry(80, 560, 330, 95)
        self.table_of_language_view_profile.setStyleSheet("""
                            QTableWidget {
                                background-color: white;
                                gridline-color: black;
                                font-size: 12px;
                                color: black;
                            }
                            QTableWidget::item {
                                border-right: 1px solid black;
                                border-bottom: 1px solid black;
                            }
                            QTableWidget::item:selected {
                                background-color: #f8f8f8;
                                color: #000;
                            }
                            QHeaderView::section {
                                background-color: rgb(85, 0, 0);
                                color: white;
                                font-size: 15px;
                                border: 1px solid black;
                                padding: 4px;
                            }
                        """)
        self.table_of_language_view_profile.verticalHeader().setVisible(False)
        header_t = self.table_of_language_view_profile.horizontalHeader()
        self._font(header_t, 15)
        header_t.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)

        self._create_view_profile_outputs()
        self._create_view_profile_labels()

    def _create_view_profile_labels(self):
        self.label_photo_output = QtWidgets.QLabel(self.frame_view_profile)
        self.label_photo_output.setGeometry(130, 30, 95, 30)
        self._font(self.label_photo_output, 30)
        self.label_photo_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_photo_output.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_photo_output.setText("Фото")

        self.label_FIO_output = QtWidgets.QLabel("", self.frame_view_profile)
        self.label_FIO_output.setGeometry(450, 70, 170, 50)
        self._font(self.label_FIO_output, 30)
        self.label_FIO_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_FIO_output.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_FIO_output.setText("ФИО")

        self.label_role_output = QtWidgets.QLabel(self.frame_view_profile)
        self.label_role_output.setGeometry(450, 140, 170, 50)
        self._font(self.label_role_output, 30)
        self.label_role_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_role_output.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_role_output.setText("Роль")

        self.label_contacts_output = QtWidgets.QLabel(self.frame_view_profile)
        self.label_contacts_output.setGeometry(450, 210, 170, 50)
        self._font(self.label_contacts_output, 30)
        self.label_contacts_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_contacts_output.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_contacts_output.setText("Контакты")

        self.label_country_output = QtWidgets.QLabel(self.frame_view_profile)
        self.label_country_output.setGeometry(80, 430, 100, 30)
        self._font(self.label_country_output, 20)
        self.label_country_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_country_output.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_country_output.setText("Страна")

        self.label_age_output = QtWidgets.QLabel(self.frame_view_profile)
        self.label_age_output.setGeometry(80, 480, 100, 30)
        self._font(self.label_age_output, 20)
        self.label_age_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_age_output.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_age_output.setText("Возраст")

        self.label_education_output = QtWidgets.QLabel(self.frame_view_profile)
        self.label_education_output.setGeometry(80, 480, 160, 30)
        self._font(self.label_education_output, 20)
        self.label_education_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_education_output.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_education_output.setText("Образование")

        self.label_language_output = QtWidgets.QLabel(self.frame_view_profile)
        self.label_language_output.setGeometry(80, 530, 65, 30)
        self._font(self.label_language_output, 20)
        self.label_language_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_language_output.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_language_output.setText("Язык")

        self.label_description_output = QtWidgets.QLabel(self.frame_view_profile)
        self.label_description_output.setGeometry(450, 380, 145, 50)
        self._font(self.label_description_output, 25)
        self.label_description_output.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_description_output.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_description_output.setText("Описание")

    def _create_view_profile_outputs(self):

        self.output_FIO = QtWidgets.QLineEdit(self.frame_view_profile)
        self.output_FIO.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.output_FIO, 15)
        self.output_FIO.setGeometry(640, 70, 510, 50)
        self.output_FIO.setReadOnly(True)

        self.output_roles = QtWidgets.QLineEdit(self.frame_view_profile)
        self.output_roles.setGeometry(640, 140, 510, 50)
        self._font(self.output_roles, 26)
        self.output_roles.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self.output_roles.setReadOnly(True)

        self.output_country = QtWidgets.QLineEdit(self.frame_view_profile)
        self.output_country.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.output_country, 15)
        self.output_country.setGeometry(190, 430, 220, 30)
        self.output_country.setReadOnly(True)

        self.output_age = QtWidgets.QLineEdit(self.frame_view_profile)
        self.output_age.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.output_age, 15)
        self.output_age.setGeometry(190, 480, 220, 30)
        self.output_age.setReadOnly(True)

        self.pushButtonDownloadEducation = QtWidgets.QPushButton(self.frame_view_profile)
        self._font(self.pushButtonDownloadEducation, 15)
        self.pushButtonDownloadEducation.setGeometry(250, 480, 160, 30)
        self.pushButtonDownloadEducation.setText("Скачать")
        self.pushButtonDownloadEducation.clicked.connect(self.download_file)
        self.pushButtonDownloadEducation.setStyleSheet("QPushButton {background-color: #cccccc; border: none; color: #808080}")

        self.output_description = QtWidgets.QTextEdit(self.frame_view_profile)
        self.output_description.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.output_description, 15)
        self.output_description.setGeometry(450, 430, 700, 225)
        self.output_description.setReadOnly(True)

    # ==============================
    # Course creation screen
    # ==============================

    def _setup_course_creation_frame(self):
        self.frame_course_creation = QtWidgets.QFrame(self.centralwidget)
        self.frame_course_creation.setGeometry(0, 0, 1200, 750)
        self.frame_course_creation.hide()
        self.frame_course_creation.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_course_creation.setStyleSheet("background-color: #EFE6DE;")
        self.frame_course_creation.setObjectName("frame_course_creation")

        self.pushButton_acceptence_creation = QtWidgets.QPushButton(self.frame_course_creation)
        self.pushButton_acceptence_creation.setGeometry(340, 675, 220, 60)
        self.pushButton_acceptence_creation.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButton_acceptence_creation, 30)
        self.pushButton_acceptence_creation.setText("Принять")
        self.pushButton_acceptence_creation.clicked.connect(self.add_course)

        self.pushButton_back_creation = QtWidgets.QPushButton(self.frame_course_creation)
        self.pushButton_back_creation.setGeometry(640, 675, 220, 60)
        self.pushButton_back_creation.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButton_back_creation, 30)
        self.pushButton_back_creation.setText("Назад")
        self.pushButton_back_creation.clicked.connect(lambda: self.switch_forms(self.frame_course_creation, self.frame_main))

        self._create_course_cr_labels()
        self._create_course_cr_inputs()

    def _create_course_cr_labels(self):
        self.label_course_name = QtWidgets.QLabel("", self.frame_course_creation)
        self.label_course_name.setGeometry(100, 50, 165, 50)
        self._font(self.label_course_name, 30)
        self.label_course_name.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_course_name.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_course_name.setText("Название")

        self.label_language = QtWidgets.QLabel(self.frame_course_creation)
        self.label_language.setGeometry(100, 175, 165, 50)
        self._font(self.label_language, 30)
        self.label_language.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_language.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_language.setText("Язык")

        self.label_course_description = QtWidgets.QLabel(self.frame_course_creation)
        self.label_course_description.setGeometry(100, 280, 175, 50)
        self._font(self.label_course_description, 30)
        self.label_course_description.setStyleSheet("color: rgb(85, 0, 0);")
        self.label_course_description.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.label_course_description.setText("Описание")

    def _create_course_cr_inputs(self):
        self.textEdit_course_name_creation = QtWidgets.QLineEdit(self.frame_course_creation)
        self.textEdit_course_name_creation.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_course_name_creation, 15)
        self.textEdit_course_name_creation.setGeometry(300, 50, 800, 50)

        self.comboBox_language = QtWidgets.QComboBox(self.frame_course_creation)
        self.comboBox_language.setGeometry(300, 175, 800, 50)
        self._font(self.comboBox_language, 26)
        self.comboBox_language.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")

        self.textEdit_course_description_creation = QtWidgets.QTextEdit(self.frame_course_creation)
        self.textEdit_course_description_creation.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")
        self._font(self.textEdit_course_description_creation, 15)
        self.textEdit_course_description_creation.setGeometry(100, 350, 1000, 300)

    # ==============================
    # Language screen
    # ==============================

    def _setup_language_frame(self):
        self.frame_language = QtWidgets.QFrame(self.centralwidget)
        self.frame_language.setGeometry(0, 0, 1200, 750)
        self.frame_language.hide()
        self.frame_language.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_language.setStyleSheet("background-color: #EFE6DE;")
        self.frame_language.setObjectName("frame_language")

        self.current_language_id = None

        self.pushButton_save_language = QtWidgets.QPushButton(self.frame_language)
        self.pushButton_save_language.setGeometry(350, 675, 220, 60)
        self.pushButton_save_language.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButton_save_language, 25)
        self.pushButton_save_language.setText("Сохранить")
        self.pushButton_save_language.clicked.connect(self.save_language_logic)

        self.pushButton_delete_language = QtWidgets.QPushButton(self.frame_language)
        self.pushButton_delete_language.setGeometry(600, 675, 220, 60)
        self.pushButton_delete_language.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButton_delete_language, 25)
        self.pushButton_delete_language.setText("Удалить")
        self.pushButton_delete_language.clicked.connect(self.delete_current_language)
        self.pushButton_delete_language.hide()

        self.label_language_name = QtWidgets.QLabel("Название", self.frame_language)
        self.label_language_name.setGeometry(100, 50, 165, 50)
        self._font(self.label_language_name, 30)
        self.label_language_name.setStyleSheet("color: rgb(85, 0, 0);")

        self.textEdit_language_name = QtWidgets.QLineEdit(self.frame_language)
        self.textEdit_language_name.setGeometry(300, 50, 800, 50)
        self._font(self.textEdit_language_name, 15)
        self.textEdit_language_name.setStyleSheet("background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);")

        self.label_language_level = QtWidgets.QLabel("Уровни", self.frame_language)
        self.label_language_level.setGeometry(100, 200, 165, 50)
        self._font(self.label_language_level, 30)
        self.label_language_level.setStyleSheet("color: rgb(85, 0, 0);")

        self.table_of_levels_model = QtGui.QStandardItemModel(0, 1)
        self.table_of_levels = QtWidgets.QTableView(self.frame_language)
        self.table_of_levels.setModel(self.table_of_levels_model)
        self.table_of_levels.setGeometry(125, 275, 800, 350)
        self.table_of_levels.setStyleSheet("""
                            QTableView {
                                background-color: white;
                                font-size: 12px;
                                color: black;
                                border: 5px solid black
                            }
                            QTableView::item {
                                border-right: 1px solid black;
                                border-bottom: 1px solid black;
                            }
                            QTableView::item:selected {
                                background-color: #f8f8f8;
                                color: #000;
                            }
                            QHeaderView::section {
                                background-color: rgb(85, 0, 0);
                                color: white;
                                font-size: 15px;
                                border: 1px solid black;
                                padding: 4px;
                            }
                        """)
        self.table_of_levels.horizontalHeader().setSectionResizeMode(
            self.table_of_levels.horizontalHeader().ResizeMode.Stretch)
        self.table_of_levels.verticalHeader().setVisible(False)
        self.table_of_levels.horizontalHeader().setVisible(False)

        self.pushButtonAddLevel = QtWidgets.QPushButton("Добавить уровень", self.frame_language)
        self.pushButtonAddLevel.setGeometry(950, 300, 200, 50)
        self.pushButtonAddLevel.clicked.connect(lambda: self.add_level(self.table_of_levels_model))

        self.pushButtonEditLevel = QtWidgets.QPushButton("Изменить уровень", self.frame_language)
        self.pushButtonEditLevel.setGeometry(950, 375, 200, 50)
        self.pushButtonEditLevel.clicked.connect(
            lambda: self.edit_level(self.table_of_levels, self.table_of_levels_model))

        self.pushButtonDeleteLevel = QtWidgets.QPushButton("Удалить уровень", self.frame_language)
        self.pushButtonDeleteLevel.setGeometry(950, 450, 200, 50)
        self.pushButtonDeleteLevel.clicked.connect(
            lambda: self.delete_level(self.table_of_levels, self.table_of_levels_model))

        for btn in [self.pushButtonAddLevel, self.pushButtonEditLevel, self.pushButtonDeleteLevel]:
            self._font(btn, 14)
            btn.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)

    # ==============================
    # Marks screen
    # ==============================

    def _setup_marks_frame(self):
        self.frame_mark = QtWidgets.QFrame(self.centralwidget)
        self.frame_mark.setGeometry(0, 0, 1200, 750)
        self.frame_mark.hide()
        self.frame_mark.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_mark.setStyleSheet("background-color: #EFE6DE;")
        self.frame_mark.setObjectName("frame_mark")

        self.pushButton_back_to_course = QtWidgets.QPushButton(self.frame_mark)
        self.pushButton_back_to_course.setGeometry(490, 675, 220, 60)
        self.pushButton_back_to_course.setStyleSheet("""
        QPushButton {
            background-color: rgb(85, 0, 0);
            color: white;
            border-radius: 8px;
            padding: 6px;
        }
        QPushButton:hover {
            background-color: rgb(120, 20, 20);
        }
        QPushButton:pressed {
            background-color: rgb(65, 0, 0);
        }
        """)
        self._font(self.pushButton_back_to_course, 30)
        self.pushButton_back_to_course.setText("Назад")
        self.pushButton_back_to_course.clicked.connect(lambda: self.switch_forms(self.frame_mark, self.frame_course))

        self.pushButtonAddMark = QtWidgets.QPushButton(self.frame_mark)
        self.pushButtonAddMark.setGeometry(860, 70, 291, 61)
        self.pushButtonAddMark.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButtonAddMark, 28)
        self.pushButtonAddMark.setText("Добавить")
        self.pushButtonAddMark.clicked.connect(self.add_mark)

        self.pushButtonEditMark = QtWidgets.QPushButton(self.frame_mark)
        self.pushButtonEditMark.setGeometry(860, 160, 291, 61)
        self.pushButtonEditMark.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButtonEditMark, 28)
        self.pushButtonEditMark.setText("Изменить")
        self.pushButtonEditMark.clicked.connect(self.edit_mark)

        self.pushButtonDeleteMark = QtWidgets.QPushButton(self.frame_mark)
        self.pushButtonDeleteMark.setGeometry(860, 250, 291, 61)
        self.pushButtonDeleteMark.setStyleSheet("""
                QPushButton {
                    background-color: rgb(85, 0, 0);
                    color: white;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: rgb(120, 20, 20);
                }
                QPushButton:pressed {
                    background-color: rgb(65, 0, 0);
                }
                """)
        self._font(self.pushButtonDeleteMark, 28)
        self.pushButtonDeleteMark.setText("Удалить")
        self.pushButtonDeleteMark.clicked.connect(self.delete_mark)

        self.table_of_marks = QtWidgets.QTableWidget(self.frame_mark)
        self.table_of_marks.setGeometry(100, 45, 700, 600)
        self._font(self.table_of_marks, 30)
        self.table_of_marks.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        font-size: 12px;
                        color: black;
                        border: 5px solid black
                    }
                    QTableWidget::item {
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;
                    }
                    QTableWidget::item:selected {
                        background-color: #f8f8f8;
                        color: #000;
                    }
                    QHeaderView::section {
                        background-color: rgb(85, 0, 0);
                        color: white;
                        font-size: 15px;
                        border: 1px solid black;
                        padding: 4px;
                    }
                """)
        header = self.table_of_marks.horizontalHeader()
        self._font(header, 20)
        self.table_of_marks.verticalHeader().setVisible(False)
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)


if __name__ == "__main__":
    import sys

    init_db()
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    ui = Program_Ui()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec())