import os
from queue import Queue
import cv2

# queue max_length = 10, index start from
SAVE_DIRECTORY = './tempFile/'


"""
add an image to the queue
if the index value is 0, which means the newest image is showed;
else if the index value is larger than 0, which means undo operation has been used
if the queue is full, add a new image after remove the earliest image put into the queue
:param src_img: image need to push into the queue
:param queue: the queue that store the name of the temp files
:param index: a pointer points to the showed image in the queue
:return the updated queue and index
"""
def add_img(src_img, queue, index):
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
        # if length < 10, add one item into it, update the save index
        if tempQueue.qsize() < 9:
            saveName = SAVE_DIRECTORY + 'temp_' + str(saveIndex) + '.png'
            cv2.imwrite(saveName, src_img)
            tempQueue.put(str(saveIndex))
            index = 0
        #     when the queue is full, remove the earliest image stored in the folder
        elif tempQueue.qsize() == 9:
            #         remove item
            deleteIndex = tempQueue.get()
            print("deleteindex", deleteIndex)
            deletePath = SAVE_DIRECTORY + 'temp_' + str(deleteIndex) + '.png'
            os.remove(deletePath)

            #       add the new one after removal
            saveName = SAVE_DIRECTORY + 'temp_' + str(saveIndex) + '.png'
            cv2.imwrite(saveName, src_img)
            tempQueue.put(str(saveIndex))
            index = 0
    #         when the cursor is not on the newest one (have undo operations)
    elif index > 0:
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

        saveName = SAVE_DIRECTORY + 'temp_' + str(saveIndex) + '.png'
        cv2.imwrite(saveName, src_img)
        newQueue.put(str(saveIndex))

        index = 0
        tempQueue = newQueue
    return tempQueue, index

"""
redo operation, pointer points to the backward one
:param queue: the queue stored all the temp file names
:param index: index value - 1, 
:return the image in the next 
"""
# in redo methods, the index value is less than the length of the queue
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

"""
undo operation, pointer points to the upward one
:param queue: the queue stored all the temp file names
:param index: index value + 1, 
:return the image in the previous
"""
# in undo methods, the index value is greater than or equal to 0
def undo(queue, index):
    tempQueue = Queue(maxsize=10)
    tempQueue = queue
    index += 1

    contentIndex = tempQueue.queue[tempQueue.qsize() - index - 1]
    contentName = SAVE_DIRECTORY + 'temp_' + str(contentIndex) + '.png'

    src_img = cv2.imread(contentName, cv2.IMREAD_COLOR)

    return src_img, index

"""
clear operation, clean up the tempfile folder and the queue
:return an empty queue with index value 0
"""
def clear():
    if os.path.exists(SAVE_DIRECTORY) == False:
        os.makedirs(SAVE_DIRECTORY)
    files = os.listdir(SAVE_DIRECTORY)
    for img in files:
        os.remove(SAVE_DIRECTORY + img)

    newQueue = Queue(maxsize=10)
    index = 0
    return newQueue, index