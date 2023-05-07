from humancursor.system_cursor import SystemCursor

cursor = SystemCursor()


def start_sys_demo():
    for _ in range(2):
        cursor.move_to([200, 200])
        cursor.move_to([800, 200])
        cursor.move_to([500, 800])
        cursor.move_to([1400, 800])
