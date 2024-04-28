def get_delta(toponym_dict):
    envelope = toponym_dict['boundedBy']['Envelope']
    lower = list(map(float, envelope['lowerCorner'].split()))
    upper = list(map(float, envelope['upperCorner'].split()))
    return upper[0] - lower[0], upper[1] - lower[1]
