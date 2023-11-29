from humancursor.HCS_files.cursor_collector import MouseTracker

mouse_coordinates, file_name, file_destination = MouseTracker()()

# [] are just movements
# () are clicks
# [(), ()] are drag and drops

imports = '# Importing SystemCursor from humancursor package\nfrom humancursor import SystemCursor\n\n'


cursor = '# Initializing the SystemCursor object\ncursor = SystemCursor()\n\n'

code = '# Script Recorded: \n\n'

for coordinate in mouse_coordinates:
    if isinstance(coordinate, tuple):
        code += f'cursor.click_on({coordinate}, clicks=1, click_duration=0, steady=False)\n'
    elif isinstance(coordinate[0], int):
        code += f'cursor.move_to({coordinate}, duration=None, steady=False)\n'
    else:
        code += f'cursor.drag_and_drop({coordinate[0]}, {coordinate[1]}, duration=None, steady=False)\n'

end = '\n# End\n\n'
try:
    script_file = file_destination + '\\' + file_name + '.py'
    try:
        with open(script_file, 'w') as file:
            file.write(imports + cursor + code + end)
    except FileNotFoundError:
        print('File Not Found')
except TypeError:
    pass
