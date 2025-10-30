from playwright.sync_api import Page, expect
from src.pages.login_page import LoginPage
from src.pages.board_page import BoardPage
import logging

logger = logging.getLogger(__name__)

username = "droxiautomation@gmail.com"
password = "Droxination013!"
droxi_board_url = "https://trello.com/b/2GzdgPlw/droxi"

def test_specific_card_validation(page: Page):

    # Login to Trello board by using username, password and verify url is as expected
    login_page = LoginPage(page)
    login_page.navigate_to_trello(droxi_board_url)
    login_page.login_to_trello(username, password)
    expect(page).to_have_url(droxi_board_url)

    # Find summarize the meeting card and extract his data
    board_page = BoardPage(page)
    summarize_card_data_list = []
    expected_card_title = "summarize the meeting"
    expected_description = "For all of us Please do so"
    expected_card_label = "New"
    expected_list_status = "To Do"
    summarize_card_url = "https://trello.com/c/cGmpThHb/16-summarize-the-meeting"

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
            # Check if card title is "summarize the meeting"
            card_title = board_page.get_card_title(card)
            if card_title == expected_card_title:

                # Click on required 'summarize the meeting' card
                board_page.get_card_title_element(card).click()

                # Verify correct card screen URL
                expect(page).to_have_url(summarize_card_url)

                # Verify card title is visible on card screen and is correct
                card_screen_title = card.locator('[data-testid="card-back-title-input"]')
                expect(card_screen_title).to_be_visible()
                card_screen_title_text = card_screen_title.text_content()
                assert card_screen_title_text == expected_card_title, (
                    logger.error(f"Card title is wrong and not as expected! Actual: {card_screen_title_text}, Expected: {expected_card_title}"))

                # Verify card description is correct
                description_elem = card.locator('data-testid="description-content-area"]')
                description = description_elem.text_content()

                assert description == expected_description, (
                    logger.error(f"Description is wrong and not as expected! Actual: {description}, Expected: {expected_description}"))

                # Verify card label is correct
                card_screen_label = card.locator('[data-testid="card-label"]')
                card_screen_label_text = card_screen_label.text_content()
                assert card_screen_label_text.lower() == expected_card_label.lower(), (
                    logger.error(f"Card label is wrong and not as expected! Actual: {card_screen_label_text}, Expected: {expected_card_label}"))

                # Verify correct list status for card
                assert status_list_name == expected_list_status, (
                    logger.error(f"Card list status is wrong and not as expected! Actual: {status_list_name}, Expected: {expected_list_status}"))

                # Extract card data to a list
                summarize_card_data_list.append({
                    'Card title': card_title,
                    'Card description': description,
                    'Label': card_screen_label_text,
                    'Current status': status_list_name
                })

                # Close card modal
                page.keyboard.press('Escape')

                # Wait for modal to close
                expect(page.locator('[data-testid="card-back-name"]')).to_be_hidden()

                logger.info(f"Found card: '{card_title}' in list '{status_list_name}'")

                # Break the above 'for' loop as we found the card so we don't want it to continue
                break

    logger.info(f"card content is: {str(summarize_card_data_list)}")
