# Frenetic steering

This project contains the code of the implementations of the algorithms described in the paper 'Frenetic steering in a nonequilibrium graph'.

step_1 signifies the disentanglement algorithm, step_2 signifies the frenetic steering algorithm.

The starting point for the implementation of the algorithm for disentangling the basins of attraction is in the file step_1/find_disentangled_system.py

The starting point for the implementation of the algorithm for frenetic steering is in the file step_2/execute_learning_step/algorithm_3/algorithm_3.py

In the folders analysis_step_1 and analysis_step_2 code can be found that was used to investigate the performance of the algorithms. 

The starting point for the local steering application is in application_on_images/local_steering.py. This application needs to be configured in config.json. The function that converts images to black white images, the same number of pixels wide and high is in application_on_images/prepare_patterns.py

The writer of the program, Bram Lefebvre, can be reached at bramlefebvre@gmail.com.