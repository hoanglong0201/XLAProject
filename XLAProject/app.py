import streamlit as st
from normal import scan_document
from PIL import Image, ImageEnhance
import io
import cv2
import numpy as np
from advanced import canny_img
from fpdf import FPDF
from gamma import Gamma

def read_image(file):
    image = Image.open(io.BytesIO(file.getvalue()))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image

def save_images(images, filenames):
    for image, filename in zip(images, filenames):
        cv2.imwrite(filename, image)

def convert_images_to_pdf(filenames, pdf_filename):
    pdf = FPDF()
    for filename in filenames:
        pdf.add_page()
        pdf.image(filename, x=10, y=8, w=190)
    pdf.output(pdf_filename, "F")

def main():
    # Tải ảnh
    logo = st.image('About/logo.png', width=50)
    st.title("📜DOCUMENT SCANNER")
    

    menu = ["Introduction", "Normal Scanner", "Advanced Scanner", "About us"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Introduction":
        st.subheader("Giới thiệu dự án")
        st.markdown("""
        👋Chào mừng đến với dự án Document Scanner đơn giản!👋 \n
        Dự án này sử dụng ngôn ngữ python và openCV để tạo giao diện người dùng trực quan cho ứng dụng quét tài liệu cơ bản. Ứng dụng cho phép người dùng tải lên ảnh tài liệu, xử lý ảnh, xem kết quả quét và tải về dưới dạng pdf. \n
        **✨Tính năng:**

        * 🔺Tải lên ảnh tài liệu
        * 🖥Xử lý ảnh
        * 🖼Quét tài liệu trong ảnh và hiển thị
        * 📃Tải ảnh về dưới dạng pdf

        **⚙️Cài đặt**

        * 🔻Cài đặt Python 
        * 🔻Cài đặt pip
        * 🔻Cài đặt các thư viện cho xử lý ảnh: Streamlit, cv2, numpy, io, PIL
        * 🦿Sau khi cài đặt xong, mở thư mục chứa App, chạy ứng dụng bằng lệnh streamlit run app.py

        **👨‍💻Hướng dẫn sử dụng**

        * 🦿Khởi chạy website ứng dụng
        * 🦿Chọn mục Normal Scanner để quét ảnh nhanh hoặc mục Advanced Scanner để chỉnh thông số nhằm quét ảnh tốt hơn
        * 🔺Tải ảnh tài liệu lên và đợi chương trình quét
        * 🔻Xem và tải về dưới dạng pdf (Nếu muốn)

        **⚠️Lưu ý:**

        * Dự án này là một dự án đơn giản về quét tài liệu nên có thể vẫn có những sai sót và đang trong quá trình khắc phục và phát triển.
        * App không thể đọc những bức ảnh có chất lượng quá kém, tài liệu trong ảnh không rõ ràng hoặc bị lẫn với nền. Lưu ý khi đưa ảnh vào quét.
        
        **🕵️‍♂️Xử lý lỗi**
        * 🦾 Nếu kết quả quét ở mục Normal Scanner không được như bạn mong muốn, hãy đổi sang mục Advanced Scanner và tự điều chỉnh thông số đến khi nhận được kết quả ưng ý.
        * 🦾 Nếu ở mục Advanced Scanner vẫn không quét được tài liệu như ý, hãy chụp lại tài liệu ở góc độ tốt hơn hoặc chất lượng cao hơn, tránh tài liệu bị lẫn với nền xung quanh.
        * 🦾 Có những ảnh bị lỗi quét do hướng của ảnh hoặc tài liệu không phù hợp, hãy thử xoay lại hướng của ảnh trước khi tải ảnh lên.
        
        ** 🙇‍♂️ Cảm ơn bạn đã sử dụng dự án này!**

        """)
    elif choice == "Normal Scanner":
        st.subheader("Quét tài liệu nhanh")

        uploaded_file = st.file_uploader("Chọn một ảnh tài liệu để quét", type=["jpg", "png"])
        if uploaded_file is not None:
            image1 = read_image(uploaded_file)
            result_image, normal_image = scan_document(image1)

            st.image(uploaded_file, caption='Ảnh gốc')
            st.image(result_image, caption='Ảnh đã quét')
            st.image(normal_image, caption='Ảnh dạng thường đã quét')

            # Lưu ảnh đã quét dưới dạng file
            save_images([result_image, normal_image], ["result_image.jpg", "normal_image.jpg"])

            #Tạo PDF từ ảnh đã quét
            pdf_filename = 'scanned_document.pdf'
            convert_images_to_pdf(["result_image.jpg", "normal_image.jpg"], pdf_filename)

            # Tạo nút tải xuống PDF
            with open(pdf_filename, "rb") as pdf_file:
                st.download_button(
                    label="Tải xuống PDF",
                    data=pdf_file,
                    file_name=pdf_filename
                )
    elif choice == "Advanced Scanner":
        st.subheader("Quét tài liệu nâng cao")
        st.markdown("""
        **Hướng dẫn điều chỉnh thông số**
        * Thông số iteration: số lần lặp để khử nhiễu trong ảnh. Việc lặp lại khử nhiễu bao nhiêu lần cũng quyết định rằng liệu app có thể quét được tài liệu hay không.
        * Thông số lower threshold và upper threshold: Ngưỡng dưới được sử dụng để phân biệt pixel sáng, trong khi ngưỡng trên được sử dụng để phân biệt pixel tối, cả hai nhằm phục vụ phân đoạn ảnh. Ngưỡng dưới thường được sử dụng để loại bỏ các pixel tối (nhiễu) hoặc giữ lại các pixel sáng (đối tượng), trong khi ngưỡng trên thường được sử dụng để loại bỏ các pixel sáng (nhiễu) hoặc giữ lại các pixel tối (đối tượng).
        * Thông số contrast: chỉnh độ tương phản của ảnh sau khi quét
        * Thông số brightness: chỉnh độ sáng của ảnh sau khi quét
        """)
        uploaded_file = st.file_uploader("Chọn một ảnh tài liệu để quét", type=["jpg", "png"])
        ite = st.slider("Pick value of iteration:", 0, 10)
        tlower = st.slider("Pick value of lower threshhold:", 0, 300)
        tupper = st.slider("Pick value of upper threshhold:", 0, 300)
        contrast = st.slider("Pick value of contrast:",0.0,10.0,1.0)
        brighness = st.slider("Pick value of brightness:",-100,0,-50)
        st.write(ite,tlower,tupper)
        if uploaded_file is not None:
            image1 = read_image(uploaded_file)
            gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            result_image, normal_image = canny_img(gray,ite,tlower,tupper)
            normal_image = np.clip(normal_image + brighness, 0, 255).astype(np.uint8)
            normal_image = Gamma(normal_image,contrast)
            #st.image(uploaded_file, caption='Ảnh gốc')
            st.image(result_image, caption='Ảnh dạng B/W đã quét')
            st.image(normal_image, caption='Ảnh dạng thường đã quét')

            # Lưu ảnh đã quét dưới dạng file
            save_images([result_image, normal_image], ["result_image.jpg", "normal_image.jpg"])

            #Tạo PDF từ ảnh đã quét
            pdf_filename = 'scanned_document.pdf'
            convert_images_to_pdf(["result_image.jpg", "normal_image.jpg"], pdf_filename)

            #Tao button rotate image
            if st.button("Xoay ảnh sang phải", type="primary"):
                st.write("Đã xoay ảnh")
                result_image = cv2.rotate(result_image,cv2.ROTATE_90_CLOCKWISE)
                normal_image = cv2.rotate(normal_image,cv2.ROTATE_90_CLOCKWISE)
                st.image(result_image, caption='Ảnh dạng B/W đã quét')
                st.image(normal_image, caption='Ảnh dạng thường đã quét')
                
            elif st.button("Xoay ảnh sang trái", type="primary"):
                st.write("Đã xoay ảnh")
                result_image = cv2.rotate(result_image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                normal_image = cv2.rotate(normal_image,cv2.ROTATE_90_COUNTERCLOCKWISE)
                st.image(result_image, caption='Ảnh dạng B/W đã quét')
                st.image(normal_image, caption='Ảnh dạng thường đã quét')
            elif st.button("Xoay ngược ảnh", type="primary"):
                st.write("Đã xoay ảnh")
                result_image = cv2.rotate(result_image,cv2.ROTATE_180)
                normal_image = cv2.rotate(normal_image,cv2.ROTATE_180)
                st.image(result_image, caption='Ảnh dạng B/W đã quét')
                st.image(normal_image, caption='Ảnh dạng thường đã quét')
            save_images([result_image, normal_image], ["result_image.jpg", "normal_image.jpg"])
            pdf_filename = 'scanned_document.pdf'
            convert_images_to_pdf(["result_image.jpg", "normal_image.jpg"], pdf_filename)
            # Tạo nút tải xuống PDF

            with open(pdf_filename, "rb") as pdf_file:
                st.download_button(
                    label="Tải xuống PDF",
                    data=pdf_file,
                    file_name=pdf_filename
                )
    else:
        st.subheader("About us")
        st.markdown("""
        👋Giới thiệu về chúng tôi👋\n
        Dự án được thực hiện bởi 3 sinh viên:\n
        1. Lê Bá Tùng
        """)
        st.image('About/Tung.jpg', caption='MSV: 715102221', width= 500)
        st.markdown("""
        Nhiệm vụ trong dự án: 
        * Hỗ trợ code chương trình xử lý ảnh
        * Xây dựng App (app.py)
        * Tìm tư liệu hình ảnh
        """)
        st.markdown("""
        2. Nguyễn Thị Duyên
        """)
        st.image('About/Duyen.jpg', caption='MSV: 715102058', width= 500)
        st.markdown("""
        Nhiệm vụ trong dự án: 
        * Code chương trình xử lý ảnh nâng cao (advanced.py)
        * Viết báo cáo 
        * Tìm tư liệu hình ảnh
        """)
        st.markdown("""
        3. Ban Hoàng Long
        """)
        st.image('About/Long.jpg', caption='MSV: 715102125', width= 500)
        st.markdown("""
        Nhiệm vụ trong dự án: 
        * Code chương trình xử lý ảnh nâng cao (advanced.py)
        * Code chương trình xử lý ảnh thường (normal.py)
        * Làm powerpoint 
        * Hỗ trợ xây dựng App (gamma.py)
        """)        
        
if __name__ == '__main__':
    main()


