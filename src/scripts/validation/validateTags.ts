import type { JSONSchema7 } from 'json-schema'
import type { Datasworn } from '../../pkg-core/index.js'

function _assemblePkgTags(rulesPackage: Datasworn.RulesPackage) {
	return {
		[rulesPackage._id]: rulesPackage.rules?.tags
	}
}

function _prepareTags(...rulesPackages: Datasworn.RulesPackage[]) {
	const properties: Record<string, JSONSchema7> = {}
	for (const pkg of rulesPackages)
		if (pkg.rules?.tags != null) properties[pkg._id] = pkg.rules?.tags

	return properties
}
