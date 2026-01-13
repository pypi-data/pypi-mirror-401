"""
Data models for the ABN Lookup response.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date

@dataclass
class EntityStatus:
    status_code: str
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None

@dataclass
class EntityName:
    name: str
    name_type: str
    is_current: bool
    score: int = 0

@dataclass
class Address:
    state: str
    postcode: str


@dataclass
class SearchResult:
    abn: str
    name: str
    score: int
    state: str
    postcode: str
    is_current: bool

@dataclass
class ABNResponse:
    abn: str
    abn_status: EntityStatus
    asic_number: Optional[str] = None
    entity_type: Optional[str] = None
    legal_name: Optional[EntityName] = None
    main_name: Optional[EntityName] = None
    business_names: List[EntityName] = field(default_factory=list)
    trading_names: List[EntityName] = field(default_factory=list)
    main_business_location: Optional[Address] = None
    
    # Specific to SearchByABNv202001
    approved_worker_entitlement_fund: Optional[str] = None 

    # Specific to SearchByASICv201408
    dgr_item_number: Optional[str] = None
    acnc_registration: Optional[str] = None
      