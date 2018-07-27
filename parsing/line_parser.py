def special_data_from_raw_line(line, configuration):
    """
    Uses the provided array of characters to extract all information we can and
    return that
    Input Type: array of data
    Output Type: json like object to be written
    """
    raw_line = ''
    raw_sections = []
    last_x = 0
    current_section = ''
    count = 0
    x_span = line[len(line)-1]['x'] - line[0]['x']
    multiplier = x_span / configuration['trained_width'] # This is the x_span the algorithm was trained on
    formatted_line = {
        'transaction_date': None,
        'posting_date': None,
        'description': None,
        'location': None,
        'reference_number': None,
        'account_number': None,
        'amount': None
    }
    for i in configuration['fields'].keys():
        right_x = configuration['fields'][i][0]
        left_x = configuration['fields'][i][1]
        field_data = ''
        space_threshold = 20 * multiplier
        last_x = -100
        for j in line:
            if j['x'] >= right_x and j['x'] < left_x:
                if (j['x'] - last_x) >= space_threshold and (j['x'] - last_x) < space_threshold * 2:
                    field_data += ' ' # add in a space
                field_data += j['contents']
                last_x = j['x']
        if i == 'amount':
            if len(field_data) >= 3 and not field_data[len(field_data)-4] == '.':
                field_data = field_data[:len(field_data)-3] + '.' + field_data[len(field_data)-2:]
        formatted_line[i] = field_data

    for i in configuration['overlapping']:
        max_gap = 0
        idx_split = -1
        right_x = i['bounding'][0]
        left_x = i['bounding'][1]
        space_threshold = 20 * multiplier
        last_x = -100
        for idx, j in enumerate(line):
            if j['x'] >= right_x and j['x'] < left_x:
                if last_x > 0 and (j['x'] - last_x) >= max_gap and (j['x'] - last_x) > space_threshold:
                    max_gap = (j['x'] - last_x)
                    idx_split = idx
            last_x = j['x']
        line_chunks = [line[:idx_split], line[idx_split:]]
        if idx_split <= 10:
            line_chunks = [line, []]
        # Process chunk 0
        last_x = -100
        field_data = ''
        for j in line_chunks[0]:
            if j['x'] >= right_x and j['x'] < left_x:
                if (j['x'] - last_x) >= space_threshold and (j['x'] - last_x) < space_threshold * 2:
                    field_data += ' ' # add in a space
                field_data += j['contents']
            last_x = j['x']
        if i['fields'][0] == 'amount':
            if len(field_data) >= 3 and not field_data[len(field_data)-4] == '.':
                field_data = field_data[:len(field_data)-3] + '.' + field_data[len(field_data)-2:]
        formatted_line[i['fields'][0]] = field_data
        # Process chunk 0
        last_x = -100
        field_data = ''
        for j in line_chunks[1]:
            if j['x'] >= right_x and j['x'] < left_x:
                if (j['x'] - last_x) >= space_threshold and (j['x'] - last_x) < space_threshold * 2:
                    field_data += ' ' # add in a space
                field_data += j['contents']
            last_x = j['x']
        if i['fields'][1] == 'amount':
            if len(field_data) >= 3 and not field_data[len(field_data)-4] == '.':
                field_data = field_data[:len(field_data)-3] + '.' + field_data[len(field_data)-2:]
        formatted_line[i['fields'][1]] = field_data

    if is_line_accurate(formatted_line):
        return formatted_line
    else:
        return {'description': raw_line} # Provide the info but not nicely put together

def is_line_accurate(formatted_line):
    try:
        int(formatted_line['transaction_date'][:2]) # Date should always begin with two numerals
        return True
    except:
        return False
