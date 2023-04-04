import os
from queue import Queue
import cv2

# queue max_length = 10, index start from

SAVE_DIRECTORY = './control/tempFile/'


def add_img(src_img, queue, index):
    # print(index)
    tempQueue = Queue(maxsize=10)
    tempQueue = queue

    # define save name
    if tempQueue.qsize() == 0:
        saveIndex = 0
    else:
        match = tempQueue.queue[tempQueue.qsize()-1]
        saveIndex = int(match) + 1

    # when the cursor is on the newest one
    if index == 0:
        # if length < 10, add one item into it
        # 当没存满的时候，保存图片，然后将图片的saveIndex存到queue中
        if tempQueue.qsize() < 9:
            saveName = SAVE_DIRECTORY + 'temp_' + str(saveIndex) + '.png'
            cv2.imwrite(saveName, src_img)
            tempQueue.put(str(saveIndex))
            index = 0
        elif tempQueue.qsize() == 9:
            #         remove item
            deleteIndex = tempQueue.get()
            print("deleteindex", deleteIndex)
            deletePath = SAVE_DIRECTORY + 'temp_' + str(deleteIndex) + '.png'
            os.remove(deletePath)

            #       add item
            saveName = SAVE_DIRECTORY + 'temp_' + str(saveIndex) + '.png'
            cv2.imwrite(saveName, src_img)
            tempQueue.put(str(saveIndex))
            index = 0
    #         when the cursor is not on the newest one (have undo operations)
    elif index > 0:
        print("yeah!")
        newQueue = Queue(maxsize=10)
        transfer_num = tempQueue.qsize() - index
        while tempQueue.empty() == 0:
            # the first several content should be trasnfer into a new queue
            if transfer_num > 0:
                transfer_num -= 1;
                temp = tempQueue.get()
                newQueue.put(temp)
                print("transfer")
            #     the rest should delete
            else:
                deletePath = SAVE_DIRECTORY + 'temp_' + str(tempQueue.get()) + '.png'
                os.remove(deletePath)

        # save image
        if newQueue.qsize() == 0:
            saveIndex = 0
        else:
            match = newQueue.queue[newQueue.qsize() - 1]
            saveIndex = int(match) + 1

        print("saveIndex:", saveIndex)

        saveName = SAVE_DIRECTORY + 'temp_' + str(saveIndex) + '.png'
        cv2.imwrite(saveName, src_img)
        newQueue.put(str(saveIndex))

        index = 0
        tempQueue = newQueue
    print("size&index:", tempQueue.qsize(), index)
    return tempQueue, index

# 在redo中，index应该要小于queue的长度
def redo(queue, index):
    tempQueue = Queue(maxsize=10)
    tempQueue = queue
    index -= 1

    contentIndex = tempQueue.queue[tempQueue.qsize() - index - 1]
    contentName = SAVE_DIRECTORY + 'temp_' + str(contentIndex) + '.png'

    src_img = cv2.imread(contentName, cv2.IMREAD_COLOR)

    print("redo:", index)
    print("contentIndex:", contentIndex)

    return src_img, index

# 在undo中 index应该要大于0
def undo(queue, index):
    tempQueue = Queue(maxsize=10)
    tempQueue = queue
    index += 1

    contentIndex = tempQueue.queue[tempQueue.qsize() - index - 1]
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