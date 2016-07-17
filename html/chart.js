angular.module("app", ["chart.js"])
  // Optional configuration 
  .config(['ChartJsProvider', function (ChartJsProvider) {
    // Configure all charts 
    ChartJsProvider.setOptions({
      chartColors: ['#FF6384', '#4BC0C0', '#FFCE56', '#E7E9ED', '#36A2EB'],
      responsive: false
    });
    // Configure all line charts 
    ChartJsProvider.setOptions('line', {
      showLines: false
    });
  }])
  .controller("LineCtrl1", ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
 
  //$scope.labels = ["January", "February", "March", "April", "May", "June", "July"];
  //$scope.series = ['Series A', 'Series B'];
  //$scope.data = [
  //  [65, 59, 80, 81, 56, 55, 40],
  //  [28, 48, 40, 19, 86, 27, 90]
  //];
  $scope.labels = ["22:39:24.115512", "22:39:24.814156", "22:39:25.513996", "22:39:26.213876"];
  $scope.series = ['Acc max', 'Acc avg', 'Acc min', 'Ruck max', 'Ruck avg'];
  $scope.data = [
    [0.001825202092467668, 0.060394608999436473, 0.0020907405192633795, 0.0020410905743001324],
    [0.0008050942507269996, 0.003177374158197578, 0.0008266969462307133, 0.0008363368716117088],
    [0.00016944134463605038, 0.0001302087958637664, 0.00018227683591191216, 0.00016944134463605038],
    [0.25287961246887636, 0.314024784241735, 0.30050537546922756, 0.2744684606521228],
    [0.015117100420775903, 0.00730557215983137, 0.003203171252102797, 0.00422606716099997]
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
}])
  .controller("LineCtrl2", ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $http.get('http://192.168.0.19:80/rest').
        success(function(data, status, headers, config) {
            $scope.data = data.data;
            $scope.labels = data.labels;
            $scope.series = data.series;
            //console.log(data.data)
        }).
        error(function(data, status, headers, config) {
            // log error
        });

  
  $scope.onClick = function (points, evt) {
    console.log(points, evt);
  };
  
  // Simulate async data update 
  $timeout(function () {
    $http.get('http://192.168.0.19:80/rest').
        success(function(data, status, headers, config) {
            $scope.data = data.data;
            $scope.labels = data.labels;
            $scope.series = data.series;
            //console.log(data.data)
        }).
        error(function(data, status, headers, config) {
            // log error
        });
    
    
  }, 3000);
}]);