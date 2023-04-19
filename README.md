# Deep-Learning-Based-Image-Enhancement-Framework

This is the implementation of an image enhancement and restoration framework based on deep learning methods. In the project, I proposed a Python application for image processing from deblurring, denoising, dehazing, deraining and inpainting. Meanwhile, it also provides some basic methods for image processing.



### Getting Started

These instructions will help you get a copy of the project, and running on your device for further development.

- ##### Clone the Project

  ```
  git clone https://github.com/YifeiShao7/Deep-Learning-Based-Image-Enhancement-Framework
  cd ./Deep-Learning-Based-Image-Enhancement-Framework
  ```

- ##### Prerequisites

  - A Python running environment which is equal to or higher than  3.9

  - After the installation of Python, please install the following packages using `pip`
  
    - Numpy
    - PyQt5
    - OpenCV
    - PyTorch
    - TensorFlow(please install the appropriate version for your device)
  
    by entering the following command
  
    ```
    pip install pyqt5 pyqt5-tools torch torchvision torchaudio opencv-python
    ```
  
- ##### Run the program

  - Firstly, please add the UI file to the Python running path

    ```
    PYTHONPATH=$PYTHONPATH:./com/Processing/imageUtil/ui/mainUI
    ```

  - Now you can run the application by

    ```
    python ./com/Processing/imageUtil/Main.py
    ```

