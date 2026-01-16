from dataclasses import replace
from typing import List, Optional, Any, Set, Tuple

from nicknames import NickNamer
from rapidfuzz import distance

from helix_personmatching.logics.rule_attribute_score import RuleAttributeScore
from helix_personmatching.logics.rule_score import RuleScore
from helix_personmatching.logics.scoring_input import ScoringInput
from helix_personmatching.models.attribute_entry import AttributeEntry
from helix_personmatching.models.rule import Rule
from helix_personmatching.models.rule_option import RuleOption
from helix_personmatching.models.rules.RuleWeight import RuleWeight
from helix_personmatching.models.string_match_type import StringMatchType

# Name attributes that should be matched against all name variants
NAME_ATTRIBUTES = {"name_given", "name_middle", "name_middle_initial", "name_family"}


class AttributeRule(Rule):
    def __init__(
        self,
        *,
        name: str,
        description: str,
        number: int,
        attributes: List[AttributeEntry],
        weight: RuleWeight,
        enabled: Optional[bool] = True,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            number=number,
            weight=weight,
            enabled=enabled,
        )
        self.attributes: List[AttributeEntry] = attributes

    def score(
        self,
        source: ScoringInput,
        target: ScoringInput,
        rule_option: RuleOption,
        verbose: bool = False,
    ) -> Optional[RuleScore]:
        """
        Calculate a matching score for one rule between FHIR Person-Person, or Person-Patient, or Person/Patient-AppUser.
        For name attributes, tries all name combinations (primary + additional names) and uses the best match.

        :param rule_option: Options for rules for calculating string match
        :param source: Dictionary of Pii data for FHIR Person/Patient data, or AppUser data
        :param target: Dictionary of Pii data for FHIR Person/Patient data, or AppUser data
        :param verbose: set to True to enable logging
        :return: Dictionary of 1 rule score result
        """

        if verbose:
            print("AttributeRule.score()...")

        id_data_source: Optional[Any] = source.id_
        id_data_target: Optional[Any] = target.id_
        if not (id_data_source and id_data_target):
            return None

        # Check if this rule involves name attributes
        rule_has_name_attributes = any(
            attr.name in NAME_ATTRIBUTES for attr in self.attributes
        )

        # If rule has name attributes, try all name combinations
        if rule_has_name_attributes:
            return self._score_with_all_name_combinations(
                source=source,
                target=target,
                rule_option=rule_option,
                verbose=verbose,
            )

        # Standard matching for non-name rules
        return self._score_single_combination(
            source=source,
            target=target,
            rule_option=rule_option,
            verbose=verbose,
        )

    def _get_all_name_variants(
        self, scoring_input: ScoringInput
    ) -> List[Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]]:
        """
        Get all name variants from a ScoringInput (primary + additional names).

        :param scoring_input: ScoringInput object
        :return: List of (given, middle, middle_initial, family) tuples
        """
        # Start with primary name
        variants: List[
            Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]
        ] = [
            (
                scoring_input.name_given,
                scoring_input.name_middle,
                scoring_input.name_middle_initial,
                scoring_input.name_family,
            )
        ]

        # Add additional names
        if scoring_input.additional_names:
            variants.extend(scoring_input.additional_names)

        return variants

    def _score_with_all_name_combinations(
        self,
        source: ScoringInput,
        target: ScoringInput,
        rule_option: RuleOption,
        verbose: bool = False,
    ) -> Optional[RuleScore]:
        """
        Try all name combinations and return the best matching score.
        """
        source_names = self._get_all_name_variants(source)
        target_names = self._get_all_name_variants(target)

        best_score: Optional[RuleScore] = None
        best_total: float = -1.0

        for src_given, src_middle, src_middle_initial, src_family in source_names:
            # Skip source name if both given and family are None (nothing to match on)
            if src_given is None and src_family is None:
                continue

            for tgt_given, tgt_middle, tgt_middle_initial, tgt_family in target_names:
                # Skip the target name if both given and family are None (nothing to match on)
                if tgt_given is None and tgt_family is None:
                    continue

                # Create temporary ScoringInput copies with this name combination
                # Using dataclasses.replace() for cleaner, more maintainable code
                source_copy = replace(
                    source,
                    name_given=src_given,
                    name_middle=src_middle,
                    name_middle_initial=src_middle_initial,
                    name_family=src_family,
                    additional_names=[],  # Don't need for matching
                )

                target_copy = replace(
                    target,
                    name_given=tgt_given,
                    name_middle=tgt_middle,
                    name_middle_initial=tgt_middle_initial,
                    name_family=tgt_family,
                    additional_names=[],  # Don't need for matching
                )

                score = self._score_single_combination(
                    source=source_copy,
                    target=target_copy,
                    rule_option=rule_option,
                    verbose=verbose,
                )

                if score and score.rule_score > best_total:
                    best_total = score.rule_score
                    best_score = score

        return best_score

    def _score_single_combination(
        self,
        source: ScoringInput,
        target: ScoringInput,
        rule_option: RuleOption,
        verbose: bool = False,
    ) -> Optional[RuleScore]:
        """
        Calculate score for a single name combination (original logic).
        """
        id_data_source: Optional[Any] = source.id_
        id_data_target: Optional[Any] = target.id_
        if not (id_data_source and id_data_target):
            return None

        rule_attribute_scores: List[RuleAttributeScore] = []
        score_avg: float = 0.0
        for attribute in self.attributes:
            rule_attribute_score: RuleAttributeScore = RuleAttributeScore(
                attribute=attribute, score=0.0, present=False, source=None, target=None
            )
            val_source: Optional[str] = getattr(source, attribute.name)
            val_target: Optional[str] = getattr(target, attribute.name)

            if val_source and val_target:
                rule_attribute_score.present = True

                # calculate string match
                score_for_attribute, string_match_type = self.calculate_string_match(
                    attribute=attribute,
                    val_source=val_source,
                    val_target=val_target,
                    nick_namer=rule_option.nick_namer,
                    verbose=verbose,
                )
                score_avg += score_for_attribute

                rule_attribute_score.score = score_for_attribute
                rule_attribute_score.source = val_source
                rule_attribute_score.target = val_target
                rule_attribute_score.string_match_type = string_match_type
            elif not val_source or not val_target:
                rule_attribute_score.score = self.weight.missing
                score_avg += self.weight.missing

            rule_attribute_scores.append(rule_attribute_score)

        score_avg /= len(self.attributes)

        final_rule_score = (
            self.weight.exact_match
            if score_avg == 1.0
            else (score_avg * self.weight.partial_match)
        )

        rule_score: RuleScore = RuleScore(
            id_source=str(id_data_source),
            id_target=str(id_data_target),
            rule_name=self.name,
            rule_description=self.description,
            rule_score=final_rule_score,
            rule_unweighted_score=score_avg,
            rule_weight=self.weight,
            attribute_scores=rule_attribute_scores,
        )

        return rule_score

    @staticmethod
    def calculate_string_match(
        *,
        attribute: AttributeEntry,
        val_source: Optional[str],
        val_target: Optional[str],
        nick_namer: NickNamer,
        verbose: bool = False,
    ) -> Tuple[float, StringMatchType]:
        """
        Returns a score from 0 to 1 where 1 is an exact match

        :param attribute:
        :param val_source:
        :param val_target:
        :param nick_namer:
        :param verbose: set to True to enable logging
        :return:
        """

        if verbose:
            print("AttributeRule.calculate_string_match()...")

        val_source_cleansed: str = str(val_source).strip().lower()
        val_target_cleansed: str = str(val_target).strip().lower()

        get_standard_weight: RuleWeight = RuleWeight.get_standard_weight()

        if attribute.name == "gender":
            if val_source_cleansed == val_target_cleansed:
                return 1.0, StringMatchType.Exact
            elif (
                val_source_cleansed == "male" and val_target_cleansed == "female"
            ) or (val_source_cleansed == "female" and val_target_cleansed == "male"):
                return 0.0, StringMatchType.NoMatch
            # for "other" or "unknown", treat them the same way.
            elif (
                val_source_cleansed in ["male", "female"]
                and val_target_cleansed in ["other", "unknown"]
            ) or (
                val_source_cleansed in ["other", "unknown"]
                and val_target_cleansed in ["male", "female"]
            ):
                # use the standard weight's missing weight, being 0.75
                return get_standard_weight.missing, StringMatchType.Partial
            else:
                return 0.0, StringMatchType.NoMatch

        if attribute.exact_only:
            if val_source_cleansed == val_target_cleansed:
                return 1.0, StringMatchType.Exact
            else:
                return 0.0, StringMatchType.NoMatch

        # Calculates a normalized levenshtein similarity in the range [0, 1] using custom
        #     costs for insertion, deletion and substitution.
        #     This is calculated as `1 - normalized_distance`
        # Algorithm - https://en.wikipedia.org/wiki/Levenshtein_distance
        # Py pkg - https://github.com/maxbachmann/RapidFuzz/blob/main/src/rapidfuzz/distance/Levenshtein_py.py#L286

        score_for_attribute = distance.Levenshtein.normalized_similarity(
            val_source_cleansed,
            val_target_cleansed,
            # (give more weight to substitution since that is more typical to press a wrong key)
            weights=(1, 1, 2),  # insert, deletion, substitution
            score_cutoff=0.7,  # usually no more than two character changes
        )

        # if exact match did not work then try matching on nicknames

        # canonicals_of(): Returns a set of all the canonical names for a name.
        # - https://github.com/carltonnorthern/nicknames/blob/master/python/src/nicknames/__init__.py#L61
        if score_for_attribute < 1.0 and attribute.nick_name_match:
            canonicals_source: Set[str] = nick_namer.canonicals_of(
                val_source_cleansed
            ) | {val_source_cleansed}
            canonicals_target: Set[str] = nick_namer.canonicals_of(
                val_target_cleansed
            ) | {val_target_cleansed}

            # Return the intersection of two sets as a new set
            matching_set: Set[str] = canonicals_source.intersection(canonicals_target)
            if len(matching_set) > 0:
                return 1.0, StringMatchType.Synonym

        return (
            score_for_attribute,
            (
                StringMatchType.Partial
                if score_for_attribute < 1.0
                else StringMatchType.Exact
            ),
        )
