import curses
from typing import List, Tuple
from cuipyd.pane import Pane


class SpreadSheet(Pane):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_column_width = 4
        self._base_row_height = 1

        self._column_widths = {}
        self._row_heights = {}

        self._start_cell_column = 0
        self._start_cell_row = 0

        self._use_row_labels = True
        self._use_col_labels = True

        self._highlights_enabled = True
        self._selection_enabled = True

        self._highlighted_rows = {}
        self._highlighted_cols = {}

        self._auto_highlight_row = True
        self._auto_highlight_row_mod = None
        self._auto_highlight_column = True
        self._auto_highlight_column_mod = None

        self._selected_cell = (0, 0)

        self._max_columns = -1

        self._selected_mod = None

    def set_max_columns(self, max_columns):
        self._max_columns = max_columns

    def set_highlights_enabled(self, enabled: bool):
        self._highlights_enabled = enabled

    def toggle_highlights_enabled(self):
        self.set_highlights_enabled(not self._highlights_enabled)

    def set_selection_enabled(self, enabled: bool):
        self._selection_enabled = enabled

    def toggle_selection_enabled(self):
        self.set_selection_enabled(not self._selection_enabled)

    def set_selected_cell(self, row: int, col: int):
        self._selected_cell = (row, col)

    def get_selected_cell(self) -> Tuple[int, int]:
        return self._selected_cell

    def move_vertically(self, amt: int):
        row, col = self.get_selected_cell()
        new_row = row - amt
        if new_row < 0:
            return
        self._selected_cell = (new_row, col)

    def move_horizontally(self, amt: int):
        row, col = self.get_selected_cell()
        new_col = col + amt
        if new_col < 0:
            return
        if self._max_columns != -1 and new_col >= self._max_columns:
            return
        self._selected_cell = (row, new_col)

    def _get_row_label(self, row_ind: int):
        return row_ind
        return "sdfasdf"
        return row_ind

    def _get_col_label(self, col_ind: int):
        return col_ind

    def _get_column_width(self, column_ind: int):
        output = None
        if column_ind in self._column_widths:
            output = self._column_widths[column_ind]
        else:
            output = self._base_column_width
        col_label = self._get_col_label(column_ind)
        if len(str(col_label)) > output:
            return len(str(col_label))
        return output

    def _get_row_height(self, row_ind: int):
        if row_ind in self._row_heights:
            return self._row_heights[row_ind]
        return self._base_row_height

    def _get_cell_value(self, row: int, col: int):
        return row + col

    def render_frame(self, time_delta):
        super().render_frame(time_delta)
        self._draw_grid()

    def _is_numeric(self, value) -> bool:
        numeric_types = [float, int]
        return any([isinstance(value, t) for t in numeric_types])

    def _to_display_value(self, val, width: int, height: int) -> List[str]:
        if val is None:
            return [" " * width] * height

        str_val = str(val)
        output_lines = [""] * (height - 1)
        output_lines += [str_val]

        output = []
        for ol in output_lines:
            line_length = len(ol)
            if line_length < width:
                if self._is_numeric(val):
                    output.append(" " * (width - line_length) + ol)
                else:
                    output.append(ol + " " * (width - line_length))
            else:
                output.append(ol[:width])
        return output

    def _get_cell_display_value(
        self, row: int, col: int, width: int, height: int
    ) -> List[str]:
        val = self._get_cell_value(row, col)
        return self._to_display_value(val, width, height)

    def add_column_highlight(self, column: int, color_mod=None):
        self._highlighted_cols[column] = color_mod

    def add_row_highlight(self, row: int, color_mod=None):
        self._highlighted_rows[row] = color_mod

    def remove_column_highlight(self, column: int):
        if column in self._highlighted_cols:
            del self._highlighted_cols[column]

    def remove_row_highlight(self, row: int):
        if row in self._highlighted_rows:
            del self._highlighted_rows[row]

    def _get_cell_color_mod(self, row: int, col: int):
        if (row, col) == self._selected_cell and self._selection_enabled:
            if self._selected_mod is not None:
                return self._selected_mod
            return self._get_color_scheme().important_mod(invert=True)

        elif row == self._selected_cell[0] and self._auto_highlight_row:
            if self._auto_highlight_row_mod is not None:
                return self._auto_highlight_row_mod
            return self._get_color_scheme().alternate_mod()

        elif col == self._selected_cell[1] and self._auto_highlight_column:
            if self._auto_highlight_column_mod is not None:
                return self._auto_highlight_column_mod
            return self._get_color_scheme().alternate_mod()

        elif row in self._highlighted_rows and self._highlights_enabled:
            color_mod = self._highlighted_rows[row]
            if color_mod:
                return color_mod
            return self._get_color_scheme().alternate_mod()

        elif col in self._highlighted_cols and self._highlights_enabled:
            color_mod = self._highlighted_cols[col]
            if color_mod:
                return color_mod
            return self._get_color_scheme().alternate_mod()
        return self._get_color_scheme().default_mod()

    def _get_col_widths(self):
        y, x = self._get_size()
        col_widths = []
        col_ind = self._start_cell_column
        if self._use_row_labels:
            row_labels = []
            for i in range(self._start_cell_row, self._start_cell_row + y):
                row_labels.append(self._get_row_label(i))

            row_label_len = max([len(str(row_label)) for row_label in row_labels])
            col_widths.append(row_label_len + 1)

        while sum(col_widths) + len(col_widths) < x:
            col_widths.append(self._get_column_width(col_ind))
            col_ind += 1
            if col_ind >= self._max_columns and self._max_columns != -1:
                break

        # Remove last column
        if sum(col_widths) + len(col_widths) > x:
            col_widths = col_widths[:-1]

        # Adjust column sizes
        if sum(col_widths) < x:
            size_diff = x - (sum(col_widths) + len(col_widths))
            for i in range(size_diff):
                col_widths[(i + 1) % len(col_widths)] += 1
        return col_widths

    def _get_row_heights(self):
        y, x = self._get_size()
        row_heights = []
        row_ind = self._start_cell_column
        if self._use_col_labels:
            row_heights.append(1)

        while sum(row_heights) + len(row_heights) < x:
            row_heights.append(self._get_row_height(row_ind))
            row_ind += 1
            if row_ind >= self._max_columns and self._max_columns != -1:
                break

        # Remove last column
        if sum(row_heights) > x:
            row_heights = row_heights[:-1]

        return row_heights

    def _draw_cell(self, value, screen_row, screen_col, cell_width, cell_height, mod):
        lines = self._to_display_value(value, cell_width, cell_height)
        underline_mod = mod | curses.A_UNDERLINE
        default_mod = mod

        for line_ind in range(len(lines)):
            mod = default_mod
            if line_ind == len(lines) - 1:
                mod = underline_mod

            self.add_str(lines[line_ind], screen_row + line_ind, screen_col, mod=mod)
            self.add_char(
                curses.ACS_SBSB,
                screen_row + line_ind,
                screen_col + cell_width,
                mod=mod,
                raw=True,
            )

    def _draw_column_labels(self, col_widths: List[int]):
        offset_width = 0
        if self._use_row_labels:
            offset_width = col_widths[0] + 1
            # mod = self._get_color_scheme().alternate_important_mod(invert=True)
            # self._draw_cell(None, 0, 0, offset_width, 1, mod)
            col_widths = col_widths[1:]

        col_ind = self._start_cell_column
        for i in range(len(col_widths)):
            mod = self._get_color_scheme().alternate_important_mod(invert=True)
            start_index = i + sum(col_widths[:i])
            col_width = col_widths[i]
            label = self._get_col_label(i + col_ind)
            self._draw_cell(label, 0, offset_width + start_index, col_width, 1, mod)

    def _draw_row_labels(self, cell_width: int, row_heights: List[int]):
        offset_height = 0
        if self._use_col_labels:
            offset_height = 1
            row_heights = row_heights[1:]

        row_ind = self._start_cell_row
        for i in range(len(row_heights)):

            row_height = row_heights[i]
            label = self._get_row_label(i + row_ind)
            # lines = self._to_display_value(label, cell_width, 1)
            mod = self._get_color_scheme().alternate_important_mod(invert=True)
            start_index = sum(row_heights[:i])

            # _draw_cell(self, value, screen_row, screen_col, cell_width, cell_height, mod)
            self._draw_cell(
                label, start_index + offset_height, 0, cell_width, row_height, mod
            )

            # for line_ind in range(len(lines)):
            # self.add_str(lines[line_ind], offset_height + i + line_ind, 0, mod=mod)
            # self.add_char(curses.ACS_SBSB, offset_height + i + line_ind, cell_width, mod=mod, raw=True)

    def _draw_grid(self):
        y, x = self._get_size()
        col_widths = self._get_col_widths()
        row_heights = self._get_row_heights()

        start_row = 0
        if self._use_col_labels:
            self._draw_column_labels(col_widths)
            start_row += row_heights[0]

        start_col = 0
        if self._use_row_labels:
            self._draw_row_labels(col_widths[0], row_heights)
            start_col += col_widths[0]

        data_start_row = self._start_cell_row
        if self._use_col_labels:
            data_start_row -= 1

        data_start_col = self._start_cell_column
        if self._use_row_labels:
            data_start_col -= 1

        for r in range(0, len(row_heights)):
            if r == 0 and self._use_col_labels:
                continue
            data_row = data_start_row + r
            row_height = row_heights[r]
            for c in range(0, len(col_widths)):
                if c == 0 and self._use_row_labels:
                    continue
                data_col = data_start_col + c
                col_width = col_widths[c]
                mod = self._get_cell_color_mod(data_row, data_col)
                val = self._get_cell_value(data_row, data_col)
                self._draw_cell(
                    val,
                    sum(row_heights[:r]),
                    sum(col_widths[:c]) + c,
                    col_width,
                    row_height,
                    mod
                )





        '''
        for r in range(1, len(row_heights)):
            data_row = self._start_cell_row + r
            row_height = row_heights[r]
            for c in range(1, len(col_widths)):
                data_col = self._start_cell_column + c
                col_width = col_widths[c]
                # if not self._use_row_labels and self._use_col_labels and c in [0, 1]:
                # col_width -= 1
                mod = self._get_cell_color_mod(data_row, data_col)
                val = self._get_cell_value(data_row, data_col)
                self._draw_cell(
                    val,
                    start_row + sum(row_heights[:r]),
                    start_col + sum(col_widths[:c]) + c,
                    col_width,
                    row_height,
                    mod,
                )
        '''
