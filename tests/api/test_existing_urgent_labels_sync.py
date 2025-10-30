from gmail_trello_apis.api_calls.gmail_actions import GmailActionsCalls
from gmail_trello_apis.api_calls.trello_actions import TrelloActionsCalls
from src.helpers.decode_mail_parts import decode_base64_mail_parts
import logging

logger = logging.getLogger(__name__)
gmail_actions = GmailActionsCalls()
trello_actions = TrelloActionsCalls()
urgent_mail_body_list = []
urgent_mail_subject_list = []

trello_api_key = '31b16456780503923097911cdf2373d0'
trello_api_token = 'ATTAa19aea4c61c76ae122f776ae77309efe387d7d737631759d53b45ce5a17b35c128217ACE'

def test_existing_urgent_labels_sync():
    """
    This test checking a sync functionality of each mail which have body that contains the word “Urgent” should
    appear as a card in Trello with an “Urgent” label:

    1. Get all mail messages from inbox
    2. Get each mail message content by ID
    3. Create lists of mail subjects and bodies with the word "Urgent" on mail body
    4. Get Trello board ID
    5. Get board lists from Trello board
    6. Get cards data of board lists from Trello board
    7. Validate if mail/s with the word "Urgent" on mail body appearing on Trello board cards

    """

    urgent_sync_status = False

    logger.info("[===========================================]")
    logger.info("   Get all mail messages from inbox")
    logger.info("[===========================================]")
    status, response = gmail_actions.get_all_mail_messages(user_id="me")
    assert status, logger.error("Failed to get all mails messages from Gmail!")
    messages_id_dict_list = response['messages']

    for message_id in messages_id_dict_list:
        logger.info("[===========================================]")
        logger.info("   Get mail message content by ID")
        logger.info("[===========================================]")
        status, response = gmail_actions.get_mail_message_content_by_id(user_id="me", id=message_id['id'])
        assert status, logger.error("Failed to get mail messages contents by ID from Gmail!")
        for part in response['payload']['parts']:
            if part['body'].get('data'):
                mail_part_text = decode_base64_mail_parts(part['body']['data'])
                logger.info(f"Mail part text: {mail_part_text}")
                if "urgent" in mail_part_text.lower():
                    urgent_mail_body_list.append(mail_part_text.replace("\r\n", ""))
                    for header in response['payload']['headers']:
                        if header['name'].lower() == "subject":
                            urgent_mail_subject_list.append(header['value'])


    logger.info("[===========================================]")
    logger.info("   Get Trello board ID")
    logger.info("[===========================================]")
    board_id = trello_actions.get_trello_board_id(trello_api_key, trello_api_token)
    assert board_id is not None, logger.error("Board ID value is empty!")

    logger.info("[===========================================]")
    logger.info("   Get board lists from Trello board")
    logger.info("[===========================================]")
    board_lists = trello_actions.get_trello_board_lists(trello_api_key, trello_api_token, board_id)
    assert board_lists is not None, logger.error("Board lists value is empty!")

    logger.info("[===========================================]")
    logger.info("   Get cards data of board lists from Trello board")
    logger.info("[===========================================]")
    board_lists_cards_dict = trello_actions.get_trello_board_cards_data_from_board_lists(trello_api_key, trello_api_token, board_lists)
    assert board_lists_cards_dict is not None, logger.error("Board lists card dictionary value is empty!")

    # Run on all card data
    for board_list_name, board_list_card_data in board_lists_cards_dict.items():
        for card_data in board_list_card_data:
            # Verify if card body is the same as urgent mail body
            card_body = card_data['desc'].replace("\n", "")
            card_title = card_data['name']
            if card_body in urgent_mail_body_list and card_title in urgent_mail_subject_list:
                for label in card_data['labels']:
                    # Verify card label is urgent
                    if label['name'].lower() == "urgent":
                        urgent_sync_status = True

    assert urgent_sync_status, logger.error("Failed to verify urgent mail message to Trello sync!")
