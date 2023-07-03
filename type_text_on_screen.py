import re


class TypeTextOnScreen:
    """
    Imports .txt file and generates python instruction for pyautogui module what to type and how
    https://pyautogui.readthedocs.io/en/latest/index.html

    Instructions can be build to type in IDE
    """
    BACKSPACE = r"backspace"
    TAB = r"tab"
    ENTER = r"enter"

    CHARACTER_CHANGE_CHARS_TO_RPA_COMMANDS = {
        "\n": ENTER,
        "\t": TAB,
    }

    def __init__(self, open_file_path: str, save_file_path: str) -> None:
        """
        Get path of files to open and to save
        :param save_file_path:
        :param open_file_path:
        """
        self.save_file_path = save_file_path
        self.open_file_path = open_file_path

    def __read_txt_file(self) -> list:
        """
        Opens file and reads line by line
        :return: list of read lines
        """
        with open(self.open_file_path) as f:
            lines = f.readlines()

        return lines

    def __get_splitter(self) -> list:
        return [s for s in self.CHARACTER_CHANGE_CHARS_TO_RPA_COMMANDS]

    @staticmethod
    def __press_special_button(button: str, press_times: int = 1):
        """
        Pressing special button.
        Pyautogui specific code
        :param button: what button to press (get updated list from pyautogui)
                    ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
                    ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
                    '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
                    'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
                    'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
                    'browserback', 'browserfavorites', 'browserforward', 'browserhome',
                    'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
                    'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
                    'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
                    'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
                    'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
                    'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
                    'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
                    'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
                    'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
                    'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
                    'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
                    'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
                    'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
                    'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
                    'command', 'option', 'optionleft', 'optionright']

        :param press_times: how many times button will be pressed
        :return: string what to press
        """
        return "pyautogui.press('{}', presses={})".format(button, press_times)

    def change_txt_for_rpa_engine(self,
                                  change_following_tabs: bool = True,
                                  remove_leading_spaces: bool = True,
                                  typing_speed: float = 0.25) -> list:
        """
        Creates list of command instructions for pyautogui

        :param change_following_tabs: will add tabs if tabs indents increase next line and decrease if tabs decrease
        :param remove_leading_spaces: removes leading spaces
                True for SQL-like queries
                select
                     row_one # leading spase is in this line
                    ,row two
                from ...
        :param typing_speed: speed of type for autogui

        :return: list of pyautogui commands
        """

        output_list = []

        write_line = "pyautogui.write('{}', interval=" + str(typing_speed) + ")"

        lines = self.__read_txt_file()

        tabs_count = 0
        leading_spaces_count = 0

        for line in lines:

            if change_following_tabs:

                new_tabs_count = re.match(r"\s*", line).group().count("\t")

                # Adds tabs on increase of tab-indents on next line
                if new_tabs_count > tabs_count:
                    output_list.append(self.__press_special_button(self.TAB, new_tabs_count - tabs_count))
                # Deletes tabs on decrease of tab-indents on next line
                if new_tabs_count < tabs_count:
                    output_list.append(self.__press_special_button(self.BACKSPACE, tabs_count - new_tabs_count))

                tabs_count = new_tabs_count

            if remove_leading_spaces:
                # Deletes leading spaces
                new_leading_spaces_count = re.match(r"\s*", line).group().count(" ")

                if new_leading_spaces_count > leading_spaces_count:
                    output_list.append(write_line.format(" " * (new_leading_spaces_count - leading_spaces_count)))

                if new_leading_spaces_count < leading_spaces_count:
                    output_list.append(self.__press_special_button(self.BACKSPACE,
                                                                   leading_spaces_count - new_leading_spaces_count))

                leading_spaces_count = new_leading_spaces_count

            split_in_tokens = re.split('([\t\n])', line.lstrip())

            for token in split_in_tokens:
                if token == "":
                    continue

                if token in self.CHARACTER_CHANGE_CHARS_TO_RPA_COMMANDS:
                    output_list.append(self.__press_special_button(self.CHARACTER_CHANGE_CHARS_TO_RPA_COMMANDS[token]))
                else:
                    output_list.append(write_line.format(token))

        return output_list

    def write_file(self) -> None:

        lines = self.change_txt_for_rpa_engine()

        with open(self.save_file_path, 'a') as the_file:

            the_file.write("import pyautogui\n")
            the_file.write("import time\n")
            the_file.write("time.sleep(5)\n")

            for line in lines:
                the_file.write("{}\n".format(line))


if __name__ == "__main__":
    input_path = r"test_scripts/sql.sql"
    output_path = r"new_file.py"

    test = TypeTextOnScreen(input_path, output_path)
    test.write_file()

