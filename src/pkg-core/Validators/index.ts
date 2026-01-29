import type TypeId from '../IdElements/TypeId.js'
import type TypeNode from '../TypeNode.js'

import { validate as oracle_collection } from './OracleCollection.js'
import { validate as oracle_rollable } from './OracleRollable.js'

const Validators = {
	// asset,
	// move,
	oracle_rollable,
	oracle_collection
} as const satisfies Partial<{
	[K in TypeId.Primary]: (obj: TypeNode.ByType<K>) => boolean
}>

export default Validators
