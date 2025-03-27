


from typing import Final, Literal
from core.matrix import Matrix


class EncodingMatrix(Matrix[bool]):
    def __init__(self, 
                 text: str,
                 size: int,
                 error_correction: Literal['L', 'M', 'Q', 'H']) -> None:
        self._text = text
        self._size = size
        self._error_correction = error_correction

        # TODO: Should be an `EmptyMatrix`
        self._matrix: list[list[bool | None]] = [[None for _ in range(self._size)] for _ in range(self._size)]

    def _add_position_markers(self) -> None:
        MARKER_SIZE: Final[int] = 7

        # Top-left marker
        self._draw_square(0, 0, MARKER_SIZE)

        # Top-right marker
        self._draw_square(0, self._size - MARKER_SIZE, MARKER_SIZE)

    def _draw_square(self, row_start: int, col_start: int, square_size: int) -> None:
        for i in range(square_size):
            for j in range(square_size):
                if (i < 1 or i > square_size - 2) or (j < 1 or j > square_size - 2):
                    self._matrix[row_start + i][col_start + j] = True
                elif (i < 2 or i > square_size - 3) or (j < 2 or j > square_size - 3):
                    self._matrix[row_start + i][col_start + j] = False
                else:   
                    self._matrix[row_start + i][col_start + j] = True

    def _place_data(self) -> None:

            

    @property
    def _value(self) -> Matrix[bool]:
        self._add_position_markers()
        self._place_data()
        return self._matrix

