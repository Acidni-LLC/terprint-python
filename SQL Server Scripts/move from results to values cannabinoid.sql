-- Combined count query for all tables
SELECT 
    (SELECT COUNT(*) FROM cannabinoidResults) AS terpeneresults_count,
    (SELECT COUNT(*) FROM TerpeneValues) AS TerpeneValues_count,
    (SELECT COUNT(*) FROM cannabinoidResults) AS cannabinoidResults_count,
    (SELECT COUNT(*) FROM THCValues) AS THCValues_count

select * from cannabinoidResults where batchid not in (select batchid from THCValues) and batchid is not null
select * from THCValues  order by created desc

SELECT 
    (SELECT COUNT(*) FROM cannabinoidResults) AS cannabinoidResults_count,
    (SELECT COUNT(*) FROM THCValues) AS THCValues_count

INSERT INTO [dbo].[THCValues]
           ([created]
           ,[createdby]
           ,[Result]
           ,[Percent]
           ,[Analyte]
           ,[BatchID]
           ,[LOD]
           ,[Index])
SELECT 
    [created],
    [createdby],
  TRY_CAST([milligrams] AS FLOAT)  [milligrams],
    ROUND(TRY_CAST([milligrams] AS FLOAT) * 0.1, 3) AS [Percent],
    
    [Cannabinoid] AS [Analyte],
    [batchid] AS [BatchID],
    'mg/g' AS [LOD],
    [Index]
FROM [dbo].[cannabinoidResults]
WHERE batchid NOT IN (SELECT batchid FROM THCValues ) and  batchid IS NOT NULL and  [milligrams]  not in  ('ND','<LOQ','None')
order by milligrams

SELECT 
    (SELECT COUNT(*) FROM cannabinoidResults) AS cannabinoidResults_count,
    (SELECT COUNT(*) FROM THCValues) AS THCValues_count


select created as c,* from cannabinoidResults order by c desc
select created as c, * from THCValues order by c desc

select * from cannabinoidResults
select * from THCValues

