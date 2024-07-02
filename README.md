**# Facial Verification App :camera: 🧐**

This README file provides a detailed explanation of the Kivy facial verification app, outlining its functionalities, usage instructions, and dependencies .

**## Project Overview 🎨**

This application leverages Kivy, OpenCV, and DeepFace to create a real-time facial verification system using your webcam . It captures frames from the camera, detects faces using DeepFace's superpowers , and compares them against a predefined database (not included in this code). If a match is found, the user's identity is displayed which can be processed to do further functions. Otherwise, a red message indicates a no match or face detection failure.

**## Features 🚀**

- Real-time webcam capture 
- Face detection using DeepFace's magic ✨
- Facial verification against a user database (needs database of image for each user inside the train repo, )
- Visual feedback with success/failure messages and color changes (green for success, red for errors )

**## Dependencies**

- Kivy: Cross-platform GUI framework ([https://kivy.org/](https://kivy.org/))
- OpenCV: Real-time computer vision library ([https://opencv.org/](https://opencv.org/))
- DeepFace: Deep learning-based facial recognition library ([https://github.com/serengil/deepface](https://github.com/serengil/deepface))
- pandas : Data manipulation library ([https://pandas.pydata.org/](https://pandas.pydata.org/))

**## Installation**

1. Ensure you have Python (version 3.x recommended) installed on your system (check with `python --version` in your terminal).
2. Create a virtual environment to manage dependencies (optional but recommended, keeps things tidy! ).
3. Install the required libraries using pip:

   ```bash
   pip install kivy opencv-python deepface
   ```

4. **(Optional)** Install pandas and numpy if you intend to modify the face detection functionality.

**## Usage 🖥️**

1. Create a 'Train' repository in the main directory and include a class of users which contain image of the user. do this for each users.(not included in this code, but you can set it up later! )
2. **(Optional)** resize the iamges inside each repo to the same shape. This will help the model learn on a uniform data.
   ```bash
   python img_resizer.py
   ```
4. Run the application from your terminal:

   ```bash
   python main.py
   ```

**## Code Structure**

The code is organized into the following classes and functions:

- **`CamApp` class:**
    - Initializes the application, including webcam capture and layout elements (creates the user interface ).
    - Provides methods for updating the webcam image, face detection, verification, and label reset (keeps things running smoothly! ).

- **`face_detect` function:**
    - Uses DeepFace to detect faces in an image and compare them against the database (needs implementation, but the code is ready to accept your custom logic! ).
    - Returns the identified user's information or a message indicating no match or face detection failure.

- **`verify` function:**
    - Captures a frame from the webcam, saves it as an image, performs face detection, and updates the verification label based on the outcome (the verification magic happens here! ✨).

- **`reset_verification_label` function:**
    - Resets the verification label to its default state (green text, "Welcome") after a verification attempt (clears the message after verification is done! ).

**## Additional Notes**

- The code assumes you have a pre-defined user database set up for verification.
- You might need to adjust the DeepFace model selection (`models[0]`) based on your requirements and installation.
- Consider error handling and logging for robustness (makes the code more reliable ).

## Contributing 💡

Contributions are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.

## Credits 🙌

This project was created by **Dawit Neri**

## Support 💬

If you encounter any issues or have any questions, feel free to reach out to dawitneri888@gmail.com or open an issue in the GitHub repository.
