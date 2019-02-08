type=linuxfs
dataset_name=linuxfs
data_dir=data/${dataset_name}
data=${data_dir}/${dataset_name}
test_data=${data_dir}/${dataset_name}.val.c2v
model_dir=models/${type}

python cpredict.py $1 --load ${model_dir}/saved_model

