# type=$1
# dataset_name=$1
# data_dir=data/${dataset_name}
# data=${data_dir}/${dataset_name}
# test_data=${data_dir}/${dataset_name}.val.c2v
# model_dir=models/${type}

# data_dir=$1
# temp_list=(${data_dir//// })
# type=${temp_list[-1]}
# dataset_name=${temp_list[-1]}

# data=${data_dir}/${dataset_name}
# test_data=${data_dir}/${dataset_name}.val.c2v
cfile=$1
model_dir=$2
python cpredict.py ${cfile} --load ${model_dir}/saved_model

