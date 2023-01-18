# This is a sample Python script.
import cv2
import csv

from arreadtest12 import imgToBoard
from multiprocessing import Process
#Qキーで終了

#X方向のマス数最大値
x_cell_num_max = 9

#Y方向のマス数最大値
y_cell_num_max = 6

#カメラ画像を表示するか否か
camera_on = True
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def update_porn_list():
    porn_dictionary = imgToBoard(x_cell_num=x_cell_num_max, y_cell_num=y_cell_num_max, camera_on=camera_on)
    ret_porn_dict = {}

    try:
        while True:
            ret_porn_dict = porn_dictionary.output_to_csv(ret_porn_dict=ret_porn_dict)

            if ret_porn_dict != {}:
                with open('./porn_list.csv', 'w') as csvfile:
                    writer = csv.writer(csvfile, lineterminator='\n')

                    for key in ret_porn_dict.keys():
                        writer.writerow([key, ret_porn_dict[key].x_zahyo, ret_porn_dict[key].y_zahyo])

                #コマの情報を記述

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except:
        raise Exception


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        p1 = Process(target=update_porn_list)
        p1.start()

    except:
        raise Exception


