# -*- encoding: utf-8 -*-

import flask
from flask import request
import os
import time
import socket
import argparse
import base64
from PIL import Image
from io import BytesIO
import numpy as np

app = flask.Flask(__name__)
folder = ""
app.config['JSON_SORT_KEYS'] = False
global MATLAB_PATH
global MATLAB_SCRIPT_FOLDER
global MATLAB_FUNCTION


@app.route("/api/matlab_run_cmd", methods=['POST'])
def api_matlab_run_cmd():
    try:
        global MATLAB_PATH
        global MATLAB_SCRIPT_FOLDER
        global MATLAB_FUNCTION

        print('Parsing input ... ')
        
        img = request.data

        print("image data received!")

        decodeit = open('image.jpg', 'wb')
        conv_img = base64.b64decode((img))
        decodeit.write(conv_img)
        decodeit.close()

        print("sending response back:")
        ans = " Query image sucessfuly recieved! "

        # # MATLAB_FUNCTION : InLoc running matlab script, with query image
       
        # answer = os.popen( MATLAB_PATH +  ' -nodisplay -batch "cd(\'' + MATLAB_SCRIPT_FOLDER + '\');' + MATLAB_FUNCTION + '(' + 'query_img' + ')' + '"').read()
        # print('Sending InLoc result: ' + answer)
        # ans_dict = dict([("inloc_localization_result", answer)])
        # ans = flask.jsonify(ans_dict)

        return ans

    except Exception as err:
        print("ko:", err)

    return "ok"


def image_modify(image_name):
    # add here some image modifications if nedded
    # for example :

    # nparr = np.fromstring(imageString, np.uint8)
    # img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)

    # height, width, channels = image_name.shape
    # crop_img = image_name[100:(height-100)][1:width]

    image = Image.open(image_name)
    new_img = image.rotate(45)
    # image.show()

    return new_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Server for running Matlab script')
    parser.add_argument("--matlab_path",
                        required=True,
                        help="Path to the matlab.exe")
    parser.add_argument("--matlab_script_folder",
                        required=True,
                        help="Path to the folder containing the .m file")
    parser.add_argument("--matlab_function",
                        required=True,
                        help="Name of the Matlab function to run")

    args = parser.parse_args()
    global MATLAB_PATH
    MATLAB_PATH = args.matlab_path
    global MATLAB_SCRIPT
    MATLAB_SCRIPT_FOLDER = args.matlab_script_folder
    global MATLAB_FUNCTION
    MATLAB_FUNCTION = args.matlab_function

    IP = socket.gethostbyname(socket.gethostname())
    app.run(port=9099, host=IP)
