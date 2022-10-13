#!/usr/bin/env python3
import ast
import re
from collections import defaultdict
from datetime import datetime


def data_check(data):
    err_dict = {
        # "bus_id": 0,
        # "stop_id": 0,
        "stop_name": 0,
        # "next_stop": 0,
        "stop_type": 0,
        "a_time": 0
    }
    
    data_type_dict = {
        # "bus_id": 0,
        # "stop_id": 0,
        "stop_name": r'[A-Z]\w+(\s[A-Z]\w+)*\s(Road|Avenue|Boulevard|Street)$',
        # "next_stop": 0,
        "stop_type": '^[SOF]?$',
        "a_time": r'([0-1]\d|2[0-3])\:[0-5]\d$'
    }

    for dictionary in data:
        for key, value in dictionary.items():
            if key in ['bus_id', 'stop_id', 'next_stop']:
                pass
            elif not re.match(data_type_dict.get(key), value):
                err_dict[key] += 1

    print(f'Format: {sum(err_dict.values())} errors')
    for key, value in err_dict.items():
        print(f'{key}: {value}')


def count_lines_stops(data):
    lines_stops_dict = {}
    for dictionary in data:
        for v in dictionary.values():
            if v not in lines_stops_dict:
                lines_stops_dict[v] = 1
            else:
                lines_stops_dict[v] += 1
    return lines_stops_dict


def gather_stops(data):
    stops = defaultdict(set)
    id_stops = defaultdict(list)
    street_stops = defaultdict(set)
    for dictionary in data:
        street_stops[dictionary.get('stop_name')].add(dictionary.get('bus_id'))
        id_stops[dictionary.get('bus_id')].append(dictionary.get('stop_type'))
        if dictionary.get('stop_type') in ['', 0, '0']:
            stops[''].add(dictionary.get('stop_name'))
        else:
            stops[dictionary.get('stop_type')].add(dictionary.get('stop_name'))
    for k, v in id_stops.items():
        if v.count('S') != 1 or v.count('F') != 1:
            print(f'There is no start or end stop for the line: {k}.')
            exit()
    start_stops = sorted(stops.get('S'))
    transfer_stops = sorted([k for k, v in street_stops.items() if len(v) > 1])
    finish_stops = sorted(stops.get('F'))
    return transfer_stops
    # print(f'Start stops: {len(start_stops)} {start_stops}')
    # print(f'Transfer stops: {len(transfer_stops)} {transfer_stops}')
    # print(f'Finish stops: {len(finish_stops)} {finish_stops}')


def check_times(data):
    print('Arrival time test:')
    err_count = 0
    err_bus = 0
    init_time = datetime.strptime('00:00', '%H:%M')
    for dictionary in data:
        if dictionary.get('stop_type') == 'S':
            bus_id = dictionary.get('bus_id')
            init_time = datetime.strptime(dictionary.get('a_time'), '%H:%M')
            continue
        arrival_time = datetime.strptime(dictionary.get('a_time'), '%H:%M')
        if bus_id != err_bus and arrival_time < init_time:
            print(f'bus_id line {bus_id}: wrong time on station {dictionary.get("stop_name")}')
            err_count += 1
            err_bus = bus_id
        init_time = arrival_time
    if err_count == 0:
        print('OK')


def not_on_demand(data):
    print('On demand stops test:')
    transfer_stops = gather_stops(data)
    stop_list = []
    for dictionary in data:
        if dictionary.get('stop_name') in transfer_stops and dictionary.get('stop_type') == 'O':
            stop_list.append(dictionary.get('stop_name'))
    if stop_list:
        stop_list = sorted(set(stop_list))
        print(f'Wrong stop type: {stop_list}')
    else:
        print('OK')


dump = ast.literal_eval(input())
# gather_stops(dump)
# check_times(dump)
not_on_demand(dump)
# d = count_lines_stops(dump)
# for k, v in d.items():
#     print(f'bus_id: {k}, stops: {v}')
# data_check(dump)
