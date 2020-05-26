import dlib
import wx
import cv2


def detector(path):
    sp = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
    detector = dlib.get_frontal_face_detector()

    save_img = cv2.imread(path)
    img = dlib.load_rgb_image(path)
    #img = io.imread('t1.jpg')
    #img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # win1 = dlib.image_window()
    # win1.clear_overlay()
    # win1.set_image(img)

    dets = detector(img,0)

    for k,d in enumerate(dets):
        print("Detection {}: Left: {} Top: {} Right: {} Bottim: {}".format(k, d.left(), d.top(), d.right(), d.bottom()))
        cv2.rectangle(save_img, (d.left(), d.top()), (d.right(), d.bottom()), (255, 0, 0), thickness=7)

    try:
        shape = sp(img, d)
        # win1.clear_overlay()
        # win1.add_overlay(d)
        # win1.add_overlay(shape)
        resized_img = cv2.resize(save_img, (400, 400))
        save_to_file = 'savedImage.jpg'
        cv2.imwrite(save_to_file, resized_img)

        face_descriptor = facerec.compute_face_descriptor(img, shape)
        return face_descriptor
    except:
        print("No face")
        wx.MessageBox("No face", "Error", wx.OK)
        return "No face"



