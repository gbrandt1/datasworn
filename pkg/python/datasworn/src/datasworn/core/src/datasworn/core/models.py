from __future__ import annotations
from typing import Any, Literal, Optional, Union
from pydantic import (
    AnyUrl,
    BaseModel as _BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    RootModel,
)
from collections.abc import Mapping, Sequence
from datetime import date as date_aliased


class BaseModel(_BaseModel):
    model_config = ConfigDict(
        extra="allow",
        use_attribute_docstrings=True,
    )


class ActionRollMethod(
    RootModel[
        Literal[
            "miss",
            "weak_hit",
            "strong_hit",
            "player_choice",
            "highest",
            "lowest",
            "all",
        ]
    ]
):
    root: Literal[
        "miss", "weak_hit", "strong_hit", "player_choice", "highest", "lowest", "all"
    ] = Field(..., title="ActionRollMethod")


class Asset(BaseModel):
    field_id: AssetId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[AssetIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    category: Label
    options: Mapping[str, AssetOptionField]
    requirement: Optional[MarkdownString] = None
    abilities: Sequence[AssetAbility]
    controls: Optional[Mapping[str, AssetControlField]] = {}
    count_as_impact: bool
    attachments: Optional[AssetAttachment] = None
    shared: bool
    type: Literal["asset"] = "asset"


class AssetAbility(BaseModel):
    field_id: AssetAbilityId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Optional[Label] = None
    text: MarkdownString
    enabled: bool
    moves: Optional[AssetAbilityMoves] = Field(
        default_factory=lambda: AssetAbilityMoves({}), title="AssetAbilityMoves"
    )
    oracles: Optional[AssetAbilityOracles] = Field(
        default_factory=lambda: AssetAbilityOracles({}), title="AssetAbilityOracles"
    )
    options: Optional[Mapping[str, AssetAbilityOptionField]] = {}
    controls: Optional[Mapping[str, AssetAbilityControlField]] = {}
    enhance_asset: Optional[AssetEnhancement] = None
    enhance_moves: Optional[Sequence[MoveEnhancement]] = None
    tags: Optional[Tags] = None


class AssetAbilityId(RootModel[str]):
    root: str = Field(..., title="AssetAbilityId")


class AssetAbilityIdWildcard(RootModel[str]):
    root: str = Field(..., title="AssetAbilityIdWildcard")


class AssetAbilityMoveId(RootModel[str]):
    root: str = Field(..., title="AssetAbilityMoveId")


class AssetAbilityMoveIdWildcard(RootModel[str]):
    root: str = Field(..., title="AssetAbilityMoveIdWildcard")


class AssetAbilityOracleRollableId(RootModel[str]):
    root: str = Field(..., title="AssetAbilityOracleRollableId")


class AssetAbilityOracleRollableIdWildcard(RootModel[str]):
    root: str = Field(..., title="AssetAbilityOracleRollableIdWildcard")


class AssetAbilityOracleRollableRowId(RootModel[str]):
    root: str = Field(..., title="AssetAbilityOracleRollableRowId")


class AssetAbilityOracleRollableRowIdWildcard(RootModel[str]):
    root: str = Field(..., title="AssetAbilityOracleRollableRowIdWildcard")


class AssetAttachment(BaseModel):
    assets: Sequence[AssetIdWildcard]
    max: Optional[int]


class AssetCardFlipField(BaseModel):
    label: Label
    value: bool
    field_type: Literal["card_flip"] = "card_flip"
    icon: Optional[SvgImageUrl] = None
    is_impact: bool
    disables_asset: bool


class AssetCheckboxField(BaseModel):
    label: Label
    value: bool
    field_type: Literal["checkbox"] = "checkbox"
    icon: Optional[SvgImageUrl] = None
    is_impact: bool
    disables_asset: bool


class AssetCollection(BaseModel):
    field_id: AssetCollectionId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[AssetCollectionIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    enhances: Optional[Sequence[AssetCollectionIdWildcard]] = None
    summary: Optional[MarkdownString] = None
    contents: Mapping[str, Asset]
    collections: Mapping[str, AssetCollection]
    type: Literal["asset_collection"] = "asset_collection"


class AssetCollectionId(RootModel[str]):
    root: str = Field(..., title="AssetCollectionId")


class AssetCollectionIdWildcard(RootModel[str]):
    root: str = Field(..., title="AssetCollectionIdWildcard")


class AssetConditionMeter(BaseModel):
    label: Label
    value: int
    min: int
    max: int
    rollable: Literal[True] = True
    field_type: Literal["condition_meter"] = "condition_meter"
    icon: Optional[SvgImageUrl] = None
    moves: Optional[Moves] = None
    controls: Mapping[str, AssetConditionMeterControlField]


class AssetConditionMeterControlField(
    RootModel[Union[AssetCheckboxField, AssetCardFlipField]]
):
    root: Union[AssetCheckboxField, AssetCardFlipField]


class AssetConditionMeterEnhancement(BaseModel):
    field_type: Literal["condition_meter"] = "condition_meter"
    max: int


class AssetControlFieldEnhancement(RootModel[AssetConditionMeterEnhancement]):
    root: AssetConditionMeterEnhancement


class AssetControlValueRef(BaseModel):
    assets: Optional[Sequence[AssetIdWildcard]]
    control: DictKey
    using: Literal["asset_control"] = "asset_control"


class AssetEnhancement(BaseModel):
    controls: Optional[Mapping[str, AssetControlFieldEnhancement]] = None
    suggestions: Optional[Suggestions] = None
    count_as_impact: Optional[bool] = None
    attachments: Optional[AssetAttachment] = None
    shared: Optional[bool] = None


class AssetId(RootModel[str]):
    root: str = Field(..., title="AssetId")


class AssetIdWildcard(RootModel[str]):
    root: str = Field(..., title="AssetIdWildcard")


class AssetOptionValueRef(BaseModel):
    assets: Optional[Sequence[AssetIdWildcard]]
    option: DictKey
    using: Literal["asset_option"] = "asset_option"


class AtlasCollection(BaseModel):
    field_id: AtlasCollectionId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[AtlasCollectionIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    enhances: Optional[Sequence[AtlasCollectionIdWildcard]] = None
    summary: Optional[MarkdownString] = None
    contents: Mapping[str, AtlasEntry]
    collections: Mapping[str, AtlasCollection]
    type: Literal["atlas_collection"] = "atlas_collection"


class AtlasCollectionId(RootModel[str]):
    root: str = Field(..., title="AtlasCollectionId")


class AtlasCollectionIdWildcard(RootModel[str]):
    root: str = Field(..., title="AtlasCollectionIdWildcard")


class AtlasEntry(BaseModel):
    field_id: AtlasEntryId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[AtlasEntryIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    features: Sequence[MarkdownString]
    summary: Optional[MarkdownString] = None
    quest_starter: Optional[MarkdownString] = None
    your_truth: Optional[MarkdownString] = None
    type: Literal["atlas_entry"] = "atlas_entry"


class AtlasEntryId(RootModel[str]):
    root: str = Field(..., title="AtlasEntryId")


class AtlasEntryIdWildcard(RootModel[str]):
    root: str = Field(..., title="AtlasEntryIdWildcard")


class AttachedAssetControlValueRef(BaseModel):
    control: DictKey
    using: Literal["attached_asset_control"] = "attached_asset_control"


class AttachedAssetOptionValueRef(BaseModel):
    option: DictKey
    using: Literal["attached_asset_option"] = "attached_asset_option"


class AuthorInfo(BaseModel):
    name: Label
    email: Optional[Email] = None
    url: Optional[WebUrl] = None


class ChallengeRank(RootModel[Literal[1, 2, 3, 4, 5]]):
    root: Literal[1, 2, 3, 4, 5] = Field(..., title="ChallengeRank")


class ClockField(BaseModel):
    label: Label
    value: int
    min: Literal[0] = 0
    max: ClockSize = Field(..., title="ClockSize")
    rollable: Literal[False] = False
    field_type: Literal["clock"] = "clock"
    icon: Optional[SvgImageUrl] = None


class ClockSize(RootModel[int]):
    root: int = Field(..., title="ClockSize")


class CollectableType(
    RootModel[Literal["atlas_entry", "npc", "oracle_rollable", "asset", "move"]]
):
    root: Literal["atlas_entry", "npc", "oracle_rollable", "asset", "move"] = Field(
        ..., title="CollectableType"
    )


class CollectionType(
    RootModel[
        Literal[
            "atlas_collection",
            "npc_collection",
            "oracle_collection",
            "asset_collection",
            "move_category",
        ]
    ]
):
    root: Literal[
        "atlas_collection",
        "npc_collection",
        "oracle_collection",
        "asset_collection",
        "move_category",
    ] = Field(..., title="CollectionType")


class ConditionMeterField(BaseModel):
    label: Label
    value: int
    min: int
    max: int
    rollable: Literal[True] = True
    field_type: Literal["condition_meter"] = "condition_meter"
    icon: Optional[SvgImageUrl] = None


class ConditionMeterRule(BaseModel):
    shared: bool
    tags: Optional[Tags] = None
    label: Label
    value: int
    min: int
    max: int
    rollable: Literal[True] = True


class ConditionMeterValueRef(BaseModel):
    condition_meter: ConditionMeterKey
    using: Literal["condition_meter"] = "condition_meter"


class CoreSchemaMetaSchema(BaseModel):
    field_id: Optional[str] = Field(None, alias="_id")
    field_schema: Optional[AnyUrl] = Field(None, alias="_schema")
    field_ref: Optional[str] = Field(None, alias="_ref")
    field_comment: Optional[str] = Field(None, alias="_comment")
    title: Optional[str] = None
    description: Optional[str] = None
    default: Optional[Any] = None
    read_only: Optional[bool] = Field(False, alias="readOnly")
    write_only: Optional[bool] = Field(False, alias="writeOnly")
    examples: Optional[Sequence[Any]] = None
    multiple_of: Optional[float] = Field(None, alias="multipleOf", gt=0.0)
    maximum: Optional[float] = None
    exclusive_maximum: Optional[float] = Field(None, alias="exclusiveMaximum")
    minimum: Optional[float] = None
    exclusive_minimum: Optional[float] = Field(None, alias="exclusiveMinimum")
    max_length: Optional[NonNegativeInteger] = Field(None, alias="maxLength")
    min_length: Optional[NonNegativeIntegerDefault0] = Field(None, alias="minLength")
    pattern: Optional[str] = None
    additional_items: Optional[Schema] = Field(
        default_factory=lambda: Schema(True), alias="additionalItems"
    )
    items: Optional[Union[Schema, SchemaArray]] = Field(
        default_factory=lambda: Schema(True)
    )
    max_items: Optional[NonNegativeInteger] = Field(None, alias="maxItems")
    min_items: Optional[NonNegativeIntegerDefault0] = Field(None, alias="minItems")
    unique_items: Optional[bool] = Field(False, alias="uniqueItems")
    contains: Optional[Schema] = Field(default_factory=lambda: Schema(True))
    max_properties: Optional[NonNegativeInteger] = Field(None, alias="maxProperties")
    min_properties: Optional[NonNegativeIntegerDefault0] = Field(
        None, alias="minProperties"
    )
    required: Optional[StringArray] = None
    additional_properties: Optional[Schema] = Field(
        default_factory=lambda: Schema(True), alias="additionalProperties"
    )
    definitions: Optional[Mapping[str, Schema]] = Field(
        default_factory=lambda: Schema({})
    )
    properties: Optional[Mapping[str, Schema]] = Field(
        default_factory=lambda: Schema({})
    )
    pattern_properties: Optional[Mapping[str, Schema]] = Field(
        default_factory=lambda: Schema({}), alias="patternProperties"
    )
    dependencies: Optional[Mapping[str, Union[Schema, StringArray]]] = None
    property_names: Optional[Schema] = Field(
        default_factory=lambda: Schema(True), alias="propertyNames"
    )
    const: Optional[Any] = None
    enum: Optional[frozenset[Any]] = Field(None, min_length=1)
    type: Optional[Union[SimpleTypes, Type]] = None
    format: Optional[str] = None
    content_media_type: Optional[str] = Field(None, alias="contentMediaType")
    content_encoding: Optional[str] = Field(None, alias="contentEncoding")
    if_: Optional[Schema] = Field(default_factory=lambda: Schema(True), alias="if")
    then: Optional[Schema] = Field(default_factory=lambda: Schema(True))
    else_: Optional[Schema] = Field(default_factory=lambda: Schema(True), alias="else")
    all_of: Optional[SchemaArray] = Field(None, alias="allOf")
    any_of: Optional[SchemaArray] = Field(None, alias="anyOf")
    one_of: Optional[SchemaArray] = Field(None, alias="oneOf")
    not_: Optional[Schema] = Field(default_factory=lambda: Schema(True), alias="not")


class CoreTags(BaseModel):
    supernatural: Optional[bool] = None
    technological: Optional[bool] = None
    requires_allies: Optional[bool] = None


class CounterField(BaseModel):
    label: Label
    value: int
    min: int
    max: Optional[int]
    rollable: Literal[False] = False
    field_type: Literal["counter"] = "counter"
    icon: Optional[SvgImageUrl] = None


class CssColor(RootModel[str]):
    root: str = Field(..., title="CssColor")


class CustomValue(BaseModel):
    label: Label
    value: int
    using: Literal["custom"] = "custom"


class Danger(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic24 = Field(..., title="DiceRangeStatic")


class Danger1(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic25 = Field(..., title="DiceRangeStatic")


class Danger2(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic26 = Field(..., title="DiceRangeStatic")


class Danger3(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic27 = Field(..., title="DiceRangeStatic")


class Danger4(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic28 = Field(..., title="DiceRangeStatic")


class Dangers(RootModel[tuple[Danger, Danger1, Danger2, Danger3, Danger4]]):
    root: tuple[Danger, Danger1, Danger2, Danger3, Danger4] = Field(
        ..., max_length=5, min_length=5
    )


class Dangers1Item(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic34 = Field(..., title="DiceRangeStatic")


class Dangers1Item1(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic35 = Field(..., title="DiceRangeStatic")


class Dangers1Item10(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic44 = Field(..., title="DiceRangeStatic")


class Dangers1Item11(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic45 = Field(..., title="DiceRangeStatic")


class Dangers1Item2(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic36 = Field(..., title="DiceRangeStatic")


class Dangers1Item3(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic37 = Field(..., title="DiceRangeStatic")


class Dangers1Item4(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic38 = Field(..., title="DiceRangeStatic")


class Dangers1Item5(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic39 = Field(..., title="DiceRangeStatic")


class Dangers1Item6(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic40 = Field(..., title="DiceRangeStatic")


class Dangers1Item7(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic41 = Field(..., title="DiceRangeStatic")


class Dangers1Item8(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic42 = Field(..., title="DiceRangeStatic")


class Dangers1Item9(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic43 = Field(..., title="DiceRangeStatic")


class Dangers1(
    RootModel[
        tuple[
            Dangers1Item,
            Dangers1Item1,
            Dangers1Item2,
            Dangers1Item3,
            Dangers1Item4,
            Dangers1Item5,
            Dangers1Item6,
            Dangers1Item7,
            Dangers1Item8,
            Dangers1Item9,
            Dangers1Item10,
            Dangers1Item11,
        ]
    ]
):
    root: tuple[
        Dangers1Item,
        Dangers1Item1,
        Dangers1Item2,
        Dangers1Item3,
        Dangers1Item4,
        Dangers1Item5,
        Dangers1Item6,
        Dangers1Item7,
        Dangers1Item8,
        Dangers1Item9,
        Dangers1Item10,
        Dangers1Item11,
    ] = Field(..., max_length=12, min_length=12)


class DelveSite(BaseModel):
    field_id: DelveSiteId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[DelveSiteIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    rank: ChallengeRank
    region: Optional[AtlasEntryId] = None
    theme: DelveSiteThemeId
    domain: DelveSiteDomainId
    extra_card: Optional[Union[DelveSiteThemeId, DelveSiteDomainId]] = None
    denizens: Union[Sequence[DelveSiteDenizen], Denizens]
    type: Literal["delve_site"] = "delve_site"


class DelveSiteDenizen(BaseModel):
    name: Optional[Label] = None
    npc: Optional[NpcId] = None
    frequency: DelveSiteDenizenFrequency
    roll: DiceRange
    field_id: Optional[DelveSiteDenizenId] = Field(None, alias="_id")


class DelveSiteDenizenFrequency(
    RootModel[Literal["very_common", "common", "uncommon", "rare", "unforeseen"]]
):
    root: Literal["very_common", "common", "uncommon", "rare", "unforeseen"] = Field(
        ..., title="DelveSiteDenizenFrequency"
    )


class DelveSiteDenizenId(RootModel[str]):
    root: str = Field(..., title="DelveSiteDenizenId")


class DelveSiteDenizenIdWildcard(RootModel[str]):
    root: str = Field(..., title="DelveSiteDenizenIdWildcard")


class DelveSiteDenizenStatic(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["very_common"] = "very_common"
    roll: DiceRangeStatic = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic1(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["common"] = "common"
    roll: DiceRangeStatic1 = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic10(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["rare"] = "rare"
    roll: DiceRangeStatic10 = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic11(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["unforeseen"] = "unforeseen"
    roll: DiceRangeStatic11 = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic2(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["common"] = "common"
    roll: DiceRangeStatic2 = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic3(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["common"] = "common"
    roll: DiceRangeStatic3 = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic4(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["uncommon"] = "uncommon"
    roll: DiceRangeStatic4 = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic5(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["uncommon"] = "uncommon"
    roll: DiceRangeStatic5 = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic6(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["uncommon"] = "uncommon"
    roll: DiceRangeStatic6 = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic7(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["uncommon"] = "uncommon"
    roll: DiceRangeStatic7 = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic8(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["rare"] = "rare"
    roll: DiceRangeStatic8 = Field(..., title="DiceRangeStatic")


class DelveSiteDenizenStatic9(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    frequency: Literal["rare"] = "rare"
    roll: DiceRangeStatic9 = Field(..., title="DiceRangeStatic")


class DelveSiteDomain(BaseModel):
    field_id: DelveSiteDomainId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[DelveSiteDomainIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    summary: MarkdownString
    descriptipn: Optional[MarkdownString] = None
    name_oracle: Optional[OracleRollableId] = None
    features: Union[Sequence[DelveSiteDomainFeature], Features]
    dangers: Union[Sequence[DelveSiteDomainDanger], Dangers]
    type: Literal["delve_site_domain"] = "delve_site_domain"


class DelveSiteDomainDanger(BaseModel):
    text: MarkdownString
    icon: Optional[SvgImageUrl] = None
    oracle_rolls: Optional[Sequence[OracleRoll]] = None
    suggestions: Optional[Suggestions] = None
    embed_table: Optional[str] = None
    template: Optional[OracleRollTemplate] = None
    field_i18n: Optional[I18nHints] = Field(None, alias="_i18n")
    roll: Optional[DiceRange]
    tags: Optional[Tags] = None
    field_id: DelveSiteDomainDangerId = Field(..., alias="_id")


class DelveSiteDomainDangerId(RootModel[str]):
    root: str = Field(..., title="DelveSiteDomainDangerId")


class DelveSiteDomainDangerIdWildcard(RootModel[str]):
    root: str = Field(..., title="DelveSiteDomainDangerIdWildcard")


class DelveSiteDomainFeature(BaseModel):
    text: MarkdownString
    icon: Optional[SvgImageUrl] = None
    oracle_rolls: Optional[Sequence[OracleRoll]] = None
    suggestions: Optional[Suggestions] = None
    embed_table: Optional[str] = None
    template: Optional[OracleRollTemplate] = None
    field_i18n: Optional[I18nHints] = Field(None, alias="_i18n")
    roll: Optional[DiceRange]
    tags: Optional[Tags] = None
    field_id: DelveSiteDomainFeatureId = Field(..., alias="_id")


class DelveSiteDomainFeatureId(RootModel[str]):
    root: str = Field(..., title="DelveSiteDomainFeatureId")


class DelveSiteDomainFeatureIdWildcard(RootModel[str]):
    root: str = Field(..., title="DelveSiteDomainFeatureIdWildcard")


class DelveSiteDomainId(RootModel[str]):
    root: str = Field(..., title="DelveSiteDomainId")


class DelveSiteDomainIdWildcard(RootModel[str]):
    root: str = Field(..., title="DelveSiteDomainIdWildcard")


class DelveSiteId(RootModel[str]):
    root: str = Field(..., title="DelveSiteId")


class DelveSiteIdWildcard(RootModel[str]):
    root: str = Field(..., title="DelveSiteIdWildcard")


class DelveSiteTheme(BaseModel):
    field_id: DelveSiteThemeId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[DelveSiteThemeIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    summary: MarkdownString
    descriptipn: Optional[MarkdownString] = None
    features: Union[Sequence[DelveSiteThemeFeature], Features1]
    dangers: Union[Sequence[DelveSiteThemeDanger], Dangers1]
    type: Literal["delve_site_theme"] = "delve_site_theme"


class DelveSiteThemeDanger(BaseModel):
    text: MarkdownString
    icon: Optional[SvgImageUrl] = None
    oracle_rolls: Optional[Sequence[OracleRoll]] = None
    suggestions: Optional[Suggestions] = None
    embed_table: Optional[str] = None
    template: Optional[OracleRollTemplate] = None
    field_i18n: Optional[I18nHints] = Field(None, alias="_i18n")
    roll: Optional[DiceRange]
    tags: Optional[Tags] = None
    field_id: DelveSiteThemeDangerId = Field(..., alias="_id")


class DelveSiteThemeDangerId(RootModel[str]):
    root: str = Field(..., title="DelveSiteThemeDangerId")


class DelveSiteThemeDangerIdWildcard(RootModel[str]):
    root: str = Field(..., title="DelveSiteThemeDangerIdWildcard")


class DelveSiteThemeFeature(BaseModel):
    text: MarkdownString
    icon: Optional[SvgImageUrl] = None
    oracle_rolls: Optional[Sequence[OracleRoll]] = None
    suggestions: Optional[Suggestions] = None
    embed_table: Optional[str] = None
    template: Optional[OracleRollTemplate] = None
    field_i18n: Optional[I18nHints] = Field(None, alias="_i18n")
    roll: Optional[DiceRange]
    tags: Optional[Tags] = None
    field_id: DelveSiteThemeFeatureId = Field(..., alias="_id")


class DelveSiteThemeFeatureId(RootModel[str]):
    root: str = Field(..., title="DelveSiteThemeFeatureId")


class DelveSiteThemeFeatureIdWildcard(RootModel[str]):
    root: str = Field(..., title="DelveSiteThemeFeatureIdWildcard")


class DelveSiteThemeId(RootModel[str]):
    root: str = Field(..., title="DelveSiteThemeId")


class DelveSiteThemeIdWildcard(RootModel[str]):
    root: str = Field(..., title="DelveSiteThemeIdWildcard")


class Denizens(
    RootModel[
        tuple[
            DelveSiteDenizenStatic,
            DelveSiteDenizenStatic1,
            DelveSiteDenizenStatic2,
            DelveSiteDenizenStatic3,
            DelveSiteDenizenStatic4,
            DelveSiteDenizenStatic5,
            DelveSiteDenizenStatic6,
            DelveSiteDenizenStatic7,
            DelveSiteDenizenStatic8,
            DelveSiteDenizenStatic9,
            DelveSiteDenizenStatic10,
            DelveSiteDenizenStatic11,
        ]
    ]
):
    root: tuple[
        DelveSiteDenizenStatic,
        DelveSiteDenizenStatic1,
        DelveSiteDenizenStatic2,
        DelveSiteDenizenStatic3,
        DelveSiteDenizenStatic4,
        DelveSiteDenizenStatic5,
        DelveSiteDenizenStatic6,
        DelveSiteDenizenStatic7,
        DelveSiteDenizenStatic8,
        DelveSiteDenizenStatic9,
        DelveSiteDenizenStatic10,
        DelveSiteDenizenStatic11,
    ] = Field(..., max_length=12, min_length=12)


class DiceExpression(RootModel[str]):
    root: str = Field(..., title="DiceExpression")


class DiceRange(BaseModel):
    min: int
    max: int


class DiceRangeStatic(BaseModel):
    min: Literal[1] = 1
    max: Literal[27] = 27


class DiceRangeStatic1(BaseModel):
    min: Literal[28] = 28
    max: Literal[41] = 41


class DiceRangeStatic10(BaseModel):
    min: Literal[98] = 98
    max: Literal[99] = 99


class DiceRangeStatic11(BaseModel):
    min: Literal[100] = 100
    max: Literal[100] = 100


class DiceRangeStatic12(BaseModel):
    min: Literal[21] = 21
    max: Literal[43] = 43


class DiceRangeStatic13(BaseModel):
    min: Literal[44] = 44
    max: Literal[56] = 56


class DiceRangeStatic14(BaseModel):
    min: Literal[57] = 57
    max: Literal[64] = 64


class DiceRangeStatic15(BaseModel):
    min: Literal[65] = 65
    max: Literal[68] = 68


class DiceRangeStatic16(BaseModel):
    min: Literal[69] = 69
    max: Literal[72] = 72


class DiceRangeStatic17(BaseModel):
    min: Literal[73] = 73
    max: Literal[76] = 76


class DiceRangeStatic18(BaseModel):
    min: Literal[77] = 77
    max: Literal[80] = 80


class DiceRangeStatic19(BaseModel):
    min: Literal[81] = 81
    max: Literal[84] = 84


class DiceRangeStatic2(BaseModel):
    min: Literal[42] = 42
    max: Literal[55] = 55


class DiceRangeStatic20(BaseModel):
    min: Literal[85] = 85
    max: Literal[88] = 88


class DiceRangeStatic21(BaseModel):
    min: Literal[89] = 89
    max: Literal[98] = 98


class DiceRangeStatic22(BaseModel):
    min: Literal[99] = 99
    max: Literal[99] = 99


class DiceRangeStatic24(BaseModel):
    min: Literal[31] = 31
    max: Literal[33] = 33


class DiceRangeStatic25(BaseModel):
    min: Literal[34] = 34
    max: Literal[36] = 36


class DiceRangeStatic26(BaseModel):
    min: Literal[37] = 37
    max: Literal[39] = 39


class DiceRangeStatic27(BaseModel):
    min: Literal[40] = 40
    max: Literal[42] = 42


class DiceRangeStatic28(BaseModel):
    min: Literal[43] = 43
    max: Literal[45] = 45


class DiceRangeStatic29(BaseModel):
    min: Literal[1] = 1
    max: Literal[4] = 4


class DiceRangeStatic3(BaseModel):
    min: Literal[56] = 56
    max: Literal[69] = 69


class DiceRangeStatic30(BaseModel):
    min: Literal[5] = 5
    max: Literal[8] = 8


class DiceRangeStatic31(BaseModel):
    min: Literal[9] = 9
    max: Literal[12] = 12


class DiceRangeStatic32(BaseModel):
    min: Literal[13] = 13
    max: Literal[16] = 16


class DiceRangeStatic33(BaseModel):
    min: Literal[17] = 17
    max: Literal[20] = 20


class DiceRangeStatic34(BaseModel):
    min: Literal[1] = 1
    max: Literal[5] = 5


class DiceRangeStatic35(BaseModel):
    min: Literal[6] = 6
    max: Literal[10] = 10


class DiceRangeStatic36(BaseModel):
    min: Literal[11] = 11
    max: Literal[12] = 12


class DiceRangeStatic37(BaseModel):
    min: Literal[13] = 13
    max: Literal[14] = 14


class DiceRangeStatic38(BaseModel):
    min: Literal[15] = 15
    max: Literal[16] = 16


class DiceRangeStatic39(BaseModel):
    min: Literal[17] = 17
    max: Literal[18] = 18


class DiceRangeStatic4(BaseModel):
    min: Literal[70] = 70
    max: Literal[75] = 75


class DiceRangeStatic40(BaseModel):
    min: Literal[19] = 19
    max: Literal[20] = 20


class DiceRangeStatic41(BaseModel):
    min: Literal[21] = 21
    max: Literal[22] = 22


class DiceRangeStatic42(BaseModel):
    min: Literal[23] = 23
    max: Literal[24] = 24


class DiceRangeStatic43(BaseModel):
    min: Literal[25] = 25
    max: Literal[26] = 26


class DiceRangeStatic44(BaseModel):
    min: Literal[27] = 27
    max: Literal[28] = 28


class DiceRangeStatic45(BaseModel):
    min: Literal[29] = 29
    max: Literal[30] = 30


class DiceRangeStatic5(BaseModel):
    min: Literal[76] = 76
    max: Literal[81] = 81


class DiceRangeStatic6(BaseModel):
    min: Literal[82] = 82
    max: Literal[87] = 87


class DiceRangeStatic7(BaseModel):
    min: Literal[88] = 88
    max: Literal[93] = 93


class DiceRangeStatic8(BaseModel):
    min: Literal[94] = 94
    max: Literal[95] = 95


class DiceRangeStatic9(BaseModel):
    min: Literal[96] = 96
    max: Literal[97] = 97


class DictKey(RootModel[str]):
    root: str = Field(..., title="DictKey")


class ConditionMeterKey(RootModel[DictKey]):
    root: DictKey = Field(..., title="ConditionMeterKey")


class Documentation(RootModel[str]):
    root: str = Field(..., title="Documentation")


class Email(RootModel[EmailStr]):
    root: EmailStr = Field(..., title="Email")


class EmbedOnlyType(
    RootModel[
        Literal["ability", "option", "row", "feature", "danger", "denizen", "variant"]
    ]
):
    root: Literal[
        "ability", "option", "row", "feature", "danger", "denizen", "variant"
    ] = Field(..., title="EmbedOnlyType")


class EmbeddedActionRollMove(BaseModel):
    field_id: EmbeddedMoveId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    text: MarkdownString
    trigger: TriggerActionRoll = Field(..., title="Trigger")
    allow_momentum_burn: bool
    outcomes: MoveOutcomes = Field(..., title="MoveOutcomes")
    type: Literal["move"] = "move"
    roll_type: Literal["action_roll"] = "action_roll"


class EmbeddedMoveId(RootModel[AssetAbilityMoveId]):
    root: AssetAbilityMoveId = Field(..., title="EmbeddedMoveId")


class EmbeddedMoveIdWildcard(RootModel[AssetAbilityMoveIdWildcard]):
    root: AssetAbilityMoveIdWildcard = Field(..., title="EmbeddedMoveIdWildcard")


class EmbeddedNoRollMove(BaseModel):
    field_id: EmbeddedMoveId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    text: MarkdownString
    trigger: TriggerNoRoll = Field(..., title="Trigger")
    allow_momentum_burn: Literal[False] = False
    outcomes: MoveOutcomes1 = Field(..., title="MoveOutcomes")
    type: Literal["move"] = "move"
    roll_type: Literal["no_roll"] = "no_roll"


class EmbeddedOracleColumnText(BaseModel):
    field_id: EmbeddedOracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText]
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["column_text"] = "column_text"


class EmbeddedOracleColumnText2(BaseModel):
    field_id: EmbeddedOracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText2]
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["column_text2"] = "column_text2"


class EmbeddedOracleColumnText3(BaseModel):
    field_id: EmbeddedOracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText3]
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["column_text3"] = "column_text3"


class EmbeddedOracleTableText(BaseModel):
    field_id: EmbeddedOracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText]
    column_labels: TextColumnLabels = Field(..., title="TextColumnLabels")
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["table_text"] = "table_text"


class EmbeddedOracleTableText2(BaseModel):
    field_id: EmbeddedOracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText2]
    column_labels: Text2ColumnLabels = Field(..., title="Text2ColumnLabels")
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["table_text2"] = "table_text2"


class EmbeddedOracleTableText3(BaseModel):
    field_id: EmbeddedOracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText3]
    column_labels: Text3ColumnLabels = Field(..., title="Text3ColumnLabels")
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["table_text3"] = "table_text3"


class EmbeddedOracleRollable(
    RootModel[
        Union[
            EmbeddedOracleTableText,
            EmbeddedOracleTableText2,
            EmbeddedOracleTableText3,
            EmbeddedOracleColumnText,
            EmbeddedOracleColumnText2,
            EmbeddedOracleColumnText3,
        ]
    ]
):
    root: Union[
        EmbeddedOracleTableText,
        EmbeddedOracleTableText2,
        EmbeddedOracleTableText3,
        EmbeddedOracleColumnText,
        EmbeddedOracleColumnText2,
        EmbeddedOracleColumnText3,
    ]


class AssetAbilityOracles(RootModel[Mapping[str, EmbeddedOracleRollable]]):
    root: Mapping[str, EmbeddedOracleRollable] = Field(..., title="AssetAbilityOracles")


class EmbeddedProgressRollMove(BaseModel):
    field_id: EmbeddedMoveId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    text: MarkdownString
    trigger: TriggerProgressRoll = Field(..., title="Trigger")
    allow_momentum_burn: Literal[False] = False
    outcomes: MoveOutcomes = Field(..., title="MoveOutcomes")
    type: Literal["move"] = "move"
    roll_type: Literal["progress_roll"] = "progress_roll"
    tracks: ProgressTrackTypeInfo


class EmbeddedSpecialTrackMove(BaseModel):
    field_id: EmbeddedMoveId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    text: MarkdownString
    trigger: TriggerSpecialTrack = Field(..., title="Trigger")
    allow_momentum_burn: Literal[False] = False
    outcomes: MoveOutcomes = Field(..., title="MoveOutcomes")
    type: Literal["move"] = "move"
    roll_type: Literal["special_track"] = "special_track"


class EmbeddedMove(
    RootModel[
        Union[
            EmbeddedActionRollMove,
            EmbeddedNoRollMove,
            EmbeddedProgressRollMove,
            EmbeddedSpecialTrackMove,
        ]
    ]
):
    root: Union[
        EmbeddedActionRollMove,
        EmbeddedNoRollMove,
        EmbeddedProgressRollMove,
        EmbeddedSpecialTrackMove,
    ]


class AssetAbilityMoves(RootModel[Mapping[str, EmbeddedMove]]):
    root: Mapping[str, EmbeddedMove] = Field(..., title="AssetAbilityMoves")


class Expansion(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    field_id: ExpansionId = Field(..., alias="_id")
    type: Literal["expansion"] = "expansion"
    datasworn_version: Literal["0.1.0"] = "0.1.0"
    title: Label
    authors: Sequence[AuthorInfo] = Field(..., min_length=1)
    date: date_aliased
    url: WebUrl
    license: Optional[WebUrl]
    oracles: Mapping[str, OracleTablesCollection]
    moves: Mapping[str, MoveCategory]
    assets: Mapping[str, AssetCollection]
    atlas: Optional[Mapping[str, AtlasCollection]] = {}
    npcs: Optional[Mapping[str, NpcCollection]] = {}
    truths: Optional[Mapping[str, Truth]] = {}
    rarities: Optional[Mapping[str, Rarity]] = {}
    delve_sites: Optional[Mapping[str, DelveSite]] = {}
    site_themes: Optional[Mapping[str, DelveSiteTheme]] = {}
    site_domains: Optional[Mapping[str, DelveSiteDomain]] = {}
    ruleset: RulesetId
    rules: Optional[RulesExpansion] = None


class ExpansionId(RootModel[str]):
    root: str = Field(..., title="ExpansionId")


class Feature(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic12 = Field(..., title="DiceRangeStatic")


class Feature1(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic13 = Field(..., title="DiceRangeStatic")


class Feature10(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic22 = Field(..., title="DiceRangeStatic")


class Feature11(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic11 = Field(..., title="DiceRangeStatic")


class Feature2(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic14 = Field(..., title="DiceRangeStatic")


class Feature3(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic15 = Field(..., title="DiceRangeStatic")


class Feature4(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic16 = Field(..., title="DiceRangeStatic")


class Feature5(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic17 = Field(..., title="DiceRangeStatic")


class Feature6(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic18 = Field(..., title="DiceRangeStatic")


class Feature7(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic19 = Field(..., title="DiceRangeStatic")


class Feature8(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic20 = Field(..., title="DiceRangeStatic")


class Feature9(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic21 = Field(..., title="DiceRangeStatic")


class Features(
    RootModel[
        tuple[
            Feature,
            Feature1,
            Feature2,
            Feature3,
            Feature4,
            Feature5,
            Feature6,
            Feature7,
            Feature8,
            Feature9,
            Feature10,
            Feature11,
        ]
    ]
):
    root: tuple[
        Feature,
        Feature1,
        Feature2,
        Feature3,
        Feature4,
        Feature5,
        Feature6,
        Feature7,
        Feature8,
        Feature9,
        Feature10,
        Feature11,
    ] = Field(..., max_length=12, min_length=12)


class Features1Item(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic29 = Field(..., title="DiceRangeStatic")


class Features1Item1(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic30 = Field(..., title="DiceRangeStatic")


class Features1Item2(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic31 = Field(..., title="DiceRangeStatic")


class Features1Item3(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic32 = Field(..., title="DiceRangeStatic")


class Features1Item4(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    roll: DiceRangeStatic33 = Field(..., title="DiceRangeStatic")


class Features1(
    RootModel[
        tuple[
            Features1Item,
            Features1Item1,
            Features1Item2,
            Features1Item3,
            Features1Item4,
        ]
    ]
):
    root: tuple[
        Features1Item, Features1Item1, Features1Item2, Features1Item3, Features1Item4
    ] = Field(..., max_length=5, min_length=5)


class I18nHint(BaseModel):
    part_of_speech: Optional[PartOfSpeech] = None


class I18nHints(BaseModel):
    text: Optional[I18nHint] = None
    text2: Optional[I18nHint] = None
    text3: Optional[I18nHint] = None
    template: Optional[Template] = None


class ImpactCategory(BaseModel):
    label: Label
    contents: Mapping[str, ImpactRule]


class ImpactRule(BaseModel):
    label: Label
    shared: bool
    prevents_recovery: Sequence[ConditionMeterKey]
    permanent: bool
    tags: Optional[Tags] = None


class Label(RootModel[str]):
    root: str = Field(..., title="Label")


class MarkdownString(RootModel[str]):
    root: str = Field(..., title="MarkdownString")


class MarkdownTemplateString(RootModel[str]):
    root: str = Field(..., title="MarkdownTemplateString")


class MoveActionRoll(BaseModel):
    field_id: MoveId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[MoveIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    text: MarkdownString
    oracles: Optional[MoveOracles] = Field(
        default_factory=lambda: MoveOracles({}), title="MoveOracles"
    )
    trigger: TriggerActionRoll = Field(..., title="Trigger")
    allow_momentum_burn: bool
    outcomes: MoveOutcomes = Field(..., title="MoveOutcomes")
    type: Literal["move"] = "move"
    roll_type: Literal["action_roll"] = "action_roll"


class MoveActionRollEnhancement(BaseModel):
    enhances: Optional[Sequence[AnyMoveIdWildcard]]
    roll_type: Literal["action_roll"] = "action_roll"
    trigger: Optional[TriggerActionRollEnhancement] = None


class MoveCategory(BaseModel):
    field_id: MoveCategoryId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[MoveCategoryIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    enhances: Optional[Sequence[MoveCategoryIdWildcard]] = None
    summary: Optional[MarkdownString] = None
    contents: Mapping[str, Move]
    collections: Mapping[str, MoveCategory]
    type: Literal["move_category"] = "move_category"


class MoveCategoryId(RootModel[str]):
    root: str = Field(..., title="MoveCategoryId")


class MoveCategoryIdWildcard(RootModel[str]):
    root: str = Field(..., title="MoveCategoryIdWildcard")


class MoveId(RootModel[str]):
    root: str = Field(..., title="MoveId")


class AnyMoveId(RootModel[Union[MoveId, AssetAbilityMoveId]]):
    root: Union[MoveId, AssetAbilityMoveId] = Field(..., title="AnyMoveId")


class MoveIdWildcard(RootModel[str]):
    root: str = Field(..., title="MoveIdWildcard")


class AnyMoveIdWildcard(RootModel[Union[MoveIdWildcard, AssetAbilityMoveIdWildcard]]):
    root: Union[MoveIdWildcard, AssetAbilityMoveIdWildcard] = Field(
        ..., title="AnyMoveIdWildcard"
    )


class MoveNoRoll(BaseModel):
    field_id: MoveId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[MoveIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    text: MarkdownString
    oracles: Optional[MoveOracles] = Field(
        default_factory=lambda: MoveOracles({}), title="MoveOracles"
    )
    trigger: TriggerNoRoll = Field(..., title="Trigger")
    allow_momentum_burn: Literal[False] = False
    outcomes: MoveOutcomes1 = Field(..., title="MoveOutcomes")
    type: Literal["move"] = "move"
    roll_type: Literal["no_roll"] = "no_roll"


class MoveNoRollEnhancement(BaseModel):
    enhances: Optional[Sequence[AnyMoveIdWildcard]]
    roll_type: Literal["no_roll"] = "no_roll"
    trigger: Optional[TriggerNoRollEnhancement] = None


class MoveOracleRollableId(RootModel[str]):
    root: str = Field(..., title="MoveOracleRollableId")


class MoveOracleRollableIdWildcard(RootModel[str]):
    root: str = Field(..., title="MoveOracleRollableIdWildcard")


class MoveOracleRollableRowId(RootModel[str]):
    root: str = Field(..., title="MoveOracleRollableRowId")


class MoveOracleRollableRowIdWildcard(RootModel[str]):
    root: str = Field(..., title="MoveOracleRollableRowIdWildcard")


class MoveOracles(RootModel[Mapping[str, EmbeddedOracleRollable]]):
    root: Mapping[str, EmbeddedOracleRollable] = Field(..., title="MoveOracles")


class MoveOutcome(BaseModel):
    text: MarkdownString
    oracle_rolls: Optional[Sequence[OracleRoll]] = None


class MoveOutcomes(BaseModel):
    strong_hit: MoveOutcome
    weak_hit: MoveOutcome
    miss: MoveOutcome


class MoveOutcomes1(RootModel[None]):
    root: None = Field(..., title="MoveOutcomes")


class MoveProgressRollEnhancement(BaseModel):
    enhances: Optional[Sequence[AnyMoveIdWildcard]]
    roll_type: Literal["progress_roll"] = "progress_roll"
    trigger: Optional[TriggerProgressRollEnhancement] = None


class MoveRollType(
    RootModel[Literal["no_roll", "action_roll", "progress_roll", "special_track"]]
):
    root: Literal["no_roll", "action_roll", "progress_roll", "special_track"] = Field(
        ..., title="MoveRollType"
    )


class MoveSpecialTrackEnhancement(BaseModel):
    enhances: Optional[Sequence[AnyMoveIdWildcard]]
    roll_type: Literal["special_track"] = "special_track"
    trigger: Optional[TriggerSpecialTrackEnhancement] = None


class MoveEnhancement(
    RootModel[
        Union[
            MoveActionRollEnhancement,
            MoveNoRollEnhancement,
            MoveProgressRollEnhancement,
            MoveSpecialTrackEnhancement,
        ]
    ]
):
    root: Union[
        MoveActionRollEnhancement,
        MoveNoRollEnhancement,
        MoveProgressRollEnhancement,
        MoveSpecialTrackEnhancement,
    ]


class Moves(BaseModel):
    suffer: Optional[Sequence[AnyMoveIdWildcard]] = None
    recover: Optional[Sequence[AnyMoveIdWildcard]] = None


class NonCollectableType(
    RootModel[
        Literal[
            "delve_site", "delve_site_domain", "delve_site_theme", "rarity", "truth"
        ]
    ]
):
    root: Literal[
        "delve_site", "delve_site_domain", "delve_site_theme", "rarity", "truth"
    ] = Field(..., title="NonCollectableType")


class NonNegativeInteger(RootModel[int]):
    root: int = Field(..., ge=0)


class NonNegativeIntegerDefault0(BaseModel):
    pass


class Npc(BaseModel):
    field_id: NpcId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[NpcIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    features: Sequence[MarkdownString]
    summary: Optional[MarkdownString] = None
    quest_starter: Optional[MarkdownString] = None
    your_truth: Optional[MarkdownString] = None
    rank: ChallengeRank
    nature: NpcNature
    drives: Sequence[MarkdownString]
    tactics: Sequence[MarkdownString]
    variants: Mapping[str, NpcVariant]
    type: Literal["npc"] = "npc"


class NpcCollection(BaseModel):
    field_id: NpcCollectionId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[NpcCollectionIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    enhances: Optional[Sequence[NpcCollectionIdWildcard]] = None
    summary: Optional[MarkdownString] = None
    contents: Mapping[str, Npc]
    collections: Mapping[str, NpcCollection]
    type: Literal["npc_collection"] = "npc_collection"


class NpcCollectionId(RootModel[str]):
    root: str = Field(..., title="NpcCollectionId")


class NpcCollectionIdWildcard(RootModel[str]):
    root: str = Field(..., title="NpcCollectionIdWildcard")


class NpcId(RootModel[str]):
    root: str = Field(..., title="NpcId")


class NpcIdWildcard(RootModel[str]):
    root: str = Field(..., title="NpcIdWildcard")


class NpcNature(RootModel[Label]):
    root: Label = Field(..., title="NpcNature")


class NpcVariant(BaseModel):
    field_id: NpcVariantId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    rank: ChallengeRank
    nature: NpcNature
    summary: Optional[MarkdownString] = None


class NpcVariantId(RootModel[str]):
    root: str = Field(..., title="NpcVariantId")


class NpcVariantIdWildcard(RootModel[str]):
    root: str = Field(..., title="NpcVariantIdWildcard")


class OracleCollectionId(RootModel[str]):
    root: str = Field(..., title="OracleCollectionId")


class OracleCollectionIdWildcard(RootModel[str]):
    root: str = Field(..., title="OracleCollectionIdWildcard")


class OracleColumnText(BaseModel):
    field_id: OracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleRollableIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText]
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["column_text"] = "column_text"


class OracleColumnText2(BaseModel):
    field_id: OracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleRollableIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText2]
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["column_text2"] = "column_text2"


class OracleColumnText3(BaseModel):
    field_id: OracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleRollableIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText3]
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["column_text3"] = "column_text3"


class OracleDuplicateBehavior(RootModel[Literal["reroll", "keep", "make_it_worse"]]):
    root: Literal["reroll", "keep", "make_it_worse"] = Field(
        ..., title="OracleDuplicateBehavior"
    )


class OracleMatchBehavior(BaseModel):
    text: MarkdownString


class OracleRoll(BaseModel):
    oracle: Optional[OracleRollableId]
    auto: bool
    duplicates: OracleDuplicateBehavior
    dice: Optional[DiceExpression]
    number_of_rolls: int


class OracleRollTemplate(BaseModel):
    text: Optional[MarkdownTemplateString] = None
    text2: Optional[MarkdownTemplateString] = None
    text3: Optional[MarkdownTemplateString] = None


class OracleRollableId(RootModel[str]):
    root: str = Field(..., title="OracleRollableId")


class OracleRollableIdWildcard(RootModel[str]):
    root: str = Field(..., title="OracleRollableIdWildcard")


class OracleRollableRowId(RootModel[str]):
    root: str = Field(..., title="OracleRollableRowId")


class OracleRollableRowIdWildcard(RootModel[str]):
    root: str = Field(..., title="OracleRollableRowIdWildcard")


class OracleRollableRowText(BaseModel):
    text: MarkdownString
    icon: Optional[SvgImageUrl] = None
    oracle_rolls: Optional[Sequence[OracleRoll]] = None
    suggestions: Optional[Suggestions] = None
    embed_table: Optional[str] = None
    template: Optional[OracleRollTemplate] = None
    field_i18n: Optional[I18nHints] = Field(None, alias="_i18n")
    roll: Optional[DiceRange]
    tags: Optional[Tags] = None
    field_id: AnyOracleRollableRowId = Field(..., alias="_id")


class OracleRollableRowText2(BaseModel):
    text: MarkdownString
    icon: Optional[SvgImageUrl] = None
    oracle_rolls: Optional[Sequence[OracleRoll]] = None
    suggestions: Optional[Suggestions] = None
    embed_table: Optional[str] = None
    template: Optional[OracleRollTemplate] = None
    field_i18n: Optional[I18nHints] = Field(None, alias="_i18n")
    roll: Optional[DiceRange]
    tags: Optional[Tags] = None
    field_id: AnyOracleRollableRowId = Field(..., alias="_id")
    text2: Optional[MarkdownString]


class OracleRollableRowText3(BaseModel):
    text: MarkdownString
    icon: Optional[SvgImageUrl] = None
    oracle_rolls: Optional[Sequence[OracleRoll]] = None
    suggestions: Optional[Suggestions] = None
    embed_table: Optional[str] = None
    template: Optional[OracleRollTemplate] = None
    field_i18n: Optional[I18nHints] = Field(None, alias="_i18n")
    roll: Optional[DiceRange]
    tags: Optional[Tags] = None
    field_id: AnyOracleRollableRowId = Field(..., alias="_id")
    text2: Optional[MarkdownString]
    text3: Optional[MarkdownString]


class OracleRollableRow(
    RootModel[
        Union[OracleRollableRowText, OracleRollableRowText2, OracleRollableRowText3]
    ]
):
    root: Union[
        OracleRollableRowText, OracleRollableRowText2, OracleRollableRowText3
    ] = Field(..., title="OracleRollableRow")


class OracleTableSharedRolls(BaseModel):
    field_id: OracleCollectionId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleCollectionIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    enhances: Optional[Sequence[OracleCollectionIdWildcard]] = None
    summary: Optional[MarkdownString] = None
    contents: Mapping[str, OracleColumnText]
    column_labels: SharedRollsLabels = Field(..., title="SharedRollsLabels")
    type: Literal["oracle_collection"] = "oracle_collection"
    oracle_type: Literal["table_shared_rolls"] = "table_shared_rolls"


class OracleTableSharedText(BaseModel):
    field_id: OracleCollectionId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleCollectionIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    enhances: Optional[Sequence[OracleCollectionIdWildcard]] = None
    summary: Optional[MarkdownString] = None
    contents: Mapping[str, OracleColumnText]
    column_labels: SharedTextLabels = Field(..., title="SharedTextLabels")
    type: Literal["oracle_collection"] = "oracle_collection"
    oracle_type: Literal["table_shared_text"] = "table_shared_text"


class OracleTableSharedText2(BaseModel):
    field_id: OracleCollectionId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleCollectionIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    enhances: Optional[Sequence[OracleCollectionIdWildcard]] = None
    summary: Optional[MarkdownString] = None
    contents: Mapping[str, OracleColumnText2]
    column_labels: SharedText2Labels = Field(..., title="SharedText2Labels")
    type: Literal["oracle_collection"] = "oracle_collection"
    oracle_type: Literal["table_shared_text2"] = "table_shared_text2"


class OracleTableSharedText3(BaseModel):
    field_id: OracleCollectionId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleCollectionIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    enhances: Optional[Sequence[OracleCollectionIdWildcard]] = None
    summary: Optional[MarkdownString] = None
    contents: Mapping[str, OracleColumnText3]
    column_labels: SharedText3Labels = Field(..., title="SharedText3Labels")
    type: Literal["oracle_collection"] = "oracle_collection"
    oracle_type: Literal["table_shared_text3"] = "table_shared_text3"


class OracleTableText(BaseModel):
    field_id: OracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleRollableIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText]
    column_labels: TextColumnLabels = Field(..., title="TextColumnLabels")
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["table_text"] = "table_text"


class OracleTableText2(BaseModel):
    field_id: OracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleRollableIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText2]
    column_labels: Text2ColumnLabels = Field(..., title="Text2ColumnLabels")
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["table_text2"] = "table_text2"


class OracleTableText3(BaseModel):
    field_id: OracleRollableId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleRollableIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    recommended_rolls: Optional[DiceRange] = None
    dice: DiceExpression
    match: Optional[OracleMatchBehavior] = None
    rows: Sequence[OracleRollableRowText3]
    column_labels: Text3ColumnLabels = Field(..., title="Text3ColumnLabels")
    type: Literal["oracle_rollable"] = "oracle_rollable"
    oracle_type: Literal["table_text3"] = "table_text3"


class OracleRollable(
    RootModel[
        Union[
            OracleTableText,
            OracleTableText2,
            OracleTableText3,
            OracleColumnText,
            OracleColumnText2,
            OracleColumnText3,
        ]
    ]
):
    root: Union[
        OracleTableText,
        OracleTableText2,
        OracleTableText3,
        OracleColumnText,
        OracleColumnText2,
        OracleColumnText3,
    ]


class AnyOracleRollable(RootModel[Union[OracleRollable, EmbeddedOracleRollable]]):
    root: Union[OracleRollable, EmbeddedOracleRollable] = Field(
        ..., title="AnyOracleRollable"
    )


class OracleRollableTable(
    RootModel[Union[OracleTableText, OracleTableText2, OracleTableText3]]
):
    root: Union[OracleTableText, OracleTableText2, OracleTableText3]


class OracleTablesCollection(BaseModel):
    field_id: OracleCollectionId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[OracleCollectionIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    enhances: Optional[Sequence[OracleCollectionIdWildcard]] = None
    summary: Optional[MarkdownString] = None
    contents: Mapping[str, OracleRollableTable]
    collections: Mapping[str, OracleCollection]
    type: Literal["oracle_collection"] = "oracle_collection"
    oracle_type: Literal["tables"] = "tables"


class OracleCollection(
    RootModel[
        Union[
            OracleTablesCollection,
            OracleTableSharedRolls,
            OracleTableSharedText,
            OracleTableSharedText2,
            OracleTableSharedText3,
        ]
    ]
):
    root: Union[
        OracleTablesCollection,
        OracleTableSharedRolls,
        OracleTableSharedText,
        OracleTableSharedText2,
        OracleTableSharedText3,
    ]


class PageNumber(RootModel[int]):
    root: int = Field(..., title="PageNumber")


class PartOfSpeech(
    RootModel[
        Literal[
            "common_noun",
            "proper_noun",
            "adjunct_common_noun",
            "adjunct_proper_noun",
            "verb",
            "gerund",
            "adjective",
            "attributive_verb",
            "adjective_as_proper_noun",
            "common_noun_as_proper_noun",
        ]
    ]
):
    root: Literal[
        "common_noun",
        "proper_noun",
        "adjunct_common_noun",
        "adjunct_proper_noun",
        "verb",
        "gerund",
        "adjective",
        "attributive_verb",
        "adjective_as_proper_noun",
        "common_noun_as_proper_noun",
    ] = Field(..., title="PartOfSpeech")


class ProgressMove(BaseModel):
    field_id: MoveId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[MoveIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    text: MarkdownString
    oracles: Optional[MoveOracles] = Field(
        default_factory=lambda: MoveOracles({}), title="MoveOracles"
    )
    trigger: TriggerProgressRoll = Field(..., title="Trigger")
    allow_momentum_burn: Literal[False] = False
    outcomes: MoveOutcomes = Field(..., title="MoveOutcomes")
    type: Literal["move"] = "move"
    roll_type: Literal["progress_roll"] = "progress_roll"
    tracks: ProgressTrackTypeInfo


class ProgressMoveSpecialTrackRoll(BaseModel):
    field_id: MoveId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[MoveIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    text: MarkdownString
    oracles: Optional[MoveOracles] = Field(
        default_factory=lambda: MoveOracles({}), title="MoveOracles"
    )
    trigger: TriggerSpecialTrack = Field(..., title="Trigger")
    allow_momentum_burn: Literal[False] = False
    outcomes: MoveOutcomes = Field(..., title="MoveOutcomes")
    type: Literal["move"] = "move"
    roll_type: Literal["special_track"] = "special_track"


class Move(
    RootModel[
        Union[MoveActionRoll, MoveNoRoll, ProgressMove, ProgressMoveSpecialTrackRoll]
    ]
):
    root: Union[MoveActionRoll, MoveNoRoll, ProgressMove, ProgressMoveSpecialTrackRoll]


class AnyMove(RootModel[Union[Move, EmbeddedMove]]):
    root: Union[Move, EmbeddedMove] = Field(..., title="AnyMove")


class ProgressRollMethod(
    RootModel[Literal["miss", "weak_hit", "strong_hit", "progress_roll"]]
):
    root: Literal["miss", "weak_hit", "strong_hit", "progress_roll"] = Field(
        ..., title="ProgressRollMethod"
    )


class ProgressRollOption(BaseModel):
    using: Literal["progress_track"] = "progress_track"


class ProgressTrackTypeInfo(BaseModel):
    category: Label
    controls: Optional[Mapping[str, Mapping[str, Any]]] = {}


class Rarity(BaseModel):
    field_id: RarityId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[RarityIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    asset: AssetId
    xp_cost: int = Field(..., le=5)
    type: Literal["rarity"] = "rarity"


class RarityId(RootModel[str]):
    root: str = Field(..., title="RarityId")


class RarityIdWildcard(RootModel[str]):
    root: str = Field(..., title="RarityIdWildcard")


class RuleType(
    RootModel[Literal["impact", "condition_meter", "special_track", "stat"]]
):
    root: Literal["impact", "condition_meter", "special_track", "stat"] = Field(
        ..., title="RuleType"
    )


class Rules(BaseModel):
    stats: Mapping[str, StatRule]
    condition_meters: Mapping[str, ConditionMeterRule]
    impacts: Mapping[str, ImpactCategory]
    special_tracks: Mapping[str, SpecialTrackRule]
    tags: Mapping[str, TagRule]


class RulesExpansion(BaseModel):
    stats: Optional[Mapping[str, StatRule]] = {}
    condition_meters: Optional[Mapping[str, ConditionMeterRule]] = {}
    impacts: Optional[Mapping[str, ImpactCategory]] = {}
    special_tracks: Optional[Mapping[str, SpecialTrackRule]] = {}
    tags: Optional[Mapping[str, TagRule]] = {}


class Ruleset(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    field_id: RulesetId = Field(..., alias="_id")
    type: Literal["ruleset"] = "ruleset"
    datasworn_version: Literal["0.1.0"] = "0.1.0"
    title: Label
    authors: Sequence[AuthorInfo] = Field(..., min_length=1)
    date: date_aliased
    url: WebUrl
    license: Optional[WebUrl]
    oracles: Mapping[str, OracleTablesCollection]
    moves: Mapping[str, MoveCategory]
    assets: Mapping[str, AssetCollection]
    atlas: Optional[Mapping[str, AtlasCollection]] = {}
    npcs: Optional[Mapping[str, NpcCollection]] = {}
    truths: Optional[Mapping[str, Truth]] = {}
    rarities: Optional[Mapping[str, Rarity]] = {}
    delve_sites: Optional[Mapping[str, DelveSite]] = {}
    site_themes: Optional[Mapping[str, DelveSiteTheme]] = {}
    site_domains: Optional[Mapping[str, DelveSiteDomain]] = {}
    rules: Rules


class RulesPackage(RootModel[Union[Ruleset, Expansion]]):
    root: Union[Ruleset, Expansion]


class DataswornV010(RootModel[RulesPackage]):
    root: RulesPackage = Field(..., title="Datasworn v0.1.0")


class RulesetId(RootModel[str]):
    root: str = Field(..., title="RulesetId")


class RulesPackageId(RootModel[Union[RulesetId, ExpansionId]]):
    root: Union[RulesetId, ExpansionId] = Field(..., title="RulesPackageId")


class Schema(RootModel[Union[CoreSchemaMetaSchema, bool]]):
    root: Union[CoreSchemaMetaSchema, bool] = Field(
        ..., title="Core schema meta-schema"
    )


class SchemaArray(RootModel[Sequence[Schema]]):
    root: Sequence[Schema] = Field(..., min_length=1)


class SelectEnhancementField(BaseModel):
    label: Label
    value: Optional[DictKey]
    choices: Mapping[
        str, Union[SelectEnhancementFieldChoice, SelectEnhancementFieldChoiceGroup]
    ]
    field_type: Literal["select_enhancement"] = "select_enhancement"
    icon: Optional[SvgImageUrl] = None


class AssetControlField(
    RootModel[
        Union[
            AssetConditionMeter,
            SelectEnhancementField,
            AssetCheckboxField,
            AssetCardFlipField,
        ]
    ]
):
    root: Union[
        AssetConditionMeter,
        SelectEnhancementField,
        AssetCheckboxField,
        AssetCardFlipField,
    ]


class SelectEnhancementFieldChoice(BaseModel):
    label: Label
    choice_type: Literal["choice"] = "choice"
    enhance_asset: Optional[AssetEnhancement] = None
    enhance_moves: Optional[Sequence[MoveEnhancement]] = None


class SelectEnhancementFieldChoiceGroup(BaseModel):
    name: Label
    choice_type: Literal["choice_group"] = "choice_group"
    choices: Mapping[str, SelectEnhancementFieldChoice]


class SelectValueField(BaseModel):
    label: Label
    value: Optional[DictKey]
    choices: Mapping[str, SelectValueFieldChoice]
    field_type: Literal["select_value"] = "select_value"
    icon: Optional[SvgImageUrl] = None


class SelectValueFieldChoice1(BaseModel):
    """
    Represents an option in a list of choices.
    """

    label: Label
    choice_type: Literal["choice"] = "choice"
    stat: StatKey
    using: Literal["stat"] = "stat"
    """
    A reference to the value of a standard player character stat.
    """


class SelectValueFieldChoice2(BaseModel):
    """
    Represents an option in a list of choices.
    """

    label: Label
    choice_type: Literal["choice"] = "choice"
    condition_meter: ConditionMeterKey
    using: Literal["condition_meter"] = "condition_meter"
    """
    A reference to the value of a standard player condition meter.
    """


class SelectValueFieldChoice3(BaseModel):
    """
    Represents an option in a list of choices.
    """

    label: Label
    choice_type: Literal["choice"] = "choice"
    assets: Optional[Sequence[AssetIdWildcard]]
    """
    Asset IDs (which may be wildcarded) that may provide the control field. For asset ability enhancements, `null` is used to represent the asset's own control fields.
    """
    control: DictKey = Field(..., examples=["health", "integrity"])
    """
    The dictionary key of the asset control field.
    """
    using: Literal["asset_control"] = "asset_control"
    """
    A reference to the value of an asset control.
    """


class SelectValueFieldChoice4(BaseModel):
    """
    Represents an option in a list of choices.
    """

    label: Label
    choice_type: Literal["choice"] = "choice"
    assets: Optional[Sequence[AssetIdWildcard]]
    """
    Asset IDs (which may be wildcarded) that may provide the option field. For asset ability enhancements, `null` is used to represent the asset's own option fields.
    """
    option: DictKey
    """
    The dictionary key of the asset option field.
    """
    using: Literal["asset_option"] = "asset_option"
    """
    A reference to the value of an asset option.
    """


class SelectValueFieldChoice5(BaseModel):
    """
    Represents an option in a list of choices.
    """

    label: Label
    choice_type: Literal["choice"] = "choice"
    control: DictKey = Field(..., examples=["health", "integrity"])
    """
    The dictionary key of the asset control field.
    """
    using: Literal["attached_asset_control"] = "attached_asset_control"
    """
    A reference to the value of an attached asset control. For example, a Module asset could use this to roll using the `integrity` control of an attached Vehicle.
    """


class SelectValueFieldChoice6(BaseModel):
    """
    Represents an option in a list of choices.
    """

    label: Label
    choice_type: Literal["choice"] = "choice"
    option: DictKey
    """
    The dictionary key of the asset option field.
    """
    using: Literal["attached_asset_option"] = "attached_asset_option"
    """
    A reference to the value of an attached asset option.
    """


class SelectValueFieldChoice7(BaseModel):
    """
    Represents an option in a list of choices.
    """

    label: Label
    choice_type: Literal["choice"] = "choice"
    value: int
    using: Literal["custom"] = "custom"
    """
    An arbitrary static integer value with a label.
    """


class SelectValueFieldChoice(
    RootModel[
        Union[
            SelectValueFieldChoice1,
            SelectValueFieldChoice2,
            SelectValueFieldChoice3,
            SelectValueFieldChoice4,
            SelectValueFieldChoice5,
            SelectValueFieldChoice6,
            SelectValueFieldChoice7,
        ]
    ]
):
    root: Union[
        SelectValueFieldChoice1,
        SelectValueFieldChoice2,
        SelectValueFieldChoice3,
        SelectValueFieldChoice4,
        SelectValueFieldChoice5,
        SelectValueFieldChoice6,
        SelectValueFieldChoice7,
    ]


class SemanticVersion(RootModel[str]):
    root: str = Field(..., title="SemanticVersion")


class SharedRollsLabels(BaseModel):
    roll: Label


class SharedText2Labels(BaseModel):
    text: Label
    text2: Label


class SharedText3Labels(BaseModel):
    text: Label
    text2: Label
    text3: Label


class SharedTextLabels(BaseModel):
    text: Label


class SimpleTypes(
    RootModel[
        Literal["array", "boolean", "integer", "null", "number", "object", "string"]
    ]
):
    root: Literal["array", "boolean", "integer", "null", "number", "object", "string"]


class SourceInfo(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    title: Label
    page: Optional[PageNumber] = None
    authors: Sequence[AuthorInfo] = Field(..., min_length=1)
    date: date_aliased
    url: WebUrl
    license: Optional[WebUrl]


class SpecialTrackRollMethod(
    RootModel[
        Literal[
            "miss",
            "weak_hit",
            "strong_hit",
            "player_choice",
            "highest",
            "lowest",
            "all",
        ]
    ]
):
    root: Literal[
        "miss", "weak_hit", "strong_hit", "player_choice", "highest", "lowest", "all"
    ] = Field(..., title="SpecialTrackRollMethod")


class SpecialTrackRule(BaseModel):
    label: Label
    shared: bool
    optional: bool
    tags: Optional[Tags] = None


class SpecialTrackType(RootModel[DictKey]):
    root: DictKey = Field(..., title="SpecialTrackType")


class StatKey(RootModel[DictKey]):
    root: DictKey = Field(..., title="StatKey")


class StatRule(BaseModel):
    label: Label
    tags: Optional[Tags] = None


class StatValueRef(BaseModel):
    stat: StatKey
    using: Literal["stat"] = "stat"


class RollableValue(
    RootModel[
        Union[
            StatValueRef,
            ConditionMeterValueRef,
            AssetControlValueRef,
            AssetOptionValueRef,
            AttachedAssetControlValueRef,
            AttachedAssetOptionValueRef,
            CustomValue,
        ]
    ]
):
    root: Union[
        StatValueRef,
        ConditionMeterValueRef,
        AssetControlValueRef,
        AssetOptionValueRef,
        AttachedAssetControlValueRef,
        AttachedAssetOptionValueRef,
        CustomValue,
    ]


class StringArray(RootModel[frozenset[str]]):
    root: frozenset[str]


class SvgImageUrl(RootModel[str]):
    root: str = Field(..., title="SvgImageUrl")


class TagRule(BaseModel):
    node_types: Optional[Sequence[TaggableNodeType]]


class TagSchema1(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    field_ref: Literal[
        "#/definitions/ActionRollMethod",
        "#/definitions/AnyId",
        "#/definitions/AnyIdWildcard",
        "#/definitions/AnyMoveId",
        "#/definitions/AnyMoveIdWildcard",
        "#/definitions/AnyOracleRollableId",
        "#/definitions/AnyOracleRollableIdWildcard",
        "#/definitions/AnyOracleRollableRowId",
        "#/definitions/AnyOracleRollableRowIdWildcard",
        "#/definitions/AssetAbilityId",
        "#/definitions/AssetAbilityIdWildcard",
        "#/definitions/AssetAbilityMoveId",
        "#/definitions/AssetAbilityMoveIdWildcard",
        "#/definitions/AssetAbilityOracleRollableId",
        "#/definitions/AssetAbilityOracleRollableIdWildcard",
        "#/definitions/AssetAbilityOracleRollableRowId",
        "#/definitions/AssetAbilityOracleRollableRowIdWildcard",
        "#/definitions/AssetCollectionId",
        "#/definitions/AssetCollectionIdWildcard",
        "#/definitions/AssetId",
        "#/definitions/AssetIdWildcard",
        "#/definitions/AtlasCollectionId",
        "#/definitions/AtlasCollectionIdWildcard",
        "#/definitions/AtlasEntryId",
        "#/definitions/AtlasEntryIdWildcard",
        "#/definitions/ChallengeRank",
        "#/definitions/CollectableType",
        "#/definitions/CollectionType",
        "#/definitions/CssColor",
        "#/definitions/DelveSiteDenizenFrequency",
        "#/definitions/DelveSiteDenizenId",
        "#/definitions/DelveSiteDenizenIdWildcard",
        "#/definitions/DelveSiteDomainDangerId",
        "#/definitions/DelveSiteDomainDangerIdWildcard",
        "#/definitions/DelveSiteDomainFeatureId",
        "#/definitions/DelveSiteDomainFeatureIdWildcard",
        "#/definitions/DelveSiteDomainId",
        "#/definitions/DelveSiteDomainIdWildcard",
        "#/definitions/DelveSiteId",
        "#/definitions/DelveSiteIdWildcard",
        "#/definitions/DelveSiteThemeDangerId",
        "#/definitions/DelveSiteThemeDangerIdWildcard",
        "#/definitions/DelveSiteThemeFeatureId",
        "#/definitions/DelveSiteThemeFeatureIdWildcard",
        "#/definitions/DelveSiteThemeId",
        "#/definitions/DelveSiteThemeIdWildcard",
        "#/definitions/DiceExpression",
        "#/definitions/DictKey",
        "#/definitions/Documentation",
        "#/definitions/Email",
        "#/definitions/EmbeddedMoveId",
        "#/definitions/EmbeddedMoveIdWildcard",
        "#/definitions/EmbeddedOracleRollableId",
        "#/definitions/EmbeddedOracleRollableIdWildcard",
        "#/definitions/EmbedOnlyType",
        "#/definitions/ExpansionId",
        "#/definitions/Label",
        "#/definitions/MarkdownString",
        "#/definitions/MarkdownTemplateString",
        "#/definitions/MoveCategoryId",
        "#/definitions/MoveCategoryIdWildcard",
        "#/definitions/MoveId",
        "#/definitions/MoveIdWildcard",
        "#/definitions/MoveOracleRollableId",
        "#/definitions/MoveOracleRollableIdWildcard",
        "#/definitions/MoveOracleRollableRowId",
        "#/definitions/MoveOracleRollableRowIdWildcard",
        "#/definitions/MoveRollType",
        "#/definitions/NonCollectableType",
        "#/definitions/NpcCollectionId",
        "#/definitions/NpcCollectionIdWildcard",
        "#/definitions/NpcId",
        "#/definitions/NpcIdWildcard",
        "#/definitions/NpcVariantId",
        "#/definitions/NpcVariantIdWildcard",
        "#/definitions/OracleCollectionId",
        "#/definitions/OracleCollectionIdWildcard",
        "#/definitions/OracleDuplicateBehavior",
        "#/definitions/OracleRollableId",
        "#/definitions/OracleRollableIdWildcard",
        "#/definitions/OracleRollableRowId",
        "#/definitions/OracleRollableRowIdWildcard",
        "#/definitions/PageNumber",
        "#/definitions/PartOfSpeech",
        "#/definitions/ProgressRollMethod",
        "#/definitions/RarityId",
        "#/definitions/RarityIdWildcard",
        "#/definitions/RulesetId",
        "#/definitions/RulesPackageId",
        "#/definitions/RuleType",
        "#/definitions/SemanticVersion",
        "#/definitions/SpecialTrackRollMethod",
        "#/definitions/SvgImageUrl",
        "#/definitions/TruthId",
        "#/definitions/TruthIdWildcard",
        "#/definitions/TruthOptionId",
        "#/definitions/TruthOptionIdWildcard",
        "#/definitions/TruthOptionOracleRollableId",
        "#/definitions/TruthOptionOracleRollableIdWildcard",
        "#/definitions/TruthOptionOracleRollableRowId",
        "#/definitions/TruthOptionOracleRollableRowIdWildcard",
        "#/definitions/WebpImageUrl",
        "#/definitions/WebUrl",
    ] = Field(..., alias="_ref")


class TagSchemaArray(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    type: Literal["array"] = "array"
    items: TagSchema


class TagSchemaBoolean(BaseModel):
    """
    Schema for a true or false value.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    type: Literal["boolean"] = "boolean"


class TagSchemaFloat(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    type: Literal["number"] = "number"


class TagSchemaInteger(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    type: Literal["integer"] = "integer"


class TagSchemaIntegerEnum(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    enum: Sequence[int]


class TagSchemaObject(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    type: Literal["object"] = "object"
    properties: Mapping[str, TagSchema]


class TagSchemaStringEnum(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    enum: Sequence[DictKey]


class TagSchema(
    RootModel[
        Union[
            Union[
                TagSchema1,
                TagSchemaStringEnum,
                TagSchemaIntegerEnum,
                TagSchemaBoolean,
                TagSchemaInteger,
                TagSchemaFloat,
                TagSchemaObject,
                TagSchemaArray,
            ],
            Schema,
        ]
    ]
):
    root: Union[
        Union[
            TagSchema1,
            TagSchemaStringEnum,
            TagSchemaIntegerEnum,
            TagSchemaBoolean,
            TagSchemaInteger,
            TagSchemaFloat,
            TagSchemaObject,
            TagSchemaArray,
        ],
        Schema,
    ]


class TaggableNodeType(
    RootModel[
        Union[
            CollectableType, NonCollectableType, CollectionType, EmbedOnlyType, RuleType
        ]
    ]
):
    root: Union[
        CollectableType, NonCollectableType, CollectionType, EmbedOnlyType, RuleType
    ] = Field(..., title="TaggableNodeType")


class Tags(BaseModel):
    field_core: Optional[CoreTags] = Field(None, alias="_core")


class Template(BaseModel):
    text: Optional[I18nHint] = None
    text2: Optional[I18nHint] = None
    text3: Optional[I18nHint] = None


class Text2ColumnLabels(BaseModel):
    roll: Label
    text: Label
    text2: Label


class Text3ColumnLabels(BaseModel):
    roll: Label
    text: Label
    text2: Label
    text3: Label


class TextColumnLabels(BaseModel):
    roll: Label
    text: Label


class TextField(BaseModel):
    label: Label
    value: Optional[str]
    field_type: Literal["text"] = "text"
    icon: Optional[SvgImageUrl] = None


class AssetAbilityControlField(
    RootModel[Union[ClockField, CounterField, AssetCheckboxField, TextField]]
):
    root: Union[ClockField, CounterField, AssetCheckboxField, TextField]


class AssetAbilityOptionField(RootModel[TextField]):
    root: TextField


class AssetOptionField(
    RootModel[Union[SelectValueField, SelectEnhancementField, TextField]]
):
    root: Union[SelectValueField, SelectEnhancementField, TextField]


class TriggerActionRoll(BaseModel):
    text: str
    conditions: Sequence[TriggerActionRollCondition]


class TriggerActionRollCondition(BaseModel):
    text: Optional[MarkdownString] = None
    by: Optional[TriggerBy] = None
    method: ActionRollMethod
    roll_options: Sequence[RollableValue]


class TriggerActionRollConditionEnhancement(BaseModel):
    text: Optional[MarkdownString] = None
    by: Optional[TriggerBy] = None
    method: Optional[ActionRollMethod]
    roll_options: Optional[Sequence[RollableValue]]


class TriggerActionRollEnhancement(BaseModel):
    conditions: Sequence[TriggerActionRollConditionEnhancement]


class TriggerBy(BaseModel):
    player: bool
    ally: bool


class TriggerNoRoll(BaseModel):
    text: str
    conditions: Sequence[TriggerNoRollCondition]


class TriggerNoRollCondition(BaseModel):
    text: Optional[MarkdownString] = None
    by: Optional[TriggerBy] = None
    method: None
    roll_options: None


class TriggerNoRollEnhancement(BaseModel):
    conditions: Sequence[TriggerNoRollCondition]


class TriggerProgressRoll(BaseModel):
    text: str
    conditions: Sequence[TriggerProgressRollCondition]


class TriggerProgressRollCondition(BaseModel):
    text: Optional[MarkdownString] = None
    by: Optional[TriggerBy] = None
    method: ProgressRollMethod
    roll_options: Sequence[ProgressRollOption]


class TriggerProgressRollConditionEnhancement(BaseModel):
    text: Optional[MarkdownString] = None
    by: Optional[TriggerBy] = None
    method: Optional[ProgressRollMethod]
    roll_options: Optional[Sequence[ProgressRollOption]]


class TriggerProgressRollEnhancement(BaseModel):
    conditions: Sequence[TriggerProgressRollConditionEnhancement]


class TriggerSpecialTrack(BaseModel):
    text: str
    conditions: Sequence[TriggerSpecialTrackCondition]


class TriggerSpecialTrackCondition(BaseModel):
    text: Optional[MarkdownString] = None
    by: Optional[TriggerBy] = None
    method: SpecialTrackRollMethod
    roll_options: Sequence[TriggerSpecialTrackConditionOption]


class TriggerSpecialTrackConditionEnhancement(BaseModel):
    text: Optional[MarkdownString] = None
    by: Optional[TriggerBy] = None
    method: Optional[SpecialTrackRollMethod]
    roll_options: Optional[Sequence[TriggerSpecialTrackConditionOption]]


class TriggerSpecialTrackConditionOption(BaseModel):
    using: SpecialTrackType


class TriggerSpecialTrackEnhancement(BaseModel):
    conditions: Sequence[TriggerSpecialTrackConditionEnhancement]


class Truth(BaseModel):
    field_id: TruthId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    name: Label
    canonical_name: Optional[Label] = None
    field_source: SourceInfo = Field(..., alias="_source")
    suggestions: Optional[Suggestions] = None
    tags: Optional[Tags] = None
    replaces: Optional[Sequence[TruthIdWildcard]] = None
    color: Optional[CssColor] = None
    images: Optional[Sequence[WebpImageUrl]] = None
    icon: Optional[SvgImageUrl] = None
    dice: DiceExpression
    options: Sequence[TruthOption]
    your_character: Optional[MarkdownString] = None
    factions: Optional[Sequence[OracleMatchBehavior]] = None
    type: Literal["truth"] = "truth"


class TruthId(RootModel[str]):
    root: str = Field(..., title="TruthId")


class TruthIdWildcard(RootModel[str]):
    root: str = Field(..., title="TruthIdWildcard")


class Tag(
    RootModel[
        Union[
            bool,
            int,
            DictKey,
            DiceExpression,
            AtlasEntryId,
            NpcId,
            OracleRollableId,
            AssetId,
            MoveId,
            AtlasCollectionId,
            NpcCollectionId,
            OracleCollectionId,
            AssetCollectionId,
            MoveCategoryId,
            DelveSiteId,
            DelveSiteDomainId,
            DelveSiteThemeId,
            RarityId,
            TruthId,
            Sequence[
                Union[
                    AtlasEntryIdWildcard,
                    NpcIdWildcard,
                    OracleRollableIdWildcard,
                    AssetIdWildcard,
                    MoveIdWildcard,
                    AtlasCollectionIdWildcard,
                    NpcCollectionIdWildcard,
                    OracleCollectionIdWildcard,
                    AssetCollectionIdWildcard,
                    MoveCategoryIdWildcard,
                    DelveSiteIdWildcard,
                    DelveSiteDomainIdWildcard,
                    DelveSiteThemeIdWildcard,
                    RarityIdWildcard,
                    TruthIdWildcard,
                ]
            ],
        ]
    ]
):
    root: Union[
        bool,
        int,
        DictKey,
        DiceExpression,
        AtlasEntryId,
        NpcId,
        OracleRollableId,
        AssetId,
        MoveId,
        AtlasCollectionId,
        NpcCollectionId,
        OracleCollectionId,
        AssetCollectionId,
        MoveCategoryId,
        DelveSiteId,
        DelveSiteDomainId,
        DelveSiteThemeId,
        RarityId,
        TruthId,
        Sequence[
            Union[
                AtlasEntryIdWildcard,
                NpcIdWildcard,
                OracleRollableIdWildcard,
                AssetIdWildcard,
                MoveIdWildcard,
                AtlasCollectionIdWildcard,
                NpcCollectionIdWildcard,
                OracleCollectionIdWildcard,
                AssetCollectionIdWildcard,
                MoveCategoryIdWildcard,
                DelveSiteIdWildcard,
                DelveSiteDomainIdWildcard,
                DelveSiteThemeIdWildcard,
                RarityIdWildcard,
                TruthIdWildcard,
            ]
        ],
    ] = Field(..., title="Tag")


class TruthOption(BaseModel):
    field_id: TruthOptionId = Field(..., alias="_id")
    field_comment: Optional[Documentation] = Field(None, alias="_comment")
    roll: DiceRange
    summary: Optional[MarkdownString] = None
    quest_starter: MarkdownString
    oracles: Optional[TruthOptionOracles] = Field(
        default_factory=lambda: TruthOptionOracles({}), title="TruthOptionOracles"
    )


class TruthOptionId(RootModel[str]):
    root: str = Field(..., title="TruthOptionId")


class TruthOptionIdWildcard(RootModel[str]):
    root: str = Field(..., title="TruthOptionIdWildcard")


class TruthOptionOracleRollableId(RootModel[str]):
    root: str = Field(..., title="TruthOptionOracleRollableId")


class AnyOracleRollableId(
    RootModel[
        Union[
            OracleRollableId,
            AssetAbilityOracleRollableId,
            TruthOptionOracleRollableId,
            MoveOracleRollableId,
        ]
    ]
):
    root: Union[
        OracleRollableId,
        AssetAbilityOracleRollableId,
        TruthOptionOracleRollableId,
        MoveOracleRollableId,
    ] = Field(..., title="AnyOracleRollableId")


class EmbeddedOracleRollableId(
    RootModel[
        Union[
            AssetAbilityOracleRollableId,
            TruthOptionOracleRollableId,
            MoveOracleRollableId,
        ]
    ]
):
    root: Union[
        AssetAbilityOracleRollableId, TruthOptionOracleRollableId, MoveOracleRollableId
    ] = Field(..., title="EmbeddedOracleRollableId")


class TruthOptionOracleRollableIdWildcard(RootModel[str]):
    root: str = Field(..., title="TruthOptionOracleRollableIdWildcard")


class AnyOracleRollableIdWildcard(
    RootModel[
        Union[
            OracleRollableIdWildcard,
            AssetAbilityOracleRollableIdWildcard,
            TruthOptionOracleRollableIdWildcard,
            MoveOracleRollableIdWildcard,
        ]
    ]
):
    root: Union[
        OracleRollableIdWildcard,
        AssetAbilityOracleRollableIdWildcard,
        TruthOptionOracleRollableIdWildcard,
        MoveOracleRollableIdWildcard,
    ] = Field(..., title="AnyOracleRollableIdWildcard")


class EmbeddedOracleRollableIdWildcard(
    RootModel[
        Union[
            AssetAbilityOracleRollableIdWildcard,
            TruthOptionOracleRollableIdWildcard,
            MoveOracleRollableIdWildcard,
        ]
    ]
):
    root: Union[
        AssetAbilityOracleRollableIdWildcard,
        TruthOptionOracleRollableIdWildcard,
        MoveOracleRollableIdWildcard,
    ] = Field(..., title="EmbeddedOracleRollableIdWildcard")


class TruthOptionOracleRollableRowId(RootModel[str]):
    root: str = Field(..., title="TruthOptionOracleRollableRowId")


class AnyId(
    RootModel[
        Union[
            AtlasEntryId,
            NpcId,
            NpcVariantId,
            OracleRollableId,
            AssetAbilityOracleRollableId,
            MoveOracleRollableId,
            TruthOptionOracleRollableId,
            OracleRollableRowId,
            AssetAbilityOracleRollableRowId,
            MoveOracleRollableRowId,
            TruthOptionOracleRollableRowId,
            AssetId,
            AssetAbilityId,
            AssetAbilityMoveId,
            MoveId,
            AtlasCollectionId,
            NpcCollectionId,
            OracleCollectionId,
            AssetCollectionId,
            MoveCategoryId,
            DelveSiteId,
            DelveSiteDenizenId,
            DelveSiteDomainId,
            DelveSiteDomainFeatureId,
            DelveSiteThemeFeatureId,
            DelveSiteDomainDangerId,
            DelveSiteThemeDangerId,
            DelveSiteThemeId,
            RarityId,
            TruthId,
            TruthOptionId,
        ]
    ]
):
    root: Union[
        AtlasEntryId,
        NpcId,
        NpcVariantId,
        OracleRollableId,
        AssetAbilityOracleRollableId,
        MoveOracleRollableId,
        TruthOptionOracleRollableId,
        OracleRollableRowId,
        AssetAbilityOracleRollableRowId,
        MoveOracleRollableRowId,
        TruthOptionOracleRollableRowId,
        AssetId,
        AssetAbilityId,
        AssetAbilityMoveId,
        MoveId,
        AtlasCollectionId,
        NpcCollectionId,
        OracleCollectionId,
        AssetCollectionId,
        MoveCategoryId,
        DelveSiteId,
        DelveSiteDenizenId,
        DelveSiteDomainId,
        DelveSiteDomainFeatureId,
        DelveSiteThemeFeatureId,
        DelveSiteDomainDangerId,
        DelveSiteThemeDangerId,
        DelveSiteThemeId,
        RarityId,
        TruthId,
        TruthOptionId,
    ] = Field(..., title="AnyId")


class AnyOracleRollableRowId(
    RootModel[
        Union[
            OracleRollableRowId,
            AssetAbilityOracleRollableRowId,
            MoveOracleRollableRowId,
            TruthOptionOracleRollableRowId,
        ]
    ]
):
    root: Union[
        OracleRollableRowId,
        AssetAbilityOracleRollableRowId,
        MoveOracleRollableRowId,
        TruthOptionOracleRollableRowId,
    ] = Field(..., title="AnyOracleRollableRowId")


class TruthOptionOracleRollableRowIdWildcard(RootModel[str]):
    root: str = Field(..., title="TruthOptionOracleRollableRowIdWildcard")


class AnyIdWildcard(
    RootModel[
        Union[
            AtlasEntryIdWildcard,
            NpcIdWildcard,
            NpcVariantIdWildcard,
            OracleRollableIdWildcard,
            AssetAbilityOracleRollableIdWildcard,
            MoveOracleRollableIdWildcard,
            TruthOptionOracleRollableIdWildcard,
            OracleRollableRowIdWildcard,
            AssetAbilityOracleRollableRowIdWildcard,
            MoveOracleRollableRowIdWildcard,
            TruthOptionOracleRollableRowIdWildcard,
            AssetIdWildcard,
            AssetAbilityIdWildcard,
            AssetAbilityMoveIdWildcard,
            MoveIdWildcard,
            AtlasCollectionIdWildcard,
            NpcCollectionIdWildcard,
            OracleCollectionIdWildcard,
            AssetCollectionIdWildcard,
            MoveCategoryIdWildcard,
            DelveSiteIdWildcard,
            DelveSiteDenizenIdWildcard,
            DelveSiteDomainIdWildcard,
            DelveSiteDomainFeatureIdWildcard,
            DelveSiteThemeFeatureIdWildcard,
            DelveSiteDomainDangerIdWildcard,
            DelveSiteThemeDangerIdWildcard,
            DelveSiteThemeIdWildcard,
            RarityIdWildcard,
            TruthIdWildcard,
            TruthOptionIdWildcard,
        ]
    ]
):
    root: Union[
        AtlasEntryIdWildcard,
        NpcIdWildcard,
        NpcVariantIdWildcard,
        OracleRollableIdWildcard,
        AssetAbilityOracleRollableIdWildcard,
        MoveOracleRollableIdWildcard,
        TruthOptionOracleRollableIdWildcard,
        OracleRollableRowIdWildcard,
        AssetAbilityOracleRollableRowIdWildcard,
        MoveOracleRollableRowIdWildcard,
        TruthOptionOracleRollableRowIdWildcard,
        AssetIdWildcard,
        AssetAbilityIdWildcard,
        AssetAbilityMoveIdWildcard,
        MoveIdWildcard,
        AtlasCollectionIdWildcard,
        NpcCollectionIdWildcard,
        OracleCollectionIdWildcard,
        AssetCollectionIdWildcard,
        MoveCategoryIdWildcard,
        DelveSiteIdWildcard,
        DelveSiteDenizenIdWildcard,
        DelveSiteDomainIdWildcard,
        DelveSiteDomainFeatureIdWildcard,
        DelveSiteThemeFeatureIdWildcard,
        DelveSiteDomainDangerIdWildcard,
        DelveSiteThemeDangerIdWildcard,
        DelveSiteThemeIdWildcard,
        RarityIdWildcard,
        TruthIdWildcard,
        TruthOptionIdWildcard,
    ] = Field(..., title="AnyIdWildcard")


class AnyOracleRollableRowIdWildcard(
    RootModel[
        Union[
            OracleRollableRowIdWildcard,
            AssetAbilityOracleRollableRowIdWildcard,
            MoveOracleRollableRowIdWildcard,
            TruthOptionOracleRollableRowIdWildcard,
        ]
    ]
):
    root: Union[
        OracleRollableRowIdWildcard,
        AssetAbilityOracleRollableRowIdWildcard,
        MoveOracleRollableRowIdWildcard,
        TruthOptionOracleRollableRowIdWildcard,
    ] = Field(..., title="AnyOracleRollableRowIdWildcard")


class Suggestions(RootModel[Sequence[AnyIdWildcard]]):
    root: Sequence[AnyIdWildcard] = Field(..., title="Suggestions")


class TruthOptionOracles(RootModel[Mapping[str, EmbeddedOracleRollable]]):
    root: Mapping[str, EmbeddedOracleRollable] = Field(..., title="TruthOptionOracles")


class Type(RootModel[frozenset[SimpleTypes]]):
    root: frozenset[SimpleTypes] = Field(..., min_length=1)


class WebUrl(RootModel[AnyUrl]):
    root: AnyUrl = Field(..., title="WebUrl")


class WebpImageUrl(RootModel[str]):
    root: str = Field(..., title="WebpImageUrl")


AssetCollection.model_rebuild()
AtlasCollection.model_rebuild()
CoreSchemaMetaSchema.model_rebuild()
Expansion.model_rebuild()
MoveCategory.model_rebuild()
NpcCollection.model_rebuild()
OracleTablesCollection.model_rebuild()
TagSchemaArray.model_rebuild()
TagSchemaObject.model_rebuild()
