predictor_requests = {};

function update_qna_div(data) {
    console.log(data);
    data['text'] = data['text'].replaceAll(data['answer']['best_span_str'], '<span style="background-color: yellow">' + data['answer']['best_span_str'] + '</span>')
    $('#qna_answer').html('<p>' + data['text'] + '</p>')
}

$(document).ready(function () {

    $('#get_response').on('click', function () {
        var uuid = uuidv4();
        var myFile = $('#QnA_files').prop('files');
        var question = $('#QnA_keywords').val();
        var files = [];
        for (var i = 0; i < myFile.length; i++) {
            files.push(myFile[i])
        }
        $('#qna_answer').html('Pending.....');
        files.forEach(function (file) {

            var reader = new FileReader();
            reader.readAsText(file, "UTF-8");
            reader.onload = function (evt) {
                request_array.push(
                    {
                        text: evt.target.result,
                        request_id: uuid,
                        type: 'QnA',
                        question: question
                    }
                )
            }
        })
    })
});