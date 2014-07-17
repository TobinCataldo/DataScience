# H similarity matrix: Write a query to compute the similarity matrix DDT. (Hint: The transpose is trivial -- just join on columns to columns instead of columns to rows.) 

SELECT docid, term, count FROM frequency WHERE docid='10080_txt_crude'
UNION
SELECT docid, term, count FROM frequency WHERE docid='17035_txt_earn'
# 10080_txt_crude' and '17035_txt_earn'.

SELECT A.docid, B.docid, SUM(A.count * B.count)
FROM 
(
SELECT docid, term, count FROM frequency WHERE docid IN ('10080_txt_crude','17035_txt_earn')
) A,
(
SELECT docid, term, count FROM frequency WHERE docid IN ('10080_txt_crude','17035_txt_earn')
) B
WHERE A.term = B.term
GROUP BY A.docid, B.docid


#SELECT A.row_num, B.col_num, SUM(A.value * B.value)
#FROM A,B
#WHERE A.col_num = B.row_num       
#GROUP BY A.row_num, B.col_num

# I

SELECT * FROM frequency
UNION
SELECT 'q' as docid, 'washington' as term, 1 as count 
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION 
SELECT 'q' as docid, 'treasury' as term, 1 as count


SELECT DocA, DocB, Counts
FROM (
    SELECT A.docid as DocA, B.docid as DocB , SUM(A.count * B.count) as Counts
    FROM 
    (
        SELECT * FROM frequency
        UNION
        SELECT 'q' as docid, 'washington' as term, 1 as count 
        UNION
        SELECT 'q' as docid, 'taxes' as term, 1 as count
        UNION 
        SELECT 'q' as docid, 'treasury' as term, 1 as count
    ) A,
    (
        SELECT * FROM frequency
        UNION
        SELECT 'q' as docid, 'washington' as term, 1 as count 
        UNION
        SELECT 'q' as docid, 'taxes' as term, 1 as count
        UNION 
        SELECT 'q' as docid, 'treasury' as term, 1 as count
    ) B
    WHERE A.term = B.term
    GROUP BY A.docid, B.docid
    ) 
WHERE DocA = 'q' 
ORDER BY Counts ASC


 # 6