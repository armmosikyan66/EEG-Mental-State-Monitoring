import asyncio
import time

from configs.board import board
from configs.concentration_model import get_concentration_model
from utils.denoise_signal import denoise_signal
from utils.filter_signal import filter_signal
from utils.save_session_plot import save_session_plot
from utils.write_session_csv import write_session_csv

from brainflow.board_shim import BoardShim
from brainflow.data_filter import DataFilter
from fastapi import WebSocket, WebSocketDisconnect


class ConcentrationService:
    """
    This service handles WebSocket connections for a concentration application.
    It enables real-time communication and processing of EEG data to determine concentration states of the users.
    """

    async def _check_concentration_session(self, eeg_channels, sampling_rate) -> float:
        await asyncio.sleep(5)

        # Retrieve the latest EEG data from the board
        data = board.get_board_data()

        # Apply a filter to remove unwanted frequencies from the EEG data
        data = filter_signal(data, eeg_channels)

        # Apply a denoising algorithm to further clean the EEG data
        data = denoise_signal(data, eeg_channels)

        # Calculate the average band powers of the EEG data which are essential features for relaxation detection
        bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, False)

        # Concatenate delta and theta band powers to form a feature vector for model prediction
        feature_vector = bands[0]

        # Load the concentration model and prepare it for prediction
        concentration = get_concentration_model()
        concentration.prepare()

        # Predict the concentration score based on the feature vector
        concentration_score = concentration.predict(feature_vector)

        # Release resources used by the model
        concentration.release()

        return float(concentration_score[0])

    async def get_concentration(self, websocket: WebSocket):
        # Accept the WebSocket connection from the clientj
        await websocket.accept()


        # Record the start time of the session for time-based calculations
        start_time = time.time()

        # Retrieve board information to get sampling rate and EEG channel details
        master_board_id = board.get_board_id()
        sampling_rate = BoardShim.get_sampling_rate(master_board_id)
        eeg_channels = BoardShim.get_eeg_channels(int(master_board_id))
        data = board.get_board_data()


        # Initialize variables to track relaxation over time
        current_step = 0
        concentration_count = 0
        total_checks = 0

        # Main loop to continuously check relaxation state
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            # Check if it's time to analyze the concentration state (every 20 seconds)
            if elapsed_time > 20:
                # Calculate the percentage of time the user was concentrated
                concentration_percentage = concentration_count / total_checks if total_checks > 0 else 0

                # Update steps based on concentration percentage
                if concentration_percentage >= 0.6:
                    current_step += 1
                    await websocket.send_json({"current_step": current_step})

                # Close the session after a specific condition is met
                if current_step == 3:
                    await websocket.close()
                    output_plot_path = "./static/concentration_statistics.png"
                    output_csv_path = "./static/concentration.csv"

                    # Save session data to files
                    save_session_plot(data, eeg_channels, output_plot_path)
                    write_session_csv(data, output_csv_path)
                    break

                concentration_count = 0
                total_checks = 0
                start_time = time.time()

                continue

            # Sleep briefly to avoid overloading the server with continuous checks
            try:
                # Check relaxation status and send the score to the client
                concentration_measure = await self._check_concentration_session(eeg_channels, sampling_rate)
                await websocket.send_json({"type": "score", "value": concentration_measure })

                # Count how often the user is concentrated
                if concentration_measure >= 0.3:
                    concentration_count += 1

                total_checks += 1
            except WebSocketDisconnect:
                # Handle client disconnection
                print("Client disconnected")
                break
