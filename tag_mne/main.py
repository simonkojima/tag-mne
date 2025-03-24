import copy

import numpy as np
import mne

from .utils import get_val_in_tag

def get_values_list(epochs, tag):
    keys = list(epochs.event_id.keys())
    values = list()
    for key in keys:
        for part in key.split("/"):
            if "%s:"%tag in part:
                values.append(part.split(":")[1])
    
    return np.unique(values).tolist() 

def get_binary_epochs(epochs):
    id_target = list(epochs["target"].event_id.values())
    id_nontarget = list(epochs["nontarget"].event_id.values())
    
    for id in id_target:
        if id in id_nontarget:
            print("id '%s' is in nontarget too"%(str(id)))

    X = epochs.copy()

    Y = copy.copy(X.events)
    for idx, y in enumerate(Y[:, 2]):
        if y in id_target:
            Y[idx, 2] = 10
        if y in id_nontarget:
            Y[idx, 2] = 1


    #Y = mne.merge_events(Y, id_target, 10, True)
    #Y = mne.merge_events(Y, id_nontarget, 1, True)
    Y = Y[:, 2]

    return X, Y

def pop_list_indexes(list, indexes_to_remove):
    list = copy.copy(list)
    indexes_to_remove = copy.copy(indexes_to_remove)
    for index in sorted(indexes_to_remove, reverse=True):
        list.pop(index)
    return list

def remove(samples, markers, tag):
    idx_to_delete = list()
    for idx, marker in enumerate(markers):
        tags = marker.split("/")
        if tag in tags:
            idx_to_delete.append(idx)
    #for idx in idx_to_delete:
    #    print(markers[idx])
    
    markers = pop_list_indexes(markers, idx_to_delete)
    samples = pop_list_indexes(samples.tolist(), idx_to_delete)
    
    return np.array(samples), np.array(markers)

def markers_from_events(events, event_id):
    from .utils import get_swap_dict
    event_id_swap = get_swap_dict(event_id)

    samples = np.array(events)[:, 0]
    
    markers = list()
    for val in np.array(events)[:, 2]:
        if "marker:" in str(event_id_swap[val]):
            markers.append(str(event_id_swap[val]))
        else:
            markers.append("marker:%s"%str(event_id_swap[val]))
    
    return samples, markers

def events_from_markers(samples, markers, offset = 0):
    unique_markers = np.unique(markers)
    
    event_id = dict()
    events = list()
    for marker, sample in zip(markers, samples):
        id = np.argwhere(unique_markers == marker)[0][0] + 1 + offset
        events.append([sample, 0, id])
        event_id[marker] = id
    events = np.array(events)

    return events, event_id

def add_event_names(markers, event_names, default_name = 'misc', pre = False):
    for idx, marker in enumerate(markers):
        val = get_val_in_tag(marker, 'marker')
        
        event_name = default_name
        for key, values in event_names.items():
            if str(val) in values:
                event_name = key
                break

        if pre:
            new = ["event:%s"%(event_name), marker]
        else:
            new = [marker, "event:%s"%(event_name)]
        marker = "/".join(new)
        markers[idx] = marker
    return markers

""""
def add_event_names(markers, event_names, default_name = 'misc', pre = False):
    for idx, marker in enumerate(markers):
        val = get_val_in_tag(marker, 'marker')
        if str(val) in list(event_names.keys()):
            event_name = str(event_names[str(val)])
        else:
            event_name = default_name
        if pre:
            new = ["event:%s"%(event_name), marker]
        else:
            new = [marker, "event:%s"%(event_name)]
        marker = "/".join(new)
        markers[idx] = marker
    return markers
"""

def add_stim_misc(markers, 
            stim = [str(val) for val in range(1, 200)],
            pre = False):
    for idx, marker in enumerate(markers):
        val = get_val_in_tag(marker, 'marker')
        if val in stim:
            new_tag = "stim"
        else:
            new_tag = "misc"
        if pre:
            new = [new_tag, marker]
        else:
            new = [marker, new_tag]
        marker = "/".join(new)
        markers[idx] = marker
    return markers

def add_tnt(markers, 
            target = [str(val) for val in range(101, 200)],
            nontarget = [str(val) for val in range(1,100)],
            pre = False):
    for idx, marker in enumerate(markers):
        val = get_val_in_tag(marker, 'marker')
        if val in target:
            new_tag = "target"
        elif val in nontarget:
            new_tag = "nontarget"
        else:
            new_tag = "misc"
        if pre:
            new = [new_tag, marker]
        else:
            new = [marker, new_tag]
        marker = "/".join(new)
        markers[idx] = marker
    return markers

def split_trials(markers,
                 trial = [str(val) for val in range(201, 300)],
                 init_trial_num = 1,
                 pre = False):
    
    trial_num = init_trial_num - 1
    for idx, marker in enumerate(markers):
        val = get_val_in_tag(marker, 'marker')
        if val in trial:
            trial_num += 1
        if pre:
            new = ["trial:%s"%str(trial_num), marker]
        else:
            new = [marker, "trial:%s"%str(trial_num)]
        marker = "/".join(new)
        markers[idx] = marker
        
    return markers
    
def add_tag(markers, tag, pre = False):
    for idx, marker in enumerate(markers):
        if pre:
            new = [tag, marker]
        else:
            new = [marker, tag]
        marker = "/".join(new)
        markers[idx] = marker
    return markers