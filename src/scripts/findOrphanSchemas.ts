import { DefsKey } from './const.js'
import { readJSON } from './utils/readWrite.js'

const usedSchemas = new Set<string>()
const schemaIds = new Set<string>()

const _data = await readJSON(
	'datasworn/datasworn.schema.json',
	function reviver(key, value) {
		if (key === DefsKey && typeof value === 'object')
			for (const schemaId in value) schemaIds.add(schemaId)
		if (key === '$ref' && typeof value === 'string')
			usedSchemas.add(value.split('/').pop() as string)
		return value
	}
)

const unusedSchemas = new Set<string>()

for (const schemaId of schemaIds)
	if (!usedSchemas.has(schemaId)) unusedSchemas.add(schemaId)
