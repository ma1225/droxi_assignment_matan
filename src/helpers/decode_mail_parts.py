import base64
import logging

logger = logging.getLogger(__name__)

def decode_base64_mail_parts(encoded_str: str):
    """
    This function decode base64 encoded mail content parts

    :param: encoded_str: encoded string value of the required mail part

    Returns: Decoded mail part text value
    """

    decoded_text = ""

    try:
        logger.info("Starting base64 decode for required encoded mail part")
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_text = decoded_bytes.decode('utf-8')
        logger.info(f"Decoded text is: '{decoded_text}'")

    except:
        logger.warning(f"Failed to decode the string or its empty!")
        pass

    return decoded_text
