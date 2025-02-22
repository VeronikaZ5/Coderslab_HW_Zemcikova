-- Client analysis - part 1
-- Who has more repaid loans - women or men?
-- What is the average age of the borrower divided by gender?

DROP TABLE IF EXISTS gender_repaid_loans;
create temporary table gender_repaid_loans (
    select
        c.gender,
        sum(l.amount) as amount_of_repaid_loans,
        count(l.loan_id) as number_of_loans,
        round(avg(2024 - (extract(YEAR from c.birth_date))), 0) as average_year
    from loan l
    join account a on l.account_id = a.account_id
    join disp d on a.account_id = d.account_id
    join client c on d.client_id = c.client_id
    where (l.status = 'A' or l.status = 'C') and d.type = 'OWNER'
    group by c.gender
);
select *
from gender_repaid_loans;

-- Client analysis - part 2
-- Select only owners of accounts as clients.

DROP TABLE IF EXISTS district_data;
create temporary table district_data (
    select
        d.A2 as district_names,
        count(distinct c.client_id) as number_of_clients,
        count(l.loan_id) as number_of_repaid_loans,
        sum(l.amount) as total_amount_of_loans
    from district d
    join client c on d.district_id = c.district_id
    join disp dp on c.client_id = dp.client_id
    join account a on dp.account_id = a.account_id
    join loan l on a.account_id = l.account_id
    where (l.status = 'A' or l.status = 'C') and dp.type = 'OWNER'
    group by A2
    order by number_of_clients
)

-- Which area has the most clients?
select *
from district_data
order by number_of_clients desc limit 1;

-- In which area the highest number of loans was paid?,
select *
from district_data
order by number_of_repaid_loans desc limit 1;

-- In which area the highest amount of loans was paid?
select *
from district_data
order by total_amount_of_loans desc limit 1;


-- Client analysis - part 3
-- Use the query created in the previous task and modify it to determine the percentage of each district in the total amount of loans granted.

with loan_percentage as (
    select
        d.A2 as district_names,
        count(distinct c.client_id) as number_of_clients,
        count(l.loan_id) as number_of_repaid_loans,
        sum(l.amount) as total_amount_of_loans
    from district d
    join client c on d.district_id = c.district_id
    join disp dp on c.client_id = dp.client_id
    join account a on dp.account_id = a.account_id
    join loan l on a.account_id = l.account_id
    where (l.status = 'A' or l.status = 'C') and dp.type = 'OWNER'
    group by d.A2
)
select
    *,
    total_amount_of_loans / sum(total_amount_of_loans) over () as percentage_of_total_loans,
    concat(round((total_amount_of_loans * 100) / sum(total_amount_of_loans) over (), 2), '%') as percentage
from loan_percentage
order by percentage_of_total_loans desc;

-- Selection - part 1
-- check the database for clients who meets these conditions:
-- their account balance is above 1000,
-- they have more than 5 loans,
-- they were born after 1990

select
    c.client_id,
    sum(l.amount - l.payments) as account_balance,
    count(distinct l.loan_id) as number_of_loans
from client c
join disp d on c.client_id = d.client_id
join account a on d.account_id = a.account_id
join loan l on a.account_id = l.account_id
where (l.status = 'A' or l.status = 'C') and d.type = 'OWNER' and c.birth_date >= '1990-01-01'
group by c.client_id
having sum(l.amount - l.payments) > 1000 and count(distinct l.loan_id) > 5;

-- Selection - part 2
-- Make an analysis to determine which condition caused the empty results.

select *
from client
where birth_date >= '1990-01-01';

select
    c.client_id,
    count(distinct l.loan_id) as number_of_loans
from client c
join disp d on c.client_id = d.client_id
join account a on d.account_id = a.account_id
join loan l on a.account_id = l.account_id
group by c.client_id
having count(distinct l.loan_id) > 5;

-- Expiring cards

select
    cl.client_id,
    c.card_id,
    date_add(c.issued, interval 3 year) as expiration_date,
    date_sub(date_add(c.issued, interval 3 year), interval 7 day) as week_before_expiration,
    ds.a3
from card c
join disp d on c.disp_id = d.disp_id
join client cl on d.client_id = cl.client_id
join district ds on cl.district_id = ds.district_id
order by week_before_expiration desc;