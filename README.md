# tag-mne
python library for handling tag of mne Epochs object

# Install
```
# using pip
pip install tag-mne 
```

# Usage
## general
```
import tag_mne as tm

events, event_id = mne.events_from_annotations(mne_raw_object_run1)

# convert mne events and event_id to samples and markers
# markers[i] is string tag corresponding to samples[i]
samples, markers = tm.markers_from_events(events, event_id)

# by doing this, you can tag name of events to each marker
event_names = {'event_1': ['1', '101'], 'event_2': ['2', '102']}
markers = tm.add_event_names(markers, event_names)

# add tag for whole markers
# in this case, 'run:1' tag will be added
markers = tm.add_tag(markers, "run:1")

# do this if you want to tag trial name or number
# for argument 'trial', specify the markers indicate new trials
markers = tm.split_trials(markers, trial = [str(val) for val in range(201, 300)])

# add target or nontarget tag by specifying the markers for target and nontarget events
markers = tm.add_tnt(markers, target = [str(val) for val in range(101, 200)], nontarget = [str(val) for val in range(1, 100)])

# you can remove events which has specific tag
# in this case, it will remove 'misc' events which is irrelevant to analysis
samples, markers = tm.remove(samples, markers, "misc")

# finally, convert to mne events and event_id
events, event_id = tm.events_from_markers(samples, makers)

# create epochs
epochs = mne.Epochs(raw = mne_raw_object_run1,
                    events = events,
                    event_id = event_id)

epochs_list = []
epochs_list.append(epochs)

# if you have raw object for different runs or recordings...
# do the same as above
events, event_id = mne.events_from_annotations(mne_raw_object_run2)

samples, markers = tm.markers_from_events(events, event_id)

event_names = {'event_1': ['1', '101'], 'event_2': ['2', '102']}
markers = tm.add_event_names(markers, event_names)

# for this raw, specify 'run:2'
markers = tm.add_tag(markers, "run:2")

markers = tm.split_trials(markers, trial = [str(val) for val in range(201, 300)])
markers = tm.add_tnt(markers, target = [str(val) for val in range(101, 200)], nontarget = [str(val) for val in range(1, 100)])
samples, markers = tm.remove(samples, markers, "misc")
events, event_id = tm.events_from_markers(samples, makers)

# create epochs object for run 2 as well
epochs = mne.Epochs(raw = mne_raw_object_run2,
                    events = events,
                    event_id = event_id)

epochs_list.append(epochs)

# epochs_list has two epochs objects correspond to run1 and run2
# you can concatenate these epochs with giving unique event_id for epoch for each run
epochs = tm.concatenate_epochs(epochs_list)

# you can access epoch data with tag
# e.g.,
epochs['run:1/trial:1/target']

# see documentation of __getitem__() methods of mne.Epochs object, how to access data with tag

```

## For classification
```
# you can get labels for classification
# X: mne.Epochs object
# Y: Y[i] is the label corresponds to X[i], 1: nontarget, 10:target

X, Y = tm.get_binary_epochs(epochs)

## Get values of tag of epochs object
# e.g., with the following code, you can get list of runs in epochs
values = tm.get_values_list(epochs, "run")
```