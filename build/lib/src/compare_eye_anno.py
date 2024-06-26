import matplotlib.pyplot as plt
import csv
import os
import  sys
import json
from shapely.geometry import Point, Polygon
import pandas as pd
import numpy as np
from matplotlib import patches


################################################
# remove string does not contain sym from list
################################################
def remove_from_list(alist, sym):
    for item in alist:
        if sym not in item:
            alist.remove(item)

################################################
# include string contain sym from list
################################################
def include_to_list(alist, sym):
    temp = []
    for item in alist:
        if sym  in item:
            temp.append(item)
    return temp


################################################
# convert a list of list to a list of tuple
################################################
def convert_to_tuple_list(alist):
    temp = []
    for item in alist:

        temp.append(tuple(item))
    return temp

################################################
# convert rectangle(2 points) to polygon (4points)
################################################
def convert_to_box(points):
    temp = []
    t1 = points[0]
    t2 = points[1]
    if t1[0] < t2[0]:
        x1 = t1[0]
        x2 = t2[0]
    else:
        x2 = t1[0]
        x1 = t2[0]
    if t1[1] < t2[1]:
        y1 = t1[1]
        y2 = t2[1]
    else:
        y2 = t1[1]
        y1 = t2[1]

    temp.append((x1, y1))
    temp.append((x2, y1))
    temp.append((x2, y2))
    temp.append((x1, y2))


    return temp

count = 0

#prevent args out of bounds error
try: 
    #interval is how often we cut the frames
    interval = sys.argv[1] 
    interval = float(interval)
    interval = int(interval)
    # datafile is the path of eye tracking file that has 2d hitting points
    datafile = sys.argv[2]
    # folder path that contains image and json of annotation
    annot_dir_curr = sys.argv[3]
    # folder to generate pics
    pics_folder_path = sys.argv[3]

    # we pause the video from start1 to end1 and start2 to end2
    # if you only pause the video once, just set start2 and end2 to 0
    df = {'start1':1, 'end1':11, 'start2':33.9, 'end2':34.9}

    if not os.path.exists(pics_folder_path + '_results'):
        os.makedirs(pics_folder_path + '_results')
    arr = os.listdir()


    # read timestamp and hitting point csv file
    time_eye_dict = {}
    f = open(datafile, 'r', encoding="utf-8")
    reader = csv.reader(f)
    start_timestamp = 0
    for row in reader:
        if start_timestamp ==0:
            start_timestamp = int(row[0])
        time_eye_dict[int(row[0])] = [float(row[1]), float(row[2])]

    poly_file_names = os.listdir(annot_dir_curr)
    poly_json_file_names = include_to_list(poly_file_names, 'json')
    poly_json_file_names.sort()


    result_scene_dict = {'timestamp':[], 'image':[]}
    for key, value in time_eye_dict.items():
        hitting_point = Point(value[0], value[1])

        curr_img = 'image'
        curr_time = (key - start_timestamp) / interval
        curr_time = int(curr_time)
        num = ''


        ####### No Pause. Replace this block of code with this line:
        # num = str(curr_time).zfill(2)
        if curr_time <= df['start1']*2:
            num= str(curr_time).zfill(2)
        elif df['start1']*2 < curr_time < df['end1']*2:
            num= str(int(df['start1']*2)).zfill(2)
        elif df['end1']*2 <= curr_time <= df['start2']*2:
            num= str(int(curr_time - 2*(df['end1'] - df['start1']))).zfill(2)
        elif df['start2']*2 < curr_time < df['end2']*2:
            num = str(int(df['start2']*2- 2*(df['end1'] - df['start1']))).zfill(2)
        elif curr_time >= df['end2']*2 and df['end2'] != 0:
            num = str(int(curr_time - 2 * (df['end2'] - df['start2']) - 2*(df['end1'] - df['start1']))).zfill(2)
        elif curr_time >= df['end1']*2 and df['start2'] == 0:
            num = str(int(curr_time - 2*(df['end1'] - df['start1']))).zfill(2)
        ########


        result_scene_dict['timestamp'].append(key)
        result_scene_dict['image'].append(num)

        # prev = curr_img

        if os.path.exists(annot_dir_curr + '/' + curr_img+num + '.json'):
            curr_img += num
        else:
            curr_img = prev

        ##############  generating pics to check, delete it if you don't need
        flag_img = False
        if os.path.exists(pics_folder_path + '_results/'+curr_img+'.png') == False:

            flag_img = True
            plt.figure()
            im = plt.imread(annot_dir_curr + '/' + curr_img + '.jpg')
            fig, ax = plt.subplots(1)
            ax.imshow(im)
            plt.scatter([value[0]], [value[1]], s=1, color='g')
        #############

        with open(annot_dir_curr + '/' + curr_img + '.json') as img_f:
            d = json.load(img_f)
            for shape in d['shapes']:
                points = shape['points']
                points = convert_to_tuple_list(points)
                label = shape['label']
                if len(points) > 2:
                    poly = Polygon(points)
                else:
                    poly = Polygon(convert_to_box(points))
                if hitting_point.within(poly) == True:
                    flag = 'True'
                else:
                    flag = 'False'
                if label in result_scene_dict:
                    while len(result_scene_dict[label]) < (len(result_scene_dict['timestamp'])-1):
                        result_scene_dict[label].append('NA')
                    result_scene_dict[label].append(flag)
                else:
                    result_scene_dict[label] = ['NA']*(len(result_scene_dict['timestamp'])-1)
                    result_scene_dict[label].append(flag)

                #### generating pics to check, delete it if you don't need
                if flag_img ==True:

                    x, y = poly.exterior.coords.xy
                    draw_points = np.array([x, y], np.int32).T

                    polygon_shape = patches.Polygon(draw_points, linewidth=1, edgecolor='r', facecolor='none')
                    ax.add_patch(polygon_shape)
                ####

            prev = curr_img

        ######## generating pics to check, delete it if you don't need
        if flag_img ==True:

            plt.savefig(pics_folder_path + '_results/' +curr_img + '.png')
            plt.close(fig)
            plt.cla()
            plt.close('all')
            count += 1
        ########
    # print(result_scene_dict)
    curr_df = pd.DataFrame(result_scene_dict)
    curr_df.to_csv(datafile+'_result.csv', sep=',', encoding='utf-8')

except:
    print("loading")

