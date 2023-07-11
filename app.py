import streamlit as st
import pandas as pd
import numpy as np
import time
from examples.track import *
import os

# from examples.multi_yolo_backend import MultiYolo
# from examples.utils import write_MOT_results


st.title("APAS (Advanced Pedestrian Aassistance System)")
st.subheader("CV-10 : Bro3Sis1 Team")


def show_app(image_placeholder, img):
    image_placeholder.image(img)


def main():
    data_type = st.selectbox("Please select data type !", ("Image", "Video"))
    # upload model
    # model =

    # upload data
    if data_type == "Image":
        st.info("Input Image File(.png or .jpg) to Inference")
        uploaded_file = st.file_uploader(
            "Input Image",
            accept_multiple_files=True,
            type=["png", "jpg"],
            label_visibility="collapsed",
        )
    elif data_type == "Video":
        st.info("Input Video File(.avi or .mp4) to Inference")
        uploaded_file = st.file_uploader(
            "Input Video",
            accept_multiple_files=False,
            type=["avi", "mp4"],
            label_visibility="collapsed",
        )

    # uploaded_file = np.array(uploaded_file)
    st.text(uploaded_file)
    st.text(type(uploaded_file))

    button = st.button("Start Inference")

    with st.spinner("Inference In Progress"):
        if button:
            button = False
            # track.py
            opt = parse_opt()

            if uploaded_file:
                # save file to tempDB
                saved_dir = os.path.join(
                    "/opt/ml/final_project/yolo_tracking/examples/tempDB",
                    uploaded_file.name,
                )
                with open(saved_dir, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                st.success("File Uploaded !")

                opt.source = saved_dir
                opt.streamlit = True
                opt.show = True

                result = run(vars(opt))
                # if data_type == "Image":
                #     for img in result:
                #         st.image(img)
                # elif data_type == "Video":
                #     st.video(result)
            else:
                st.error("Please Input Necessary Data !")

    st.success("Inference Complete !")


if __name__ == "__main__":
    main()
