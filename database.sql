create table passenger
(
    id         serial
        primary key,
    name       varchar(50)       not null,
    total_cost integer default 0 not null
);

alter table passenger
    owner to postgres;

create table taxi
(
    id         serial
        primary key,
    model      varchar(50)          not null,
    position_x real                 not null,
    position_y real                 not null,
    available  boolean default true not null
);

alter table taxi
    owner to postgres;
