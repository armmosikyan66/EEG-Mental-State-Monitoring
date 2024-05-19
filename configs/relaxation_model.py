# This code defines a function to get a machine learning model for relaxation analysis
# It imports necessary modules from the brainflow library

from brainflow.ml_model import MLModel, BrainFlowModelParams, BrainFlowMetrics, BrainFlowClassifiers


# Function to get a relaxation model
def get_relaxation_model() -> MLModel:
    # Define parameters for the relaxation model using BrainFlowModelParams
    relaxation_params = BrainFlowModelParams(BrainFlowMetrics.RESTFULNESS.value,
                                             BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)

    # Create an instance of MLModel with the defined parameters
    relaxation = MLModel(relaxation_params)

    # Return the relaxation model
    return relaxation
