--SELECT TOP (20) *  FROM [dbo].[cannabinoidResults]

--SELECT TOP (20) *  FROM [dbo].terpeneResults

DECLARE @dispensaryid int = 2;
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
  order by batch,[index]
  SELECT *
  FROM vw_cannabinoidResults
 where batch not in (select batch from vw_terpeneResults) and 
  dispensaryId = @dispensaryid
  order by batch,[index]
  
  SELECT distinct Cannabinoid
  FROM vw_cannabinoidResults
 --where batch ='57901_0007452411'
 
  where dispensaryId = @dispensaryid
  order by Cannabinoid
  
  SELECT distinct terpene
  FROM vw_terpeneResults
 --where batch ='57901_0007452411' 
  where dispensaryId = @dispensaryid
  order by terpene


  SELECT *
  FROM vw_cannabinoidResults
 --where batch ='57901_0007452411' 
  where dispensaryId = @dispensaryid
  order by batch,[index]
  

  SELECT *
  FROM vw_terpeneResults
 --where batch ='57901_0007452411' 
  where dispensaryId = @dispensaryid
  order by batch,[index]

  /*
  delete from terpeneResults  
  where dispensaryId = @dispensaryid
  
  delete from cannabinoidResults 
  where dispensaryId = @dispensaryid
  */
