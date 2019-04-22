summary_requests = {};
String.prototype.replaceAll = function (search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
};

function update_request_rows(data) {
    if (summary_requests[data['request_id']]) {
        var row = summary_requests[data['request_id']];
        var string = '<ul>';
        for (i in data['summary']) {
            for (j in data['keywords']) {
                console.log(data['keywords'][j]);
                data['summary'][i] = data['summary'][i].replaceAll(' ' + data['keywords'][j] + ' ', '<span style="background-color: yellow"> ' + data['keywords'][j] + ' </span>')
            }
            string += '<li>' + data['summary'][i] + '</li>'
        }
        string += '</ul>';
        var row_data = row.data();
        row_data[1] = string;
        row.data(row_data);
        row.draw(false);
    }
}

$(document).ready(function () {

    var table = $('#summarization_table').DataTable({
        searching: false,
        ordering: false
    });
    $('#get_summary').on('click', function () {
        var keywords = $('#summary_keywords').val().split(',')
        var badge_string = '<h4>';
        for (j in keywords) {
            keywords[j] = keywords[j].trim();
            badge_string += '<span class="badge badge-secondary" style="margin: 2px">' + keywords[j] + '</span>'
        }
        badge_string += '</h4>';
        $('#summary_tags').html(badge_string);
        var myFile = $('#summarization_files').prop('files');
        var files = []
        for (var i = 0; i < myFile.length; i++) {
            files.push(myFile[i])
        }
        files.forEach(function (file) {
            var reader = new FileReader();
            reader.readAsText(file, "UTF-8");
            reader.onload = function (evt) {
                var row = table.row.add([
                    file.name,
                    "Pending....."
                ]);
                var uuid = uuidv4();
                summary_requests[uuid] = row;
                row.draw()
                // socket.emit('request', {
                //     text: evt.target.result,
                //     request_id: uuid,
                //     type: 'summarize'
                // })
                request_array.push(
                    {
                        text: evt.target.result,
                        request_id: uuid,
                        type: 'summarize',
                        keywords: keywords,
                        summary_type: $("input[name='inlineRadioOptions']:checked").val()
                    }
                )
            };
            reader.onerror = function (evt) {
                console.log(evt);
            }
        })
    })
});