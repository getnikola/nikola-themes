// generated on 2017-02-25 using generator-webapp 2.4.1
const gulp = require('gulp');
const critical = require('critical');

gulp.task('critical', function (cb) {
    critical.generate({
        inline: true,
        base: '../../output/',
        src: 'index.html',
        dest: 'index-critical.html',
        minify: true,
        dimensions: [{
            height: 200,
            width: 500
        }, {
            height: 900,
            width: 1200
        }]
    });
});
