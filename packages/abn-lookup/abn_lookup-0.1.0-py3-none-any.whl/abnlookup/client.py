"""
Client for interacting with the ABN Lookup API.
"""
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional, Union

from . import endpoints
from . import exceptions
from . import models

class ABNLookupClient:
    """
    A client to interact with the ABN Lookup API.
    
    Args:
        guid (str): The authentication GUID provided by the ABR.
    """
    
    NAMESPACE = "{http://abr.business.gov.au/ABRXMLSearch/}"

    def __init__(self, guid: str):
        self.guid = guid

    def search_by_abn(self, abn: str, include_historical: bool = False) -> models.ABNResponse:
        """Search for an entity by its ABN using SearchByABNv202001."""
        abn = abn.replace(" ", "")
        params = {
            "searchString": abn,
            "includeHistoricalDetails": "Y" if include_historical else "N",
            "authenticationGuid": self.guid
        }
        return self._perform_request(endpoints.SEARCH_BY_ABN, params, is_list_search=False)

    def search_by_asic(self, asic: str, include_historical: bool = False) -> models.ABNResponse:
        """Search for an entity by its ASIC number using SearchByASICv201408."""
        asic = asic.replace(" ", "")
        params = {
            "searchString": asic,
            "includeHistoricalDetails": "Y" if include_historical else "N",
            "authenticationGuid": self.guid
        }
        return self._perform_request(endpoints.SEARCH_BY_ASIC, params, is_list_search=False)

    def search_by_name(self, name: str, state: str = None, postcode: str = None, 
                       min_score: int = 0) -> List[models.SearchResult]:
        """
        Search for entities by name using ABRSearchByNameAdvancedSimpleProtocol2017.
        """
        params = {
            "name": name,
            "postcode": postcode or "",
            "legalName": "",
            "tradingName": "",
            "NSW": "Y" if state == "NSW" or not state else "N",
            "SA": "Y" if state == "SA" or not state else "N",
            "ACT": "Y" if state == "ACT" or not state else "N",
            "VIC": "Y" if state == "VIC" or not state else "N",
            "WA": "Y" if state == "WA" or not state else "N",
            "NT": "Y" if state == "NT" or not state else "N",
            "QLD": "Y" if state == "QLD" or not state else "N",
            "TAS": "Y" if state == "TAS" or not state else "N",
            "authenticationGuid": self.guid,
            "minScore": min_score
        }
        return self._perform_request(endpoints.SEARCH_BY_NAME, params, is_list_search=True)

    def search_by_abn_status(self, postcode: str, active_only: bool = False, 
                             gst_registered_only: bool = False, 
                             entity_type_code: str = "") -> List[models.SearchResult]:
        """
        Search for ABNs by postcode and selected status.
        
        Args:
            postcode (str): The postcode to search.
            active_only (bool): If True, returns only active ABNs.
            gst_registered_only (bool): If True, returns only ABNs with current GST registration.
            entity_type_code (str, optional): Filter by specific entity type code.

        Returns:
            List[models.SearchResult]: List of matching ABNs.
        """
        params = {
            "postcode": postcode,
            "activeABNsOnly": "Y" if active_only else "N",
            "currentGSTRegistrationOnly": "Y" if gst_registered_only else "N",
            "entityTypeCode": entity_type_code,
            "authenticationGuid": self.guid
        }
        return self._perform_request(endpoints.SEARCH_BY_ABN_STATUS, params, is_list_search=True)

    def search_by_charity(self, postcode: str = "", state: str = "", 
                          charity_type_code: str = "", 
                          concession_type_code: str = "") -> List[models.SearchResult]:
        """
        Search for ABNs that have charities tax concessions.
        
        Args:
            postcode (str, optional): Filter by postcode.
            state (str, optional): Filter by state.
            charity_type_code (str, optional): Filter by charity type.
            concession_type_code (str, optional): Filter by concession type.
        """
        params = {
            "postcode": postcode,
            "state": state,
            "charityTypeCode": charity_type_code,
            "concessionTypeCode": concession_type_code,
            "authenticationGuid": self.guid
        }
        return self._perform_request(endpoints.SEARCH_BY_CHARITY, params, is_list_search=True)

    def search_by_postcode(self, postcode: str) -> List[models.SearchResult]:
        """
        Search for currently active ABNs for a postcode.
        """
        params = {
            "postcode": postcode,
            "authenticationGuid": self.guid
        }
        return self._perform_request(endpoints.SEARCH_BY_POSTCODE, params, is_list_search=True)

    def search_by_registration_event(self, month: int, year: int, postcode: str = "", 
                                     state: str = "", entity_type_code: str = "") -> List[models.SearchResult]:
        """
        Search for ABNs that have been registered/re-activated in a specific month and year.
        
        Args:
            month (int): The month (1-12).
            year (int): The year (YYYY).
        """
        params = {
            "postcode": postcode,
            "state": state,
            "entityTypeCode": entity_type_code,
            "month": str(month),
            "year": str(year),
            "authenticationGuid": self.guid
        }
        return self._perform_request(endpoints.SEARCH_BY_REGISTRATION_EVENT, params, is_list_search=True)

    def search_by_update_event(self, update_date: datetime, postcode: str = "", 
                               state: str = "", entity_type_code: str = "") -> List[models.SearchResult]:
        """
        Search for ABNs by update event (includes registrations).
        
        Args:
            update_date (datetime | str): The date of the update (YYYY-MM-DD).
        """
        if isinstance(update_date, datetime) or hasattr(update_date, 'strftime'):
            date_str = update_date.strftime("%Y-%m-%d")
        else:
            date_str = str(update_date)

        params = {
            "postcode": postcode,
            "state": state,
            "entityTypeCode": entity_type_code,
            "updatedate": date_str,
            "authenticationGuid": self.guid
        }
        return self._perform_request(endpoints.SEARCH_BY_UPDATE_EVENT, params, is_list_search=True)

    def _perform_request(self, operation: str, params: dict, is_list_search: bool) -> Union[models.ABNResponse, List[models.SearchResult]]:
        """Helper to build URL, make request, and parse response."""
        query_string = urllib.parse.urlencode(params)
        url = f"{endpoints.BASE_URL}/{operation}?{query_string}"

        try:
            with urllib.request.urlopen(url, timeout=20) as response:
                content = response.read()
                if is_list_search:
                    return self._parse_list_response(content)
                else:
                    return self._parse_single_response(content)
        except urllib.error.HTTPError as e:
            raise exceptions.APIConnectionError(f"HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            raise exceptions.APIConnectionError(f"Failed to connect to ABN Lookup API: {e.reason}")
        except Exception as e:
            raise exceptions.ABNLookupError(f"An unexpected error occurred: {e}")

    def _parse_single_response(self, content: bytes) -> models.ABNResponse:
        """Parses a single entity response (ABN/ASIC search)."""
        try:
            root = ET.fromstring(content)
        except ET.ParseError as e:
            raise exceptions.APIExceptionError(f"Failed to parse XML response: {e}")

        response_node = root.find(f"{self.NAMESPACE}response")
        self._check_exceptions(response_node)

        # Find entity node (handles 202001, 201408, etc.)
        entity = None
        for child in response_node:
            if child.tag.startswith(f"{self.NAMESPACE}businessEntity"):
                entity = child
                break
        
        if entity is None:
            raise exceptions.ABNNotFoundError("No business entity returned in the response.")

        return self._map_entity_to_model(entity)

    def _parse_list_response(self, content: bytes) -> List[models.SearchResult]:
        """Parses a list response (Name, Postcode, Charity, etc.)."""
        try:
            root = ET.fromstring(content)
        except ET.ParseError as e:
            raise exceptions.APIExceptionError(f"Failed to parse XML response: {e}")

        response_node = root.find(f"{self.NAMESPACE}response")
        self._check_exceptions(response_node)

        results = []
        ns = self.NAMESPACE

        # Iterate over all searchResultsRecord elements
        # Note: In most list operations, these are direct children of 'response' in the SimpleProtocol/XMLSearch
        for record in response_node.findall(f"{ns}searchResultsRecord"):
            
            def get_text(tag):
                el = record.find(f"{ns}{tag}")
                return el.text if el is not None else ""

            abn_node = record.find(f"{ns}ABN")
            abn = abn_node.text if abn_node is not None else ""
            
            result = models.SearchResult(
                abn=abn,
                name=get_text("name") or get_text("legalName") or get_text("mainName"), # Different searches might populate different name fields
                score=int(get_text("score") or 0),
                state=get_text("mainBusinessLocationState"),
                postcode=get_text("mainBusinessLocationPostcode"),
                is_current=get_text("isCurrentIndicator") == "Y"
            )
            results.append(result)

        return results

    def _check_exceptions(self, response_node):
        """Checks for API exceptions in the response node."""
        if response_node is None:
             raise exceptions.APIExceptionError("Invalid response structure: 'response' node missing.")
        
        exception_node = response_node.find(f"{self.NAMESPACE}exception")
        if exception_node is not None:
            desc = exception_node.find(f"{self.NAMESPACE}exceptionDescription")
            msg = desc.text if desc is not None else "Unknown API Exception"
            raise exceptions.APIExceptionError(f"API Error: {msg}")

    def _map_entity_to_model(self, entity: ET.Element) -> models.ABNResponse:
        """Maps an XML entity element to the ABNResponse model."""
        ns = self.NAMESPACE
        
        def get_text(node, tag):
            if node is None: return None
            el = node.find(f"{ns}{tag}")
            return el.text if el is not None else None

        def parse_date(date_str):
            if not date_str: return None
            try: return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError: return None

        status_node = entity.find(f"{ns}entityStatus")
        status_obj = models.EntityStatus(
            status_code=get_text(status_node, "entityStatusCode") or "Unknown",
            effective_from=parse_date(get_text(status_node, "effectiveFrom")),
            effective_to=parse_date(get_text(status_node, "effectiveTo"))
        )

        legal_name = None
        legal_node = entity.find(f"{ns}legalName")
        if legal_node:
            org_name = get_text(legal_node, "organisationName")
            if not org_name:
                given = get_text(legal_node, "givenName")
                family = get_text(legal_node, "familyName")
                if given or family:
                    org_name = f"{given or ''} {family or ''}".strip()
            
            legal_name = models.EntityName(
                name=org_name,
                name_type="Legal",
                is_current=get_text(legal_node, "isCurrentIndicator") == "Y"
            )

        main_name = None
        main_node = entity.find(f"{ns}mainName")
        if main_node:
            main_name = models.EntityName(
                name=get_text(main_node, "organisationName"),
                name_type="Main",
                is_current=get_text(main_node, "isCurrentIndicator") == "Y"
            )

        addr_node = entity.find(f"{ns}mainBusinessLocation")
        address = None
        if addr_node:
            address = models.Address(
                state=get_text(addr_node, "mainBusinessLocationState"),
                postcode=get_text(addr_node, "mainBusinessLocationPostcode")
            )

        awef_text = get_text(entity, "approvedWorkerEntitlementFund")
        
        dgr_text = None
        dgr_node = entity.find(f"{ns}dgrFund")
        if dgr_node:
            dgr_text = get_text(dgr_node, "DGRItemNumber")

        acnc_text = None
        acnc_node = entity.find(f"{ns}acncRegistration")
        if acnc_node:
             status = get_text(acnc_node, "status")
             eff_from = get_text(acnc_node, "effectiveFrom")
             acnc_text = f"{status} (Since {eff_from})" if status else "Registered"

        return models.ABNResponse(
            abn=get_text(entity, "ABN"),
            abn_status=status_obj,
            asic_number=get_text(entity, "ASICNumber"),
            entity_type=get_text(entity, "entityType") and get_text(entity.find(f"{ns}entityType"), "entityDescription"),
            legal_name=legal_name,
            main_name=main_name,
            main_business_location=address,
            approved_worker_entitlement_fund=awef_text,
            dgr_item_number=dgr_text,
            acnc_registration=acnc_text
        )