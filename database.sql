create table passenger
(
    id         serial
        primary key,
    name       varchar(50)    not null,
    total_cost real default 0 not null
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
    available  boolean default true not null,
    ppk        real    default 1    not null
);

alter table taxi
    owner to postgres;

create table "order"
(
    id           serial,
    start_x      real not null,
    start_y      real,
    end_x        real,
    end_y        real,
    distance     real,
    cost         real,
    passenger_id integer
        constraint passenger_id
            references passenger,
    taxi_id      integer
        constraint taxi_id
            references taxi
);

alter table "order"
    owner to postgres;

create table offer
(
    id           serial,
    distance_min real,
    distance_max real,
    percent      real
);

alter table offer
    owner to postgres;

