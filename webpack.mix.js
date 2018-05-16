let mix = require('laravel-mix');

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */
//
mix.copy('semantic/dist/semantic.min.css', 'static/css/semantic.css')
    .copy('semantic/dist/semantic.min.js', 'static/js/semantic.js')
    .copy('semantic/dist/themes', 'static/css/themes', false);

mix.browserSync({
    proxy: "127.0.0.1:5000",
    files: ["*.py","static/*.*"]
});
