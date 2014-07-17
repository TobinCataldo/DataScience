# A  σ10398_txt_earn(frequency)
SELECT * FROM frequency WHERE docid = '10398_txt_earn';
SELECT COUNT(*) FROM frequency WHERE docid = '10398_txt_earn';
# 138

# B πterm(σdocid=10398_txt_earn and count=1(frequency))
SELECT term FROM frequency WHERE docid =  '10398_txt_earn' AND count = 1;  
SELECT COUNT(term) FROM frequency WHERE docid =  '10398_txt_earn' AND count = 1;
# 110

# C πterm(σdocid=10398_txt_earn and count=1(frequency)) U πterm(σdocid=925_txt_trade and count=1(frequency))
SELECT term FROM frequency WHERE docid =  '10398_txt_earn' AND count = 1
UNION
SELECT term FROM frequency WHERE docid =  '925_txt_trade' AND count = 1;

SELECT COUNT(term) FROM
(SELECT term FROM frequency WHERE docid =  '10398_txt_earn' AND count = 1
UNION
SELECT term FROM frequency WHERE docid =  '925_txt_trade' AND count = 1) as b
# 324

# D (d) count: Write a SQL statement to count the number of documents containing the word "parliament"
SELECT COUNT(*) FROM frequency WHERE term = 'parliament';
# 15

# E (e) big documents Write a SQL statement to find all documents that have more than 300 total terms, including duplicate terms. 
SELECT docid, c
FROM (SELECT docid, SUM(count) as c FROM frequency GROUP BY docid) b
WHERE b.c > 300;

SELECT count(*)
FROM (SELECT docid, SUM(count) as c FROM frequency GROUP BY docid) b
WHERE b.c > 300;
# 107

# Write a SQL statement to count the number of unique documents that contain both the word 'transactions' and the word 'world'.
SELECT docid FROM frequency WHERE term = 'world'
INTERSECT
SELECT docid FROM frequency WHERE term = 'transactions'

# 3 records 