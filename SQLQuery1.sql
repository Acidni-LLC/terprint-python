--SELECT TOP (20) *  FROM [dbo].[cannabinoidResults]

--SELECT TOP (20) *  FROM [dbo].terpeneResults

  SELECT distinct count(batch)
  FROM vw_cannabinoidResults
  SELECT distinct count(batch)
  FROM vw_terpeneResults

  SELECT *
  FROM vw_cannabinoidResults
 where batch ='57901_0007452411'
  order by batch
  

  SELECT *
  FROM vw_terpeneResults
 where batch ='57901_0007452411'
  order by batch

  /*
  delete from terpeneResults
  delete from cannabinoidResults
  */
