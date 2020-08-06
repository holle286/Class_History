execute_process(COMMAND "/home/csci5551/Desktop/jason_project/ros_ws2/build/baxter_tools/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/csci5551/Desktop/jason_project/ros_ws2/build/baxter_tools/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
