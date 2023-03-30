# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/compiling.ipynb.

# %% auto 0
__all__ = ['convert_model', 'convert_to_c_array', 'plot_size']

# %% ../nbs/compiling.ipynb 1
import subprocess
import tensorflow as tf
import os
import pandas as pd

# %% ../nbs/compiling.ipynb 2
import binascii


def convert_model(train_ds):
    """Model conversion into TFLite model

    Args:
        train_ds (_dataset_): Training data used for the quantization process
    """

    model = 'models/keras_model'

       
    # Convert the model to the TensorFlow Lite format without quantization
    converter = tf.lite.TFLiteConverter.from_saved_model(model)
    model_no_quant_tflite = converter.convert()
    # Save the model to disk
    open('models/model_no_quant.tflite', "wb").write(model_no_quant_tflite)

    # Convert the model with quantization.
    converter = tf.lite.TFLiteConverter.from_saved_model(model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.int8
    converter.inference_output_type = tf.int8

    def representative_dataset():
        for images, labels in train_ds.take(96):
            for img in images:
                input = tf.cast(img, tf.float32)
                input = tf.reshape(input, [1,96,96])
                yield([input])

    converter.representative_dataset = representative_dataset
    tflite_model = converter.convert()

    # Save the model.
    with open('models/model.tflite', 'wb') as f:
        f.write(tflite_model)

def convert_to_c_array(bytes)->str:
    """C array conversion

    Args:
        model_file_name (string): TFLite model name for the conversion command
    """
    hexstr = binascii.hexlify(bytes).decode("UTF-8") 
    hexstr = hexstr.upper() 
    array = ["0x" + hexstr[i:i + 2] for i in range(0, len(hexstr), 2)] 
    array = [array[i:i+10] for i in range(0, len(array), 10)] 
    return ",\n  ".join([", ".join(e) for e in array])

def plot_size():
    """Plots the size difference before and after quantization

    Returns:
        pandas dataframe: Pandas dataframe containing information
    """

    size_no_quant_tflite = os.path.getsize('models/model_no_quant.tflite')
    size_tflite = os.path.getsize('models/model.tflite')
    
    frame = pd.DataFrame.from_records(
        [["TensorFlow Lite", f"{size_no_quant_tflite} bytes "],
        ["TensorFlow Lite Quantized", f"{size_tflite} bytes", f"{size_no_quant_tflite - size_tflite} bytes"]],
        columns = ["Model", "Size", "Size Reduced"], index="Model")

    return frame

