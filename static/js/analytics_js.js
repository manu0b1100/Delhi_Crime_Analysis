$(document).ready(function () {
    $('#sub').click(function () {

        sel_val = $('#heatmap_select').val();
        console.log(sel_val);
        $.ajax({

            type: 'POST',
            url: "calc_func",
            data: {
                function: 'heatmap',
                sel_val: sel_val,
                dis_pol: $('#heatmap_select2').val()
            }
            , success: function (data) {
                $('#heatmap_graph').html(data)

            }

        });

    });

    $('#sublc').click(function () {
        $.ajax({

            type: 'POST',
            url: "calc_func",
            data: {
                function: 'linechart',
                time1_val: $('#linechart_select1').val(),
                time2_val: $('#linechart_select2').val()
            }
            , success: function (data) {
                $('#linechart_graph').html(data)

            }

        });

    });
    $('#subvc').click(function () {
        $.ajax({

            type: 'POST',
            url: "calc_func",
            data: {
                function: 'violinchart',
                time_val: $('#violinchart_select').val(),
            }
            , success: function (data) {
                $('#violinchart_graph').html(data);

            }

        });

    });
    $('#subsc').click(function () {
        $.ajax({

            type: 'POST',
            url: "calc_func",
            data: {
                function: 'scatterchart',
                x_val: $('#scatterchart_select').val(),
                y_val: $('#scatterchart_crime').val()
            }
            , success: function (data) {
                $('#scatterchart_graph').html(data)

            }

        });
    });

    $('#subproba').click(function () {
        $.ajax({

            type: 'POST',
            url: "calc_func",
            data: {
                function: 'probachart',
                model: $('#proba_model_select').val(),
                hour: $('#proba_hour_select').val(),
                month: $('#proba_month_select').val()
            }
            , success: function (data) {
                $('#proba_graph').html(data)

            }


        });


    });


});