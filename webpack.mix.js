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
mix.copy('semantic/dist/semantic.min.css', 'app/static/css/semantic.css')
    .copy('semantic/dist/semantic.min.js', 'app/static/js/semantic.js')
    .copy('node_modules/jquery/dist/jquery.js', 'app/static/js/jquery.js')
    .copy('node_modules/jquery-serializejson/jquery.serializejson.js', 'app/static/js/jquery.serializejson.js')
    .copy('semantic/dist/themes', 'app/static/css/themes', false);

mix.browserSync({
    proxy: "127.0.0.1:5000",
    files: ["*.py", "app/static/**", "app/templates/**"]
});
