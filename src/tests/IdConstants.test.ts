import { describe, expect, test } from 'bun:test'
import {
	AssetIds as ClassicAssetIds,
	MoveIds as ClassicMoveIds,
	OracleIds as ClassicOracleIds
} from '../../pkg/nodejs/@datasworn/ironsworn-classic/ids.js'
// Import ID constants from packages
import {
	AssetIds as StarforgedAssetIds,
	MoveIds as StarforgedMoveIds,
	OracleIds as StarforgedOracleIds
} from '../../pkg/nodejs/@datasworn/starforged/ids.js'
import { IdParser } from '../pkg-core/IdParser.js'
import { loadDatasworn } from './loadJson.js'

const { tree } = await loadDatasworn()
IdParser.tree = tree

describe('ID Constants - Starforged', () => {
	describe('MoveIds', () => {
		test('MoveIds contains expected categories', () => {
			expect(StarforgedMoveIds).toHaveProperty('adventure')
			expect(StarforgedMoveIds).toHaveProperty('combat')
			expect(StarforgedMoveIds).toHaveProperty('exploration')
			expect(StarforgedMoveIds).toHaveProperty('fate')
		})

		test('MoveIds.adventure contains expected moves', () => {
			expect(StarforgedMoveIds.adventure).toHaveProperty('face_danger')
			expect(StarforgedMoveIds.adventure).toHaveProperty('secure_an_advantage')
			expect(StarforgedMoveIds.adventure).toHaveProperty('gather_information')
		})

		test('MoveIds values are valid move IDs', () => {
			const faceDangerId = StarforgedMoveIds.adventure.face_danger
			expect(faceDangerId).toBe('move:starforged/adventure/face_danger')

			// Verify the ID resolves to an actual move
			const move = IdParser.get(faceDangerId)
			expect(move._id).toBe(faceDangerId)
			expect(move.type).toBe('move')
		})

		test('all move IDs in constants are resolvable', () => {
			for (const [_category, moves] of Object.entries(StarforgedMoveIds)) {
				for (const [_moveKey, moveId] of Object.entries(
					moves as Record<string, string>
				)) {
					const move = IdParser.get(moveId)
					expect(move._id).toBe(moveId)
				}
			}
		})
	})

	describe('OracleIds', () => {
		test('OracleIds contains expected collections', () => {
			expect(StarforgedOracleIds).toHaveProperty('core')
			expect(StarforgedOracleIds).toHaveProperty('character')
			expect(StarforgedOracleIds).toHaveProperty('planet')
		})

		test('OracleIds.core contains expected oracles', () => {
			expect(StarforgedOracleIds.core).toHaveProperty('action')
			expect(StarforgedOracleIds.core).toHaveProperty('theme')
			expect(StarforgedOracleIds.core).toHaveProperty('descriptor')
			expect(StarforgedOracleIds.core).toHaveProperty('focus')
		})

		test('nested oracle collections work', () => {
			// character.name is a nested collection
			expect(StarforgedOracleIds.character).toHaveProperty('name')
			expect(StarforgedOracleIds.character.name).toHaveProperty('given_name')
			expect(StarforgedOracleIds.character.name).toHaveProperty('family_name')
			expect(StarforgedOracleIds.character.name).toHaveProperty('callsign')
		})

		test('OracleIds values are valid oracle IDs', () => {
			const actionId = StarforgedOracleIds.core.action
			expect(actionId).toBe('oracle_rollable:starforged/core/action')

			const oracle = IdParser.get(actionId)
			expect(oracle._id).toBe(actionId)
			expect(oracle.type).toBe('oracle_rollable')
		})

		test('nested oracle IDs are resolvable', () => {
			const givenNameId = StarforgedOracleIds.character.name
				.given_name as string
			expect(givenNameId).toBe(
				'oracle_rollable:starforged/character/name/given_name'
			)

			const oracle = IdParser.get(givenNameId)
			expect(oracle._id).toBe(givenNameId)
		})
	})

	describe('AssetIds', () => {
		test('AssetIds contains expected collections', () => {
			expect(StarforgedAssetIds).toHaveProperty('companion')
			expect(StarforgedAssetIds).toHaveProperty('path')
			expect(StarforgedAssetIds).toHaveProperty('command_vehicle')
		})

		test('AssetIds.companion contains expected assets', () => {
			expect(StarforgedAssetIds.companion).toHaveProperty('banshee')
			expect(StarforgedAssetIds.companion).toHaveProperty('glowcat')
			expect(StarforgedAssetIds.companion).toHaveProperty('rockhorn')
		})

		test('AssetIds values are valid asset IDs', () => {
			const bansheeId = StarforgedAssetIds.companion.banshee
			expect(bansheeId).toBe('asset:starforged/companion/banshee')

			const asset = IdParser.get(bansheeId)
			expect(asset._id).toBe(bansheeId)
			expect(asset.type).toBe('asset')
		})

		test('all asset IDs in constants are resolvable', () => {
			for (const [_collection, assets] of Object.entries(StarforgedAssetIds)) {
				for (const [_assetKey, assetId] of Object.entries(
					assets as Record<string, string>
				)) {
					const asset = IdParser.get(assetId)
					expect(asset._id).toBe(assetId)
				}
			}
		})
	})
})

describe('ID Constants - Classic', () => {
	describe('MoveIds', () => {
		test('MoveIds contains expected categories', () => {
			expect(ClassicMoveIds).toHaveProperty('adventure')
			expect(ClassicMoveIds).toHaveProperty('combat')
			expect(ClassicMoveIds).toHaveProperty('relationship')
		})

		test('classic Face Danger ID is correct', () => {
			const faceDangerId = ClassicMoveIds.adventure.face_danger
			expect(faceDangerId).toBe('move:classic/adventure/face_danger')

			const move = IdParser.get(faceDangerId)
			expect(move._id).toBe(faceDangerId)
		})
	})

	describe('OracleIds', () => {
		test('OracleIds contains expected collections', () => {
			expect(ClassicOracleIds).toHaveProperty('action_and_theme')
			expect(ClassicOracleIds).toHaveProperty('name')
		})
	})

	describe('AssetIds', () => {
		test('AssetIds contains expected collections', () => {
			expect(ClassicAssetIds).toHaveProperty('companion')
			expect(ClassicAssetIds).toHaveProperty('path')
			expect(ClassicAssetIds).toHaveProperty('combat_talent')
		})
	})
})

describe('ID Constants - Type Safety', () => {
	test('ID constants have literal string types', () => {
		// This is a compile-time check - if types are wrong, this file won't compile
		const faceDangerId: 'move:starforged/adventure/face_danger' =
			StarforgedMoveIds.adventure.face_danger
		const actionId: 'oracle_rollable:starforged/core/action' =
			StarforgedOracleIds.core.action
		const bansheeId: 'asset:starforged/companion/banshee' =
			StarforgedAssetIds.companion.banshee

		// Runtime verification
		expect(faceDangerId).toBe('move:starforged/adventure/face_danger')
		expect(actionId).toBe('oracle_rollable:starforged/core/action')
		expect(bansheeId).toBe('asset:starforged/companion/banshee')
	})
})
