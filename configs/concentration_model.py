from brainflow.ml_model import MLModel, BrainFlowModelParams, BrainFlowMetrics, BrainFlowClassifiers


def get_concentration_model() -> MLModel:
    relaxation_params = BrainFlowModelParams(BrainFlowMetrics.MINDFULNESS.value, BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)
    relaxation = MLModel(relaxation_params)

    return relaxation
