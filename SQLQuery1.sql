--SELECT TOP (20) *  FROM [dbo].[cannabinoidResults]

--SELECT TOP (20) *  FROM [dbo].terpeneResults

DECLARE @dispensaryid int = 1;

  SELECT distinct count(batch)
  FROM vw_cannabinoidResults
  where dispensaryId = @dispensaryid
  SELECT distinct count(batch)
  FROM vw_terpeneResults
  where dispensaryId = @dispensaryid
  
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
 
  where dispensaryId = @dispensaryid
  order by cannabinoidResultId desc
  
  SELECT distinct terpene
  FROM vw_terpeneResults
 --where batch ='57901_0007452411' 
  where dispensaryId = @dispensaryid


  SELECT *
  FROM vw_cannabinoidResults
 --where batch ='57901_0007452411' 
  where dispensaryId = @dispensaryid
  order by cannabinoidResultId desc, batch,[index]
  

  SELECT *
  FROM vw_terpeneResults
 --where batch ='57901_0007452411' 
  where dispensaryId = @dispensaryid
  order by terpeneResultId desc, batch,[index]

  /*
  delete from terpeneResults  
  where dispensaryId = @dispensaryid
  
  delete from cannabinoidResults 
  where dispensaryId = @dispensaryid
  */
