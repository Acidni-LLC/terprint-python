--SELECT TOP (20) *  FROM [dbo].[cannabinoidResults]

--SELECT TOP (20) *  FROM [dbo].terpeneResults

DECLARE @dispensaryid int = 2;
DECLARE @date date =      '2025-11-10';   
    /*
DECLARE @dispensaryid int = 2;
DECLARE @date date =      '2025-11-10';  
  delete from cannabinoidResults 2
  where dispensaryId = @dispensaryid and created  >= @date
  delete from Batch 
  where BatchId > 220
  delete from terpeneResults 
  where dispensaryId = @dispensaryid and created  >= @date

  */
  select * from Batch where created >= @date
  SELECT *
  FROM vw_terpeneResults where created >= @date
  SELECT *
  FROM vw_cannabinoidResults where created >= @date
  SELECT distinct count(batch)
  FROM vw_terpeneResults
  where dispensaryId = @dispensaryid and created  >= @date
  SELECT distinct count(batch) 
  FROM vw_cannabinoidResults
  where dispensaryId = @dispensaryid and created  >= @date
  SELECT distinct count(batch)
  FROM vw_terpeneResults
  where dispensaryId = @dispensaryid and created  >= @date
  
  SELECT *
  FROM vw_terpeneResults
 where batch not in (select batch from vw_cannabinoidResults) and 
  dispensaryId = @dispensaryid
  order by created desc,batch,[index]
  SELECT *
  FROM vw_cannabinoidResults
 where batch not in (select batch from vw_terpeneResults) and 
  dispensaryId = @dispensaryid
  order by created desc, batch,[index]
  
  SELECT distinct Cannabinoid
  FROM vw_cannabinoidResults
 --where batch ='57901_0007452411' 
  where dispensaryId = @dispensaryid and created  >= @date
  
  SELECT distinct terpene
  FROM vw_terpeneResults
 --where batch ='57901_0007452411' 
  where dispensaryId = @dispensaryid and created  >= @date


  SELECT *
  FROM vw_cannabinoidResults
 --where batch ='57901_0007452411' 
  where dispensaryId = @dispensaryid and created  >= @date
  order by cannabinoidResultId desc, batch,[index]
  

  SELECT *
  FROM vw_terpeneResults
 --where batch ='57901_0007452411' 
  --where batch like '%gbxx%'
  where dispensaryId = @dispensaryid and created  >= @date
  order by terpeneResultId desc, batch,[index]

  /*
  delete from terpeneResults  
  where dispensaryId = @dispensaryid

  delete from cannabinoidResults 
  where dispensaryId = @dispensaryid

  delete from cannabinoidResults 
  where batch like '%gbxx%'
  
  delete from terpeneResults  
 where batch like '%gbxx%'
  */
