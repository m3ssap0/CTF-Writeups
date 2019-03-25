create database webn;
create table users (id int auto_increment primary key, login varchar(100), password varchar(100), role boolean default 0);
create table posts (id int auto_increment primary key, title varchar(50), content text, date Date, author varchar(100));
