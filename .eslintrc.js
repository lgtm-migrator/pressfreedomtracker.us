module.exports = {
	"extends": "airbnb",

	"ignorePatterns": ["client/statistics/js/searchstats.js", "client/charts/"],

	"plugins": [
		"react"
	],

	"settings": {
		"import/resolver": {
			webpack: {
				config: {
					extensions: ['.js', '.jsx']
				}
			}
		}
	},

	"parserOptions": {
		"ecmaFeatures": {
			"experimentalObjectRestSpread": true
		}
	},

	"globals": {
		"window": true,
		"HTMLInputElement": true,
		"FormData": true,
		"fetch": true,
		"document": true,
		"import": true,
	},

	"rules": {
		"arrow-body-style": 0,
		"prefer-template": 0,
		"no-tabs": 0,
		"indent": ["error", "tab"],
		"no-underscore-dangle": 0,
		"react/jsx-indent": ["error", "tab"],
		"react/jsx-indent-props": ["error", "tab"],
		"react/jsx-no-bind": ["warn"],
		"prefer-destructuring": 0,
		"import/no-unresolved": 0,
		"radix": ["error", "as-needed"],
		"semi": ["error", "never"]
	}
};
