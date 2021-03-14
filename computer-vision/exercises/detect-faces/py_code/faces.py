def show_faces(image_path, detected_faces, show_id=False, show_attributes=False):
    import matplotlib.pyplot as plt
    from PIL import Image, ImageDraw

    # Open an image
    img = Image.open(image_path)

    # Create a figure to display the results
    fig = plt.figure(figsize=(8, 6))

    if detected_faces:
        # If there are faces, how many?
        num_faces = len(detected_faces)
        prediction = ' (' + str(num_faces) + ' faces detected)'
        # Draw a rectangle around each detected face
        for face in detected_faces:
            r = face.face_rectangle
            bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
            draw = ImageDraw.Draw(img)
            draw.rectangle(bounding_box, outline='magenta', width=5)

            if show_id:
                plt.annotate(face.face_id,(r.left, r.top + r.height + 15), backgroundcolor='white')

            if show_attributes:
                # Annotate with face attributes (only age and emotion are used in this sample)
                detected_attributes = face.face_attributes.as_dict()
                print(detected_attributes)
                age = 'age unknown' if 'age' not in detected_attributes.keys() else int(detected_attributes['age'])
                gender = 'Person' if 'gender' not in detected_attributes.keys() else detected_attributes['gender']
                annotations = '{}-year-old {}'.format(age, gender)
                txt_lines = 1
                if 'hair' in detected_attributes.keys():
                    annotations += '\nHair:'
                    for hair_type in detected_attributes['hair']:
                        txt_lines += 1
                        annotations += '\n - {}: {}'.format(hair_type, detected_attributes['hair'][hair_type])
                if 'facial_hair' in detected_attributes.keys():
                    annotations += '\nFacial Hair:'
                    for facial_hair_type in detected_attributes['facial_hair']:
                        txt_lines += 1
                        annotations += '\n - {}: {}'.format(facial_hair_type, detected_attributes['facial_hair'][facial_hair_type])
                if 'emotion' in detected_attributes.keys():
                    annotations += '\nEmotions:'
                    for emotion_name in detected_attributes['emotion']:
                        txt_lines += 1
                        annotations += '\n - {}: {}'.format(emotion_name, detected_attributes['emotion'][emotion_name])
                
                att_left = r.left if num_faces > 1 else (r.left + r.width)
                plt.annotate(annotations,(att_left, (r.top + r.height + (txt_lines * 10))), backgroundcolor='yellow')

        # Plot the image
        fig.suptitle(prediction)

    plt.axis('off')
    plt.imshow(img)

def show_similar_faces(image_1_path, image_1_face, image_2_path, image_2_faces, similar_faces):
    import matplotlib.pyplot as plt
    from PIL import Image, ImageDraw

    # Create a figure to display the results
    fig = plt.figure(figsize=(20, 6))

    # Show face 1
    img1 = Image.open(image_1_path)
    r = image_1_face.face_rectangle
    bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
    draw = ImageDraw.Draw(img1)
    draw.rectangle(bounding_box, outline='magenta', width=5)
    
    plt.axis('off')
    plt.imshow(img1)
    

    # get the matching face IDs
    matching_face_ids = list(map(lambda face: face.face_id, similar_faces))

    # Draw a rectangle around each similar face in image 2
    img2 = Image.open(image_2_path)
    a = fig.add_subplot(1,2,2)
    plt.axis('off')
    for face in image_2_faces:
        r = face.face_rectangle
        bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
        draw = ImageDraw.Draw(img2)
        if face.face_id in matching_face_ids:
            draw.rectangle(bounding_box, outline='lightgreen', width=10)
            plt.annotate('Match!',(r.left, r.top + r.height + 35), backgroundcolor='white')
        else:
            draw.rectangle(bounding_box, outline='red', width=5)
            plt.annotate('Not A Match!',(r.left, r.top + r.height + 35), backgroundcolor='orange')
    plt.imshow(img2)
    plt.show()
