from playwright.sync_api import Page, Locator, expect
import logging

logger = logging.getLogger(__name__)

class BoardPage:

    def __init__(self, page: Page):
        self.page = page
        self.status_list_selector = '[data-testid="lists"]'
        self.status_list_header_selector = '[data-testid="list-header"]'
        self.card_selector = '[data-testid="trello-card"]'
        self.card_label_selector = '[data-testid="compact-card-label"]'
        self.card_name_selector = '[data-testid="card-name"]'
        self.description_icon = '[data-testid="DescriptionIcon"]'
        self.description_in_card = '[data-testid="description-content-area"]'

    def get_all_status_lists(self) -> list[Locator]:
        """Return a list of Locator objects for each column/list on the board."""

        return self.page.locator(self.status_list_selector).all()

    def get_status_list_name(self, status_list: Locator) -> str:
        """Return the visible name/title of a given list column."""

        text = status_list.locator(self.status_list_header_selector).text_content() or ""
        return text.strip()

    def get_cards_from_status_list(self, status_list: Locator) -> list[Locator]:
        """Return locators for cards inside a list element."""

        return status_list.locator(self.card_selector).all()

    def get_labels_from_card(self, card: Locator) -> list[Locator]:
        """Return locators for cards inside a list element."""

        return card.locator(self.card_label_selector).all()

    def get_card_title(self, card: Locator) -> str:
        """Return the title/text of a card locator."""

        card_title = card.locator(self.card_name_selector).text_content() or ""
        return card_title.strip()

    def get_card_title_element(self, card: Locator) -> Locator:
        """Return the title/text of a card locator."""

        return card.locator(self.card_name_selector)

    def click_on_description_icon(self, card: Locator):
        """Click on description icon on card."""

        description_icon = card.locator(self.description_icon)
        description_icon.click()

    def get_card_description(self, card: Locator) -> str:
        """Return the description of a card locator."""

        description_in_card = card.locator(self.description_in_card)
        expect(description_in_card).to_be_visible()
        description = description_in_card.text_content()

        return description.strip()
