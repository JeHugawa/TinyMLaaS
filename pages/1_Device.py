import streamlit as st
import pandas as pd
# Define the list of steps and their statuses
import usb.core
import usb.util
import requests

st.set_page_config(
    page_title='Device',
    page_icon='✅',
    layout='wide'
)


def page_info(title):
    col = st.columns(4)
    col[0].title(title)
    with col[-1].expander("ℹ️ Help"):
        st.markdown("On this page you can connect to a bridging device.")
        st.markdown(
            "It will eventually also show an overview of connected devices.")
        st.markdown("[See the doc page for more info](/Documentation)")


state = st.session_state

ACCEPTED_VENDORS = ["Raspberry Pi", "Arduino"]


def get_id_max():
    df = pd.read_csv("TinyMLaaS.csv")
    return df["id"].astype(int).max() + 1


def add():
    new_device_data = {
        "id": [get_id_max()],
        "Device name": [state.device_name],
        "Connection": [state.connection],
        "Installer": [state.installer],
        "Compiler": [state.compiler],
        "Model": [state.model],
        "Description": [state.description]
    }
    df = pd.DataFrame(new_device_data)
    with open("TinyMLaaS.csv", "a") as f:
        f.write("\n")
    df.to_csv("TinyMLaaS.csv", mode="a", header=False, index=False)
    st.info("Added new data")


def delete(df, id):
    df = df[~df['id'].isin([id])]
    df.to_csv("TinyMLaaS.csv", mode="w", index=False)
    st.success(f"Device #{id} removed.")


def modify(df, id):
    df = df[~df['id'].isin([id])]
    new_device_data = {
        "id": [id],
        "Device name": [state.device_name],
        "Connection": [state.connection],
        "Installer": [state.installer],
        "Compiler": [state.compiler],
        "Model": [state.model],
        "Description": [state.description]
    }
    df_modified = pd.DataFrame(new_device_data)
    df = pd.concat([df, df_modified], ignore_index=True)
    df.to_csv("TinyMLaaS.csv", mode="w", index=False)
    st.warning(f"Device #{id} modified")


def handle_add(manufacturer="", product="", serial=""):
    with st.form("new_device"):
        st.write("Add a new device")
        st.text_input("Device name", key="device_name", value=manufacturer)
        st.text_input("Connection", key="connection")
        st.text_input("Installer", key="installer")
        st.text_input("Compiler", key="compiler")
        st.text_input("Model", key="model", value=product)
        st.text_input("Description", key="description")

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.form_submit_button(label='Add', on_click=add)
        col6.form_submit_button(label='Cancel')


def handle_modify(df, id, name, connection, installer, compiler, model, description):
    with st.form("modify_device"):
        st.write("Modify a device")
        st.text_input("Device name", value=name, key="device_name")
        st.text_input("Connection", value=connection, key="connection")
        st.text_input("Installer", value=installer, key="installer")
        st.text_input("Compiler", value=compiler, key="compiler")
        st.text_input("Model", value=model, key="model")
        st.text_input("Description", value=description, key="description")

        st.form_submit_button("Cancel")
        st.form_submit_button(
            "Modify Device", on_click=modify, args=(df, id,))


def handle_select(id, name, connection, installer, compiler, model, description):
    "Stores data of selected device to session state for other pages to use"
    device_data = {
        "id": id,
        "Device name": name,
        "Connection": connection,
        "Installer": installer,
        "Compiler": compiler,
        "Model": model,
        "Description": description
    }
    state.selected_device = device_data
    st.success(f"Selected device: **{name}**")


def list_devices():

    st.header('All registered devices')
    df = pd.read_csv('TinyMLaaS.csv')
    # Device name, Connection, Installer, Compiler, Model, Description
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)

    for row in df.sort_values("id").itertuples():
        index, id, name, connection, installer, compiler, model, description = row
        col = st.columns(10)
        col[0].write(id)
        # make selected device name bold
        if "selected_device" in state and state.selected_device["id"] == id:
            col[1].write("**"+name+"**")
        else:
            col[1].write(name)
        col[2].write(connection)
        col[3].write(installer)
        col[4].write(compiler)
        col[5].write(model)
        col[6].write(description)
        col[7].button("Delete", key=name, on_click=delete, args=(df, id))
        col[8].button("Modify", key=f'm_{name}', on_click=handle_modify, args=(
            df, id, name, connection, installer, compiler, model, description))
        col[9].button("Select", key=f"s_{name}", on_click=handle_select, args=(
            id, name, connection, installer, compiler, model, description))


def list_connected_devices():
    st.header("All connected devices")

    st.button("Refresh", key="refresh")

    # List all connected devices
    devices = list(usb.core.find(find_all=True))

    # Check if device is in ACCEPTED VENDORS
    st.write(":red[Should show only raspberries or arduinos, does not work]")
    for device in devices:
        try:
            if usb.util.get_string(device, device.iManufacturer) not in ACCEPTED_VENDORS:
                devices.remove(device)
        except:
            devices.remove(device)
            continue

    col1, col2, col3, col4 = st.columns(4)

    if devices:
        for i, device in enumerate(devices, start=1):
            # Try / Except if any error occurs
            try:
                manufacturer = usb.util.get_string(
                    device, device.iManufacturer)
                product = usb.util.get_string(device, device.iProduct)
                serial = usb.util.get_string(device, device.iSerialNumber)

                if manufacturer is not None:
                    col1.write(manufacturer)
                    col2.write(product)
                    col3.write(serial)
                    col4.button("register this device", key=i, on_click=handle_add, args=(
                        manufacturer, product, serial))
            except Exception as e:
                # Placeholder
                st.write("Error: " + str(e))
                continue
    else:
        st.write("No devices found")


def device_page():
    page_info('Device')
    st.header('Register a device')

    st.button("register a new device", key="add_button", on_click=handle_add)

    with st.expander("Register a bridging device", expanded=False):
        ip_addr = st.text_input('IP address of the bridging server')
        register = st.button('Add')

        if register:
            try:
                response = requests.get(ip_addr)
                st.success("Bridging device registered successfully! 🔥")
                st.session_state.bridge = str(ip_addr)
            except:
                st.error('Invalid ip address for the bridging device 🚨')
                response = ""

    list_connected_devices()
    list_devices()


device_page()
