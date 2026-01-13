"""
Centralized configuration constants for the crawler framework.

All timeout values, delay constants, and control variables are defined here.
"""

import logging
import random

logger = logging.getLogger(__name__)


def random_wait_ms(min_ms: int) -> int:
    """Generate a random wait time in milliseconds between min_ms and min_ms * 2."""
    sampled = random.randint(min_ms, min_ms * 2)
    logger.debug(f"Random wait sampled: {sampled}ms (range: {min_ms}-{min_ms * 2}ms)")
    return sampled


def random_wait_seconds(min_seconds: float) -> float:
    """Generate a random wait time in seconds between min_seconds and min_seconds * 2."""
    sampled = random.uniform(min_seconds, min_seconds * 2)
    logger.debug(f"Random wait sampled: {sampled:.3f}s (range: {min_seconds}-{min_seconds * 2}s)")
    return sampled


DEFAULT_VIEWPORT_WIDTH = 1920
DEFAULT_VIEWPORT_HEIGHT = 1080

# Cookie Consent Timeouts (milliseconds) - minimum values, actual wait is random [min, min*2]
COOKIE_BANNER_SETTLE_DELAY_MIN_MS = 1000
COOKIE_BANNER_VISIBLE_TIMEOUT_MIN_MS = 1500
COOKIE_ACCEPT_BUTTON_TIMEOUT_MIN_MS = 2500
COOKIE_POST_CONSENT_DELAY_MIN_MS = 500

# Action Timeouts (milliseconds) - minimum values, actual wait is random [min, min*2]
ACTION_PRE_DELAY_MIN_MS = 1000
ACTION_POST_DELAY_MIN_MS = 2500
ACTION_ELEMENT_ATTACHED_TIMEOUT_MIN_MS = 15000
ACTION_WAIT_TIMEOUT_MIN_MS = 15000

# Field Handler Timeouts (milliseconds) - minimum values, actual wait is random [min, min*2]
FIELD_VISIBLE_TIMEOUT_MIN_MS = 5000
FIELD_POST_CLICK_DELAY_MIN_MS = 500
FIELD_TYPE_DELAY_MIN_MS = 25
FIELD_WAIT_AFTER_TYPE_MIN_MS = 500
FIELD_OPTION_VISIBLE_TIMEOUT_MIN_MS = 5000
FIELD_WAIT_AFTER_CLICK_MIN_MS = 250

# Field Handler Delays (seconds) - minimum values, actual wait is random [min, min*2]
COMBOBOX_PRE_TYPE_DELAY_MIN_SECONDS = 0.15
COMBOBOX_POST_CLEAR_DELAY_MIN_SECONDS = 0.1
COMBOBOX_POST_ENTER_DELAY_MIN_SECONDS = 0.15

# Discovery Timeouts (milliseconds) - minimum values
DISCOVERY_PAGE_LOAD_TIMEOUT_MIN_MS = 15000

# CSS Selector Special Characters that need escaping
CSS_SELECTOR_ESCAPE_CHARS = ":[]().#>+~="

# Characters that need escaping in CSS attribute values
CSS_ATTRIBUTE_VALUE_ESCAPE_CHARS = "\"'\\[]"
