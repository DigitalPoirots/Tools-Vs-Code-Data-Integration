create table public.users_cntl(
	start_timestamp timestamp,
	end_timestamp timestamp,
	flag varchar(1),
	batch_id int
);


create table public.users_stage(
	email varchar(100) primary key,
	gender varchar(10),
	phone_number varchar(20),
	birthdate bigint,
	street varchar(100),
	city varchar(100),
	state varchar(100),
	postcode varchar(10)
);


create table public.users(
	email varchar(100) primary key,
	gender varchar(10),
	phone_number varchar(20),
	birthdate date,
	street varchar(100),
	city varchar(100),
	state varchar(100),
	postcode varchar(10),
	last_updated_timestamp timestamp default now(),
	batch_id int
);

select * from public.users_cntl

select count(*) from public.users_stage

select * from public.users

