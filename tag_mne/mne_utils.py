import numpy as np
import mne

def concatenate_epochs(epochs_list, add_offset_event_id = True, add_offset = True):
    if add_offset_event_id:
        events = epochs_list[0].events
        ids = events[:, 2]
        offset = np.max(ids)

        for epochs in epochs_list[1:len(epochs_list)]:
            epochs.events[:,2] += offset
            epochs.event_id = {k: v + offset for k, v in epochs.event_id.items()}
            offset = np.max(epochs.events[:, 2])
    return mne.concatenate_epochs(epochs_list, add_offset)