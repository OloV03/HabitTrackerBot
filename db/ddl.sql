create database habits;
create schema habits;
create table habits.habit (
    habit_id int8,
    habit_nm varchar,
    created_ts timeStamp
);
create table habits.habit_x_user (
    row_id int4,
    habit_id int8,
    user_id int8,
    created_ts timeStamp
);
create table habits.event (
    row_id int4,
    habit_id int8,
    user_id int8,
    comment_txt varchar,
    event_ts timeStamp,
    changed_ts timeStamp
);