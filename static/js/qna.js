predictor_requests = {};


$(document).ready(function () {

    $('#get_response').on('click', function () {
        var uuid = uuidv4();
        var myFile = $('#QnA_files').prop('files');
        var question = $('#QnA_keywords').val().split('')

        files.forEach(function (file) {
            var reader = new FileReader();
            reader.readAsText(file, "UTF-8");
            reader.onload = function (evt) {
                request_array.push(
                    {
                        text: evt.target.result,
                        request_id: uuid,
                        type: 'QnA'
                        question: question
                    }
                )
            }
        }
    })
});