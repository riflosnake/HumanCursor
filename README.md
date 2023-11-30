# HumanCursor: A Python package for simulating human mouse movements

<div style="display:flex;flex-direction:row;">
  <img src="https://user-images.githubusercontent.com/108073687/234356166-719efddc-4618-4d32-b40e-2055d17b3edd.jpg" width="40%" height="300">
  <img src="https://media.giphy.com/media/D2D9BfjscHEG1DzBKu/giphy.gif" width="45%" height="300">
</div>

_**HumanCursor**_ is a Python package that allows you to _**simulate realistic human mouse movements**_ on the web and the system. It can be used for _**automating scripts**_ that require mouse interactions, such as _**web scraping**_, _**automated tasks**_, _**testing**_, or _**gaming**_.

# Content:

- [Features](#features)
- [Requirements](#requirements)
- [How to install](#installation)
- [How to use](#usage)
  - [HCScripter](#hcscripter)
  - [WebCursor](#webcursor)
  - [SystemCursor](#systemcursor)
- [Demonstration](#demonstration)

# Features

- HumanCursor uses a `natural motion algorithm` that mimics the way `humans` move the mouse cursor, with `variable speed`, `acceleration`, and `curvature`.
- Can perform various mouse actions, such as `clicking`, `dragging`, `scrolling`, and `hovering`.
- Designed specifically to `bypass security measures and bot detection software`.
- Includes:
    - 🚀 `HCScripter` app to create physical cursor automated scripts without coding.
    - 🌐 `WebCursor` module for web cursor code automation.
        - Fully supported for `Chrome` and `Edge`, not optimal/tested for Firefox and Safari, using `Selenium`.
    - 🤖 `SystemCursor` module for physical cursor code automation.
    

# Requirements

- ```Python >= 3.7```
  - [Download the installer](https://www.python.org/downloads/), run it and follow the steps.
  - Make sure to check the box that says `Add Python to PATH` during installation.
  - Reboot computer.

# Installation

To install, you can use pip:

    pip install --upgrade humancursor

# Usage

## HCScripter

To quickly create an automated system script, you can use `HCScripter`, which registers mouse actions from point to point using key commands and creates a script file for you.

After installing `humancursor` package, open up `terminal/powershell` and just copy paste this command which runs `launch.py` file inside the folder named `HCScripter` of `humancursor` package:

```powershell
python -m humancursor.HCScripter.launch
```

#### A window will show up looking like this:

<img width="270" alt="Screenshot 2023-11-29 165810" src="https://github.com/riflosnake/HumanCursor/assets/108073687/bc162443-1390-44fd-9dd9-69a8e0a9953b">

Firstly, you can specify the `name` of the python file which will contain the script and choose the `location` where that file should be saved.

Then, you can turn on movement listener by pressing the `ON/OFF` button, where it will start registering your movements, by these commands below:

- Press `Z` -> `Move`
- Press `CTRL` -> `Click`
- Press and hold `CTRL` -> `Drag and drop`

After completing your script, press `Finish` button and the script file .py should be ready to go!

## WebCursor

To use HumanCursor for Web, you need to import the `WebCursor` class, and create an instance:

```python
from humancursor import WebCursor

cursor = WebCursor(driver)
```

Then, you can use the following methods to simulate mouse movements and actions:

- `cursor.move_to()`: Moves the mouse cursor to the element or location on the webpage.
- `cursor.click_on()`: Clicks on the element or location on the webpage.
- `cursor.drag_and_drop()`: Drags the mouse cursor from one element and drops it to another element on the screen.
- `cursor.move_by_offset()`: Moves the cursor by x and y pixels.
- `cursor.control_scroll_bar()`: Sets the scroll bar to a certain level, can be a volume, playback slider or anything. Level is set by float number from 0 to 1, meaning fullness
- `cursor.scroll_into_view_of_element()`: Scrolls into view of element if not already there, it is called automatically from above functions.

These functions can accept as destination, either the `WebElement` itself, or a `list of 'x' and 'y' coordinates`.

Some parameters explained:

- `relative_position`: Takes a list of x and y percentages as floats from 0 to 1, which indicate the exact position by width and height inside an element
                                       for example, if you set it to [0.5, 0.5], it will move the cursor to the center of the element.
- `absolute_offset`: If you input a list of coordinates instead of webelement, if you turn this to True, the coordinates will be interpreted as absolute movement by pixels, and not like coordinates in the webpage.
- `steady`: Tries to make movement in straight line, mimicking human, if set to True


## SystemCursor
<div style="display:flex;flex-direction:row;">
  <img src="https://media.giphy.com/media/U9Y3uFwjVlCzoB4HJX/giphy.gif" width="30%" height="280">
  <img src="https://media.giphy.com/media/D7geMT10Eatk2X2DUF/giphy.gif" width="30%" height="280">
  <img src="https://media.giphy.com/media/J3DyvU4raVEGvFiDjg/giphy.gif" width="30%" height="280">
</div>
To use HumanCursor for your system mouse, you need to import the `SystemCursor` class, and create an instance just like we did above:

```python
from humancursor import SystemCursor

cursor = SystemCursor()
```

The `SystemCursor` class, which should be used for controlling the system mouse (with pyautogui), only inherits the `move_to()`, `click_on()` and `drag_and_drop` functions, accepting only the list of 'x' and 'y' coordinates as input, as there are no elements available.


# DEMONSTRATION:
To quickly check how the cursor moves, you can do this:

#### SystemCursor
  ```powershell
    python -m humancursor.test.system
  ```
#### WebCursor
  ```powershell
    python -m humancursor.test.web
  ```

#### Some code examples:

```python
cursor.move_to(element)  # moves to element 
cursor.move_to(element, relative_position=[0.5, 0.5])  # moves to the center of the element
cursor.move_to([450, 600])  # moves to coordinates relative to viewport x: 450, y: 600
cursor.move_to([450, 600], absolute_offset=True)  # moves 450 pixels to the right and 600 pixels down

cursor.move_by_offset(200, 170)  # moves 200 pixels to the right and 170 pixels down
cursor.move_by_offset(-10, -20)  # moves 10 pixels to the left and 20 pixels up

cursor.click_on([170, 390])  # clicks on coordinates relative to viewport x: 170, y: 390
cursor.click_on(element, relative_position=[0.2, 0.5])  # clicks on 0.2 x width, 0.5 x height position of the element.
cursor.click_on(element, click_duration=1.7) # clicks and holds on element for 1.7 seconds

cursor.drag_and_drop(element1, element2)  # clicks and hold on first element, and moves to and releases on the second
cursor.drag_and_drop(element, [640, 320], drag_from_relative_position=[0.9, 0.9])  # drags from element on 0.9 x width, 0.9 x  height (far bottom right corner) and moves to and releases to coordinates relative to viewport x: 640, y: 320

cursor.control_scroll_bar(element, amount_by_percentage=0.75)  # sets a slider to 75% full
cursor.controll_scroll_bar(element, amount_by_percentage=0.2, orientation='vertical')  # sets a vertical slider to 20% full

cursor.scroll_into_view_of_element(element)  # scrolls into view of element if not already in it
cursor.show_cursor()  # injects javascript that will display a red dot over the cursor on webpage. Should be called only for visual testing before script and not actual work.

```

# License

HumanCursor is licensed under the MIT License. See LICENSE for more information.
