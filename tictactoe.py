WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),
             (0,3,6),(1,4,7),(2,5,8),
             (0,4,8),(2,4,6)]

def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None

def minimax(board, is_ai_turn, ai, human, depth=0):
    w = winner(board)
    if w == ai:
        return 10 - depth
    if w == human:
        return depth - 10
    if " " not in board:
        return 0

    if is_ai_turn:
        best = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = ai
                best = max(best, minimax(board, False, ai, human, depth + 1))
                board[i] = " "
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == " ":
                board[i] = human
                best = min(best, minimax(board, True, ai, human, depth + 1))
                board[i] = " "
        return best

def best_move(board, ai, human):
    best_score, move = -100, None
    for i in range(9):
        if board[i] == " ":
            board[i] = ai
            score = minimax(board, False, ai, human, 1)
            board[i] = " "
            if score > best_score:
                best_score, move = score, i
    return move

def show(board):
    for r in range(3):
        print(" " + " | ".join(board[r*3:r*3+3]))
        if r < 2:
            print("---+---+---")
    print()

def main():
    human, ai = "X", "O"
    board = [" "] * 9
    print("칸 번호: 1~9 (왼쪽 위 = 1, 오른쪽 아래 = 9)\n")
    show(board)

    turn = "human"  # AI 선공은 "ai"로 변경
    while True:
        if turn == "human":
            try:
                pos = int(input("내 차례 (1-9): ")) - 1
            except ValueError:
                print("숫자를 입력하세요.")
                continue
            if pos not in range(9) or board[pos] != " ":
                print("둘 수 없는 칸입니다.")
                continue
            board[pos] = human
            turn = "ai"
        else:
            board[best_move(board, ai, human)] = ai
            print("AI가 두었습니다.")
            turn = "human"

        show(board)
        w = winner(board)
        if w:
            print("사람 승리!" if w == human else "AI 승리!")
            break
        if " " not in board:
            print("무승부!")
            break

if __name__ == "__main__":
    main()
