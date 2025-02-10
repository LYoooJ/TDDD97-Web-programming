create table userinfo(
    email text not null primary key,
    password text,
    firstname text,
    familyname text,
    gender text,
    city text,
    country text
);

create table loggedInUsers(
    email text not null primary key,
    token text
);

create table messages(
    fromemail text,
    toemail text,
    msg text
);
