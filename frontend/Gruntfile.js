module.exports = function(grunt) {

  require('jit-grunt')(grunt);

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    uglify: {
      options: {
        banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
      },
      build: {
        src: 'src/<%= pkg.name %>.js',
        dest: 'dist/<%= pkg.name %>.min.js'
      }
    },
    connect: {
      server: {
        options: {
          port: process.env.PORT || 3000,
          useAvailablePort: true,
          livereload: true,
          hostname: process.env.HOST || '0.0.0.0',
          base: 'src'
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
    }
  });

  // Default task(s).
  grunt.registerTask('default', ['uglify', 'connect:server', 'watch']);

};
