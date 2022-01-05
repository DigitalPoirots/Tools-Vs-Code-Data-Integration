target_dir=$1
env_name=$2

python3 -m venv "$env_name";
source "$target_dir/$env_name/bin/activate";
"$target_dir/$env_name/bin/pip3" install pandas;
"$target_dir/$env_name/bin/pip3" install psycopg2;
"$target_dir/$env_name/bin/pip3" install requests;
"$target_dir/$env_name/bin/pip3" freeze > "$target_dir/requirements.txt";
