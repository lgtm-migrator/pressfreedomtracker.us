// jest.config.js
module.exports = {
  testEnvironment: "jsdom",
  verbose: true,
  moduleNameMapper: {
    '^~/(.*)$': '<rootDir>/client/common/js/$1',
    '^WagtailAutocomplete/(.*)$': '<rootDir>/client/autocomplete/js/components/$1',
  },
	transformIgnorePatterns: [
		"<rootDir>/node_modules/(?!d3|internmap|delaunator|robust-predicates)"
	],
  setupFiles: ["<rootDir>/client/common/js/setupTests.js"],
}
