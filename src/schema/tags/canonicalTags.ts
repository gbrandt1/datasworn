import { type TSchema, Type } from '@sinclair/typebox'

const _TagsClassic = {}
const _TagsStarforged = {
	recommended: Type.Boolean({
		description: 'This object is ideal for use in Starforged.'
	})
} satisfies Record<string, TSchema>
const _TagsDelve = {} satisfies Record<string, TSchema>
type TagParams = {
	schema: TSchema
	node_types: []
}
// TODO:
const _TagsSunderedIsles = {
	recommended: Type.Boolean({
		description: 'This object is ideal for use in Sundered Isles.'
	}),
	cursed_version_of: Type.Array(Type.Ref('OracleRollableIdWildcard')),
	// wrap these into their own objects: "cursed" and "curses"?
	curse_behavior: Type.Array(Type.String()), // TODO: enum
	cursed_by: Type.Array(Type.String()),
	region: Type.String() // TODO: enum
	// overland_region
	// location
	// faction_type
	// ship_size
	// treasure_size
} satisfies Record<string, TSchema>
