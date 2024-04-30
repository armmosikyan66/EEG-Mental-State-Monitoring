from brainflow.ml_model import MLModel, BrainFlowModelParams, BrainFlowMetrics, BrainFlowClassifiers


def get_relaxation_model() -> MLModel:
    relaxation_params = BrainFlowModelParams(BrainFlowMetrics.RESTFULNESS.value, BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)
    relaxation = MLModel(relaxation_params)

    return relaxation
