def get_swap_dict(d):
    return {v: k for k, v in d.items()}

def get_val_in_tag(tag, key):
    tag_list = list(tag.split('/'))
    for tag in tag_list:
        if key in tag:
            return tag.split(':')[1]