'use strict';
module.exports = function(grunt) {
  require('jit-grunt')(grunt);
  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    browserify: {
      options: {
        transform: ['babelify'],
        browserifyOptions: {
          debug: true
        }
      },
      analyzer: {
        src: ['src/js/crowd-analyzer.js'],
        dest: 'dist/js/crowd-analyzer.js'
      },
      graph: {
        src: ['src/js/graph.js'],
        dest: 'dist/js/graph.js'
      },
      components: {
        src: ['src/components/**/*.js'],
        dest: 'dist/js/components.js'
      }
    },
    'dom_munger': {
      components: {
        options: {
          remove: ['script[src]'],
          append: [{
            selector: 'body',
            html: '<script src="js/components.js"></script>'
          }]
        },
        src: 'dist/components.html',
        dest: 'dist/components.html'
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
      'js': { 
        cwd: 'src',
        src: 'js/external/**/*.js',
        dest: 'dist',
        expand: true
      },
      'css': {
        cwd: 'src',
        src: 'css/**/*.css',
        dest: 'dist',
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
    vulcanize: {
      components: {
        options: {
          inlineCss: true,
          inlineScripts: false,
          stripComments: true
        },
        files: {
          'dist/components.html': 'src/components/all-components.html'
        }
      }
    },
    clean: ['dist']
  });

  let buildPipeline = ['clean', 'browserify', 'vulcanize', 'dom_munger', 'copy'];
  grunt.registerTask('build', 'Build the project', buildPipeline);
  grunt.registerTask('default', 'Default task', ['build']);
  grunt.registerTask('serve', 'Start a local dev server', ['build', 'connect:server', 'watch']);
};