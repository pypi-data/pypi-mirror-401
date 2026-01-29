from cuipyd.mouse import MouseEvent


class IPane:

    def __init__(
        self,
        name=None,
        max_height=None,
        min_height=None,
        max_width=None,
        min_width=None,
    ):

        self._pane_parent = None
        self._is_active = True
        self._window = None
        self._name = name
        self._max_height_val = max_height
        self._min_height_val = min_height
        self._max_width_val = max_width
        self._min_width_val = min_width
        self._color_scheme = None

    def _get_color_scheme(self):
        if self._color_scheme:
            return self._color_scheme
        else:
            return self._pane_parent._get_color_scheme()

    @property
    def _max_height(self):
        return self._max_height_val

    @property
    def _min_height(self):
        return self._min_height_val

    @property
    def _max_width(self):
        return self._max_width_val

    @property
    def _min_width(self):
        return self._min_width_val

    def _has_max_width(self):
        self._max_width != None

    def _has_min_width(self):
        self._min_width != None

    def _has_max_height(self):
        self._max_height != None

    def _has_min_height(self):
        self._min_height != None

    def _set_max_width(self, width):
        self._max_width = width

    def _set_min_width(self, width):
        self._min_width = width

    def _set_max_height(self, height):
        self._max_height = height

    def _set_min_height(self, height):
        self._min_height = height

    def _get_name(self):
        if self._name:
            return self._name
        return ""

    @property
    def _parent(self):
        return self._pane_parent

    @property
    def _root(self):
        return self._parent._root

    def is_rendering_paused(self):
        if not self._root._delayed_rendering:
            if self._root._render_thread.is_paused():
                return True
        return False

    @property
    def delayed_rendering(self):
        return self._root._delayed_rendering

    def _has_window(self):
        if hasattr(self, "_window") and self._window != None:
            return True
        return False

    @property
    def _base_screen(self):
        return self._root._screen

    def _set_parent(self, parent):
        self._pane_parent = parent
        self._window = self._parent._window.derwin(0, 0)

    def _refresh(self):
        pass

    def _render_frame(self, time_delta):
        pass

    def _set_active(self, is_active):
        self._is_active = is_active

    def _update_window_size(self, rows, cols, r_pos, c_pos):
        if not self._window:
            return
        # self._window.resize(rows, cols)
        # self._window.mvderwin(r_pos, c_pos)
        with self._root._pause_rendering():
            del self._window
            self._window = self._parent._window.derwin(rows, cols, r_pos, c_pos)

    def _edit_file(self, filename):
        self._root._edit_file(filename)

    def _register_mouse_event(self, mouse_event: MouseEvent):
        pass

    def _get_raw_size(self):
        if not self._window:
            return 0, 0
        return self._window.getmaxyx()

    def _get_size(self):
        return self._get_raw_size()

    def _get_raw_top_left(self):
        if not self._window:
            return 0, 0
        return self._window.getbegyx()

    def _get_top_left(self):
        return self._get_raw_top_left()

    def _tweak_row_col(self, row, col):
        return row, col

    def add_char(self, character, row, col, mod=None, raw=False):
        if self.is_rendering_paused():
            return
        if mod is None:
            mod = self._get_color_scheme().default_mod()
        row, col = self._tweak_row_col(row, col)
        if not raw:
            character = ord(character)
        try:
            self._window.addch(row, col, character, mod)
        except Exception:
            pass

    def add_str(self, string, row, col, mod=None):
        if self.is_rendering_paused():
            return
        row, col = self._tweak_row_col(row, col)
        if mod is None:
            mod = self._get_color_scheme().default_mod()

        try:
            self._window.addstr(row, col, string, mod)
        except:
            pass
