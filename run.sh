#!/bin/bash -l

#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --gres=gpu:rtx2080ti:1
#SBATCH --time=01:00:00           
#SBATCH --job-name=test

module load python
conda activate mynewenv
nnUNetv2_predict -d Dataset001_BrainCoW -i test/input/images/head-ct-angio -o test/output/images/cow-multiclass-segmentation -f 1 -c 3d_fullres -tr nnUNetTrainer

#nnUNetv2_predict -d Dataset001_BrainCoW -i prediction/test/input -o prediction/test/output -f 1 -tr nnUNetTrainer -c 3d_fullres -p nnUNetPlans

#nnUNetv2_predict -d Dataset001_BrainCoW -i input/images/head-ct-angio -o output/images/cow-multiclass-segmentation -tr nnUNetTrainer -c 3d_fullres -p nnUNetPlans

#nnUNetv2_evaluate_folder -djfile prediction/evaluation/dataset.json -pfile prediction/evaluation/plans.json -np 8 --chill prediction/evaluation/imagesGT prediction/evaluation/predictedImages


#nnUNetv2_apply_postprocessing -i prediction/ensemble -o prediction/postprocessed -pp_pkl_file nnUNet_results/Dataset001_BrainCoW/nnUNetTrainer__nnUNetPlans__3d_fullres/crossval_results_folds_0_1_2_3_4/postprocessing.pkl -np 8 -plans_json nnUNet_results/Dataset001_BrainCoW/nnUNetTrainer__nnUNetPlans__3d_fullres/crossval_results_folds_0_1_2_3_4/plans.json -dataset_json nnUNet_results/Dataset001_BrainCoW/nnUNetTrainer__nnUNetPlans__3d_fullres/crossval_results_folds_0_1_2_3_4/dataset.json


#nnUNetv2_ensemble -i prediction/fold_0 prediction/fold_1 prediction/fold_2 prediction/fold_3 prediction/fold_4 -o prediction/ensemble -np 8

#nnUNetv2_predict -d Dataset001_BrainCoW -i nnUNet_raw/Dataset001_BrainCoW/imagesTs -o prediction/fold_4 -f  4 -tr nnUNetTrainer -c 3d_fullres -p nnUNetPlans --save_probabilities


#nnUNetv2_predict -i nnUNet_raw/Dataset001_BrainCoW/imagesTs -o prediction/fold_4  -d 001 -c 3d_fullres -f 4 --save_probabilities

#nnUNetv2_find_best_configuration 001 -c 3d_fullres

#CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 001 3d_fullres 0 &
#CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 001 3d_fullres 1 &
#CUDA_VISIBLE_DEVICES=2 nnUNetv2_train 001 3d_fullres 2 &
#CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 3d_fullres 3 &
#CUDA_VISIBLE_DEVICES=4 nnUNetv2_train 001 3d_fullres 4
#wait

#nnUNetv2_train 001 3d_fullres 2

#nnUNetv2_plan_and_preprocess -d 001 -c 3d_fullres --verify_dataset_integrity

