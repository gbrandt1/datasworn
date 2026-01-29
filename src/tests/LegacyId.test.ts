import { describe, expect, test } from 'bun:test'

import { buildLegacyDataforgedIdMap } from '../scripts/pkg/nodejs/buildLegacyIdMap.js'
import { loadDatasworn } from './loadJson.js'

const idMap = await buildLegacyDataforgedIdMap()
const { index } = await loadDatasworn()

const validTargets = new Set([null, ...index.keys()])

describe('Legacy ID map target', () => {
	test.each(Object.entries(idMap))('%p => %p', (_oldId, newId) =>
		expect(newId).toBeOneOf(validTargets))
})
