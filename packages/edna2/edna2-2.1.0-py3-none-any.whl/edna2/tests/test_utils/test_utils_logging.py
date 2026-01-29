from edna2.utils import UtilsLogging


def test_logging():
    logger = UtilsLogging.getLogger("DEBUG")
    logger.debug("Test message debug")
    logger.info("Test message info")
    logger.warning("Test message warning")
    logger.error("Test message error")
    logger.critical("Test message critical")
    logger.fatal("Test message fatal")
    assert True
