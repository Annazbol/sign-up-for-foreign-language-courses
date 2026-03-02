from connection import get_db_connection
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtCore import Qt
import traceback

def fetch_all(query, values=(), with_description=False):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(query, values)
        f = cur.fetchall()
        desc = cur.description
        if f:
            rows = [tuple(k.values()) for k in f]
        else:
            rows = None
        cur.close()
        conn.close()
        if not(with_description):
            return rows
        else:
            return rows, desc
    except Exception as e:
        print(e)
        traceback.print_exc()

def fetch_one(table_name, column, value):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE {column} = %s"
        cur.execute(query, (value,))
        f = cur.fetchone()
        if f:
            result = tuple(f.values())
        else:
            result = None
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        traceback.print_exc()

def fetch_cell(table_name, column, value, primary_key):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"SELECT {column} FROM {table_name} WHERE {primary_key} = %s"
        cur.execute(query, (value,))
        f = cur.fetchone()
        if f:
            result = tuple(f.values())[0]
        else:
            result = None
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(e)
        traceback.print_exc()

def insert_row(table, values):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cols = ", ".join(f"`{col}`" for col in values.keys())
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders});"
        cur.execute(query, list(values.values()))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        traceback.print_exc()

def update_row(table, record_id, values, primary_key):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        set_clause = ", ".join([f"{col} = %s" for col in values.keys()])
        query = f"UPDATE `{table}` SET {set_clause} WHERE `{primary_key}` = %s"
        params = list(values.values()) + [record_id]
        cur.execute(query, params)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        traceback.print_exc()

def delete_row(table, record_id, primary_key):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = f"DELETE FROM `{table}` WHERE `{primary_key}` = %s"
        cur.execute(query, (record_id,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        traceback.print_exc()

def get_row_count(table_name):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*) AS cnt FROM `{table_name}`")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result["cnt"]
    except Exception as e:
        print(e)
        traceback.print_exc()

def get_new_id(table_name, id_name):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT COALESCE(MAX({id_name}), 0) + 1 AS new_id FROM {table_name}")
        result = cur.fetchone()["new_id"]
        return result
    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def reload_table(table_widget, query, columns=None, values=(), show_pk=False):
    try:
        rows, desc = fetch_all(query, values, True)

        # Очищаем таблицу перед обновлением
        table_widget.clearContents()
        table_widget.setRowCount(0)
        if not columns and desc:
            all_db_columns = [d[0] for d in desc]
            if show_pk:
                columns = all_db_columns
            else:
                columns = all_db_columns[1:]
        if columns:
            display_cols_count = len(columns)
            table_widget.setColumnCount(display_cols_count)
            table_widget.setHorizontalHeaderLabels(columns)
        else:
            display_cols_count = 0
        if not rows:
            return
        table_widget.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            pk = row_data[0]

            for col_idx in range(display_cols_count):
                db_idx = col_idx if show_pk else col_idx + 1

                if db_idx < len(row_data):
                    item_value = row_data[db_idx]
                    item = QTableWidgetItem(str(item_value) if item_value is not None else "")
                    if col_idx == 0:
                        item.setData(Qt.ItemDataRole.UserRole, pk)

                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

                    font = QFont()
                    font.setFamily("BabyPop (Kerning sherbackoffale")
                    font.setPointSize(15)
                    item.setFont(font)

                    table_widget.setItem(row_idx, col_idx, item)

    except Exception as e:
        print(f"Ошибка в reload_table: {e}")
        traceback.print_exc()

def reload_line(line_widget, table_name, column, primary_key, key_value):
    try:
        value = fetch_cell(table_name=table_name, column=column, value=key_value, primary_key=primary_key)
        line_widget.clear()
        line_widget.setText(str(value))
    except Exception as e:
        print(e)
        traceback.print_exc()

def reload_image(image_widget, table_name, column, primary_key, key_value):
    try:
        image_blob = fetch_cell(table_name=table_name, column=column, value=key_value, primary_key=primary_key)
        if not image_blob:
            image_widget.clear()
            return
        image_widget.show()
        pixmap = QPixmap()
        if not pixmap.loadFromData(image_blob):
            image_widget.clear()
            return

        image_widget.setPixmap(pixmap)
    except Exception as e:
        print(e)
        traceback.print_exc()