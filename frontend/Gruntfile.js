'use strict';
module.exports = function(grunt) {
  require('jit-grunt')(grunt);
  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    sass: {
      options: {
        sourceMap: true
      },
      dist: {
        files: [{
          expand: true,
          cwd: 'src/scss/',
          src: ['*.scss'],
          dest: 'dist/css/',
          ext: '.css'
        }]
      },
      components: {
        files: [{
          expand: true,
          cwd: 'src/components/',
          src: ['**/*.scss'],
          dest: 'src/components/',
          ext: '.css'
        }]
      }
    },
    browserify: {
      options: {
        transform: ['babelify'],
        browserifyOptions: {
          debug: true
        }
      },
      index: {
        src: ['src/js/index/index.js'],
        dest: 'dist/js/index/index.js'
      },
      components: {
        src: ['src/components/**/*.js'],
        dest: 'dist/js/components.js'
      }
    },
    'extract_sourcemap': {
      options: {
        'removeSourcesContent': true
      },
      components: {
        files: {
          'dist/js': ['dist/js/components.js']
        }
      },
      index: {
        files: {
          'dist/js/index': ['dist/js/index/index.js']
        }
      }
    },
    connect: {
      server: {
        options: {
          port: 9000,
          useAvailablePort: true,
          livereload: true,
          hostname: '0.0.0.0',
          base: 'dist'
        }
      }
    },
    watch: {
      scripts: {
        files: 'src/**/*',
        tasks: ['build'],
        options: {
          spawn: false,
          livereload: true
        }
      }
    },
    copy: {
      'js-sourcemaps': { // Needed for sourcemap. Hence, disting inside src folder
        cwd: 'src',
        src: '**/*.js',
        dest: 'dist/src',
        expand: true
      },
      'scss-sourcemaps': { // Needed for sourcemap. Hence, disting inside src folder
        cwd: 'src',
        src: '**/*.scss',
        dest: 'dist/src',
        expand: true
      },
      'assets': {
        cwd: 'src',
        src: 'assets/**/*',
        dest: 'dist/',
        expand: true
      },
      'html': {
        expand: true,
        cwd: 'src',
        src: ['*.html'],
        dest: 'dist',
        ext: '.html'
      }
    },
    eslint: {
      options: {
        configFile: './.eslintrc'
      },
      target: ['src/**/*.js']
    },
    vulcanize: {
      components: {
        options: {
          inlineCss: true,
          inlineScripts: false,
          stripComments: true
        },
        files: {
          'dist/components.html': 'src/components/components-list.html'
        }
      }
    },
    uglify: {
      options: {
        mangle: false,
        sourceMap: true,
        sourceMapIncludeSources: true
      },
      components: {
        src: 'dist/js/components.js',
        dest: 'dist/js/components.min.js',
        options: {
          sourceMapIn: 'dist/js/components.js.map',
          sourceMapRoot: '../' // TODO: See if we can eliminate this redirection
        }
      },
      index: {
        src: 'dist/js/index/index.js',
        dest: 'dist/js/index/index.min.js',
        options: {
          sourceMapIn: 'dist/js/index/index.js.map',
          sourceMapRoot: '../../'
        }
      }
    },
    clean: ['dist']
  });

  let buildPipeline = ['clean','sass', 'browserify', 'extract_sourcemap', 'vulcanize', 'uglify', 'copy:html'];
  grunt.registerTask('build-components', ['clean', 'sass', 'browserify:components', 'extract_sourcemap:components', 'uglify:components']);
  grunt.registerTask('build-commons', buildPipeline.concat(['copy:js-sourcemaps', 'copy:scss-soucemaps','copy:assets']));
  grunt.registerTask('build', 'Build the project', buildPipeline);
  grunt.registerTask('default', 'Default task', ['build']);
  grunt.registerTask('serve', 'Start a local dev server', ['build', 'connect:server', 'watch']);
};
