from gmail_trello_apis.api_calls.gmail_actions import GmailActionsCalls
from gmail_trello_apis.api_calls.trello_actions import TrelloActionsCalls
from src.helpers.decode_mail_parts import decode_base64_mail_parts
import logging

logger = logging.getLogger(__name__)
gmail_actions = GmailActionsCalls()
trello_actions = TrelloActionsCalls()
mail_subject_list = []
duplicated_subject_list = []

trello_api_key = '31b16456780503923097911cdf2373d0'
trello_api_token = 'ATTAa19aea4c61c76ae122f776ae77309efe387d7d737631759d53b45ce5a17b35c128217ACE'

def test_mail_body_merge_to_same_card_sync():
    """
    This test checking a sync functionality when there are some emails with the same subject (and different body)
    so they will appear as one card in Trello:

    1. Get all mail messages from inbox
    2. Get each mail message content by ID - first time to get all subject
    3. Get each mail message content by ID - second time to get duplicated subject
    4. Get Trello board ID
    5. Get board lists from Trello board
    6. Get cards data of board lists from Trello board
    7. Validate if mail with same subject and different bodies are merged on one Trello card

    """

    subject_bodies_map = {}

    logger.info("[===========================================]")
    logger.info("   Get all mail messages from inbox")
    logger.info("[===========================================]")
    status, response = gmail_actions.get_all_mail_messages(user_id="me")
    assert status, logger.error("Failed to get all mails messages from Gmail!")
    messages_id_dict_list = response['messages']

    # Collect all subjects
    for message_id in messages_id_dict_list:
        logger.info("[===========================================]")
        logger.info("   Get mail message content by ID")
        logger.info("[===========================================]")
        status, response = gmail_actions.get_mail_message_content_by_id(user_id="me", id=message_id['id'])
        assert status, logger.error("Failed to get mail messages contents by ID from Gmail!")

        for header in response['payload']['headers']:
            if header['name'].lower() == "subject":
                mail_subject_list.append(header['value'])

        for subject in mail_subject_list:
            if mail_subject_list.count(subject) > 1 and subject not in duplicated_subject_list:
                duplicated_subject_list.append(subject.replace("Task: ", ""))

    # Collect bodies for only duplicated subjects
    for message_id in messages_id_dict_list:
        status, response = gmail_actions.get_mail_message_content_by_id(user_id="me", id=message_id['id'])
        assert status, logger.error("Failed to get mail messages contents by ID from Gmail!")

        # Get the subject
        current_subject = None
        for header in response['payload']['headers']:
            if header['name'].lower() == "subject":
                current_subject = header['value'].replace("Task: ", "")
                break

        # If this is a duplicated subject, get its body
        if current_subject in duplicated_subject_list:
            # Initialize list for this subject if not exists
            if current_subject not in subject_bodies_map:
                subject_bodies_map[current_subject] = []

            # Extract body from parts
            for part in response['payload']['parts']:
                if part['body'].get('data'):
                    mail_part_text = decode_base64_mail_parts(part['body']['data'])
                    subject_bodies_map[current_subject].append(mail_part_text.replace("\r\n", ""))
                    logger.info(f"Found body for subject: {current_subject}")

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
            if card_data['name'] in set(duplicated_subject_list):
                expected_card_body = "".join(list(filter(None, subject_bodies_map[card_data['name']])))
                actual_card_body = card_data['desc'].replace("\n","")
                assert expected_card_body == actual_card_body, (
                    logger.error(f"Failed to verify Trello card with card title '{card_data['name']}' is having merged body from mail!"
                                 f" Actual: {actual_card_body}, Expected: {expected_card_body}"))
