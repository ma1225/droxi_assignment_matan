from playwright.sync_api import Page, expect
from src.pages.login_page import LoginPage
from src.pages.board_page import BoardPage
import logging

logger = logging.getLogger(__name__)

username = "droxiautomation@gmail.com"
password = "Droxination013!"
droxi_board_url = "https://trello.com/b/2GzdgPlw/droxi"

def test_urgent_cards_validation(page: Page):

    # Login to Trello board by using username, password and verify url is as expected and POM login_page.py
    login_page = LoginPage(page)
    login_page.navigate_to_trello(droxi_board_url)
    login_page.login_to_trello(username, password)
    expect(page).to_have_url(droxi_board_url)

    # Find all cards with 'urgent' label is as expected and POM board_page.py
    board_page = BoardPage(page)
    urgent_cards = []
    expected_card_label = 'urgent'

    # Get all lists (columns)
    status_lists = board_page.get_all_status_lists()
    assert status_lists, logger.error("No status lists was found!")

    for status_list in status_lists:

        # Get list name
        status_list_name = board_page.get_status_list_name(status_list)

        # Find cards with Urgent label in this list
        cards = board_page.get_cards_from_status_list(status_list)

        # Starting to find on each card for each list
        for card in cards:
            # Check if card has 'Urgent' label and get card data
            labels = board_page.get_labels_from_card(card)
            for label in labels:

                # Get label text
                label_text = label.get_attribute('title')
                if expected_card_label in label_text.lower():

                    # Get card title
                    card_title = board_page.get_card_title(card)

                    # Get description by clicking on card description icon and get the description text
                    board_page.click_on_description_icon(card)
                    description = board_page.get_card_description(card)

                    # Extract cards data to a list
                    urgent_cards.append({
                        'Card title': card_title,
                        'Card description': description,
                        'Label': label_text,
                        'Current status': status_list_name
                    })

                    logger.info(f"Found urgent card: '{card_title}' in list '{status_list_name}'")

    logger.info(f"Urgent card contents are: {str(urgent_cards)}")
