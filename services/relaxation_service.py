import asyncio
import time

import numpy as np

from configs.board import board
from configs.relaxation_model import get_relaxation_model
from utils.denoise_signal import denoise_signal
from utils.filter_signal import filter_signal
from utils.save_session_plot import save_session_plot
from utils.write_session_csv import write_session_csv
from brainflow.board_shim import BoardShim
from brainflow.data_filter import DataFilter
from fastapi import WebSocket, WebSocketDisconnect


class RelaxationService:
    """
    This service handles WebSocket connections for a relaxation application.
    It enables real-time communication and processing of EEG data to determine relaxation states of the users.
    """

    async def _check_relaxation_session(self, eeg_channels, sampling_rate) -> float:
        data = board.get_board_data()
        data = filter_signal(data, eeg_channels)
        data = denoise_signal(data, eeg_channels)
        bands = DataFilter.get_avg_band_powers(data, eeg_channels, sampling_rate, False)
        feature_vector = np.concatenate((bands[0], bands[1]))
        relaxation = get_relaxation_model()
        relaxation.prepare()
        relaxation_score = relaxation.predict(feature_vector)
        relaxation.release()
        print('Relaxation: %f' % relaxation_score)
        return relaxation_score[0]

    async def get_relaxation(self, websocket: WebSocket):
        await websocket.accept()
        start_time = time.time()  # Record the start time
        master_board_id = board.get_board_id()
        sampling_rate = BoardShim.get_sampling_rate(master_board_id)
        eeg_channels = BoardShim.get_eeg_channels(int(master_board_id))
        data = board.get_board_data()
        current_step = 0
        relaxation_count = 0
        total_checks = 0

        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time > 60:
                relaxation_percentage = relaxation_count / total_checks if total_checks > 0 else 0

                if relaxation_percentage >= 0.6:
                    current_step += 1
                    await websocket.send_json({"current_step": current_step, "type": "plus"})
                elif current_step >= 1:
                    current_step -= 1
                    await websocket.send_json({"current_step": current_step, "type": "minus"})

                if current_time == 3:
                    await websocket.close()
                    output_plot_path = "./static/relaxation_statistics.png"
                    output_csv_path = "./static/relaxation.csv"
                    save_session_plot(data, eeg_channels, output_plot_path)
                    write_session_csv(data, output_csv_path)
                    break

                relaxation_count = 0
                total_checks = 0
                start_time = time.time()

                continue

            try:
                await websocket.send_text(f"process")
                await asyncio.sleep(5)
                relaxation_measure = await self._check_relaxation_session(eeg_channels, sampling_rate)
                await websocket.send_json({"type": "score", "value": 1 - relaxation_measure })

                if relaxation_measure <= 0.2:
                    relaxation_count += 1

                total_checks += 1
            except WebSocketDisconnect:
                print("Client disconnected")
                break
