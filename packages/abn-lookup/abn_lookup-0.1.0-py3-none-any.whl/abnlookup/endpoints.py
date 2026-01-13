"""
API endpoints for the ABN Lookup service.
"""

BASE_URL = "https://abr.business.gov.au/abrxmlsearch/abrxmlsearch.asmx"

# Operations
SEARCH_BY_ABN = "SearchByABNv202001"
SEARCH_BY_ASIC = "SearchByASICv201408"
SEARCH_BY_NAME = "ABRSearchByNameAdvancedSimpleProtocol2017"
SEARCH_BY_ABN_STATUS = "SearchByABNStatus"
SEARCH_BY_CHARITY = "SearchByCharity"
SEARCH_BY_POSTCODE = "SearchByPostcode"
SEARCH_BY_REGISTRATION_EVENT = "SearchByRegistrationEvent"
SEARCH_BY_UPDATE_EVENT = "SearchByUpdateEvent"