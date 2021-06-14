var webpack       = require('webpack');
const { merge }   = require('webpack-merge');
var autoprefixer  = require('autoprefixer');
var BundleTracker = require('webpack-bundle-tracker');
var MiniCssExtractPlugin = require('mini-css-extract-plugin');
var path = require('path');

var TARGET = process.env.npm_lifecycle_event;
process.env.BABEL_ENV = TARGET;

var target = __dirname + '/build/static/bundles';

var STATIC_URL = process.env.STATIC_URL || '/common/static/';
var sassData = '$static-url: "' + STATIC_URL + '"';
console.log('Using STATIC_URL', STATIC_URL);


var common = {
	entry: {
		common: __dirname + '/client/common/js/common.js',
		editor: __dirname + '/client/autocomplete/js/editor.js',
		topic: __dirname + '/client/topic/js/index.js',
		statistics: __dirname + '/client/statistics/js/searchstats.js',
	},

	output: {
		path: target,
		filename: '[name].js'
	},

	resolve: {
		alias: {
			'~': __dirname + '/client/common/js',
			WagtailAutocomplete: path.resolve(__dirname, 'client/autocomplete/js/components'),
			modernizr$: path.resolve(__dirname, '.modernizrrc')
		},
		extensions: ['.js', '.jsx'],
		modules: ['node_modules']
	},

	module: {
		rules: [
			{
				test: /\.jsx?$/,
				use: [
					{
						loader: 'babel-loader',
						options: {
							presets: [
								'@babel/preset-react',
								// Setting `modules` false, prevents babel from trying to use
								// commonjs imports, which messes up our nice clean ES6 imports
								// provided directly by Webpack:
								// https://github.com/webpack/webpack/issues/4961#issuecomment-304938963
								['@babel/preset-env', { modules: false }]
							],
						},
					}
				],
				include: [
					path.join(__dirname, '/client/common/js'),
					path.join(__dirname, '/client/autocomplete/js'),
					path.join(__dirname, '/client/topic/js'),
					path.join(__dirname, '/client/statistics/js'),
				],
			},
			{
				test: /\.s[ca]ss$/,
				use: [
					MiniCssExtractPlugin.loader,
					'css-loader',
					'postcss-loader',
					{
						loader: 'sass-loader',

						options: {
							sassOptions: {
								includePaths: [path.resolve(__dirname, 'node_modules/')],
							},
							prependData: sassData,
						}
					}
				]
			},
			{
				test: /\.css$/,
				use: [MiniCssExtractPlugin.loader, 'css-loader', 'postcss-loader']
			},
			// Currently unused, but we'll want it if we install modernizr:
			{
				test: /\.modernizrrc$/,
 				use: ['modernizr-loader']
			},
			{
				test: /\.(png|svg|jpg|gif)$/,
				use: [
					'file-loader',
				],
			},
			{
				test: /\.(woff|woff2|eot|ttf|otf)$/,
				use: [
					'file-loader',
				],
			},
		]
	},

	plugins: [
		new MiniCssExtractPlugin({
			filename: TARGET === 'build' ? '[name]-[hash].css' : '[name].css',
			chunkFilename: TARGET === 'build' ? '[id]-[hash].css' : '[id].css'
		}),
		new BundleTracker({
			path: target,
			filename: './webpack-stats.json'
		})
	]
};

if (TARGET === 'build') {
	module.exports = merge(common, {
		output: {
			filename: '[name]-[contenthash].js'
		},
		plugins: [
			new webpack.DefinePlugin({
				'process.env': { 'NODE_ENV': JSON.stringify('production') }
			})
		]
	});
}

if (TARGET === 'start') {
	module.exports = merge(common, {
		devtool: 'eval-source-map',
		devServer: {
			contentBase: target,
			progress: true,
		}
	});
}
