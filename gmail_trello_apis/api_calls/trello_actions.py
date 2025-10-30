import requests
import logging

logger = logging.getLogger(__name__)

class TrelloActionsCalls:

    def __init__(self):
        pass

    @staticmethod
    def get_trello_board_id(api_key: str, api_token: str, board_name: str = "Droxi"):
        """
        This function GET board ID by required name

        :param: api_key: Trello API key
        :param: api_token: Trello API token
        :param: board_name: Trello required board name

        Returns: Board ID value (string)
        """

        board_id = None

        try:

            get_boards_api_url = f"https://api.trello.com/1/members/me/boards?key={api_key}&token={api_token}"
            get_boards_api_response = requests.get(get_boards_api_url)
            boards = get_boards_api_response.json()

            for board in boards:
                if board_name.lower() in board['name'].lower():
                    board_id = board['id']

        except Exception as e:
            logger.error(f"Unexpected error in Trello API occurred: {str(e)}")

        return board_id


    @staticmethod
    def get_trello_board_lists(api_key: str, api_token: str, board_id: str):
        """
        This function GET lists from the board

        :param: api_key: Trello API key
        :param: api_token: Trello API token
        :param: board_id: Trello board ID

        Returns: Board lists value (list)
        """

        board_lists = None

        try:

            get_lists_url = f"https://api.trello.com/1/boards/{board_id}/lists?key={api_key}&token={api_token}"
            get_lists_api_response = requests.get(get_lists_url)
            board_lists = get_lists_api_response.json()

        except Exception as e:
            logger.error(f"Unexpected error in Trello API occurred: {str(e)}")

        return board_lists

    @staticmethod
    def get_trello_board_cards_data_from_board_lists(api_key: str, api_token: str, board_lists: list):
        """
        This function GET cards data from board lists

        :param: api_key: Trello API key
        :param: api_token: Trello API token
        :param: board_lists: Trello board status lists

        Returns: Board cards dictionary with board list name and their cards (dict)
        """

        board_list_cards_dict = {}

        try:

            for board_list in board_lists:
                board_list_id = board_list["id"]
                get_cards_api_url = f"https://api.trello.com/1/lists/{board_list_id}/cards?key={api_key}&token={api_token}"
                get_cards_api_response = requests.get(get_cards_api_url)
                cards = get_cards_api_response.json()
                board_list_cards_dict[board_list['name']] = cards

        except Exception as e:
            logger.error(f"Unexpected error in Trello API occurred: {str(e)}")

        return board_list_cards_dict
