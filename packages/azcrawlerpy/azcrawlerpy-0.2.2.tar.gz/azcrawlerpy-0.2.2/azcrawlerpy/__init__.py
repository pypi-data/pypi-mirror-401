"""
Crawler framework for navigating and filling multi-step web forms.

This package provides an abstract framework for automating form completion
on any website given a starting URL, input data, and JSON instructions.
"""

from .crawling import (
    ActionDefinition,
    ActionType,
    ContextOptions,
    CrawlerBrowserConfig,
    CrawlerError,
    CrawlResult,
    DataExtractionConfig,
    DebugMode,
    ElementDiscovery,
    ExtractionFieldDefinition,
    FieldDefinition,
    FieldType,
    FinalPageDefinition,
    FormCrawler,
    GeolocationConfig,
    InMemoryCrawlResult,
    Instructions,
    PageDiscoveryReport,
    ProxyConfig,
    StepDefinition,
    StepExtractionDefinition,
)

__all__ = [
    "ActionDefinition",
    "ActionType",
    "ContextOptions",
    "CrawlResult",
    "CrawlerBrowserConfig",
    "CrawlerError",
    "DataExtractionConfig",
    "DebugMode",
    "ElementDiscovery",
    "ExtractionFieldDefinition",
    "FieldDefinition",
    "FieldType",
    "FinalPageDefinition",
    "FormCrawler",
    "GeolocationConfig",
    "InMemoryCrawlResult",
    "Instructions",
    "PageDiscoveryReport",
    "ProxyConfig",
    "StepDefinition",
    "StepExtractionDefinition",
]
