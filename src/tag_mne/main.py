import numpy as np
from .utils import get_val_in_tag

def markers_from_events(events, event_id):
    from .utils import get_swap_dict
    event_id_swap = get_swap_dict(event_id)

    samples = np.array(events)[:, 0]
    
    markers = ["marker:%s"%str(event_id_swap[val]) for val in np.array(events)[:, 2]]
    
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

def modify_events(events,
                  event_id,
                  target = [val for val in range(101, 201)],
                  nontarget = [val for val in range(1, 101)],
                  event_names = None):
    
    samples, markers = markers_from_events(events, event_id)
    
    markers = add_event_names(markers, event_names)
    
    markers = add_tnt(markers, target, nontarget)

    events, event_id = events_from_markers(samples, markers)
    
    return events, event_id