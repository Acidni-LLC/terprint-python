-- Combined count query for all tables
SELECT 
    (SELECT COUNT(*) FROM terpeneresults) AS terpeneresults_count,
    (SELECT COUNT(*) FROM TerpeneValues) AS TerpeneValues_count,
    (SELECT COUNT(*) FROM cannabinoidResults) AS cannabinoidResults_count,
    (SELECT COUNT(*) FROM THCValues) AS THCValues_count

select * from terpeneresults where batchid not in (select batchid from TerpeneValues) and batchid is not null
select * from TerpeneValues  order by created desc

SELECT 
    (SELECT COUNT(*) FROM terpeneresults) AS terpeneresults_count,
    (SELECT COUNT(*) FROM TerpeneValues) AS TerpeneValues_count,
    (SELECT COUNT(*) FROM cannabinoidResults) AS cannabinoidResults_count,
    (SELECT COUNT(*) FROM THCValues) AS THCValues_count
INSERT INTO [dbo].[TerpeneValues]
           ([created]
           ,[createdby]
           ,[Value]
           ,[TerpeneName]
           ,[BatchID]
           ,[Scale]
           ,[Index])
SELECT 
    [created],
    [createdby],
    [milligrams],
    [terpene] AS [TerpeneName],
    [batchid] AS [BatchID],
    'mg/g' AS [Scale],
    [Index]
FROM [dbo].[terpeneresults]
WHERE batchid NOT IN (SELECT batchid FROM TerpeneValues ) and  batchid IS NOT NULL

SELECT 
    (SELECT COUNT(*) FROM terpeneresults) AS terpeneresults_count,
    (SELECT COUNT(*) FROM TerpeneValues) AS TerpeneValues_count,
    (SELECT COUNT(*) FROM cannabinoidResults) AS cannabinoidResults_count,
    (SELECT COUNT(*) FROM THCValues) AS THCValues_count

    
select created as c,* from terpeneresults order by c desc
select created as c, * from TerpeneValues order by c desc

select * from cannabinoidResults
select * from THCValues

