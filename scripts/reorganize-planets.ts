#!/usr/bin/env bun

/**
 * Reorganize planets_expanded oracles into hierarchical collections by planet type.
 * Uses the yaml library which preserves anchors and aliases.
 */

import { readFileSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { Pair, parseDocument, Scalar, YAMLMap } from 'yaml'

// Planet types to organize (in display order)
const PLANET_TYPES = [
	'anomalous_world',
	'chemical_world',
	'crystalline_world',
	'desert_world',
	'furnace_world',
	'grave_world',
	'ice_world',
	'jovian_world',
	'jungle_world',
	'karst_world',
	'kintsugi_world',
	'living_world',
	'metallic_world',
	'ocean_world',
	'quarry_world',
	'rocky_world',
	'shattered_world',
	'tainted_world',
	'tidally_locked_world',
	'vital_world'
]

function snakeToTitle(name: string): string {
	return name
		.split('_')
		.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
		.join(' ')
}

function getPlanetType(oracleKey: string): string | null {
	// Handle tidally_locked_world_dark_side variants
	if (oracleKey.startsWith('tidally_locked_world_dark_side_')) {
		return 'tidally_locked_world'
	}

	for (const planetType of PLANET_TYPES) {
		if (oracleKey.startsWith(`${planetType}_`)) {
			return planetType
		}
	}
	return null
}

function getOracleSubkey(oracleKey: string, planetType: string): string {
	if (oracleKey.startsWith('tidally_locked_world_dark_side_')) {
		return oracleKey.slice('tidally_locked_world_'.length)
	}
	return oracleKey.slice(planetType.length + 1) // +1 for underscore
}

const oraclesPath = join(
	import.meta.dir,
	'..',
	'source_data',
	'ancient_wonders',
	'oracles.yaml'
)

console.log('Reading:', oraclesPath)
const yamlContent = readFileSync(oraclesPath, 'utf8')
const doc = parseDocument(yamlContent, { keepSourceTokens: true })

// Get the planets_expanded contents (nested under oracles)
const root = doc.contents as YAMLMap
const oracles = root.get('oracles', true) as YAMLMap
const planetsExpanded = oracles.get('planets_expanded', true) as YAMLMap
const contents = planetsExpanded.get('contents', true) as YAMLMap

// Categorize oracles
const planetOracles = new Map<string, Map<string, any>>()
const generalOracles = new Map<string, any>()

for (const item of contents.items) {
	const pair = item as Pair
	const key = (pair.key as Scalar).value as string
	const value = pair.value

	const planetType = getPlanetType(key)
	if (planetType) {
		if (!planetOracles.has(planetType)) {
			planetOracles.set(planetType, new Map())
		}
		const subkey = getOracleSubkey(key, planetType)
		planetOracles.get(planetType)?.set(subkey, { key, value, pair })
	} else {
		generalOracles.set(key, { key, value, pair })
	}
}

console.log(
	`\nCategorized ${planetOracles.size} planet types, ${generalOracles.size} general oracles`
)
for (const [type, oracles] of planetOracles) {
	console.log(`  ${type}: ${oracles.size} oracles`)
}

// Build new structure - keep general oracles in contents, move planet collections to collections
const newContents = new YAMLMap()
const newCollections = new YAMLMap()

// Add general oracles to contents
for (const [_key, { pair }] of generalOracles) {
	newContents.add(pair)
}

// Get the _source from planets_expanded to use as template
const parentSource = planetsExpanded.get('_source', true)

// Add planet type collections to collections
for (const planetType of PLANET_TYPES) {
	const oracles = planetOracles.get(planetType)
	if (!oracles || oracles.size === 0) continue

	// Create collection map
	const collection = new YAMLMap()
	collection.add(
		new Pair(new Scalar('name'), new Scalar(snakeToTitle(planetType)))
	)
	collection.add(new Pair(new Scalar('type'), new Scalar('oracle_collection')))
	collection.add(new Pair(new Scalar('oracle_type'), new Scalar('tables')))

	// Add _source - clone from parent
	if (parentSource) {
		collection.add(
			new Pair(new Scalar('_source'), doc.createNode(parentSource))
		)
	}

	// Create contents for this collection (oracle tables go in contents)
	const collectionContents = new YAMLMap()
	for (const [subkey, { value }] of oracles) {
		collectionContents.add(new Pair(new Scalar(subkey), value))
	}
	collection.add(new Pair(new Scalar('contents'), collectionContents))

	newCollections.add(new Pair(new Scalar(planetType), collection))
}

// Replace contents and add collections
planetsExpanded.set('contents', newContents)
planetsExpanded.set('collections', newCollections)

// Write output
const output = doc.toString()
writeFileSync(oraclesPath, output)

console.log(`\nWritten reorganized file to: ${oraclesPath}`)
console.log('Output size:', output.length, 'bytes')
