from typing import Tuple, Optional, List, Set

class TicTacGame:
    def __init__(self, rows: int, cols: int, win_count: int) -> None:
        self.win_count = win_count
        self.rows = rows
        self.cols = cols
        self.empty = rows * cols
        self.possible_win_player: Set[Tuple[int, int]] = set() # This is only for the "AI".
        self.possible_win_computer: Set[Tuple[int, int]] = set() # This is only for the "AI".
        self.winning_pos = (0, 0)
        self.winning_dir = (0, 0)

        self.scale_row = "   |"
        for i in range(cols):
            self.scale_row = self.scale_row + "".join([" ", chr(ord('A') + i), " |"])

        self.horizontal_line = "".join(["---+" for i in range(cols + 1)])
        self.board = [[" " for _ in range(cols)] for _ in range(rows)]

    def printBoard(self) -> None:
        print(self.scale_row)
        print(self.horizontal_line)

        for i in range(self.rows):
            if i < 9:
                print(" " + str(i + 1) + " |", end="")
            else:
                print(" " + str(i + 1) + "|", end="")

            for player in self.board[i]:
                print("".join([" ", player, " |"]), end="")
            print()
            print(self.horizontal_line)
        print()

    def correct_pos(self, position: str) -> bool:
        return len(position) >= 2 and position[0].isalpha() and\
               position[1:].isdecimal() and\
               0 <= ord(position[0]) - ord('A') < self.cols and\
               1 <= int(position[1:]) <= self.rows

    def validCoord(self, row: int, col: int) -> bool:
        return 0 <= row and row < self.rows and \
               0 <= col and col < self.cols

    def highlightWin(self) -> None:
        row, col = self.winning_pos
        dRow, dCol = self.winning_dir
        winner = self.board[row][col]
        highlited_winner = '\033[1m' + winner + '\033[0m'

        r, c = row, col
        while self.validCoord(r, c) and self.board[r][c] == winner:
            self.board[r][c] = highlited_winner
            r += dRow
            c += dCol

        r, c = row - dRow, col - dCol
        while self.validCoord(r, c) and self.board[r][c] == winner:
            self.board[r][c] = highlited_winner
            r -= dRow
            c -= dCol

def parseInput(to_parse: str) -> Optional[Tuple[int, int]]:
    splited = to_parse.split('x')
    if len(splited) != 2 or\
            not splited[0].isdecimal() or not splited[1].isdecimal():
        return None

    return int(splited[0]), int(splited[1])

def settingGameUp() -> Tuple[str, str, str, bool, TicTacGame]:
    print("Hello! This is a game of Tic-Tac-Toe, please answer these questions, before playing.")
    print()

    while True:
        size = input("Write how big the play board should be. (In the form MxN):\n")
        parsed_size = parseInput(size)
        if parsed_size is None:
            print("The size must be of the form MxN, where M,N are positive integers! Try again.")
            print()
            continue

        rows, cols = parsed_size
        if rows > 26 or cols > 26:
            print("Number of rows and columns should both be at most 26! Try again.")
            print()
            continue
        break
    print()

    while True:
        player = input("Write X if you want to be X and O otherwise.\n")
        if player == 'X':
            computer = 'O'
            break
        elif player == 'O':
            computer = 'X'
            break
        print("You have to write X or O!")
        print()
    print()

    starting = input("If you want to start first, type 1, else type something different.\n")
    if starting == '1':
        current_player = player
    else:
        current_player = computer
    print()

    while True:
        count = input("Write how many of your characters do you have to have in row, column or diagonal to win.\n")

        if not count.isdecimal():
            continue

        win_count = int(count)
        if win_count > min(rows, cols):
            print("The number you enter cannot be greater than " + str(min(rows, cols)) + "!")
            print("Because otherwise noone could win the game, no matter how you both play.")
            print()
            continue
        break

    while True:
        alone_answer = input("Do you want to play against computer? (Y/N)\n")
        if alone_answer == 'Y':
            alone = True
            break
        elif alone_answer == "N":
            alone = False
            break

        print()
        print("You must enter Y if you want to play against computer and N otherwise.")
        continue

    board = TicTacGame(rows, cols, win_count)

    return player, computer, current_player, alone, board

def getPosition(board: TicTacGame) -> Tuple[int, int]:
    while True:
        play = input("You should first write column and then row, like this: B1 means 2nd col and 1st row.\n")
        if board.correct_pos(play):
            row = int(play[1:]) - 1
            col = ord(play[0]) - ord('A')
            if board.board[row][col] != ' ':
                print()
                print("The position is already occupied! Choose a different one.")
                continue
            break
        print()
        print("You must enter a valid position! (eg. C2 means 3rd col and 2nd row)")

    return row, col

def maxSame(row: int, col: int, player: str, board: TicTacGame) -> Tuple[int, Tuple[int, int]]:
    max_same = 1
    direction = (0, 0)
    for dRow, dCol in NEIGHBORS:
        r, c = row + dRow, col + dCol
        count = 1

        while board.validCoord(r, c) and board.board[r][c] == player:
            count += 1
            r += dRow
            c += dCol

        r, c = row - dRow, col - dCol
        while board.validCoord(r, c) and board.board[r][c] == player:
            count += 1
            r -= dRow
            c -= dCol

        if max_same < count:
            max_same = count
            direction = (dRow, dCol)

    return max_same, direction

def checkWin(row: int, col: int, player: str, board: TicTacGame) -> bool:
    same, direction = maxSame(row, col, player, board)
    result = board.win_count <= same
    if result:
        board.winning_pos = (row, col)
        board.winning_dir = direction
    return result

def playMulti(current_player: str, board: TicTacGame) -> None:
    while True:
        board.printBoard()
        print("Where does a player " + current_player + " want to play?")
        row, col = getPosition(board)
        board.board[row][col] = current_player
        board.empty -= 1

        if checkWin(row, col, current_player, board):
            board.highlightWin()
            board.printBoard()
            print("Player " + current_player + " won!")
            break

        if board.empty == 0:
            board.printBoard()
            print("It's a tie.")
            break

        current_player = "O" if current_player == "X" else "X"

def canFinish(row: int, col: int, player: str, board: TicTacGame):
    opponent = "O" if player == "X" else "X"
    possible = False
    max_same = 1
    direction = (0, 0)
    for dRow, dCol in NEIGHBORS:
        r, c = row + dRow, col + dCol
        count = 1
        max_possible = 0

        while board.validCoord(r, c) and board.board[r][c] == player:
            count += 1
            r += dRow
            c += dCol

        while board.validCoord(r, c) and board.board[r][c] != opponent:
            max_possible += 1
            r += dRow
            c += dCol

        r, c = row - dRow, col - dCol
        while board.validCoord(r, c) and board.board[r][c] == player:
            count += 1
            r -= dRow
            c -= dCol

        while board.validCoord(r, c) and board.board[r][c] != opponent:
            max_possible += 1
            r -= dRow
            c -= dCol

        max_possible += count

        if max_possible < board.win_count:
            continue

        possible = True

        if max_same < count:
            max_same = count
            direction = (dRow, dCol)

    return possible, max_same, direction

def spaceAround(row: int, col: int, direction: Tuple[int, int], player: str, board: TicTacGame) -> bool:
    dRow, dCol = direction
    r, c = row + dRow, col + dCol
    while board.validCoord(r, c) and board.board[r][c] == player:
        r += dRow
        c += dCol

    if not board.validCoord(r, c) or board.board[r][c] != " ":
        return False

    r, c = row - dRow, col - dCol
    while board.validCoord(r, c) and board.board[r][c] == player:
        r -= dRow
        c -= dCol

    if not board.validCoord(r, c) or board.board[r][c] != " ":
        return False

    return True

def computerPlay(computer: str, board: TicTacGame) -> Tuple[int, int]:
    player = "O" if computer == "X" else "X"

    result_row, result_col = board.rows // 2, board.cols // 2
    if len(board.possible_win_computer) == 0:
        if len(board.possible_win_player) == 0:
            return result_row, result_col
        for result_row, result_col in board.possible_win_player:
            return result_row, result_col

    highest_same = 0
    direction = (0, 0)
    for row, col in board.possible_win_computer:
        finish, same, dire = canFinish(row, col, computer, board)
        if not finish:
            continue

        if same > highest_same:
            result_row, result_col = row, col
            highest_same = same
            direction = dire
            continue

        if same == highest_same and spaceAround(row, col, dire, computer, board):
            result_row, result_col = row, col
            highest_same = same
            direction = dire

    if highest_same >= board.win_count:
        return result_row, result_col

    highest_player = 0
    direction_player = (0, 0)
    for row, col in board.possible_win_player:
        same, dire = maxSame(row, col, player, board)
        if same > highest_player:
            player_row, player_col = row, col
            highest_player = same
            direction_player = dire

    if highest_same == 0:
        if highest_player == 0:
            for result_row, result_col in board.possible_win_computer:
                return result_row, result_col
        return player_row, player_col

    if highest_player >= board.win_count:
        return player_row, player_col

    if spaceAround(result_row, result_col, direction, computer, board) and highest_same == board.win_count - 1:
        return result_row, result_col

    if spaceAround(player_row, player_col, direction_player, player, board) and highest_player == board.win_count - 1:
        return player_row, player_col

    return result_row, result_col

NEIGHBORS = [(1, 1), (1, -1), (1, 0), (0, 1)]

def possibleWinManager(board: TicTacGame, 
                       possible_win_this: Set[Tuple[int, int]],
                       possible_win_that: Set[Tuple[int, int]],
                       row, col) -> None:
    if (row, col) in possible_win_this:
        possible_win_this.remove((row, col))
    if (row, col) in possible_win_that:
        possible_win_that.remove((row, col))
    for dRow, dCol in NEIGHBORS:
        if board.validCoord(row + dRow, col + dCol) and board.board[row + dRow][col + dCol] == " ":
            possible_win_this.add((row + dRow, col + dCol))
        if board.validCoord(row - dRow, col - dCol) and board.board[row - dRow][col - dCol] == " ":
            possible_win_this.add((row - dRow, col - dCol))

def playSingle(computer: str, current_player: str, board: TicTacGame) -> None:
    while True:
        if current_player == computer:
            row, col = computerPlay(computer, board)
            possibleWinManager(board, board.possible_win_computer,
                               board.possible_win_player, row, col)
        else:
            board.printBoard()
            print("Where do you want to play?")
            row, col = getPosition(board)
            possibleWinManager(board, board.possible_win_player,
                               board.possible_win_computer, row, col)

        board.board[row][col] = current_player
        board.empty -= 1

        if checkWin(row, col, current_player, board):
            board.highlightWin()
            board.printBoard()
            if current_player == computer:
                print("You lost.")
            else:
                print("You won!")
            break

        if board.empty == 0:
            board.printBoard()
            print("It's a tie.")
            break

        current_player = "O" if current_player == "X" else "X"

def main() -> None:
    new_settings = True
    want_to_play = True

    while want_to_play:
        if new_settings:
            player, computer, current_player, alone, board = settingGameUp()
            new_settings = False
        else:
            board = TicTacGame(board.rows, board.cols, board.win_count)

        if alone:
            playSingle(computer, current_player, board)
        else:
            playMulti(current_player, board)

        print("=======================================================================")
        print()
        another = input("What do you want to do? Write 1, 2 or arbitrary different character to:\n\
                         1 = Want to play again with same settings.\n\
                         2 = Want to play again with different settings.\n\
                         _ = Want to quit.\n")

        if another == "1":
            continue

        if another == "2":
            new_settings = True
            continue

        want_to_play = False

if __name__ == '__main__':
    main()
