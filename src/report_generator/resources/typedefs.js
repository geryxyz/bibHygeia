// Do not copy this file to the report folder.

/**
 * @typedef {Object} Entry
 * @property {string} key
 * @property {string} type
 * @property {string} file_path
 * @property {number} line_number
 * @property {[string]} fields
 */

/**
 * @typedef {Object} Failure
 * @property {string} type
 */

/**
 * @typedef {Failure & Object} EntryFailure
 * @property {string} entry_key
 * @property {string} message
 * @property {[Hint]} hints
 */

/**
 * @typedef {Failure & Object} FileLineFailure
 * @property {string} file_path
 * @property {string} line_number
 * @property {string} message
 */

/**
 * @typedef {Object} Hint
 * @property {string} title
 * @property {string} recommendation
 * @property {string} reason
 * @property {string} phase
 */

/**
 * @typedef {Object} Report
 * @property {string} start_time
 * @property {string} end_time
 * @property {{string: Entry}} entries
 * @property {[Failure]} failures
 */
