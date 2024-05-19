# It imports necessary modules from the brainflow library

from brainflow.ml_model import MLModel, BrainFlowModelParams, BrainFlowMetrics, BrainFlowClassifiers


# Function to get a concentration model
def get_concentration_model() -> MLModel:
    # Define parameters for the concentration model using BrainFlowModelParams
    concentration_params = BrainFlowModelParams(BrainFlowMetrics.MINDFULNESS.value,
                                                BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)

    # Create an instance of MLModel with the defined parameters
    concentration = MLModel(concentration_params)

    # Return the concentration model
    return concentration
