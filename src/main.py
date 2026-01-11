import cv2
import face_recognition
from djitellopy import Tello
import serial
import time

# Initialize serial communication with Arduino via USB.
# The timeout is set to 1 second; if no data is received/sent within this window, an exception might be raised.
arduino = serial.Serial(port='COM5', baudrate=9600, timeout=1) 

# Initialize the Tello drone object to access its functions and controls.
tello = Tello()

# Establish Wi-Fi connection with the drone.
tello.connect()

# Print current battery level to the console.
print(tello.get_battery())

# Variable to store the previous data received from Arduino (initialized to 4 to ensure entry into condition).
previous_number = 4 

# Start the video stream from the drone's camera.
tello.streamon()

# List of known names corresponding to the images in the database.
known_face_names = ["Yarin", "Noam", "Osher"]

# List to store the mathematical encoding of the known faces.
known_face_encodings = []

# Dictionary mapping names to specific signals ('1', '2', '3') to be sent to the Arduino.
known_face_names_communication = {"Yarin": '1', "Noam": '2', "Osher": '3'}

# Load images and generate encodings for each known person.
for name in known_face_names:
    # Load the image file into a numpy array.
    image = face_recognition.load_image_file(name + ".jpeg")

    # Generate the facial encoding (mathematical representation of the face).
    # We take the first face found in the image ([0]).
    encoding = face_recognition.face_encodings(image)[0]

    # Append the encoding to the known_face_encodings list.
    known_face_encodings.append(encoding)

# Initialize variables for face tracking loop.
face_locations = []
face_encodings = []
face_names = []

# Boolean to control frame processing frequency for optimization.
# Processing every single frame can cause lag, so we process every other frame.
process_this_frame = True

while True:
    # Capture the live video frame from the Tello drone.
    frame = tello.get_frame_read().frame

    # Resize the frame of video to 1/4 size for faster face recognition processing.
    small_frame = cv2.resize(frame, (320, 240))
    
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses).
    rgb_small_frame = small_frame[:, :, ::-1]
    
    # Only process every other frame of video to save time.
    if process_this_frame:
        
        # Find all the faces and face encodings in the current frame of video.
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = [] # Reset the list of names for the current frame.

        # Loop through each face found in the current frame.
        for face_encoding in face_encodings:
            
            # See if the face is a match for the known face(s).
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                
                # Send the corresponding signal to the Arduino based on the identified name.
                arduino.write(bytes(known_face_names_communication[name], 'utf-8')) 
                
                # Sleep to prevent flooding the Arduino/Seeeduino with data.
                time.sleep(0.6)
            
            else: 
                # If the face is unknown, send signal '4' to Arduino.
                arduino.write(bytes('4', 'utf-8'))
                time.sleep(0.6)

            # Add the name to the list of names detected in this frame.
            face_names.append(name)

    # Flip the boolean so the next frame is skipped (optimization).
    process_this_frame = not process_this_frame
    
    # Display the results.
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size.
        top *= 3
        right *= 3
        bottom *= 3
        left *= 3

        # Draw a box around the face.
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face.
        cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 2)

    # Resize the frame for display purposes.
    small_frame = cv2.resize(frame, (320, 240))

    # Display the resulting image.
    cv2.imshow('video', small_frame)

    # Check for incoming data from Arduino.
    if arduino.in_waiting > 0:
        data = arduino.read()
        
        # Only act if the data received is different from the previous command.
        if data != previous_number: 
            if data == b'\x01':
                print("Received the number 1 from Arduino!")
                tello.takeoff()
            elif data == b'\x02':
                print("Received the number 2")
                tello.land()
            elif data == b'\x00':
                print("Received the number 0")
            elif data == b'\x03':
                print("Received the number 3")
            
            previous_number = data   
            time.sleep(0.8)

    # Emergency exit: Hit 'q' on the keyboard to quit.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Stop the video stream.
tello.streamoff()

# Disconnect from the Tello drone.
tello.disconnect()

# Close all OpenCV windows.
cv2.destroyAllWindows()