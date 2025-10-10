--SELECT TOP (20) *  FROM [dbo].[cannabinoidResults]

--SELECT TOP (20) *  FROM [dbo].terpeneResults

  SELECT distinct count(batch)
  FROM vw_cannabinoidResults
  SELECT distinct count(batch)
  FROM vw_terpeneResults
  
  SELECT *
  FROM vw_terpeneResults
 where batch not in (select batch from vw_cannabinoidResults)
  order by batch,[index]
  SELECT *
  FROM vw_cannabinoidResults
 where batch not in (select batch from vw_terpeneResults)
  order by batch,[index]
  
  SELECT distinct Cannabinoid
  FROM vw_cannabinoidResults
 --where batch ='57901_0007452411'
  order by Cannabinoid


  SELECT *
  FROM vw_cannabinoidResults
 --where batch ='57901_0007452411'
  order by batch,[index]
  

  SELECT *
  FROM vw_terpeneResults
 --where batch ='57901_0007452411'
  order by batch,[index]

  /*
  delete from terpeneResults
  delete from cannabinoidResults
  */
