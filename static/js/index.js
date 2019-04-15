$(document).ready(function () {

    var table = $('#summarization_table').DataTable({
        searching: false,
        ordering: false
    });
    var requests = {};
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
                requests[uuid] = row;
                row.draw()
                socket.emit('request', {
                    text: evt.target.result,
                    request_id: uuid,
                    type: 'summarize'
                })
            };
            reader.onerror = function (evt) {
                console.log(evt);
            }
        })
    })
});