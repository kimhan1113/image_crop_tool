import cv2, os
import numpy as np
from tkinter import filedialog


img_path = filedialog.askopenfilename()
# img_path = './img/pexels-photo-276690.jpg'
filename, ext = os.path.splitext(os.path.basename(img_path))
ori_img = cv2.imread(img_path)
ori_img = cv2. resize(ori_img, dsize=(840, 680), interpolation=cv2.INTER_LINEAR)

src = []
# mouse callback handler
def mouse_handler(event, x, y, flags, param):
  if event == cv2.EVENT_LBUTTONUP:
    img = ori_img.copy()

    src.append([x, y])

    for xx, yy in src:
      cv2.circle(img, center=(xx, yy), radius=5, color=(255, 0, 0), thickness=-1, lineType=cv2.LINE_AA)

    cv2.imshow('img', img)

    # perspective transform
    if len(src) == 4:
      src_np = np.array(src, dtype=np.float32)

      #np.linalg.norm 은 float형 값으로 떨어짐
      width = max(np.linalg.norm(src_np[0] - src_np[1]), np.linalg.norm(src_np[3] - src_np[2]))
      height = max(np.linalg.norm(src_np[0] - src_np[3]), np.linalg.norm(src_np[1] - src_np[2]))

      dst_np = np.array([
        [0, 0],
        [width, 0],
        [width, height],
        [0, height]
      ], dtype=np.float32)

      M = cv2.getPerspectiveTransform(src=src_np, dst=dst_np)
      result = cv2.warpPerspective(ori_img, M=M, dsize=(width, height))

      cv2.namedWindow('result', cv2.WINDOW_NORMAL)
      cv2.imshow('result', result)
      # cv2.imwrite('./result/%s_result%s' % (filename, ext), result)

def image_show():

  cv2.namedWindow('img')
  cv2.setMouseCallback('img', mouse_handler)
  cv2.imshow('img', ori_img)
  ch = cv2.waitKey(0)

  if ch == ord('q'):
    cv2.destroyWindow('img')
  elif ch == ord('r'):
    print('Reset')
    global src
    src = []
    image_show()

# main
image_show()







