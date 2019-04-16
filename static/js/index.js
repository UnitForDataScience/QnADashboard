summary_requests = {};

function update_request_rows(data) {
    if (summary_requests[data['request_id']]) {
        var row = summary_requests[data['request_id']];
        var string = '<ul>';
        for (i in data['summary']) {
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
                        type: 'summarize'
                    }
                )
            };
            reader.onerror = function (evt) {
                console.log(evt);
            }
        })
    })
});