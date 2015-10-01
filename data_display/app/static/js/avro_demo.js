$(function () {
    Highcharts.setOptions({
        global : {
            useUTC : false
        }
    });
    $('#Avrostart').click(function(){
            start_url='http://seriotics.info/api/avro_run/true';
            $.ajax({url: start_url, 
                    cache: false
                }
            );
        });
    $('#Avrostop').click(function(){
            stop_url='http://seriotics.info/api/avro_run/false';
            $.ajax({url: stop_url,
                    cache: false
                }
            );
        });
    $('#AvrostartProducer').click(function(){
            start_url='http://seriotics.info/api/avro_run_producer/true';
            $.ajax({url: start_url, 
                    cache: false
                }
            );
        });
    $('#AvrostopProducer').click(function(){
            stop_url='http://seriotics.info/api/avro_run_producer/false';
            $.ajax({url: stop_url,
                    cache: false
                }
            );
        });
    // Create the chart
    $('#container').highcharts('StockChart', {
        chart : {
            events : {
                load : function () {

                    // set up the updating of the chart each second
                    var series = this.series[0];
                    tp_url = 'http://seriotics.info/api/avro_throughput'
					setInterval(function () {
                        var x = (new Date()).getTime(), // current time
                            y = $.getJSON(tp_url, function(data){
                            	series.addPoint([x, data.result.records_per_second], true, true);
                    		});
                    }, 1000);
                }
            }
        },

        rangeSelector: {
            buttons: [{
                count: 1,
                type: 'minute',
                text: '1M'
            }, {
                count: 5,
                type: 'minute',
                text: '5M'
            }, {
                type: 'all',
                text: 'All'
            }],
            inputEnabled: false,
            selected: 0
        },

        title : {
            text : 'Average Records-Processed/Second'
        },

        exporting: {
            enabled: false
        },

        series : [{
            name : 'data',
            data : (function () {
                // generate an array of random data
                var data = [], time = (new Date()).getTime(), i;

                for (i = -999; i <= 0; i += 1) {
                    data.push([
                        time + i * 1000,
                        0
                    ]);
                }
                return data;
            }())
        }]
    });
});
