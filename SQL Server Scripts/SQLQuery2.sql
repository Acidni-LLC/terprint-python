select distinct(terpene) from terpeneresults  order by terpene--where dispensaryid =2
select distinct(Cannabinoid) from cannabinoidResults  order by Cannabinoid--where dispensaryid =2

select distinct(batch), created from cannabinoidResults where dispensaryid =2
select distinct(batch),  created from terpeneResults where dispensaryid =2 

-- Delete specific batches from cannabinoidResults
DELETE FROM cannabinoidResults 
WHERE batch IN (
    'AfCP8Lj3XkzHems','REYxZB8sRQ4KwKG','NJiRDgnPDYBtAnX','XF4zAKoQj8yCx3p',
    'fmNHWqZYycqDAgd','dfA63am93BqkAeR','ABbmjHwkrRK5F4e','ERHxaFsjM9pyotE',
    'iCm33pB7LjWnd5q','KTcZ6JgHdpqoAEx','zDF5f7E6ggrca73','Ay2ZkZyeQNDjyfa',
    'nP7REAQ5aQ4RYW2','5RzcEb3k8B4ALo4','dxDjCKX2xmAwYtW','6DMQwXFGMqs8zX5',
    '4REmwgHG6A5fwcL','9yWQQm4aaRsgHNa','FMPqqHtKQFdEdMd','r87Bi5xrLPpCSfo',
    'xCZ57p6SmP4GkFP','y8YBxxsizxsCHRE','mj6WiyWX8HiAFxE','Yad7LeWTiqZc3Jm'
);

-- Extract date from datetime column examples:
-- Method 1: Using CAST (recommended for SQL Server 2008+)
--SELECT distinct(batch), CAST(created AS DATE) AS created 
SELECT '''' + name + '"',', *
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
FROM cannabinoidResults 
WHERE dispensaryid = 2
order by created

-- Method 3: Format as string in YYYY-MM-DD format
SELECT distinct(batch), FORMAT(created, 'yyyy-MM-dd') AS created_date_string 
FROM cannabinoidResults 
WHERE dispensaryid = 2

-- Method 4: Remove time by converting to midnight of same day
SELECT distinct(batch), DATEADD(dd, 0, DATEDIFF(dd, 0, created)) AS created_date_midnight 
FROM cannabinoidResults 
WHERE dispensaryid = 2 



-- Remove leading and trailing spaces from cannabinoid names