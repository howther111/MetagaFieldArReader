### マーカーIDと、動画を重ねて表示する
import math

import cv2
from cv2 import aruco
import time


class markerPoint:
    corners = []
    id = []


class markerInfo:
    id = 999
    x_zahyo = 0
    y_zahyo = 0


class imgToBoard:
    def __init__(self, ret_porn_dict={}, window_baisu=1,
                 hanten_flg=False, cap=cv2.VideoCapture(0),
                 x_cell_num=9, y_cell_num=6, dict_aruco=aruco.DICT_4X4_50,
                 camera_on=True
                 ) -> None:
        self.ret_porn_dict = ret_porn_dict
        self.dict_aruco = aruco.Dictionary_get(dict_aruco)
        self.parameters = aruco.DetectorParameters_create()
        self.window_baisu = window_baisu
        self.hanten_flg = hanten_flg
        self.camera_on = camera_on
        # ワークブックの認証
        #wb = gspread.service_account(filename=account_json)
        #self.sp_sheet = wb.open_by_url(spread_sheet_url)
        #self.ar_sheet = self.sp_sheet.worksheet(ar_sheet_name)
        # 四隅のコーナーの位置を記録
        self.x_cell_num = x_cell_num
        self.y_cell_num = y_cell_num
        self.left_up_corner_x = 0.0
        self.left_up_corner_y = 0.0
        self.left_up_corner_id = 0
        self.right_up_corner_x = 100.0
        self.right_up_corner_y = 0.0
        self.right_up_corner_id = 1
        self.left_down_corner_x = 0.0
        self.left_down_corner_y = 100.0
        self.left_down_corner_id = 2
        self.right_down_corner_x = 100.0
        self.right_down_corner_y = 100.0
        self.right_down_corner_id = 3
        self.map_width = 100.0
        self.map_height = 100.0
        self.cap = cap

    def output_to_csv(self, ret_porn_dict={}):
        try:
            self.ret_porn_dict = ret_porn_dict
            ret, frame = self.cap.read()

            if self.hanten_flg:
                frame = cv2.rotate(frame, cv2.ROTATE_180)

            # image画像から大きさ情報を取得する。(image_colorは使用しないです。)
            image_hight, image_width, image_color = frame.shape

            # windowを名前付きで作成: nameは任意のstring; WINDOW_NORMALなら次のサイズ調整が可能 AUTO
            if self.camera_on:
                cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

            # image画像を2倍にする。
            cv2.resizeWindow('frame', image_width * self.window_baisu, image_hight * self.window_baisu)

            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.dict_aruco, parameters=self.parameters)
            points = []
            idcount = 0

            points = []
            for i in range(len(ids)):
                point = markerPoint()
                point.corners = corners[i]
                point.id = ids[i]
                points.append(point)

            for point in points:
                # print(point.corners[0])
                center_x = (point.corners[0][0][0] + point.corners[0][1][0]
                            + point.corners[0][2][0] + point.corners[0][3][0]) / 4
                center_y = (point.corners[0][0][1] + point.corners[0][1][1]
                            + point.corners[0][2][1] + point.corners[0][3][1]) / 4
                print("id = " + str(point.id[0]))
                print("center_x = " + str(center_x))
                print("center_y = " + str(center_y))
                if point.id[0] == self.left_up_corner_id:
                    self.left_up_corner_x = center_x
                    self.left_up_corner_y = center_y
                elif point.id[0] == self.right_up_corner_id:
                    self.right_up_corner_x = center_x
                    self.right_up_corner_y = center_y
                elif point.id[0] == self.left_down_corner_id:
                    self.left_down_corner_x = center_x
                    self.left_down_corner_y = center_y
                elif point.id[0] == self.right_down_corner_id:
                    self.right_down_corner_x = center_x
                    self.right_down_corner_y = center_y
                else:
                    x_left = (self.left_up_corner_x + self.left_down_corner_x) / 2
                    x_cell = self.map_width / self.x_cell_num
                    x_zahyo = math.ceil((center_x - x_left) / x_cell)
                    if x_zahyo < 1 or x_zahyo > self.x_cell_num:
                        x_zahyo = 0


                    num2alpha = lambda c: chr(c + 64)
                    y_up = (self.left_up_corner_y + self.right_up_corner_y) / 2
                    y_cell = self.map_height / self.y_cell_num
                    y_zahyo = math.ceil((center_y - y_up) / y_cell)
                    if y_zahyo < 1 or y_zahyo > self.y_cell_num:
                        y_zahyo = 0

                    print("zahyo = " + str(x_zahyo) + "-" + num2alpha(y_zahyo))

                    ret_porn = markerInfo()
                    ret_porn.id = point.id[0]
                    ret_porn.x_zahyo = x_zahyo
                    ret_porn.y_zahyo = y_zahyo
                    self.ret_porn_dict[ret_porn.id] = ret_porn

            self.map_width = ((self.right_up_corner_x - self.left_up_corner_x)
                              + (self.right_down_corner_x - self.left_down_corner_x)) / 2
            self.map_height = ((self.right_down_corner_y - self.right_up_corner_y)
                               + (self.left_down_corner_y - self.left_up_corner_y)) / 2
            print("map_width = " + str(self.map_width))
            print("map_height = " + str(self.map_height))

            # 無ければ追加、あれば移動（削除はしない）
            # print(corners)
            # print(ids)

            frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
            if self.camera_on:
                cv2.imshow('frame', frame_markers)
            time.sleep(1)
            return self.ret_porn_dict

        except KeyboardInterrupt:
            cv2.destroyWindow('frame')
            self.cap.release()
            return self.ret_porn_dict