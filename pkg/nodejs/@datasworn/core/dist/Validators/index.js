"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const OracleCollection_js_1 = require("./OracleCollection.js");
const OracleRollable_js_1 = require("./OracleRollable.js");
const Validators = {
    // asset,
    // move,
    oracle_rollable: OracleRollable_js_1.validate,
    oracle_collection: OracleCollection_js_1.validate
};
exports.default = Validators;
