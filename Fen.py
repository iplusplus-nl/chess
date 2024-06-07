

def getFen(game):
    board = game.board.copy()
    board = reversed(board)
    fen = ""
    for row in board:
        empty = 0
        for cell in row:
            if cell == ' ':
                empty += 1
            else:
                if empty > 0:
                    fen += str(empty)
                    empty = 0
                fen += cell
        if empty > 0:
            fen += str(empty)
        fen += "/"
    fen = fen[:-1]
    fen+=' b '

    whiteCastle = ''

    if not game.kingMoved:
        if not game.castleKingMoved:
            whiteCastle += 'K'
        if not game.castleQueenMoved:
            whiteCastle += 'Q'

    whiteCastle += game.blackCastle
    
    if whiteCastle == '':
        whiteCastle = '-'

    fen += whiteCastle + ' ' + game.enPassant

    fen += ' ' + str(game.halfMove) + ' '
    fen += str(game.fullMove)

    return fen

def getGame(game, fen):
    board = []
    for row in fen.split(' ')[0].split('/'):
        board.append([])
        for cell in row:
            if cell.isdigit():
                for i in range(int(cell)):
                    board[-1].append(' ')
            else:
                board[-1].append(cell)
    board = reversed(board)
    game.board = board
    temp = fen.split(' ')[1]
    game.blackCastle = ''
    for i in temp:
        if i == 'k':
            game.blackCastle += i
        elif i == 'q':
            game.blackCastle += i

    game.enPassant = fen.split(' ')[3]
    game.halfMove = int(fen.split(' ')[4])
    game.fullMove = int(fen.split(' ')[5])

    return game
