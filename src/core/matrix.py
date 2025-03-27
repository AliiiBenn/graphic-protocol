from typing import TypeVar, Protocol, runtime_checkable, Generic, Iterator, Sequence, MutableSequence, overload
from collections.abc import Sized, Iterable
from typing_extensions import Self

T = TypeVar('T')
T_co = TypeVar('T_co', covariant=True)

@runtime_checkable
class Matrix(Protocol[T_co], Sized, Iterable[Sequence[T_co]]):
    """Protocol defining the basic interface for a matrix."""
    
    @property
    def rows(self) -> int:
        """Returns the number of rows in the matrix."""
        ...
    
    @property
    def cols(self) -> int:
        """Returns the number of columns in the matrix."""
        ...
    
    def __getitem__(self, key: tuple[int, int]) -> T_co:
        """Gets the element at the specified position."""
        ...
    
    def __iter__(self) -> Iterator[Sequence[T_co]]:
        """Returns an iterator over the rows of the matrix."""
        ...
    
    def __len__(self) -> int:
        """Returns the number of rows in the matrix."""
        ...

@runtime_checkable
class MutableMatrix(Protocol[T], Matrix[T]):
    """Protocol defining a mutable matrix interface."""
    
    def __setitem__(self, key: tuple[int, int], value: T) -> None:
        """Sets the element at the specified position."""
        ...
    
    def clear(self) -> None:
        """Clears all elements in the matrix."""
        ...
    
    def resize(self, rows: int, cols: int, fill_value: T | None = None) -> None:
        """Resizes the matrix to the specified dimensions."""
        ...

class ListMatrix(Generic[T]):
    """Concrete implementation of a mutable matrix using nested lists."""
    
    def __init__(self, rows: int, cols: int, fill_value: T | None = None) -> None:
        self._data: list[list[T | None]] = [[fill_value for _ in range(cols)] for _ in range(rows)]
        self._rows = rows
        self._cols = cols
    
    @classmethod
    def from_nested_lists(cls, data: list[list[T]]) -> Self:
        """Creates a matrix from a nested list structure."""
        if not data or not data[0]:
            raise ValueError("Data must be non-empty")
        
        rows = len(data)
        cols = len(data[0])
        
        if not all(len(row) == cols for row in data):
            raise ValueError("All rows must have the same length")
        
        matrix = cls(rows, cols)
        matrix._data = [[x for x in row] for row in data]  # Cast each element explicitly
        return matrix
    
    @property
    def rows(self) -> int:
        return self._rows
    
    @property
    def cols(self) -> int:
        return self._cols
    
    def __getitem__(self, key: tuple[int, int]) -> T | None:
        row, col = key
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("Matrix index out of range")
        return self._data[row][col]
    
    def __setitem__(self, key: tuple[int, int], value: T) -> None:
        row, col = key
        if not (0 <= row < self._rows and 0 <= col < self._cols):
            raise IndexError("Matrix index out of range")
        self._data[row][col] = value
    
    def __iter__(self) -> Iterator[list[T | None]]:
        return iter(self._data)
    
    def __len__(self) -> int:
        return self._rows
    
    def clear(self) -> None:
        for row in range(self._rows):
            for col in range(self._cols):
                self._data[row][col] = None
    
    def resize(self, rows: int, cols: int, fill_value: T | None = None) -> None:
        if rows < 0 or cols < 0:
            raise ValueError("Dimensions must be non-negative")
        
        # Create new data structure
        new_data = [[fill_value for _ in range(cols)] for _ in range(rows)]
        
        # Copy existing data
        for i in range(min(self._rows, rows)):
            for j in range(min(self._cols, cols)):
                new_data[i][j] = self._data[i][j]
        
        self._data = new_data
        self._rows = rows
        self._cols = cols
    
    def __str__(self) -> str:
        return "\n".join(" ".join(str(cell) for cell in row) for row in self._data)
    
    def __repr__(self) -> str:
        return f"ListMatrix(rows={self._rows}, cols={self._cols})"
    
