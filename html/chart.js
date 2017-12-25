angular.module("app", ["chart.js"])
  // Optional configuration 
  .config(['ChartJsProvider', function (ChartJsProvider) {
    // Configure all charts 
    ChartJsProvider.setOptions({
      chartColors: ['#FF6384', '#4BC0C0', '#FFCE56', '#E7E9ED', '#36A2EB'],
      responsive: false,
      animation: false,
      scaleUse2Y: true,
    });
    // Configure all line charts 
    ChartJsProvider.setOptions('line', {
      showLines: false
    });

  }])
  .controller("LineCtrl1", ['$scope', '$http', '$timeout', '$interval', function ($scope, $http, $timeout, $interval) {
    $http.get('http://192.168.0.19:80/rest').
        success(function(data, status, headers, config) {
            $scope.data = data.Acc.data;
            $scope.labels = data.Acc.labels;
            $scope.series = data.Acc.series;
        }).
        error(function(data, status, headers, config) {
            // log error
        });

  
  
  // Simulate async data update 
  $interval(function () {
    $http.get('http://192.168.0.19:80/rest').
        success(function(data, status, headers, config) {
            $scope.data = data.Acc.data;
            $scope.labels = data.Acc.labels;
            $scope.series = data.Acc.series;
        }).
        error(function(data, status, headers, config) {
            // log error
        });
  }, 5000);
}])
  .controller("LineCtrl2", ['$scope', '$http', '$timeout', '$interval', function ($scope, $http, $timeout, $interval) {
    $http.get('http://192.168.0.19:80/rest').
        success(function(data, status, headers, config) {
            $scope.data = data.Ruck.data;
            $scope.labels = data.Ruck.labels;
            $scope.series = data.Ruck.series;
        }).
        error(function(data, status, headers, config) {
            // log error
        });

  
  
  // Simulate async data update 
  $interval(function () {
    $http.get('http://192.168.0.19:80/rest').
        success(function(data, status, headers, config) {
            $scope.data = data.Ruck.data;
            $scope.labels = data.Ruck.labels;
            $scope.series = data.Ruck.series;
        }).
        error(function(data, status, headers, config) {
            // log error
        });
  }, 5000);
}])
  .controller("LineCtrl3", ['$scope', '$http', '$timeout', '$interval', function ($scope, $http, $timeout, $interval) {
    $http.get('http://192.168.0.19:80/rest').
        success(function(data, status, headers, config) {
            $scope.data = data.SDEV.data;
            $scope.labels = data.SDEV.labels;
            $scope.series = data.SDEV.series;
        }).
        error(function(data, status, headers, config) {
            // log error
        });

  
  
  // Simulate async data update 
  $interval(function () {
    $http.get('http://192.168.0.19:80/rest').
        success(function(data, status, headers, config) {
            $scope.data = data.SDEV.data;
            $scope.labels = data.SDEV.labels;
            $scope.series = data.SDEV.series;
        }).
        error(function(data, status, headers, config) {
            // log error
        });
  }, 5000);
}]);