import random
import sys
import time

WIN_LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
             (0, 3, 6), (1, 4, 7), (2, 5, 8),
             (0, 4, 8), (2, 4, 6)]

memo = {}  # 같은 상태 재계산 방지 (속도 향상)


def winner(board):
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return None


def minimax(board, is_ai_turn, ai, human):
    key = (tuple(board), is_ai_turn, ai)
    if key in memo:
        return memo[key]

    moves_played = 9 - board.count(" ")  # 지금까지 둔 수 (빠른 승리 선호용)
    w = winner(board)
    if w == ai:
        score = 10 - moves_played
    elif w == human:
        score = moves_played - 10
    elif " " not in board:
        score = 0
    elif is_ai_turn:
        score = -100
        for i in range(9):
            if board[i] == " ":
                board[i] = ai
                score = max(score, minimax(board, False, ai, human))
                board[i] = " "
    else:
        score = 100
        for i in range(9):
            if board[i] == " ":
                board[i] = human
                score = min(score, minimax(board, True, ai, human))
                board[i] = " "

    memo[key] = score
    return score


def best_move(board, me, other):
    """me 입장에서 최선의 수 반환 (동점이면 무작위)"""
    best_score, candidates = -100, []
    for i in range(9):
        if board[i] == " ":
            board[i] = me
            score = minimax(board, False, me, other)
            board[i] = " "
            if score > best_score:
                best_score, candidates = score, [i]
            elif score == best_score:
                candidates.append(i)
    return random.choice(candidates)


def random_move(board):
    return random.choice([i for i in range(9) if board[i] == " "])


def play_game(ai_first, opponent):
    """한 판 자동 진행 → 'ai' / 'opp' / 'draw' 반환"""
    ai, opp = "O", "X"
    board = [" "] * 9
    ai_turn = ai_first

    while True:
        if ai_turn:
            board[best_move(board, ai, opp)] = ai
        elif opponent == "random":
            board[random_move(board)] = opp
        else:  # "minimax"
            board[best_move(board, opp, ai)] = opp

        w = winner(board)
        if w:
            return "ai" if w == ai else "opp"
        if " " not in board:
            return "draw"
        ai_turn = not ai_turn


def run_simulation(n, opponent):
    result = {"ai": 0, "opp": 0, "draw": 0}
    start = time.time()
    for i in range(n):
        ai_first = (i % 2 == 0)  # 선공을 번갈아 진행
        result[play_game(ai_first, opponent)] += 1
    elapsed = time.time() - start

    print(f"[AI(minimax) vs {opponent}] {n}판, {elapsed:.2f}초")
    print(f"  AI 승 : {result['ai']:>5} ({result['ai'] / n * 100:5.1f}%)")
    print(f"  무승부: {result['draw']:>5} ({result['draw'] / n * 100:5.1f}%)")
    print(f"  AI 패 : {result['opp']:>5} ({result['opp'] / n * 100:5.1f}%)")
    print()


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    run_simulation(n, "random")   # 무작위 상대
    run_simulation(n, "minimax")  # 완벽한 상대 (항상 무승부 예상)


if __name__ == "__main__":
    main()
