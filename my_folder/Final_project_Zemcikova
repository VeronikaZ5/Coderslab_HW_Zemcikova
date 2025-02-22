-- History of granted loans
select extract(YEAR from date)    as loan_year,
       extract(QUARTER from date) as loan_quarter,
       extract(MONTH from date)   as loan_month,
       sum(amount) as loans_total,
       round(avg(amount), 2) as loans_avg,
       count(amount) as loans_count
from loan
group by extract(YEAR from date), extract(QUARTER from date), extract(MONTH from date) with rollup
order by loan_year;


-- Loan status
select status, count(loan_id) as number_of_loans
from loan
group by status;


-- Analysis of accounts
select
    a.account_id,
    count(loan_id) as number_of_given_loans,
    sum(amount) as amount_of_given_loans,
    round(avg(amount), 0) as average_loan_amount
from loan l
join account a on l.account_id = a.account_id
where status = 'A' or status = 'C'
group by a.account_id
order by number_of_given_loans desc, amount_of_given_loans desc;


-- Fully paid loans
select
    c.gender,
    sum(l.amount) as amount_of_repaid_loans
from loan l
join account a on l.account_id = a.account_id
join disp d on a.account_id = d.account_id
join client c on d.client_id = c.client_id
where l.status = 'A' or l.status = 'C' and d.type = 'OWNER'
group by c.gender;

-- checking if the query is correct
with balance_gender as (
    select
        c.gender,
        sum(l.amount) as amount_of_repaid_loans
    from loan l
    join account a on l.account_id = a.account_id
    join disp d on a.account_id = d.account_id
    join client c on d.client_id = c.client_id
    where (l.status = 'A' or l.status = 'C') and d.type = 'OWNER'
    group by c.gender
), repaid_loans_amount as (
    select sum(amount) as sum_of_repaid_loans
    from loan
    where status = 'A' or status = 'C'
)
select
    case
        when sum(amount_of_repaid_loans) = max(sum_of_repaid_loans) then 'TRUE'
        else 'FALSE'
    end as 'result'
from balance_gender
cross join repaid_loans_amount;




