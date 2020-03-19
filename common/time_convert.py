# coding:utf-8


def time_str2sec(t):
    h, m, s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def time_sec2str(sec):
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


if __name__ == '__main__':
    start_time = time_str2sec("21:35:00")
    # print(start_time)
    time_interval = time_str2sec("00:05:00")
    # print(time_interval)
    print(time_sec2str(start_time+time_interval))
