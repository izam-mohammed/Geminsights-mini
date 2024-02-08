import streamlit as st
import pandas as pd
import os
from utils import save_json, load_json
from markdown import markdown
from utils import load_json
from autoviz import AutoViz_Class
import base64
from google.cloud import aiplatform
import base64
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part
import json


aiplatform.init(
    project = "geminsights",
    location="us-central1"
    )

json_file = json.loads(st.secrets["credentials"], strict=False)
with open("credentials.json", "w") as f:
    json.dump(json_file, f, indent=2)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"


dataframe = None
st.title("GemInsights 📊")
st.caption('A gemini powered data analysis tool to get insights from data 🔥')
file = st.file_uploader(
    "Pick a dataframe", type=["csv", "xlsx"], accept_multiple_files=False
)

if file is not None:
    _, extension = os.path.splitext(file.name)
    if extension == ".csv":
        dataframe = pd.read_csv(file)
    else:
        dataframe = pd.read_excel(file)
    st.write(dataframe.head())
    st.write(f"updated a dataframe with shape {dataframe.shape}")

if file is not None:
    text_input = st.text_input(
        "Enter something about the data 👇",
        label_visibility="visible",
        disabled=False,
        placeholder="eg:- This is a sales dataframe",
    )

    option = st.selectbox(
        "Which is the target column ? 🎯",
        tuple(list(dataframe.columns)),
        index=None,
        placeholder="Select one column in here",
    )

def plot(dataframe, target):

    AV = AutoViz_Class()

    dft = AV.AutoViz(
    "",
    sep=",",
    depVar=target,
    dfte=dataframe,
    header=0,
    verbose=2,
    lowess=False,
    chart_format="jpg",
    max_rows_analyzed=500,
    max_cols_analyzed=20,
    save_plot_dir="plots",
    )

def prompt_make(dataframe, target, info):
    images = []
    image_dir = f"plots/{target}"
    image_files = os.listdir(image_dir)
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        img = open(image_path, "rb").read()
        img_bytes = Part.from_data(
            base64.b64decode(base64.encodebytes(img)), mime_type="image/jpeg"
        )
        images.append(img_bytes)
    with open("prompt.txt", "rb") as file:
        data = file.read()
    prompt = f"{data}\n Here are some of the informations related to the dataset - '{info}'"
    
    # print(f"{prompt}")
    # print(images)
    return prompt, images

def generate_res(prompt, images):
    print("prompting ...")
    model = GenerativeModel("gemini-pro-vision")
    responses = model.generate_content(
        [prompt]+images,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32
        },
    )
    return responses.text



def generate(dataframe, text_input, option):
    plot(dataframe, option)
    prompt, images = prompt_make(dataframe, option, text_input)
    res = generate_res(prompt, images)
    return res

if st.button("Get Insights", type="primary"):
    st.write("generating insights ⏳ ... ")
    # running the pipeline

    response = generate(dataframe, text_input, option)
    res = markdown(response)
    st.markdown(res, unsafe_allow_html=True)

else:
    st.write("")
