# BA PROJECT: clinet_server_communication for ARI ROS.

Send image data retrieved from ros topics to a server and receive a resulting answear:

# Server

Server is located in matlap_serve_img.py

Run matlab server code: 
python matlab_server-img.py  --matlab_path "Path to the matlab" --matlab_script_folder "Path to the folder containing the .m file"  --matlab_function "Name of the Matlab function to run

Change matlab path, script folder and matlab file.

Run test example in python from ROS workspace: rosrun ros_server_communication test_communication.py

# Client

Client is located in ros_server_communication/src/communication.py

1. Install Ros and ARI software 
  http://wiki.ros.org/Robots/ARI
2. Start ARI simulation 
  http://wiki.ros.org/Robots/ARI/Tutorials
3. Strat ARI communication node
  rosrun ros-server-communication communication.py

Change the URL in the in test_communication.py file to the IP running on your server.

