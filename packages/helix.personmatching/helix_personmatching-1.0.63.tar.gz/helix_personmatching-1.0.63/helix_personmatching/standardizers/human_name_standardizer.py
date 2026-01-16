import re
from typing import Optional, List, Sequence, cast
from fhir.resources.R4B.humanname import HumanName
from fhir.resources.R4B.fhirtypes import String, HumanNameType
from nominally import parse_name
from helix_personmatching.fhir_manager.parse_name_result import ParseNameResult
from helix_personmatching.standardizers.human_name_standardizer_result import (
    HumanNameStandardizerResult,
)

import logging

logger = logging.getLogger(__name__)


class HumanNameStandardizer:
    # Common pronouns that might appear in name fields
    PRONOUNS = {
        "she",
        "her",
        "hers",
        "he",
        "him",
        "his",
        "they",
        "them",
        "their",
        "theirs",
        "ze",
        "zir",
        "zirs",
        "xe",
        "xem",
        "xyr",
        "ey",
        "em",
        "eir",
    }

    @staticmethod
    def is_likely_pronoun_only(name_text: str) -> bool:
        """
        Check if a name text contains only pronouns
        :param name_text: The name text to check
        :return: True if the text contains only pronouns, False otherwise
        """
        if not name_text or not name_text.strip():
            return True

        # Tokenize on non-letters so strings like "she/her" become ["she", "her"].
        tokens = re.findall(r"[a-z]+", name_text.lower())
        if not tokens:
            return True

        return set(tokens).issubset(HumanNameStandardizer.PRONOUNS)

    @staticmethod
    def strip_pronouns_from_text(text: str) -> str:
        """
        Remove pronoun tokens from text while preserving non-pronoun content.
        Handles patterns like "Jane (she/her)" -> "Jane" or "Jane she/her" -> "Jane".
        Pronouns are removed when they appear as isolated tokens separated by
        non-letter characters (spaces, slashes, parentheses, etc.).

        :param text: The text that may contain pronouns
        :return: The text with pronoun tokens removed
        """
        if not text or not text.strip():
            return text

        # Pattern matches pronoun words with optional surrounding non-letter delimiters
        # This handles: (she/her), she/her, (they/them/theirs), etc.
        # We build a pattern that matches pronouns as whole words
        pronouns_pattern = r"\b(" + "|".join(HumanNameStandardizer.PRONOUNS) + r")\b"

        # Remove all pronoun tokens (case-insensitive)
        result = re.sub(pronouns_pattern, "", text, flags=re.IGNORECASE)

        # Clean up leftover delimiters: collapse multiple spaces, remove empty parens, etc.
        # Remove parentheses containing only slashes and whitespace like "(/ )" or "( /)"
        result = re.sub(r"\([/\s]*\)", "", result)
        # Remove standalone slashes surrounded by spaces or at boundaries
        result = re.sub(r"\s*/\s*", " ", result)
        # Remove leading/trailing slashes
        result = re.sub(r"^/+|/+$", "", result)
        # Collapse multiple spaces into one
        result = re.sub(r"\s+", " ", result)

        return result.strip()

    @staticmethod
    def is_valid_name_components(name: HumanName | HumanNameType | None) -> bool:
        """
        Check if a HumanName has valid name components (not just pronouns)
        :param name: HumanName object to validate
        :return: True if the name has valid components, False otherwise
        """
        if not name:
            return False

        # FHIR models use *Type aliases (HumanNameType) in many places.
        # Coerce to a concrete HumanName so attribute access is well-typed.
        human_name: HumanName
        if isinstance(name, HumanName):
            human_name = name
        else:
            human_name = HumanName.parse_obj(name)

        # Prefer structured components. If we have a real given/family, treat as valid
        # even if the free-text field contains pronouns.
        if human_name.given:
            for given in human_name.given:
                if given and not HumanNameStandardizer.is_likely_pronoun_only(
                    str(given)
                ):
                    return True

        if human_name.family and not HumanNameStandardizer.is_likely_pronoun_only(
            str(human_name.family)
        ):
            return True

        # Fall back to text when structured components aren't present.
        if human_name.text and str(human_name.text).strip():
            return not HumanNameStandardizer.is_likely_pronoun_only(
                str(human_name.text)
            )

        return False

    @staticmethod
    def standardize(
        *,
        names: list[HumanName] | None,
        capitalize: bool = False,
        verbose: bool = False,
    ) -> list[HumanNameStandardizerResult] | None:
        """
        Standardize a list of human names
        :param names: List of HumanName objects to standardize
        :param capitalize: Whether to capitalize the names
        :param verbose: Whether to print verbose output
        :return: List of HumanNameStandardizerResult objects
        """
        if not names:
            return None
        assert isinstance(names, list)
        return [
            n
            for n in [
                HumanNameStandardizer.standardize_single(
                    name=name, verbose=verbose, capitalize=capitalize
                )
                for name in names
            ]
            if n is not None
        ]

    @staticmethod
    def standardize_single(
        *, name: HumanName | None, capitalize: bool = False, verbose: bool = False
    ) -> HumanNameStandardizerResult | None:
        """
        Standardize a single human name
        :param name: HumanName object to standardize
        :param capitalize: Whether to capitalize the names
        :param verbose: Whether to print verbose output
        :return: HumanNameStandardizerResult object
        """
        if not name:
            return None
        assert isinstance(name, HumanName)

        # Check if the name contains valid components (not just pronouns)
        if not HumanNameStandardizer.is_valid_name_components(name):
            if verbose:
                logger.info(
                    f"Skipping name with invalid components (likely pronouns): {name.text or 'N/A'}"
                )
            return None

        first_name: Optional[str] = (
            str(name.given[0]) if name and name.given and len(name.given) > 0 else None
        )
        family_name: Optional[str] = str(name.family) if name and name.family else None
        middle_name: Optional[str] = (
            str(name.given[1]) if name and name.given and len(name.given) > 1 else None
        )
        # convert FHIR String list to plain list[str]
        suffix: List[str] | None = (
            [str(s) for s in name.suffix] if name.suffix else None
        )
        prefix: List[str] | None = (
            [str(p) for p in name.prefix] if name.prefix else None
        )
        # try to parse names using nominally since the names can be stored in wrong fields
        parsed_name: Optional[ParseNameResult] = HumanNameStandardizer.safe_name_parse(
            name=name,
            verbose=verbose,
        )
        if parsed_name is not None:
            if parsed_name.first:
                first_name = (
                    parsed_name.first.title() if capitalize else parsed_name.first
                )
            if parsed_name.middle:
                # Filter out pronoun-only middle names (e.g., "she/her" without parens)
                if not HumanNameStandardizer.is_likely_pronoun_only(parsed_name.middle):
                    middle_name = (
                        parsed_name.middle.title() if capitalize else parsed_name.middle
                    )
                else:
                    middle_name = None
            if parsed_name.last:
                family_name = (
                    parsed_name.last.title() if capitalize else parsed_name.last
                )
            if parsed_name.title:
                parsed_name.title = (
                    parsed_name.title.title() if capitalize else parsed_name.title
                )
            if parsed_name.suffix:
                if isinstance(parsed_name.suffix, str):
                    parsed_suffix = [s for s in parsed_name.suffix.split(" ")]
                elif isinstance(parsed_name.suffix, list):
                    parsed_suffix = [str(s) for s in parsed_name.suffix]
                else:
                    parsed_suffix = []
                suffix = parsed_suffix
            if parsed_name.prefix and parsed_name.title:
                if isinstance(parsed_name.prefix, str):
                    parsed_prefix = [s for s in parsed_name.prefix.split(" ")]
                elif isinstance(parsed_name.prefix, list):
                    parsed_prefix = [str(s) for s in parsed_name.prefix]
                else:
                    parsed_prefix = []
                prefix = parsed_prefix + [str(parsed_name.title)]
            elif parsed_name.title:
                prefix = [str(parsed_name.title)]

        # Final validation: if we still don't have valid name components after parsing, return None
        if not first_name and not family_name:
            if verbose:
                logger.info("No valid first or family name found after parsing")
            return None

        name_parts: List[str] = []
        if prefix:
            name_parts.extend([str(p) for p in prefix])
        if first_name:
            name_parts.append(first_name)
        if middle_name:
            name_parts.append(middle_name)
        if family_name:
            name_parts.append(family_name)
        if suffix:
            name_parts.extend([str(s) for s in suffix])
        name_text = " ".join(name_parts) if name_parts and len(name_parts) > 0 else None

        standardized_name: HumanName = name.copy()
        if first_name:
            standardized_name.given = cast(
                List[String | None], [cast(String, first_name)]
            )
        if middle_name:
            # ensure the given is initialized as expected list type
            if not standardized_name.given:
                standardized_name.given = cast(List[String | None], [])
            assert standardized_name.given is not None
            standardized_name.given.append(cast(String, middle_name))
        if family_name:
            standardized_name.family = cast(String, family_name)
        if name_text:
            standardized_name.text = cast(String, name_text)
        if suffix:
            standardized_name.suffix = cast(List[String | None], suffix)
        if prefix:
            standardized_name.prefix = cast(List[String | None], prefix)

        nick_name = parsed_name.nickname if parsed_name else None
        # Filter out pronoun-only nicknames (including empty strings)
        if nick_name is not None and HumanNameStandardizer.is_likely_pronoun_only(
            nick_name
        ):
            nick_name = None
        if nick_name and capitalize:
            nick_name = nick_name.title()
        middle_initial = (
            middle_name[0] if middle_name and len(middle_name) > 0 else None
        )
        return HumanNameStandardizerResult(
            name=cast(HumanNameType, standardized_name),
            middle_initial=middle_initial,
            nick_name=nick_name,
        )

    @staticmethod
    def safe_name_parse(
        *,
        name: Optional[HumanName],
        verbose: bool = False,
    ) -> Optional[ParseNameResult]:
        # noinspection PyUnresolvedReferences
        if name is None:
            return None
        assert isinstance(name, HumanName)
        if verbose:
            logger.info("FhirToAttributeDict:safe_name_parse()...")
        combined_name = ""
        try:
            # if both family and given are populated then ignore text
            if name.given is not None and len(name.given) > 0 and name.family:
                combined_name += " ".join([str(g) for g in name.given])
                combined_name += f" {name.family}"
            elif name.text is not None:
                combined_name = name.text
            if not combined_name:
                return None

            # Check if the combined name is just pronouns before parsing
            if HumanNameStandardizer.is_likely_pronoun_only(combined_name):
                if verbose:
                    logger.info(
                        f"Skipping parsing for pronoun-only name: {combined_name}"
                    )
                return None

            # Strip pronouns from the name before parsing
            combined_name = HumanNameStandardizer.strip_pronouns_from_text(
                combined_name
            )

            # Check if the name is empty after stripping pronouns
            if not combined_name or not combined_name.strip():
                if verbose:
                    logger.info("Name became empty after stripping pronouns")
                return None

            result = parse_name(combined_name)
            return ParseNameResult(
                first=result.get("first"),
                middle=result.get("middle"),
                last=result.get("last"),
                title=result.get("title"),
                suffix=result.get("suffix"),
                prefix=result.get("prefix"),
                nickname=result.get("nickname"),
            )
        except Exception as e:
            if verbose:
                logger.info(
                    f"Exception (returning None): Parsing Name: {combined_name}: {e}"
                )
            return None

    @staticmethod
    def get_name_use_priority(name: HumanName) -> int:
        """
        Get the priority order for name use type (lower number = higher priority).
        Used to select primary name for display purposes.
        Note: Matching uses all names (primary + additional_names), so this only affects display.

        :param name: HumanName object
        :return: Priority value (lower is higher priority)
        """
        # Priority order based on FHIR valueset-name-use
        # https://hl7.org/FHIR/valueset-name-use.html
        # All valid FHIR names use codes: usual, official, temp, nickname, anonymous, old, maiden
        use_priority = {
            "usual": 1,  # The name normally used (e.g., "Ken" for "Kenneth")
            "official": 2,  # Legal/registered name as on official documents
            "maiden": 3,  # Name used prior to marriage (typically family name)
            "old": 4,  # Previous/former names
            "temp": 5,  # Temporary names
            "nickname": 6,  # Informal names/aliases
            "anonymous": 7,  # Used when identity is not disclosed
        }
        return use_priority.get(name.use if name.use else "", 999)

    @staticmethod
    def get_primary_human_name(
        *, name: Optional[Sequence[HumanNameType | HumanName]]
    ) -> Optional[HumanName]:
        """
        Get the primary human name from a list of human names, filtering out pronoun-only names.
        Selects name based on FHIR name use priority (usual > official > maiden > old > temp > nickname > anonymous).

        Note: Since matching tries all name combinations (primary + additional_names),
        this primarily determines which name appears in the primary fields for display purposes.

        :param name: List of HumanName objects
        :return: HumanName object with the highest priority
        """
        if name is None:
            return None

        # Normalize to concrete HumanName, then filter out pronoun-only entries.
        normalized_names: List[HumanName] = [
            n if isinstance(n, HumanName) else HumanName.parse_obj(n) for n in name
        ]
        valid_names: List[HumanName] = [
            n
            for n in normalized_names
            if HumanNameStandardizer.is_valid_name_components(n)
        ]

        if not valid_names:
            return None

        # If only one valid name, return it
        if len(valid_names) == 1:
            return valid_names[0]

        # Sort by priority (lower number = higher priority) and return the best
        valid_names.sort(key=HumanNameStandardizer.get_name_use_priority)
        return valid_names[0]

    @staticmethod
    def standardize_text(
        *,
        name: Optional[str],
        capitalize: bool = False,
    ) -> HumanNameStandardizerResult | None:
        """
        Standardize a full name and return the result object
        :param name: Full name to standardize
        :param capitalize: Whether to capitalize the names
        :return: HumanNameStandardizerResult object
        """
        if not name:
            return HumanNameStandardizerResult(
                name=None, middle_initial=None, nick_name=None
            )
        assert isinstance(name, str)

        # Check if the name is just pronouns
        if HumanNameStandardizer.is_likely_pronoun_only(name):
            return HumanNameStandardizerResult(
                name=None, middle_initial=None, nick_name=None
            )

        result = HumanNameStandardizer.standardize_single(
            name=HumanName.validate({"text": name}),
            capitalize=capitalize,
        )
        return result

    @staticmethod
    def standardize_text_simple(
        *,
        name: Optional[str],
        capitalize: bool = False,
    ) -> Optional[str]:
        """
        Standardize a full name and return the text
        :param name: Full name
        :param capitalize: Whether to capitalize the names
        """
        if not name:
            return None
        assert isinstance(name, str)

        # Check if the name is just pronouns
        if HumanNameStandardizer.is_likely_pronoun_only(name):
            return None

        result = HumanNameStandardizer.standardize_text(
            name=name, capitalize=capitalize
        )
        return result.name.text if result and result.name else None
