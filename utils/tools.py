from datetime import datetime as dt


def get_time() -> str:
    time = dt.now().strftime('%H:%M:%S')
    return '"{}"'.format(time)


def get_date() -> str:
    date = dt.now().strftime('%Y-%m-%d')
    return '"{}"'.format(date)


def get_timestamp():
    return "{}_{}".format(get_date(), get_time()).replace(":", "_").replace("-", "_").replace('"', '')


def get_timestamp_milli():
    return dt.datetime.now().strftime('%H:%M:%S.%f')


def unit_system(_format=b'cm') -> float:
    if _format == b'in':
        return 0.393701
    else:
        return 1
#
#
# def distance_screen_ref(distance_ref):
#     y = b'"%d"' % distance_ref
#     if distance_ref > 0 and distance_ref <= 50:
#         ser3.write(t8 + y + eof)
#         initial_distance = distance_ref * unit
#         print('Initial distance:', initial_distance)
#         return initial_distance