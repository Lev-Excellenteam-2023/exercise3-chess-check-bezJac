from enums import Player
import logging as lg

board_states_logger = None
game_stats_logger = None
turns_with_full_pieces = 0  # number of turns that either one of players has all his pieces on the board together.
total_knight_moves = 0  # total number of moves the knights (all four) made in the game.
total_checks = 0  # total number of checks that accrued in the game.


def initialize_loggers() -> None:
    global board_states_logger
    global game_stats_logger
    # Create a logger for board states
    board_states_logger = lg.getLogger('board_states_logger')
    board_states_logger.setLevel(lg.DEBUG)

    # Create a file handler for board_states.log
    board_states_handler = lg.FileHandler('board_states.log')
    board_states_handler.setLevel(lg.DEBUG)
    board_states_handler.setFormatter(lg.Formatter('%(asctime)s:%(levelname)s:%(message)s'))

    # Add the handler to the board states logger
    board_states_logger.addHandler(board_states_handler)

    # Create a logger for game statistics
    game_stats_logger = lg.getLogger('game_stats_logger')
    game_stats_logger.setLevel(lg.DEBUG)

    # Create a file handler for game_statistics.log
    game_stats_handler = lg.FileHandler('game_statistics.log')
    game_stats_handler.setLevel(lg.DEBUG)
    game_stats_handler.setFormatter(lg.Formatter('%(asctime)s:%(levelname)s:%(message)s'))

    # Add the handler to the game statistics logger
    game_stats_logger.addHandler(game_stats_handler)


def start_game_procedure(board: str, human_player: str) -> None:
    board_states_logger.debug(' GAME STARTED:' + "\n" + "=" * 80 + '\nInitial Board State :\n{}'.format(board))

    game_stats_logger.debug("\nGAME STARTED" + "\n" + "=" * 80)

    if human_player is 'b':
        game_stats_logger.debug("Computer is white and started the game")
    else:
        game_stats_logger.debug("Player is white and started the game")


def end_game_procedure(endgame: int) -> None:
    if endgame == 2:
        game_stats_logger.info("Game Ended in a Tie")
    elif endgame == 1:
        game_stats_logger.info("The game did not end in a Tie")
        game_stats_logger.info("WHITE won the game")
    elif endgame ==0:
        game_stats_logger.info("The game did not end in a Tie")
        game_stats_logger.info("BLACK won the game")
    else:
        game_stats_logger.info("Game ended abruptly")

    game_stats_logger.info(
        "Number of turns either player had all pieces on board: {}".format(turns_with_full_pieces))
    game_stats_logger.debug('Total moves made ny Knights in the game: {}'.format(total_knight_moves))
    game_stats_logger.debug('Total checks in the game: {}'.format(total_checks))
    board_states_logger.debug("GAME ENDED\n" + "=" * 80)
    game_stats_logger.debug("GAME ENDED\n" + "=" * 80)


def log_board_state(board: str) -> None:
    board_states_logger.debug('\nBoard State :\n{}'.format(board))


def check_full_pieces(board: str) -> None:
    global turns_with_full_pieces
    current_pieces = count_number_pieces(board)
    if current_pieces[0] == 16 or current_pieces[1] == 16:
        turns_with_full_pieces += 1


def draw_board_for_log(board: list) -> str:
    string = '-' * (8 * 10) + '\n'
    for row in board:
        string += '|'
        for item in row:
            if item != -9:
                if item.is_player(Player.PLAYER_1):
                    string += f" {'white_' + str(item.get_name()):^7} |"
                else:
                    string += f" {'black_' + str(item.get_name()):^7} |"
            else:
                string += " empty   |"
        string += '\n'
        string += '-' * (8 * 10) + '\n'
    return string


def add_knight_move() -> None:
    global total_knight_moves
    total_knight_moves += 1


def add_check() -> None:
    global total_checks
    total_checks += 1


def count_number_pieces(string: str) -> tuple[int, int]:
    count_black = string.count("black")
    count_white = string.count("white")
    return count_black, count_white
