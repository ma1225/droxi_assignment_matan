from googleapiclient.errors import HttpError
from src.configs.config_helpers import build_gmail_user_credentials_for_api_calls
import logging

logger = logging.getLogger(__name__)

class GmailActionsCalls:

    def __init__(self):
        pass

    @staticmethod
    def get_all_mail_messages(user_id: str, label_ids: str = None, q: str = None, page_token: str = None,
                              max_results: int = None, include_spam_trash: bool = False):
        """
        This function GET the lists of messages in the user's mailbox.

        param: userId: The user's email address. The special value me can be used to indicate the authenticated user. (required)
        param: labelIds: Only return messages with labels that match all of the specified label IDs. (repeated)
        param: q: Only return messages matching the specified query. Supports the same query format as the Gmail search box. For example, "from:someuser@example.com rfc822msgid:<somemsgid@example.com> is:unread". Parameter cannot be used when accessing the api using the gmail.metadata scope.
        param: pageToken: Page token to retrieve a specific page of results in the list.
        param: maxResults: Maximum number of messages to return.
        param: includeSpamTrash: Include messages from SPAM and TRASH in the results.

        Returns: All mail messages in user inbox
        """

        status = False
        api_results = ""

        try:
            api_build = build_gmail_user_credentials_for_api_calls()
            # Send Gmail API call
            api_results = api_build.users().messages().list(userId=user_id, labelIds=label_ids, q=q,
                                                            pageToken=page_token, maxResults=max_results,
                                                            includeSpamTrash=include_spam_trash).execute()
            if len(api_results['messages']) > 0:
                logger.info("Successfully got Gmail messages from API call")
                status = True

        except HttpError as error:
            if error.resp.status == 400:
                logger.info("API response failed with 400 code bad request!")
            elif error.resp.status == 401:
                logger.info("API response failed with 401 code Authentication error! Please check your credentials!")
            elif error.resp.status == 403:
                logger.info("API response failed with 403 code Permission denied! Check if you have access to Gmail API!")
            elif error.resp.status == 429:
                logger.info("API response failed with 429 code Quota exceeded! Too many requests! please try again later.")
            elif error.resp.status == 500:
                logger.info("API response failed with 500 code internal server error!")
            else:
                logger.info(f"An error occurred while trying to call Gmail API: {error}")

        return status, api_results

    @staticmethod
    def get_mail_message_content_by_id(user_id: str, id: str, format: str = None, metadata_headers: str = None):

        """
        This function GET the specified message.

        :param: userId: The user's email address. The special value me can be used to indicate the authenticated user. (required)
        :param: id: The ID of the message to retrieve. (required)
        :param: format: The format to return the message in.
        :param: metadataHeaders: When given and format is METADATA, only include headers specified. (repeated)

        Returns: Message content by ID
        """

        status = False
        api_results = ""

        try:
            api_build = build_gmail_user_credentials_for_api_calls()
            # Send Gmail API call
            api_results = api_build.users().messages().get(userId=user_id, id=id, format=format, metadataHeaders=metadata_headers).execute()
            if len(api_results['payload']) > 0:
                logger.info("Successfully got Gmail message by ID from API call")
                status = True

        except HttpError as error:
            if error.resp.status == 400:
                logger.info("API response failed with 400 code bad request!")
            elif error.resp.status == 401:
                logger.info("API response failed with 401 code Authentication error! Please check your credentials!")
            elif error.resp.status == 403:
                logger.info("API response failed with 403 code Permission denied! Check if you have access to Gmail API!")
            elif error.resp.status == 429:
                logger.info("API response failed with 429 code Quota exceeded! Too many requests! please try again later.")
            elif error.resp.status == 500:
                logger.info("API response failed with 500 code internal server error!")
            else:
                logger.info(f"An error occurred while trying to call Gmail API: {error}")

        return status, api_results
