import numpy as np
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations, NoiseTypes
from brainflow.board_shim import BoardShim, BoardIds


def filter_signal(data, eeg_channels, board_id=BoardIds.CYTON_BOARD.value):
    res = np.copy(data)

    for count, channel in enumerate(eeg_channels):
        # filters work in-place
        if count == 0:
            DataFilter.perform_bandpass(res[channel], BoardShim.get_sampling_rate(board_id), 2.0, 50.0, 4,
                                        FilterTypes.BESSEL_ZERO_PHASE, 0)
        elif count == 1:
            DataFilter.perform_bandstop(res[channel], BoardShim.get_sampling_rate(board_id), 48.0, 52.0, 3,
                                        FilterTypes.BUTTERWORTH_ZERO_PHASE, 0)
        elif count == 2:
            DataFilter.perform_lowpass(res[channel], BoardShim.get_sampling_rate(board_id), 50.0, 5,
                                       FilterTypes.CHEBYSHEV_TYPE_1_ZERO_PHASE, 1)
        elif count == 3:
            DataFilter.perform_highpass(res[channel], BoardShim.get_sampling_rate(board_id), 2.0, 4,
                                        FilterTypes.BUTTERWORTH, 0)
        elif count == 4:
            DataFilter.perform_rolling_filter(res[channel], 3, AggOperations.MEAN.value)
        else:
            DataFilter.remove_environmental_noise(res[channel], BoardShim.get_sampling_rate(board_id),
                                                  NoiseTypes.FIFTY.value)

    return res
