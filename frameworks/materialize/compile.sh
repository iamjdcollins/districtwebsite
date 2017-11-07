#!/bin/bash
grunt sass:min
grunt concat:dist
grunt babel:dist
grunt uglify:dist
/bin/cp dist/css/materialize.min.css ../../www_slcschools_org/static/www_slcschools_org/css/
/bin/cp dist/js/materialize.min.js ../../www_slcschools_org/static/www_slcschools_org/js/
/bin/cp -R fonts/* ../../www_slcschools_org/static/www_slcschools_org/fonts/
