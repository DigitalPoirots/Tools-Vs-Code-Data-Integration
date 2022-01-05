
import datetime
import json
import requests
import psycopg2

# connect to the PSQL DB
print('Connecting to the PSQL DB')
conn = psycopg2.connect('dbname=postgres')
cursor = conn.cursor()

# set the metadata
print('Fetching control information')
start_timestamp = datetime.datetime.now()
cursor.execute('SELECT COALESCE(MAX(batch_id), 0) + 1 as batch_id FROM public.users_cntl')
batch_id = cursor.fetchone()[0]
failed = False

# update control table
print('Updating control table')
cursor.execute('INSERT INTO public.users_cntl(start_timestamp, end_timestamp, flag, batch_id) VALUES(%s, %s, %s, %s)', (start_timestamp, None, 'P', batch_id))

try:
    # extract data
    url = 'http://localhost:8080/users.json'
    req = requests.get(url)

    # load
    # truncate staging table
    print('Truncating stage table')
    cursor.execute('TRUNCATE TABLE public.users_stage')
    # load data to staging table
    for user_data in req.json():
        cursor.execute('INSERT INTO public.users_stage(email,gender,phone_number,birthdate,street,city,state,postcode) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)', (user_data['email'], user_data['gender'], user_data['phone_number'], user_data['birthdate'], user_data['location']['street'], user_data['location']['city'], user_data['location']['state'], user_data['location']['postcode']))

    # transform data and move it to the final table 
    print('Moving data from stage to final')
    cursor.execute('DELETE FROM public.users WHERE email IN (SELECT email FROM public.users_stage)')
    cursor.execute('INSERT INTO public.users SELECT  email, gender, phone_number, to_timestamp(birthdate)::date, street, city, state, postcode, %s, %s FROM public.users_stage', (start_timestamp, batch_id))
except Exception as e:
    # update control table on failure
    failed = True
    print('FAILURE!')
    cursor.execute('UPDATE public.users_cntl SET flag=%s, end_timestamp=%s WHERE batch_id=%s', ('N', datetime.datetime.now(), batch_id))
    print(e)

# update control table on success
if not failed:
    print('SUCCESS!')
    cursor.execute('UPDATE public.users_cntl SET flag=%s, end_timestamp=%s WHERE batch_id=%s', ('Y', datetime.datetime.now(), batch_id))


conn.commit()
cursor.close()
conn.close()

