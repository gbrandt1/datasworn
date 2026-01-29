/**
 * Generates TypeScript ID constant objects from built Datasworn JSON.
 *
 * This allows consumers to get full auto-complete for IDs:
 *
 * ```typescript
 * import { MoveIds, OracleIds, AssetIds } from '@datasworn/starforged/ids'
 *
 * const id = MoveIds.adventure.face_danger
 * // Type: "move:starforged/adventure/face_danger"
 * ```
 */

import type { Datasworn } from '../../../pkg-core/index.js'

type IdConstantObject = { [key: string]: string | IdConstantObject }

/** Extract IDs from a move category */
function extractMoveIds(category: Datasworn.MoveCategory): IdConstantObject {
	const result: IdConstantObject = {}

	if (category.contents) {
		for (const [key, move] of Object.entries(category.contents)) {
			result[key] = move._id
		}
	}

	return result
}

/** Extract IDs from an oracle collection (recursive) */
function extractOracleIds(
	collection: Datasworn.OracleCollection
): IdConstantObject {
	const result: IdConstantObject = {}

	// Handle direct oracle tables in contents
	if (collection.contents) {
		for (const [key, item] of Object.entries(collection.contents)) {
			if (item.type === 'oracle_rollable') {
				result[key] = item._id
			} else if (item.type === 'oracle_collection') {
				// Nested collection - recurse
				result[key] = extractOracleIds(item as Datasworn.OracleCollection)
			}
		}
	}

	// Handle collections property (alternative structure)
	if ('collections' in collection && collection.collections) {
		for (const [key, subcollection] of Object.entries(collection.collections)) {
			result[key] = extractOracleIds(
				subcollection as Datasworn.OracleCollection
			)
		}
	}

	return result
}

/** Extract IDs from an asset collection */
function extractAssetIds(
	collection: Datasworn.AssetCollection
): IdConstantObject {
	const result: IdConstantObject = {}

	if (collection.contents) {
		for (const [key, asset] of Object.entries(collection.contents)) {
			result[key] = asset._id
		}
	}

	return result
}

/** Generate ID constants from a ruleset or expansion */
export function generateIdConstants(
	data: Datasworn.Ruleset | Datasworn.Expansion
): {
	MoveIds: IdConstantObject
	OracleIds: IdConstantObject
	AssetIds: IdConstantObject
} {
	const MoveIds: IdConstantObject = {}
	const OracleIds: IdConstantObject = {}
	const AssetIds: IdConstantObject = {}

	// Extract move IDs
	if (data.moves) {
		for (const [categoryKey, category] of Object.entries(data.moves)) {
			MoveIds[categoryKey] = extractMoveIds(category)
		}
	}

	// Extract oracle IDs
	if (data.oracles) {
		for (const [collectionKey, collection] of Object.entries(data.oracles)) {
			OracleIds[collectionKey] = extractOracleIds(collection)
		}
	}

	// Extract asset IDs
	if (data.assets) {
		for (const [collectionKey, collection] of Object.entries(data.assets)) {
			AssetIds[collectionKey] = extractAssetIds(collection)
		}
	}

	return { MoveIds, OracleIds, AssetIds }
}

/** Generate JavaScript source for ID constants */
export function generateIdConstantsJs(
	data: Datasworn.Ruleset | Datasworn.Expansion
): string {
	const { MoveIds, OracleIds, AssetIds } = generateIdConstants(data)

	const formatObject = (obj: IdConstantObject, indent = 0): string => {
		const pad = '\t'.repeat(indent)
		const entries = Object.entries(obj)

		if (entries.length === 0) return '{}'

		const lines = entries.map(([key, value]) => {
			// Ensure key is a valid JS identifier or quote it
			const safeKey = /^[a-z_][a-z0-9_]*$/i.test(key) ? key : `'${key}'`

			if (typeof value === 'string') {
				return `${pad}\t${safeKey}: '${value}'`
			} else {
				return `${pad}\t${safeKey}: ${formatObject(value, indent + 1)}`
			}
		})

		return `{\n${lines.join(',\n')}\n${pad}}`
	}

	return `// Auto-generated ID constants - do not edit manually
// Generated from Datasworn JSON data

export const MoveIds = ${formatObject(MoveIds)}

export const OracleIds = ${formatObject(OracleIds)}

export const AssetIds = ${formatObject(AssetIds)}
`
}

/** Generate TypeScript declaration for ID constants */
export function generateIdConstantsDts(
	data: Datasworn.Ruleset | Datasworn.Expansion
): string {
	const { MoveIds, OracleIds, AssetIds } = generateIdConstants(data)

	const formatTypeObject = (obj: IdConstantObject, indent = 0): string => {
		const pad = '\t'.repeat(indent)
		const entries = Object.entries(obj)

		if (entries.length === 0) return '{}'

		const lines = entries.map(([key, value]) => {
			const safeKey = /^[a-z_][a-z0-9_]*$/i.test(key) ? key : `'${key}'`

			if (typeof value === 'string') {
				// Use literal type for the ID string
				return `${pad}\treadonly ${safeKey}: '${value}'`
			} else {
				return `${pad}\treadonly ${safeKey}: ${formatTypeObject(value, indent + 1)}`
			}
		})

		return `{\n${lines.join('\n')}\n${pad}}`
	}

	return `// Auto-generated ID constant types - do not edit manually

export declare const MoveIds: ${formatTypeObject(MoveIds)}

export declare const OracleIds: ${formatTypeObject(OracleIds)}

export declare const AssetIds: ${formatTypeObject(AssetIds)}
`
}
