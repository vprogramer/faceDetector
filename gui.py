import wx
import cv2
from detect_face import detector
from scipy.spatial import distance


class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)

        self.path_start_photo = "no_photo.png"
        img = cv2.imread(self.path_start_photo)
        self.path_save_to_file = 'savedImage.jpg'
        resized_img = cv2.resize(img, (400, 400))
        cv2.imwrite(self.path_save_to_file, resized_img)

        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        photoSizer = wx.BoxSizer(wx.HORIZONTAL)
        loadFileSizer = wx.BoxSizer(wx.HORIZONTAL)
        compareSizer = wx.BoxSizer(wx.HORIZONTAL)
        resultSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.title = wx.StaticText(self, wx.ID_ANY, "Детектирование лиц на фото")
        titleSizer.Add(self.title, 0, wx.Center | wx.ALL, 10)

        self.photo1 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.path_save_to_file,
                                                         wx.BITMAP_TYPE_ANY))
        photoSizer.Add(self.photo1, 0, wx.CENTER | wx.ALL, 20)
        self.photo2 = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(self.path_save_to_file,
                                                                 wx.BITMAP_TYPE_ANY))
        photoSizer.Add(self.photo2, 0, wx.CENTER | wx.ALL, 20)

        self.choosePhotoButton1 = wx.Button(self, label="Выберите фотографию")
        self.choosePhotoButton1.Bind(wx.EVT_BUTTON, self.find_photo_one)
        self.choosePhotoButton2 = wx.Button(self, label="Выберите фотографию")
        self.choosePhotoButton2.Bind(wx.EVT_BUTTON, self.find_photo_two)
        loadFileSizer.Add(self.choosePhotoButton1, 0, wx.CENTER | wx.ALL, 10)
        loadFileSizer.Add(self.choosePhotoButton2, 0, wx.CENTER | wx.ALL, 10)

        self.resultButton = wx.Button(self, label="Сравнить")
        self.resultButton.Bind(wx.EVT_BUTTON, self.result)
        compareSizer.Add(self.resultButton, 0, wx.CENTER | wx.ALL, 10)

        self.resultText = wx.StaticText(self, wx.ID_ANY, "Результат:")
        resultSizer.Add(self.resultText, 0, wx.CENTER | wx.ALL, 5)
        self.resultAnswer = wx.TextCtrl(self, style=wx.TE_READONLY, size = (200, 30))
        resultSizer.Add(self.resultAnswer, 0, wx.CENTER | wx.ALL, 5)
        self.resultNumber = wx.TextCtrl(self, style=wx.TE_READONLY, size = (200, 30))
        resultSizer.Add(self.resultNumber, 0, wx.CENTER | wx.ALL, 5)

        self.mainSizer.Add(titleSizer, 0, wx.CENTER)
        self.mainSizer.Add(photoSizer, 0, wx.CENTER)
        self.mainSizer.Add(loadFileSizer, 0, wx.CENTER)
        self.mainSizer.Add(compareSizer, 0, wx.CENTER)
        self.mainSizer.Add(resultSizer, 0, wx.CENTER)
        self.SetSizer(self.mainSizer)

    def find_photo_one(self, event):
        try:
            openFileDialog = wx.FileDialog(self, "Open", "", "",
                                           "Photo files (*.jpg)|*.jpg| \ Photo files (*.png)|*.png|\ All files (*.*)|*.*",
                                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            openFileDialog.ShowModal()
            self.path_photo = openFileDialog.GetPath()
            self.face_descriptor1 = detector(self.path_photo)
            self.resultAnswer.SetValue("")
            self.resultNumber.SetValue("")
            if self.face_descriptor1 == "No face":
                img = cv2.imread(self.path_start_photo)
                self.path_save_to_file = 'savedImage.jpg'
                resized_img = cv2.resize(img, (400, 400))
                cv2.imwrite(self.path_save_to_file, resized_img)
                Img = wx.Image(self.path_save_to_file, wx.BITMAP_TYPE_ANY)
                self.photo1.SetBitmap(wx.BitmapFromImage(Img))
                wx.MessageBox("No face", "Error", wx.OK)
                raise ZeroDivisionError
            else:
                Img = wx.Image(self.path_save_to_file, wx.BITMAP_TYPE_ANY)
                self.photo1.SetBitmap(wx.BitmapFromImage(Img))
            self.Refresh()
        except:
            print("Нет данного файла")
            wx.MessageBox("Нет файла", "Error", wx.OK)
            return 0

    def find_photo_two(self, event):
        try:
            openFileDialog = wx.FileDialog(self, "Open", "", "",
                                           "Photo files (*.jpg)|*.jpg| \ Photo files (*.png)|*.png|\ All files (*.*)|*.*",
                                           wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
            openFileDialog.ShowModal()
            self.path_photo = openFileDialog.GetPath()
            self.face_descriptor2 = detector(self.path_photo)
            self.resultAnswer.SetValue("")
            self.resultNumber.SetValue("")
            if self.face_descriptor2 == "No face":
                img = cv2.imread(self.path_start_photo)
                self.path_save_to_file = 'savedImage.jpg'
                resized_img = cv2.resize(img, (400, 400))
                cv2.imwrite(self.path_save_to_file, resized_img)
                Img = wx.Image(self.path_save_to_file, wx.BITMAP_TYPE_ANY)
                self.photo2.SetBitmap(wx.BitmapFromImage(Img))
                wx.MessageBox("No face", "Error", wx.OK)
                raise ZeroDivisionError
            else:
                Img = wx.Image(self.path_save_to_file, wx.BITMAP_TYPE_ANY)
                self.photo2.SetBitmap(wx.BitmapFromImage(Img))
            self.Refresh()
        except:
            print("Нет данного файла")
            wx.MessageBox("Нет файла", "Error", wx.OK)
            return 0

    def result(self, event):
        try:
            a = distance.euclidean(self.face_descriptor1, self.face_descriptor2)
            print(a)
            self.resultAnswer.SetValue("")
            self.resultNumber.SetValue("")
            self.resultNumber.AppendText(str(a))
            if a > 0.6:
                self.resultAnswer.AppendText("Не похожи")
            else:
                self.resultAnswer.AppendText("Похожи")
            self.Refresh()
        except:
            message = "No face"
            print(message)
            self.resultAnswer.SetValue("")
            self.resultNumber.SetValue("")
            self.resultAnswer.AppendText(message)
            self.resultNumber.AppendText(message)
            self.Refresh()
            wx.MessageBox(message, "Error", wx.OK)


class MainFrame(wx.Frame):
    def __init__(self, parent, title, flag=True):
        wx.Frame.__init__(self, parent, title=title, size=(900, 900))
        # Центрирование
        self.Center()
        self.Show(flag)
        # Добавляем панели на фрейм
        self.panel_menu = MainPanel(self)

        # White style
        self.panel_menu.SetBackgroundColour("White")

        # Прячем две панели
        self.panel_menu.Show()

        # Добавляем сайзеры
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panel_menu, 1, wx.EXPAND)
        self.SetSizer(self.sizer)


if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame(None, title='Программа по детектированию лица')
    app.MainLoop()