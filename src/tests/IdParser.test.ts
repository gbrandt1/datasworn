import { expect, test, describe } from 'bun:test'

import { IdParser } from '../pkg-core/IdParser.js'
import { loadDatasworn } from './loadJson.js'

const { tree, index } = await loadDatasworn()

IdParser.tree = tree

const cases = Array.from(index.keys()).map((id) => [id, IdParser.get(id)._id])

describe('IdParser lookup', () => {
	test.each(cases)('%p', (id, lookupId) => expect(id).toBe(lookupId))
})

describe('Condition ID parsing', () => {
	// Get all condition IDs from the index
	const conditionIds = Array.from(index.keys()).filter((id) =>
		id.includes('.condition:')
	)

	test('condition IDs exist in the data', () => {
		expect(conditionIds.length).toBeGreaterThan(0)
	})

	test('move condition IDs have correct format', () => {
		const moveConditionIds = conditionIds.filter((id) =>
			id.startsWith('move.condition:')
		)
		expect(moveConditionIds.length).toBeGreaterThan(0)

		for (const id of moveConditionIds) {
			// Format: move.condition:package/path/move_key.index
			expect(id).toMatch(/^move\.condition:[a-z_]+\/[a-z_/]+\.\d+$/)
		}
	})

	test('embedded move condition IDs have correct format', () => {
		const embeddedConditionIds = conditionIds.filter((id) =>
			id.includes('ability.move.condition:')
		)

		// These exist in asset abilities that define custom moves
		if (embeddedConditionIds.length > 0) {
			for (const id of embeddedConditionIds) {
				// Format: asset.ability.move.condition:package/path/asset_key.ability_index.move_key.condition_index
				expect(id).toMatch(
					/^asset\.ability\.move\.condition:[a-z_]+\/[a-z_/]+\.\d+\.[a-z_]+\.\d+$/
				)
			}
		}
	})

	test('condition IDs resolve to objects with _id property', () => {
		for (const id of conditionIds.slice(0, 10)) {
			// Test first 10 for speed
			const parsed = IdParser.get(id)
			expect(parsed._id).toBe(id)
		}
	})

	test('condition objects have expected properties', () => {
		const sampleId = conditionIds[0]
		if (sampleId) {
			const condition = IdParser.get(sampleId)
			expect(condition).toHaveProperty('_id')
			expect(condition).toHaveProperty('method')
			expect(condition).toHaveProperty('roll_options')
		}
	})
})

describe('Outcome ID parsing', () => {
	// Get all outcome IDs from the index
	const outcomeIds = Array.from(index.keys()).filter((id) =>
		id.includes('.outcome:')
	)

	test('outcome IDs exist in the data', () => {
		expect(outcomeIds.length).toBeGreaterThan(0)
	})

	test('move outcome IDs have correct format', () => {
		const moveOutcomeIds = outcomeIds.filter((id) =>
			id.startsWith('move.outcome:')
		)
		expect(moveOutcomeIds.length).toBeGreaterThan(0)

		for (const id of moveOutcomeIds) {
			// Format: move.outcome:package/path/move_key.outcome_type
			expect(id).toMatch(/^move\.outcome:[a-z_]+\/[a-z_/]+\.(strong_hit|weak_hit|miss)$/)
		}
	})

	test('embedded move outcome IDs have correct format', () => {
		const embeddedOutcomeIds = outcomeIds.filter((id) =>
			id.includes('ability.move.outcome:')
		)

		// These exist in asset abilities that define custom moves
		if (embeddedOutcomeIds.length > 0) {
			for (const id of embeddedOutcomeIds) {
				// Format: asset.ability.move.outcome:package/path/asset_key.ability_index.move_key.outcome_type
				expect(id).toMatch(
					/^asset\.ability\.move\.outcome:[a-z_]+\/[a-z_/]+\.\d+\.[a-z_]+\.(strong_hit|weak_hit|miss)$/
				)
			}
		}
	})

	test('outcome IDs resolve to objects with _id property', () => {
		for (const id of outcomeIds.slice(0, 10)) {
			// Test first 10 for speed
			const parsed = IdParser.get(id)
			expect(parsed._id).toBe(id)
		}
	})

	test('outcome objects have expected properties', () => {
		const sampleId = outcomeIds[0]
		if (sampleId) {
			const outcome = IdParser.get(sampleId)
			expect(outcome).toHaveProperty('_id')
			expect(outcome).toHaveProperty('text')
		}
	})

	test('each move has three outcomes (strong_hit, weak_hit, miss)', () => {
		const moveOutcomeIds = outcomeIds.filter((id) =>
			id.startsWith('move.outcome:')
		)

		// Group by move ID (everything before the last dot)
		const byMove = new Map<string, string[]>()
		for (const id of moveOutcomeIds) {
			const moveId = id.substring(0, id.lastIndexOf('.'))
			if (!byMove.has(moveId)) byMove.set(moveId, [])
			byMove.get(moveId)!.push(id)
		}

		// Each move should have exactly 3 outcomes
		for (const [moveId, outcomes] of byMove) {
			expect(outcomes.length).toBe(3)
			const outcomeTypes = outcomes.map(id => id.substring(id.lastIndexOf('.') + 1))
			expect(outcomeTypes).toContain('strong_hit')
			expect(outcomeTypes).toContain('weak_hit')
			expect(outcomeTypes).toContain('miss')
		}
	})
})
