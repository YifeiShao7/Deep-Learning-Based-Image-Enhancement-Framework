# import os
#
# import cv2
#
# LIST_CAPACITY = 11
# PREFIX = "./control/tempFile/"
# SUFFIX = ".png"
#
# def addElement(undoList, src_img, index):
#     length = len.undoList
#     if length < LIST_CAPACITY:
#         fileName = "temp_" + (length+1)
#         # add the image to the folder
#         cv2.imwrite(PREFIX + fileName + SUFFIX, src_img, [cv2.IMWRITE_PNG_COMPRESSION,0])
#         undoList.append(fileName)
#     elif length == LIST_CAPACITY:
#         fileName = "temp_" + undoList[9][5:] + 1
#         os.remove(PREFIX + undoList[0] + ".png")
#         undoList = undoList[1:]
#         cv2.imwrite(PREFIX + fileName + SUFFIX, src_img, [cv2.IMWRITE_PNG_COMPRESSION,0])
#         undoList.append(fileName)
#     return len(undoList)
#
# # currentIndex should in range of 0-10
# def undo(undoList, currentIndex):
#     if currentIndex > 0:
#         targetImgName = undoList[currentIndex-1]
#         img = cv2.imread(PREFIX + targetImgName + SUFFIX)
#         return img, currentIndex-1
#
# def redo(undoList, currentIndex):
#     if currentIndex < 10 and len(undoList) >= currentIndex:
#         targetImgName = undoList[currentIndex]
#         img = cv2.imread(PREFIX + targetImgName + SUFFIX)
#         return img, currentIndex
#
# def changeBranch(undoList, currentIndex):
#
#
# def clear(undoList):
#     undoList = []
#     for filename in os.listdir(PREFIX):
#         file_path = os.path.join(PREFIX, filename)
#         try:
#             if os.path.isfile(file_path) or os.path.islink(file_path):
#                 os.remove(file_path)
#         except Exception as e:
#             print(e)
#     return undoList
#
# def main():
#     print("finish")
#
# if __name__ == '__main__':
#     main()