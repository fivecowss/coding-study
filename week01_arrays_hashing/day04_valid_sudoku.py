def is_valid_sudoku(board):
    rows = set()
    cols = set()
    boxes = set()

    for r in range(9):
        for c in range(9):
            value = board[r][c]

            if value == ".":
                continue

            box_id = (r // 3, c // 3)

            row_key = (r, value)
            col_key = (c, value)
            box_key = (box_id, value)

            if row_key in rows or col_key in cols or box_key in boxes:
                return False
            
            rows.add(row_key)
            cols.add(col_key)
            boxes.add(box_key)
    
    return True

if __name__ == "__main__":
    valid_board = [
            ["5", "3", ".", ".", "7", ".", ".", ".", "."],
            ["6", ".", ".", "1", "9", "5", ".", ".", "."],
            [".", "9", "8", ".", ".", ".", ".", "6", "."],
            ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
            ["4", ".", "8", "8", "6", "3", ".", ".", "1"],
            ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
            [".", "6", ".", ".", ".", ".", "2", "8", "."],
            [".", ".", ".", "4", "1", "9", ".", ".", "5"],
            [".", ".", ".", ".", "8", ".", ".", "7", "9"]
        ]
    invalid_board = [
            ["8","3",".",".","7",".",".",".","."],
            ["6",".",".","1","9","5",".",".","."],
            [".","9","8",".",".",".",".","6","."],
            ["8",".",".",".","6",".",".",".","3"],
            ["4",".","8",".","3",".",".",".","1"],
            ["7",".",".",".","2",".",".",".","6"],
            [".","6",".",".",".",".","2","8","."],
            [".",".",".","4","1","9",".",".","5"],
            [".",".",".",".","8",".",".","7","9"]
        ]
    print(is_valid_sudoku(valid_board))  # Output: True
    print(is_valid_sudoku(invalid_board))  # Output: False