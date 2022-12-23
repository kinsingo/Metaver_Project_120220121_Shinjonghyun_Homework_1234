import numpy as np
import argparse
import os
from os import path

# ToDo 1: set path to this folder for importing PyMo properly


from motion_visualizer.model_animator import create_video
from motion_visualizer.convert2bvh import Get_Motions_After_Writing_bvh

from pymo.writers import *

def Get_Motions_After_Creating_bvh(motion_in, bvh_file, data_pipe_dir):
    return Get_Motions_After_Writing_bvh((data_pipe_dir,), motion_in, bvh_file, 20)

def generate_videos(raw_input_folder, output_folder, run_name, data_pipe_dir, start_t=0, end_t=10):
# Go over all the results we have
    for filename in os.listdir(raw_input_folder):
        filepath = path.join(raw_input_folder, filename)
        # TODO: the newlines are only there so that the joblib warning doesn't hide these prints
        print("\nCurrent file:", filename, end='\n\n') 
        if os.path.isfile(filepath):
            motion = np.load(filepath)
        else:
            error_msg = \
            f"""The given input folder does not contain the expected raw data ({filename}),
            please run `python generate_videos.py --help` for instructions."""
            
            raise ValueError(error_msg)


        # shorten
        motion = motion[:1200]

        resulting_bvh_file   = output_folder + "/" +  filename + ".bvh"
        resulting_npy_file   = output_folder + "/" + filename +"_3d.npy"
        resulting_video_file = output_folder + "/" + filename + ".mp4"

        Get_Motions_After_Writing_bvh(motion,
                                      resulting_bvh_file,
                                      resulting_npy_file,
                                      resulting_video_file,
                                      start_t,
                                      end_t,
                                      data_pipe_dir)

        os.remove(resulting_bvh_file)
        os.remove(resulting_npy_file)

def create_arg_parser():
    parser = argparse.ArgumentParser(description="Generate videos from the motion that is represented by exponential maps")
    
    parser.add_argument("--start_t", "-st", default=0, 
                        help="Start time for the sequence")
    parser.add_argument("--end_t", "-end", default=10, 
                        help="End time for the sequence")
    parser.add_argument("--raw_input_folder", "-in", default=None,
                        help="""The folder that contains the motion input (represented with exponential maps) for creating the videos
                             (default: ../../../results/<run_name>/generated_gestures/test/raw_gestures)""")
    parser.add_argument("--output_folder", "-out", default=None,
                        help="""The folder where the generated videos will be saved
                             (default: ../../../results/<run_name>/test_videos/)""")
    parser.add_argument("--run_name", "-run", default="last_run",
                        help="""If the results were saved in the default folders during training,
                             the input/output folders for generating the videos can be inferred from this parameter.""")
    parser.add_argument("--data_pipe_dir", "-pipe", type=str, default="../../utils/data_pipe.sav",
                        help="Temporary pipe file used during conversion")
    
    return parser


if __name__ == "__main__":
    # Parse command line params
    args = create_arg_parser().parse_args()

    if args.raw_input_folder is None:
        args.raw_input_folder = f"../../../results/{args.run_name}/generated_gestures/test/raw_gestures/"
    
    if args.output_folder is None:
        args.output_folder = f"../../../results/{args.run_name}/generated_gestures/test/manually_generated_videos"
        os.makedirs(args.output_folder, exist_ok=True)

    generate_videos(**vars(args))
   
    """
    # Visualize training data
    raw_data_folder = "/home/taras/Documents/Datasets/SpeechToMotion/Irish/processed/Test/test/labels"

    results_folder = "/home/taras/Desktop/Work/Code/Git/AAMAS2020/gesticulator/log/gestures/train/"

    for epoch in range(2, 10, 2):
        # ToDo 3: here you should set the path to the sequences which the model produces (which should be saved as npy)
        motion = np.load(raw_data_folder + "NaturalTalking_0" +str(epoch) + "_raw.npz")['clips']

        # shorten
        motion = motion[:1200]

        # ToDo 4: define files where you want to store the resulting gesture, the most important one is the video
        resulting_bvh_file = results_folder + "result_ep" + str(epoch) + ".bvh"
        resulting_npy_file = results_folder + "result_ep" + str(epoch) + ".npy"
        resulting_video_file = results_folder + "result_ep" + str(epoch) + ".mp4"

        visualize(
            motion,
            resulting_bvh_file,
            resulting_npy_file,
            resulting_video_file,
            args.start_t,
            args.end_t,
        )
        
    """
