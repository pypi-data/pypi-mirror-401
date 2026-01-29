import curses
from typing import List, Tuple
from cuipyd.pane import Pane


class SpreadSheet(Pane):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_column_width = 6
        self._base_row_height = 1

        self._column_widths = {2: 8}
        self._row_heights = {4: 2}

        self._start_cell_column = 0
        self._start_cell_row = 0

        self._use_row_labels = True
        self._use_col_labels = True

        self._highlights_enabled = True
        self._selection_enabled = True

        self._highlighted_rows = {3:None}
        self._highlighted_cols = {5:None}

        self._auto_highlight_row = True
        self._auto_highlight_row_mod = None
        self._auto_highlight_column = True
        self._auto_highlight_column_mod = None

        self._selected_cell = (2, 5)

        self._max_columns = 6

        self._selected_mod = None

    def set_max_columns(self, max_columns):
        self._max_columns = max_columns

    def set_highlights_enabled(self, enabled:bool):
        self._highlights_enabled = enabled

    def toggle_highlights_enabled(self):
        self.set_highlights_enabled(not self._highlights_enabled)

    def set_selection_enabled(self, enabled:bool):
        self._selection_enabled = enabled

    def toggle_selection_enabled(self):
        self.set_selection_enabled(not self._selection_enabled)

    def set_selected_cell(self, row:int, col:int):
        self._selected_cell = (row, col)

    def get_selected_cell(self) -> Tuple[int, int]:
        return self._selected_cell

    def move_vertically(self, amt:int):
        row, col = self.get_selected_cell()
        new_row = row-amt
        if new_row < 0:
            return
        self._selected_cell = (new_row, col)

    def move_horizontally(self, amt:int):
        row, col = self.get_selected_cell()
        new_col = col + amt
        if new_col < 0:
            return
        if self._max_columns != -1 and new_col >= self._max_columns:
            return
        self._selected_cell = (row, new_col)

    def _get_row_label(self, row_ind:int):
        return "ROW"

    def _get_col_label(self, col_ind:int):
        return "COL"

    def _get_column_width(self, column_ind: int):
        if column_ind in self._column_widths:
            return self._column_widths[column_ind]
        return self._base_column_width

    def _get_row_height(self, row_ind: int):
        if row_ind in self._row_heights:
            return self._row_heights[row_ind]
        return self._base_row_height

    def _get_cell_value(self, row:int, col:int):
        return row + col

    def render_frame(self, time_delta):
        super().render_frame(time_delta)
        self._draw_grid()

    def _is_numeric(self, value) -> bool:
        numeric_types = [float, int]
        return any([isinstance(value, t) for t in numeric_types])


    def _get_cell_display_value(self, row:int, col:int, width:int, height:int) -> List[str]:
        val = self._get_cell_value(row, col)

        str_val = str(val)
        output_lines = [''] * (height - 1)
        output_lines += [str_val]

        output = []
        for ol in output_lines:
            line_length = len(ol)
            if line_length < width:
                if self._is_numeric(val):
                    output.append(' ' * (width - line_length) + ol)
                else:
                    output.append(ol + ' ' * (width - line_length))


        return output

    def add_column_highlight(self, column:int, color_mod=None):
        self._highlighted_cols[column] = color_mod

    def add_row_highlight(self, row:int, color_mod=None):
        self._highlighted_rows[row] = color_mod

    def remove_column_highlight(self, column:int):
        if column in self._highlighted_cols:
            del self._highlighted_cols[column]

    def remove_row_highlight(self, row:int):
        if row in self._highlighted_rows:
            del self._highlighted_rows[row]

    def _get_cell_color_mod(self, row:int, col:int):
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

    def _draw_grid(self):
        y, x = self._get_size()

        # Get number of visible columns and rows
        col_widths = []
        col_ind = self._start_cell_column
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
                col_widths[i % len(col_widths)] += 1

        row_heights = []
        row_ind = self._start_cell_row
        while sum(row_heights) < y:
            row_heights.append(self._get_row_height(row_ind))
            row_ind += 1

        # Draw Cells
        for r in range(len(row_heights)):
            row_id = self._start_cell_row + r
            row_height = row_heights[r]

            cell_start_row = sum(row_heights[:r])

            for c in range(len(col_widths)):
                col_id = self._start_cell_column + c
                col_width = col_widths[c]

                default_mod = self._get_cell_color_mod(r, c)
                underline_mod = default_mod | curses.A_UNDERLINE

                #TODO: Draw Cell Value Here
                cell_start_col = sum(col_widths[:c]) + c
                cell_display_lines = self._get_cell_display_value(row_id, col_id, col_width, row_height)
                for i in range(row_height):
                    line = cell_display_lines[i]
                    if i == row_height - 1:
                        mod = underline_mod
                    else:
                        mod = default_mod

                    self.add_str(line, cell_start_row + i, cell_start_col, mod=mod)

                for i in range(row_height):
                    if i == row_height - 1:
                        self.add_char(curses.ACS_SBSB, cell_start_row + i, cell_start_col + col_width, mod=underline_mod, raw=True)
                    else:
                        self.add_char(curses.ACS_SBSB, cell_start_row + i, cell_start_col + col_width, mod=default_mod, raw=True)

                if default_mod != self._get_color_scheme().default_mod():
                    for i in range(row_height):
                        if (row_id, col_id-1) == self._selected_cell:
                            break
                        if i == row_height - 1:
                            self.add_char(curses.ACS_SBSB, cell_start_row + i, cell_start_col -1, mod=underline_mod, raw=True)
                        else:
                            self.add_char(curses.ACS_SBSB, cell_start_row + i, cell_start_col -1, mod=default_mod, raw=True)




