import streamlit as st
import pandas as pd
from tflm_hello_world.aws_s3 import s3_conn
import os
from PIL import Image
import shutil

def get_img_df(img_list):
    " Converts img list to pd.DataFrame "
    img_df = pd.DataFrame(columns=['File name', 'Label'])
    for img in img_list:
        row_to_append = pd.DataFrame([{'File name': img[2], 'Label':img[1]}])
        img_df = pd.concat([img_df, row_to_append], ignore_index=True)

    return img_df

def store_uploaded_images(img_set, i, selected_dataset, unlabeled=False, pil_img=False):
    " Stores a list of images to AWS S3"
    selected_imgs = []
    label_list=("Unlabeled", 0, 1)

    # If the image is in Unlabeled directory
    if unlabeled is True:
        label_list = (0, 1)
    
    for img in img_set:
        st.image(img, width=300)
        check = st.checkbox("Choose image", key=f"check_{i}")
        if check:
            label = st.radio("Select label", label_list, key=f"label_{i}")
            if pil_img:
                selected_imgs.append([img, label, img.name])
            else:
                selected_imgs.append([img, label, img.name])
        i += 1

    if len(selected_imgs) > 0:
        st.write('You selected following images:')
        images_df = get_img_df(selected_imgs)
        st.dataframe(images_df)

        store_btn = st.button("Store images", key=f"button_{i}")
        if store_btn:
            for img in selected_imgs:
                if unlabeled:
                    # Move image from Unlabled to dir 0 or 1
                    shutil.move(f'temp/Unlabeled/{img[2]}', f'temp/{selected_dataset}/{img[1]}/{img[2]}')
                else:
                    store_image_locally(selected_dataset, img[0], img[1], img[2])
            st.write("Images stored successfully!")
        
    else:
        st.write("You haven't chosen any image")

    return i

def store_image_locally(selected_dataset, img, selected_folder, img_name):
    if selected_folder == 'Unlabeled':
        output_dir = f"temp/{selected_folder}"
    else:
        output_dir = f"temp/{selected_dataset}/{selected_folder}"
    output_path = os.path.join(output_dir, img_name)
    img = Image.open(img)
    img.save(output_path)

def store_dataset(img_set):
    " Store a dataset to AWS S3"
    for img in img_set:
        s3_conn.upload_img(img, img.label, img.filename, True)
    st.write("Images stored successfully!")

def move_to_next_page(count_pages, current_page):
    if current_page < count_pages - 1:
        current_page += 1
        st.session_state["current_page"] = current_page
        st.experimental_rerun()

def move_to_previous_page(current_page):
    if current_page > 0:
        current_page -= 1
        st.session_state["current_page"] = current_page
        st.experimental_rerun()

def display_current_page(current_page, selected_folder, img_count, selected_dataset):
    " Selects images for displaying"

    num_cols, images_per_page = 5, 50
    
    with st.container():
        start_idx = current_page * images_per_page
        end_idx = min(start_idx + images_per_page, img_count)
        page_images = fetch_local_imgs(start_idx, end_idx, selected_folder, selected_dataset)

        num_rows = img_count // num_cols + (img_count % num_cols > 0)

        for j in range(num_rows):
            cols = st.columns(num_cols)
            for k in range(num_cols):
                index = j * num_cols + k
                if index < len(page_images):
                    cols[k].image(page_images[index], caption=f"{page_images[index].name}")

def display_images(selected_folder, selected_dataset):
    " Show max 50 images on each page in Data tab"

    images_per_page = 50

    img_count = get_img_count(selected_folder, selected_dataset)
    count_pages = img_count// images_per_page + (img_count % images_per_page > 0)
    current_page = st.session_state.get("current_page", 0)

    button_container = st.container()

    prev_col, page_col, next_col = button_container.columns([1, 1, 1])

    if current_page > 0:
        if prev_col.button("Previous", key=f"Previous"):
            move_to_previous_page(current_page)

    with page_col:
        if count_pages != 0:
            st.write(f"{current_page + 1}/{count_pages}")

    if current_page < count_pages - 1:
        if next_col.button("Next", key=f"Next"):
            move_to_next_page(count_pages, current_page)
    
    display_current_page(current_page, selected_folder, img_count, selected_dataset)

def get_img_count(selected_folder, selected_dataset):
    if selected_folder == 'Unlabeled':
        img_path = f"temp/{selected_folder}"
    else:
        img_path = f"temp/{selected_dataset}/{selected_folder}"

    if not os.path.isdir(img_path):
        os.makedirs(img_path)
    return len(os.listdir(img_path))

def update_stored_images(selected_dataset):
    " Fetching images from AWS/Localstack for viewing or deleting"

    folders = ["0", "1"]

    selected_folder = st.selectbox('Choose a folder', folders)
    if get_img_count(selected_folder, selected_dataset) > 0:
        if st.button(f"Remove images from {selected_folder}", key=f"remove_button_{i}"):
            delete_imgs(selected_dataset, selected_folder)
    
    display_images(selected_folder, selected_dataset)

def delete_imgs(selected_dataset, selected_folder):
    folder_path = f"temp/{selected_dataset}/{selected_folder}"
    files = os.listdir(folder_path)
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        os.remove(file_path)

def fetch_local_imgs(start_idx, end_idx, selected_folder, selected_dataset):
    images = []
    idx = 0
        
    for image in os.listdir(f"temp/{selected_dataset}/{selected_folder}"):
        if idx >= start_idx and idx <= end_idx:
            img = load_img(f"temp/{selected_dataset}/{selected_folder}/{image}")
            img.name = image
            images.append(img)

        idx += 1
        if idx >= end_idx:
            break
    
    return images

def fetch_unlabeled_img(unlabeled_dir):
    images = []
        
    for image in os.listdir(unlabeled_dir):
        img = load_img(f"temp/Unlabeled/{image}")
        img.name = image
        images.append(img)
    
    return images

def label_unlabeled_imgs(i, selected_dataset):
    unlabeled_dir = f"temp/Unlabeled"
    unlabeled_count = get_img_count('Unlabeled', selected_dataset)

    if unlabeled_count > 0:
        with st.expander("Click to label unlabeled images"):
            st.write(f"{unlabeled_count} unlabeled images found")
            unlabeled_imgs = fetch_unlabeled_img(unlabeled_dir)
            i = store_uploaded_images(unlabeled_imgs, i, selected_dataset, unlabeled=True, pil_img=True)
            i += 1


st.set_page_config(
    page_title='Data',
    page_icon='✅',
    layout='wide'
)

if "photo" not in st.session_state:
    st.session_state["photo"] = "not done"

col1, col2, col3 = st.columns([1, 2, 1])

col1.markdown(" # Upload data")


def change_photo_state():
    st.session_state["photo"] = "done"


dataset_names = []
dataset_locations = []
dataset_sizes = []
dataset_descriptions = []

name_column_name = "Dataset_Name"
url_column_name = "Location"
size_column_name = "Size"
description_column_name = "Description"

def upload_csv():
    df = pd.read_csv("dataset.csv")
    name_list = df[name_column_name]
    location_list = df[url_column_name]
    size_list = df[size_column_name]
    description_list = df[description_column_name]

    for name in name_list:
        dataset_names.append(name)
    for location in location_list:
        dataset_locations.append(location)
    for size in size_list:
        dataset_sizes.append(size)
    for description in description_list:
        dataset_descriptions.append(description)

upload_csv()

def load_img(url):
    size = (300, 300)
    img = Image.open(url)
    img = img.resize(size)
    return img

st.header("Available datasets")
with st.expander("Click to choose datasets"):
        for j in range(len(dataset_names)):
            st.write(dataset_names[j],dataset_sizes[j],dataset_descriptions[j])
            btn = st.button("Choose dataset", key=dataset_names[j])
            if btn: 
                st.session_state["selected_dataset"] = f"temp/{dataset_locations[j]}"
                selected_dataset = dataset_locations[j]
                selected_dataset = selected_dataset[: -1]
                s3_conn.download_tar_file(f'{selected_dataset}.tar.gz')
                st.success(f"Selected {dataset_names[j]}")

uploaded_photo = col2.file_uploader(
    "Upload a photo", accept_multiple_files=True, on_change=change_photo_state)
# TODO: kun upload photot on tallennettu, valittuja filejä ei kuuluisi enää näkyä streamlitissä
camera_photo = col2.camera_input("Take a photo", on_change=change_photo_state)

if "selected_dataset" in st.session_state:
    selected_dataset = os.path.basename(st.session_state["selected_dataset"].rstrip('/'))
    i = 0
    if st.session_state["photo"] == "done":
        bar = col2.progress(0)
        for x in range(100):
            bar.progress(x+1)

        col2.success("Photo uploaded successfully")

        if uploaded_photo:
            st.header("Uploaded images")
            with st.expander("Click to see uploaded images"):
                if "selected_dataset" not in st.session_state:
                    st.write('No dataset selected.')
                else:
                    i = store_uploaded_images(uploaded_photo, i, selected_dataset)
                    i += 1

    label_unlabeled_imgs(i, selected_dataset)

    st.header("Stored images")
    update_stored_images(selected_dataset)