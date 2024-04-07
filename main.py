import time
import numpy as np
import uvicorn
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter
from brainflow.ml_model import BrainFlowMetrics, BrainFlowClassifiers, BrainFlowModelParams, MLModel

async def main(websocket):
    params = BrainFlowInputParams()
    params.serial_port = "/dev/cu.usbserial-DM01N8KH"
    board = BoardShim(BoardIds.CYTON_BOARD, params)
    master_board_id = board.get_board_id()
    eeg_channels = BoardShim.get_eeg_channels(master_board_id)
    sampling_rate = BoardShim.get_sampling_rate(master_board_id)
    board.prepare_session()
    board.start_stream()
    BoardShim.log_message(LogLevels.LEVEL_INFO.value, 'start sleeping in the main thread')
    time.sleep(5)
    data = board.get_board_data()

    current_step = 2

    def check_relax_session():
        start_time = time.time()

        relax_count = 0
        total_checks = 0

        while time.time() - start_time < 5: # 60
            bands = DataFilter.get_avg_band_powers(
                data, eeg_channels, sampling_rate, True)
            feature_vector = np.concatenate((bands[0], bands[1]))

            relaxation_params = BrainFlowModelParams(
                BrainFlowMetrics.MINDFULNESS.value, BrainFlowClassifiers.DEFAULT_CLASSIFIER.value)
            relaxation = MLModel(relaxation_params)
            relaxation.prepare()
            # print('Relaxation: %f' % relaxation.predict(feature_vector))
            relaxed_measure = relaxation.predict(feature_vector)
            relaxation.release()

            if relaxed_measure >= 0.8:
                relax_count += 1

            total_checks += 1

        relax_percentage = relax_count / total_checks if total_checks > 0 else 0

        if relax_percentage >= 0.6:
            return True
        else:
            return False

    while True:
        if current_step > 3:
            board.stop_stream()
            board.release_session()
            break

        if check_relax_session():
            current_step += 1
            await websocket.send_json({"status": "True"})
        elif current_step != 1:
            current_step -= 1
            await websocket.send_json({"status": "False"})
        else:
            time.sleep(5)
            continue





#
# if __name__ == "__main__":
#     main()
# app.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.websocket("/relax-session")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive()
            await main(websocket)
    except WebSocketDisconnect:
        pass


@app.get("/")
async def root():
    return HTMLResponse("""
    <!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
</head>
<body>
    <h1>WebSocket Test</h1>
    <div id="messages"></div>

    <script>
        var ws = new WebSocket("ws://localhost:5001/relax-session");
        ws.onopen = function() {
            ws.send("start");
        }
        ws.onmessage = function(event) {
            console.log(event.data);
        };
    </script>
</body>
</html>
    """)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5001, log_level="debug", reload=True)