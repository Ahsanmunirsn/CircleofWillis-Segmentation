"""
The following is a simple example algorithm for task 1: CoW multi-class segmentation.

It can be run locally (good for setting up and debugging your algorithm)
or in a docker container (required for submission to grand-challenge.org).

If you use this template you can simply replace the `your_segmentation_algorithm` function with your own algorithm.
The suggested inputs are np.arrays of the MR and CT images respectively, the output is your segmentation prediction array.

To run your algorithm, execute the `inference.py` script (inference.py is the entry point for the docker container).
NOTE: You don't need to change anything in the inference.py script!

The relevant paths are as follows:
    input_path: contains the input images inside the folders /images/head-mr-angio or /images/head-ct-angio
        Docker: /input
        Local: ./test/input
    output_path: output predictions are stored inside the folder /images/cow-multiclass-segmentation
        Docker: /output
        Local: ./test/output
    resource_path: any additional resources needed for the algorithm during inference can be stored here (optional)
        Docker: resources
        Local: ./resources

Before submitting to grand-challenge.org, you must ensure that your algorithm runs in the docker container. To do this, run
  ./test_run.sh
This will start the inference and reads from ./test/input and outputs to ./test/output

To save the container and prep it for upload to Grand-Challenge.org you can call:
  ./save.sh
"""
from pathlib import Path
import subprocess
import numpy as np
from glob import glob
import SimpleITK as sitk
#######################################################################################
# TODO-1:
# Choose your TRACK. Track is either 'MR' or 'CT'.
TRACK = "CT"  # or 'MR'
# END OF TODO-1
#######################################################################################


def your_segmentation_algorithm(
    *, mr_input_array: np.array, ct_input_array: np.array
) -> np.array:
    """
    This is an example of a prediction algorithm.
    It is a dummy algorithm that returns an array of the correct shape with randomly assigned integers between 0 and 12.
    args:
        mr_input_array: np.array - input image for MR track
        ct_input_array: np.array - input image for CT track
    returns:
        np.array - prediction
    """

    #######################################################################################
    # TODO-2: place your own prediction algorithm here.
    # You are free to remove everything! Just return to us an npy in (x,y,z).
    # You can use the input_head_mr_angiography and/or input_head_ct_angiography
    # to make your prediction.

    # NOTE: the prediction array must have the same shape as the input image of the chosen track!

    # NOTE: If you extract the array from SimpleITK, note that
    #              SimpleITK npy array axis order is (z,y,x).
    #              Then you might have to transpose this to (x,y,z)

    #######################################################################################

    # load and initialize your model here
    # model = ...
    # device = ...

    # You can also place and load additional files in the resources folder
    # with open(resources / "some_resource.txt", "r") as f:
    #     print(f.read())

    # For now, let us set make bogus predictions
    output_shape = tuple()
    if TRACK == "CT":
        input_path = Path("/input/images/head-ct-angio")
        input_file = (glob(str(input_path / "*.mha")) + glob(str(input_path / "*.nii.gz")))[0]  # There is just one file in the input folder!
        if input_file.endswith(".mha"):
            mha_image = sitk.ReadImage(input_file)
            # Convert and save it as .nii.gz
            sitk.WriteImage(mha_image, input_file.replace(".mha", ".nii.gz"))
        command = [
            "nnUNetv2_predict",
            "-d", "Dataset001_BrainCoW",
            "-i", "/input/images/head-ct-angio",
            "-o", "/output/images/cow-multiclass-segmentation",
            "-c", "3d_fullres",
            "-tr", "nnUNetTrainer",
            "-p", "nnUNetPlans",
        ]
        try:
            subprocess.run(command, check=True)
            print("Prediction completed successfully.")
            output_path = Path("/output/images/cow-multiclass-segmentation")
            output_file = (glob(str(output_path / "*.mha")) + glob(str(output_path / "*.nii.gz")))[0]  # There is just one file in the input folder!
            if input_file.endswith(".mha"):
                out_image = sitk.ReadImage(output_file)
                # Convert and save it as .mha
                sitk.WriteImage(out_image, output_file.replace(".nii.gz", ".mha"))
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
        output_shape = ct_input_array.shape
    elif TRACK == "MR":
        output_shape = mr_input_array.shape
    else:
        raise ValueError("Invalid TRACK chosen. Choose either 'MR' or 'CT'.")

    pred_array = np.ones(output_shape)

    return pred_array
