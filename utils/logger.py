import time
def logger(info, type='INFO'):
    print('[{}]{}: {}'.format(time.strftime("%Y-%m-%d %H:%M:%S"),type, info))

if __name__ == '__main__':
    logger('qweqwe')