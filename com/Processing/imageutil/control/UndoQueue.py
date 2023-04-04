import os
from queue import Queue
import cv2

# queue max_length = 10, index start from

SAVE_DIRECTORY = './control/tempFile/'


def add_img(src_img, queue, index):
    tempQueue = Queue(maxsize=10)
    tempQueue = queue

    # define save name
    # 通过re获得末位名称（index）
    if tempQueue.qsize() == 0:
        saveIndex = 0
    else:
        match = tempQueue.queue[tempQueue.qsize()]
        saveIndex = match + 1

    # 如果就是从queue的末尾开始加内容
    if tempQueue.qsize() == index:
        # if length < 10, add one item into it
        # 当没存满的时候，保存图片，然后将图片的saveIndex存到queue中
        if tempQueue.qsize() < 9:
            saveName = SAVE_DIRECTORY + 'temp_' + str(saveIndex) + '.png'
            cv2.imwrite(saveName, src_img)
            tempQueue.put(str(saveIndex))
            index += 1
        # add a new item before remove one
        if tempQueue.qsize() == 9:
            #         remove item
            deleteIndex = tempQueue.get()
            deletePath = SAVE_DIRECTORY + 'temp_' + str(deleteIndex) + '.png'
            os.remove(deletePath)

            #       add item
            saveName = SAVE_DIRECTORY + 'temp_' + str(saveIndex) + '.png'
            cv2.imwrite(saveName, src_img)
            tempQueue.put(str(saveIndex))
            index = 9
    # 如果之前undo过，从中间开始加内容
    elif tempQueue.qsize() > index:
# 先把多出来的几条东西删掉
        newQueue = Queue(maxsize=10)
        while tempQueue.empty() == 0:
            if index > 0:
                temp = tempQueue.get()
                newQueue.put(temp)
            else:
                deletePath = SAVE_DIRECTORY + 'temp_' + str(tempQueue.get()) + '.png'
                os.remove(deletePath)
            index -= 1

        index = newQueue.qsize()
        tempQueue = newQueue

    return tempQueue, index

# 在redo中，index应该要小于queue的长度
def redo(queue, index):
    tempQueue = Queue(maxsize=10)
    tempQueue = queue
    index += 1

    contentIndex = tempQueue.queue[index]
    contentName = SAVE_DIRECTORY + 'temp_' + str(contentIndex) + '.png'

    src_img = cv2.imread(contentName, cv2.IMREAD_COLOR)

    return src_img, index

# 在undo中 index应该要大于0
def undo(queue, index):
    tempQueue = Queue(maxsize=10)
    tempQueue = queue
    index -= 1

    contentIndex = tempQueue.queue[index]
    contentName = SAVE_DIRECTORY + 'temp_' + str(contentIndex) + '.png'

    src_img = cv2.imread(contentName, cv2.IMREAD_COLOR)

    return src_img, index

def clear():
    files = os.listdir(SAVE_DIRECTORY)
    for img in files:
        os.remove(SAVE_DIRECTORY + img)

    newQueue = Queue(maxsize=10)
    index = 0
    return newQueue, index