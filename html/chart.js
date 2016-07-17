angular.module("app", ["chart.js"])
  // Optional configuration 
  .config(['ChartJsProvider', function (ChartJsProvider) {
    // Configure all charts 
    ChartJsProvider.setOptions({
      chartColors: ['#FF5252', '#FF8A80'],
      responsive: false
    });
    // Configure all line charts 
    ChartJsProvider.setOptions('line', {
      showLines: false
    });
  }])
  .controller("LineCtrl", ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
 
  $scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
  $scope.series = ['Series A', 'Series B'];
  $scope.data = [
    [65, 59, 80, 81, 56, 55, 40],
    [28, 48, 40, 19, 86, 27, 90]
  ];
  $scope.onClick = function (points, evt) {
    console.log(points, evt);
  };
  
  // Simulate async data update 
  $timeout(function () {
    $scope.data = [
      [28, 18, 40, 19, 86, 27, 90],
      [65, 29, 80, 81, 56, 55, 40]
    ];
    $http.get('http://192.168.0.19:80/rest').
        success(function(data, status, headers, config) {
            $scope.data = data.data;
            console.log(data.data)
        }).
        error(function(data, status, headers, config) {
            // log error
        });
    
    
  }, 3000);
}]);