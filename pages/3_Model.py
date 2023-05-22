
import streamlit as st
import pandas as pd
import cv2
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import load_model


st.set_page_config(
    page_title='Model',
    page_icon='✅',
    layout='wide'
)


def page_info(title):
    col = st.columns(4)
    col[0].title(title)
    with col[-1].expander("ℹ️ Help"):
        st.markdown("On this page you can select a model for training")
        st.markdown(
            "Currently this only selects the model path, and only the default one is valid")
        st.markdown("[See the doc page for more info](/Documentation)")


def save_selections(category, model, model_data):
    st.session_state["selected_model_type"] = model
    st.session_state["selected_model_category"] = category
    st.session_state["selected_model"] = model_data
    st.info("Your selections have been saved", icon="✅")


def visualize(model_meta, model_path):
    try:
        path = f'{model_path}/keras_model.h5'
        model = load_model(path)
        plot_model(model, to_file=f"{model_path}/model.png", show_shapes=True)
        image = cv2.imread(f"{model_path}/model.png")
        st.image(image)
    except:
        st.error("No model found")


def model_page():
    page_info("Model")

    models_df = read_file_with_models()

    if "selected_model" in st.session_state:  # select selected model by default in radiobuttons
        category = st.session_state["selected_model_category"]
        model_type = st.session_state["selected_model_type"]
        default_category_id = models_df["Models"].keys().get_loc(category)
        default_model_id = list(
            models_df["Models"][category].keys()).index(model_type)
    else:
        default_category_id = 0
        default_model_id = 0

    print(models_df)
    # Display the models?
    col1, col2, col3 = st.columns(3)
    st.write(":red[Options hard coded]")
    category = col1.radio('Select a category: ',
                          models_df['Models'].keys(), index=default_category_id)

    if category:
        models = models_df['Models'][category]
        if st.session_state.get("selected_model_category", None) != category:
            default_model_id = 0

        select_model = col2.radio("Select a model:", list(
            models.keys()), index=default_model_id)

        if select_model:
            st.markdown(
                f" You have selected: **{select_model}** submodel under **{category}** model")

            table = "| Field | Description |\n| --- | --- | \n"
            for key, item in models[select_model].items():

                table += f"| {key} | {item} \n"

            st.markdown(table)

    col3.button("Select", on_click=save_selections, kwargs={
                "model_data": models[select_model], "category": category, "model": select_model})
    col3.button("Visualize", on_click=visualize, kwargs={
                'model_meta': models[select_model], "model_path": models[select_model]["Model Path"]})
    col3.markdown(
        ":red[Does nothing. Has the ability to do something, but can't do it]")


def read_file_with_models():
    "Reads csv file that has the models and sets it to pandas dataframe "
    models_df = pd.read_json('pages/models.json')
    return models_df


model_page()
