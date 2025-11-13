select distinct(terpene) from terpeneresults  order by terpene--where dispensaryid =2
select distinct(Cannabinoid) from cannabinoidResults  order by Cannabinoid--where dispensaryid =2

select distinct(batch), created from cannabinoidResults where dispensaryid =2
select distinct(batch),  created from terpeneResults where dispensaryid =2 
select distinct(name), created from batch where GrowerID =2

-- Delete specific batches from cannabinoidResults
DELETE FROM cannabinoidResults 
WHERE  dispensaryId =2 

DELETE FROM terpeneResults 
WHERE  dispensaryId =2 
DELETE FROM Batch
WHERE  growerid =2 

-- Extract date from datetime column examples:
-- Method 1: Using CAST (recommended for SQL Server 2008+)
--SELECT distinct(batch), CAST(created AS DATE) AS created 
SELECT  *
FROM Batch 
WHERE GrowerID = 2
order by created

SELECT *
FROM cannabinoidResults 
WHERE dispensaryid = 2
order by created

-- Method 2: Using CONVERT (alternative method)
--SELECT distinct(batch), CONVERT(DATE, created) AS created 
SELECT *
FROM terpeneResults 
WHERE dispensaryid = 2
order by created

-- Method 3: Format as string in YYYY-MM-DD format
SELECT distinct(batch), FORMAT(created, 'yyyy-MM-dd') AS created_date_string 
FROM terpeneResults 
WHERE dispensaryid = 2

-- Method 4: Remove time by converting to midnight of same day
SELECT distinct(batch), DATEADD(dd, 0, DATEDIFF(dd, 0, created)) AS created_date_midnight 
FROM terpeneResults 
WHERE dispensaryid = 2 



-- Remove leading and trailing spaces from cannabinoid names