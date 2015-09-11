# my_message_package
debug package for https://github.com/ros/genpy/issues/37

###Steps:

1. Compile this package using catkin_make in your workspace

2. Use ```> roslaunch my_message_package generate_bag.launch ``` to generate a sample ROS bag file. This bag will be put in the "my_message_package" package folder. You can use ```ctrl-c``` to kill it after recording for about 10 seconds.

3. Subsititute the modified version **my_message_package/src/dynamic.modified.py** to **/opt/ros/indigo/lib/python2.7/dist-packages/genpy/dynamic.py**. A backup of the original file **dynamic.py** is recommended. The modified version of **dynamic.py** will print some useful information to track the bug, eliminate deleting the generated tmp files and generate a **raw.py**.

4. Use rosbag filter to trigger the bug:
``` bash
> roscd my_message_package
> rosbag filter raw.bag filtered.bag 'topic=="/message_generator/myodom"'
```

My output is:
```
> rosbag filter raw.bag filtered.bag 'topic=="/message_generator/myodom"'
filtered.bag                                                                       0%   0.0 KB /   1.9 MB --:-- ETA

core_type: rosgraph_msgs/Log file_path:/tmp/genpy_UYzEnW/tmpSYt4d4.py

core_type: nav_msgs/Odometry file_path:/tmp/genpy_l6Wx2_/tmpXx6Ivk.py

core_type: my_message_package/Odometry file_path:/tmp/genpy_Mc0Jkf/tmps_UQuR.py

Traceback (most recent call last):
  File "/opt/ros/indigo/bin/rosbag", line 35, in <module>
    rosbag.rosbagmain()
  File "/opt/ros/indigo/lib/python2.7/dist-packages/rosbag/rosbag_main.py", line 855, in rosbagmain
    cmds[cmd](argv[2:])
  File "/opt/ros/indigo/lib/python2.7/dist-packages/rosbag/rosbag_main.py", line 319, in filter_cmd
    for topic, raw_msg, t in inbag.read_messages(raw=True):
  File "/opt/ros/indigo/lib/python2.7/dist-packages/rosbag/bag.py", line 2306, in read_messages
    yield self.seek_and_read_message_data_record((entry.chunk_pos, entry.offset), raw)
  File "/opt/ros/indigo/lib/python2.7/dist-packages/rosbag/bag.py", line 2444, in seek_and_read_message_data_record
    msg_type = _get_message_type(connection_info)
  File "/opt/ros/indigo/lib/python2.7/dist-packages/rosbag/bag.py", line 1547, in _get_message_type
    raise ROSBagException('Error generating datatype %s: %s' % (info.datatype, str(ex)))
rosbag.bag.ROSBagException: Error generating datatype my_message_package/Odometry: cannot retrieve message class for my_message_package/Odometry: _my_message_package__Odometry
```

The third line ```core_type: my_message_package/Odometry file_path:/tmp/genpy_Mc0Jkf/tmps_UQuR.py``` shows that the corresponding tmp scripts are located in ```/tmp/genpy_Mc0Jkf```. In the ```/tmp/genpy_Mc0Jkf/```, there is also a **raw.py** generated by the modified version **dynamic.py**. 

There is a subsititution function in dynamic.py. https://github.com/ros/genpy/blob/indigo-devel/src/genpy/dynamic.py#L81 

``` python
def _gen_dyn_modify_references(py_text, types):
```

See ```tmps_UQuR.py``` and ```raw.py``` in the ```/tmp/genpy_*```. The first one is the message script after subsititution, and the second one is before subsititution. Search ```my_message_package``` in the two files, and you can see this:

/tmp/genpy_Mc0Jkf/raw.py
``` python
"""autogenerated by genpy from my_message_package/Odometry.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

import geometry_msgs.msg
import nav_msgs.msg
import std_msgs.msg

class Odometry(genpy.Message):
  _md5sum = "b0000ede82c84c55526c6def9e1f567f"
  _type = "my_message_package/Odometry"
  _has_header = False #flag to mark the presence of a Header object

.............................
```

/tmp/genpy_Mc0Jkf/tmps_UQuR.py
``` python
"""autogenerated by genpy from my_message_package/Odometry.msg. Do not edit."""
import sys
python3 = True if sys.hexversion > 0x03000000 else False
import genpy
import struct

class _nav_msgs__Odometry(genpy.Message):
  _md5sum = "b0000ede82c84c55526c6def9e1f567f"
  _type = "my_message_package/Odometry"
  _has_header = False #flag to mark the presence of a Header object

.............................
```

In the ```raw.py```, class name is ```Odometry```, which should be subsitituted with ```_my_message_package__Odometry```. But in the ```tmps_UQuR.py```, it is substituted with ```_nav_msgs__Odometry```, which causes the problem.
