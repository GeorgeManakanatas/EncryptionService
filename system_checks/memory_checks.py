# -*- coding: utf-8 -*-
'''
functions for checking system memory
'''
import os
import sys
import platform
import psutil


def check_memory_requirement(data_file):
    '''
    Determines if there is enough available ram on the system to proceed.
    If there is insuficient memory execution stops alse warnings are printed

    Arguments
        data_file(str) : The path to the file

    Returns
        nothing
    '''
    # Get the size of the file
    file_size = check_the_file_size(data_file)
    # check memory depnding on system type
    if get_the_os_type() == 'windows':
        free_mem, upper_limit = get_memory_windows()
    else:
        free_mem, upper_limit = get_memory_linux()
    # if data size less than free memory ok
    if file_size < free_mem:
        # do nothing
        print('the data is a fraction of the free memory')
    elif file_size > free_mem and file_size < upper_limit:
        # still go on but give warning, print for now popup window later
        print('the data is a significant fraction of the available memory the \
              pc may slow down!')
    elif file_size > upper_limit:
        # do not move on
        print('the data is too big try to make more memory available')
        print('data size: ', file_size, ' and memory limit: ', upper_limit)
        sys.exit(0)



def get_the_os_type():
    '''
    Detect the type of operating system

    Arguments
        none

    Returns
        String with the operating system detected
    '''
    operating_system = platform.system()
    # print(platform.version())
    # print(platform.platform())
    return operating_system.lower()


def check_the_file_size(data_file):
    '''
    Check the size of a file

    Arguments
        data_file(str) : The path to the file

    Returns
        The file size in kB as integer
    '''
    # information on the file
    file_stat_info = os.stat(data_file)
    # returning the file size in kB
    return file_stat_info.st_size / 1024


def get_memory_windows():
    '''
    Check the available memory for windows

    Arguments
        none

    Returns
        System free memory in kB as integer
        System available memory in kB as integer
    '''
    memory_stats = {}
    # building list of tuples from file info, all values in kB
    memory_stats['total'] = int(psutil.virtual_memory().total)
    memory_stats['available'] = int(psutil.virtual_memory().available)
    memory_stats['used'] = int(psutil.virtual_memory().used)
    memory_stats['free'] = int(psutil.virtual_memory().free)
    # free memory and upper_limit
    free_mem = memory_stats.get('free') / 1024
    upper_limit = memory_stats.get('available') / 1024
    return free_mem, upper_limit


def get_memory_linux():
    '''
    Check the available memory for Linux

    Arguments
        none

    Returns
        System free memory in kB as integer
        System available memory in kB as integer
    '''
    # linux specific solution for memory info
    with open('/proc/meminfo', 'r') as system_memory:
        meminfo_lines = system_memory.readlines()
    # initialise memory stats
    memory_stats = {}
    # building list of tuples from file info, all values in kB
    memory_stats['tot'] = int(meminfo_lines[0].split()[1])
    memory_stats['free'] = int(meminfo_lines[1].split()[1])
    memory_stats['buff'] = int(meminfo_lines[2].split()[1])
    memory_stats['cached'] = int(meminfo_lines[3].split()[1])
    memory_stats['shared'] = int(meminfo_lines[20].split()[1])
    # Get free value from tuple ( 'free', ... ) in memory_stats list of tuples
    free_mem = memory_stats.get('free')
    # Same for buff and cached
    buff_mem = memory_stats.get('buff')
    cached_mem = memory_stats.get('cached')
    # calculating upper limit set to 80% of max available memory
    # (configurable in the future)
    max_memory = (free_mem + buff_mem + cached_mem)
    upper_limit = max_memory / 1024
    return free_mem, upper_limit
