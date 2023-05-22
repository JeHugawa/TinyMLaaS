import streamlit as st
import time
import requests
from tflm_hello_world.installing import ArduinoNano33BLE_Installer
from tflm_hello_world.installing import ArducamPico4ML_Installer

# Skip compiling for testing purposes to save time and just use the one in dockerhub
debug_skip_compile = False


devices = {
    "Arducam Pico4ML": {"arch": "ARM", "cpu": "RP2040", "installer": ArducamPico4ML_Installer(), "relay_id": "RPI"},
    "Arduino Nano 33 BLE": {"arch": "ARM", "cpu": "RP2040", "installer": ArduinoNano33BLE_Installer(), "relay_id": "Nano"},
}


def install_settings(selected_model, selected_device):
    st.header("Installation Settings")
    st.write(f"Selected Model: **{selected_model}**")
    st.write(f"Selected Device: **{selected_device}**")


def page_info():
    col = st.columns(4)
    col[0].title("TinyML Install")
    with col[-1].expander("ℹ️ Help"):
        st.markdown(
            "On this page you can generate a device-specific installer of a compiled model, and upload it to a device.")
        st.markdown("Select a connected device and the compiled model you want to use and click the generate button. Once the installer is built,  click the install button to send the model to the device.")
        st.markdown("[See the doc page for more info](/Documentation)")


def install_status(device, model_path):
    installer = device["installer"]
    generate_clicked = st.button("Generate")
    if generate_clicked:

        st.header("Compilation Status")
        with st.spinner("Compiling  image..."):
            if debug_skip_compile == False:
                installer.compile(model_path)
                installer.upload()
            st.session_state["install_compile_done"] = True
            st.success("Compiling done! Uploaded to Dockerhub")

    if st.session_state.get("install_compile_done", False):
        if not "bridge" in st.session_state:
            st.error("No relay server selected. Select one in the device tab.")
            return

        if "dataset_name" not in st.session_state:
            st.error("No dataset was selected. Please select one on the Data page.")
            return

        install_clicked = st.button(
            "Install", disabled=(not "bridge" in st.session_state))
        if install_clicked:
            st.session_state["device"] = selected_device
            with st.spinner("Uploading..."):
                url = st.session_state.bridge+'/install'
                r = requests.post(url, json={'device': device["relay_id"]})
                st.success("Upload done!")


st.set_page_config(page_title="TinyML Install",
                   page_icon=":rocket:", layout='wide')
page_info()

if (not "compiled_models" in st.session_state) or len(st.session_state["compiled_models"].keys()) == 0:
    st.error(
        "There are no compiled models present. Please compile a model in the compiling tab")
else:
    models = st.session_state["compiled_models"]
    selected_model = st.selectbox("Select Model", list(models.keys()))
    selected_device = st.selectbox("Select Device", list(devices.keys()))

    install_settings(selected_model, selected_device)
    install_status(devices[selected_device], models[selected_model])
