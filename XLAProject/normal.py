import cv2
import numpy as np

def rectify(h):
    h = h.reshape((4,2))
    hnew = np.zeros((4,2),dtype = np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h,axis = 1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew
def scan_document(image): 
    # thay đổi kích thước hình ảnh để xử lý dễ hơn, 
    # chọn kích thước tối ưu để nội dung quan trọng không bị mất
    image = cv2.resize(image,(1500, 880))

    # tạo một bản sao của ảnh gốc
    orig = image.copy()

    # chuyển đổi sang thang độ xám và mờ thành mịn
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    #blurred = cv2.medianBlur(gray, 5)

    # sử dụng phương pháp Canny Edge Detection
    edged = cv2.Canny(blurred, 0, 50)
    orig_edged = edged.copy()

    # tìm các đường viền trong các cạnh của hình ảnh, 
    # chỉ giữ lại những đường viền lớn nhất và khởi tạo đường viền màn hình.
    (contours, _) = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    #x,y,w,h = cv2.boundingRect(contours[0])
    #cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),0)

    # lấy đường viền xấp xỉ
    for c in contours:
        p = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * p, True)

        if len(approx) == 4:
            target = approx
            break


    # ánh xạ điểm mục tiêu tới hình tứ giác 1000x800
    approx = rectify(target)
    pts2 = np.float32([[0,0],[1000,0],[1000,800],[0,800]])

    M = cv2.getPerspectiveTransform(approx,pts2)
    dst = cv2.warpPerspective(orig,M,(1000,800))

    cv2.drawContours(image, [target], -1, (0, 255, 0), 2)
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)


    # sử dụng ngưỡng trên hình ảnh đã ánh xạ để có được hiệu ứng quét
    ret,th = cv2.threshold(dst,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return th, dst

    #cv2.imshow("Original.jpg", orig)
    #cv2.imshow("Original Gray.jpg", gray)
    #cv2.imshow("Original Blurred.jpg", blurred)
    #cv2.imshow("Original Edged.jpg", orig_edged)
    #cv2.imshow("Outline.jpg", image)
    #cv2.imshow("Otsu's.jpg", th)
    #cv2.imshow("dst.jpg", dst)

#cv2.waitKey(0)
#cv2.destroyAllWindows()

