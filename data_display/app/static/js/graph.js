$(document).ready(function() {
	console.log('hi from grapgh.js!!')
	console.log(chart_id)
	$(chart_id).highcharts({
		chart: chart,
		title: title,
		xAxis: xAxis,
		yAxis: yAxis,
		series: series
	});
});