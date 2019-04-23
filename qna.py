from allennlp.predictors.predictor import Predictor

predictor = Predictor.from_path(
    "https://s3-us-west-2.amazonaws.com/allennlp/models/bidaf-model-2017.09.15-charpad.tar.gz")


def get_response(question, passage):
    # print(question, passage)
    response = predictor.predict(passage=question, question=passage)
    return response
