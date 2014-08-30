"""
Set list of gauges used in in paper and where to find the observations and
simulation results.  Used in other scripts when looping over all gauges.
"""

def set_gauges():
    gaugenos = [1107, 1116, 1118, 1119, 1120, 1121, 1122, 1123, 1125, 1126]

    HAIdirs = {}
    HAIdirs[1107] = 'HAI1107_Hon_Harbor'
    HAIdirs[1116] = 'HAI1116_Kalohi_Channel'
    HAIdirs[1118] = 'HAI1118_Hawea_point'
    HAIdirs[1119] = 'HAI1119_Auau_channel'
    HAIdirs[1120] = 'HAI1120_Lahaina'
    HAIdirs[1121] = 'HAI1121_Alalakeiki_channel'
    HAIdirs[1122] = 'HAI1122_Maalaea_bay'
    HAIdirs[1123] = 'HAI1123_Kahului_harbor'
    HAIdirs[1125] = 'HAI1125_Hilo'
    HAIdirs[1126] = 'HAI1126_Hilo'
    
    rundirs = {}
    rundirs[1107] = 'HAI1107'
    rundirs[1116] = 'HAI1116-18-19-20-21-22'
    rundirs[1118] = 'HAI1116-18-19-20-21-22'
    rundirs[1119] = 'HAI1116-18-19-20-21-22'
    rundirs[1120] = 'HAI1116-18-19-20-21-22'
    rundirs[1121] = 'HAI1116-18-19-20-21-22'
    rundirs[1122] = 'HAI1116-18-19-20-21-22'
    rundirs[1123] = 'HAI1123'
    rundirs[1125] = 'HAI1125-26'
    rundirs[1126] = 'HAI1125-26'

    return gaugenos, HAIdirs, rundirs
