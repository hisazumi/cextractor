type=$1
dataset_name=$1
data_dir=data/${dataset_name}
data=${data_dir}/${dataset_name}
test_data=${data_dir}/${dataset_name}.val.c2v
model_dir=models/${type}

python cpredict.py $2 --load ${model_dir}/saved_model

