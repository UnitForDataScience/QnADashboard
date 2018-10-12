var table = $('#summary_table').DataTable();
$(function () {

    $('#summary_search').on('click', function () {
        console.log('request made');
        table.clear();
        $('#overlay').css('display', 'block');
        $.get({
            url: '/polls/summary?keywords=' + $('#summary_textbox').val(),
            success: function (data) {
                $('#overlay').css('display', 'none');
                data = data['message'];
                console.log(data);
                $('#summary_list').html('');
                for (iter in data) {

                    var string = '<ul>';
                    for (i in data[iter][1]) {
                        string += '<li>' + data[iter][1][i] + '</li>'
                    }

                    string += '</ul>';

                    table.row.add([data[iter][0], string])
                }

                table.draw();

            },
            error: function (data) {
                console.log(data);
            }
        })
    })
});