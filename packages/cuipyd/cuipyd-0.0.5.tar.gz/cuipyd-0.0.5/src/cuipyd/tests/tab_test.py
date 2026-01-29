import curses
from cuipyd.main_window import MainWindow
from cuipyd.pane import Pane
from cuipyd.layouts.tab_layout import TabLayout
from cuipyd.popup import BasePopup, PopupBorderStyle
from cuipyd.mouse import MouseEvent, MouseButton
from cuipyd.widgets.spreadsheet import SpreadSheet

import time


class MySpreadSheet(SpreadSheet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time = False

    def render_frame(self, time_delta):
        super().render_frame(time_delta)
        start_time = time.time()
        self._draw_grid()
        end_time = time.time()
        if self.time:
            raise Exception(end_time - start_time)


class ColorPane(Pane):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _register_mouse_event(self, mouse_event: MouseEvent):
        if mouse_event.is_null:
            return
        row = mouse_event.row
        column = mouse_event.column
        if mouse_event.button == MouseButton.LEFT_MOUSE:
            self._click_location = [row, column]
        self._render_frame(0)
        self._refresh()

    def render_frame(self, time_delta):
        super().render_frame(time_delta)
        if not self.default_char == " ":
            return
        # return
        y, x = self._get_size()
        cmod = self._get_color_scheme().default_mod()
        click_cmod = self._get_color_scheme().default_mod(invert=True)

        special_names = [
            "ACS_BBSS",
            "ACS_BLOCK",
            "ACS_BOARD",
            "ACS_BSBS",
            "ACS_BSSB",
            "ACS_BSSS",
            "ACS_BTEE",
            "ACS_BULLET",
            "ACS_CKBOARD",
            "ACS_DARROW",
            "ACS_DEGREE",
            "ACS_DIAMOND",
            "ACS_GEQUAL",
            "ACS_HLINE",
            "ACS_LANTERN",
            "ACS_LARROW",
            "ACS_LEQUAL",
            "ACS_LLCORNER",
            "ACS_LRCORNER",
            "ACS_LTEE",
            "ACS_NEQUAL",
            "ACS_PI",
            "ACS_PLMINUS",
            "ACS_PLUS",
            "ACS_RARROW",
            "ACS_RTEE",
            "ACS_S1",
            "ACS_S3",
            "ACS_S7",
            "ACS_S9",
            "ACS_SBBS",
            "ACS_SBSB",
            "ACS_SBSS",
            "ACS_SSBB",
            "ACS_SSBS",
            "ACS_SSSB",
            "ACS_SSSS",
            "ACS_STERLING",
            "ACS_TTEE",
            "ACS_UARROW",
            "ACS_ULCORNER",
            "ACS_URCORNER",
            "ACS_VLINE",
        ]

        ind = 0
        for r in range(y):
            for c in range(x):
                # char = curses_specials[ind % len(curses_specials)]
                special_name = special_names[r % len(special_names)]
                special_char = getattr(curses, special_name)
                self.add_str(special_name, r, 0)
                self.add_char(special_char, r, 2 + len(special_name), raw=True)


class TestPopup(BasePopup):

    def __init__(self, *args, **kwargs):
        kwargs["border_style"] = PopupBorderStyle.BLOCK
        super().__init__(*args, **kwargs)


class TestWindow(MainWindow):

    def __init__(self):
        super().__init__()
        self.layout = TabLayout(name="Tab Layout")
        self.set_root_layout(self.layout)
        self.popup = None
        self.spreadsheet = None

        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        for letter in list(letters):
            if letter == "B":
                pane = MySpreadSheet(name="Spradsheet")
                self.spreadsheet = pane
            else:
                pane = ColorPane(default_char=letter, name="Pane{}".format(letter))
                if letter == "A":
                    pane._name = "Char Showcase"
                    pane.default_char = " "
                if letter == "B":
                    pane._name = "BIG NAME FOR B"
                if letter == "Y":
                    pane._name = "OTHER BIG NAME HERE"

            self.layout._add_child(pane)
        # self.layout._set_tab_active(23)
        # self.layout._set_tabs_on_top(False)

    def _process_character(self, char):
        if chr(char) == "b":
            self.layout._next_tab()
        if chr(char) == "B":
            self.layout._previous_tab()
        if chr(char) == "p":
            self.popup = TestPopup()
            self.add_popup(self.popup)
        if chr(char) == "P":
            self.pop_popup()
            # if self.popup:
            #    self.popup.close()
        if chr(char) == "w":
            self.spreadsheet.move_vertically(1)
        if chr(char) == "s":
            self.spreadsheet.move_vertically(-1)
        if chr(char) == "d":
            self.spreadsheet.move_horizontally(1)
        if chr(char) == "a":
            self.spreadsheet.move_horizontally(-1)
        if chr(char) == "t":
            self.spreadsheet.time = True


if __name__ == "__main__":
    TestWindow().run()
