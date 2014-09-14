/**
 * Created by tneier on 9/6/14.
 */
angular.module('FlockApp',[])

   .constant('VERSION', '1.0')

  .run(['VERSION', '$rootScope', function(VERSION, $rootScope) {
    $rootScope.version = VERSION;
    $rootScope.name = 'hello there';
    $rootScope.klass = 'red';
  }]);