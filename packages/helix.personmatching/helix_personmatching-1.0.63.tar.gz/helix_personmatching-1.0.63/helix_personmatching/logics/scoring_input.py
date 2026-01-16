import json
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from helix_personmatching.utils.json_serializer import EnhancedJSONEncoder


@dataclass
class ScoringInput:
    id_: Optional[str]
    name_given: Optional[str]
    name_middle: Optional[str]
    name_middle_initial: Optional[str]
    name_family: Optional[str]
    gender: Optional[str]
    birth_date: Optional[str]
    address_postal_code: Optional[str]
    address_postal_code_first_five: Optional[str]
    address_line_1: Optional[str]
    address_line_1_st_num: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    birth_date_year: Optional[str]
    birth_date_month: Optional[str]
    birth_date_day: Optional[str]
    phone_area: Optional[str]
    phone_local: Optional[str]
    phone_line: Optional[str]
    email_username: Optional[str]
    is_adult_today: Optional[bool]
    ssn: Optional[str]
    ssn_last4: Optional[str]
    meta_security_client_slug: Optional[str]
    # Additional names for matching against all name variants (usual, official, maiden, old, etc.)
    # Each tuple is (given_name, middle_name, middle_initial, family_name)
    additional_names: List[
        Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]
    ] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(self, cls=EnhancedJSONEncoder)
