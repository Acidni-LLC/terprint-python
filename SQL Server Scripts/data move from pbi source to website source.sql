
select * from TerpeneValues
select * from batch where name ='gFAcXTRYpnfkSfk'
select * FROM vw_terpeneResults v where dispensaryId = 1

----

INSERT INTO TerpeneValues ([created]
           ,[createdby]
           ,[Value]
           ,[TerpeneName]
           ,[BatchID]
           ,[Scale]
           ,[Index])
select   v.created,v.createdBy,v.milligrams,v.terpene,
(select b.batchid from batch b where b.name= RIGHT(v.batch,NULLIF(CHARINDEX('_',REVERSE(v.batch)),0)-1)) as batchid  ,
'',v.[Index]

from vw_terpeneResults v 
where v.batch like '%COA%' and ISNUMERIC((select b.batchid from batch b where b.name= RIGHT(v.batch,NULLIF(CHARINDEX('_',REVERSE(v.batch)),0)-1))) = 1
--------------


INSERT INTO TerpeneValues ([created]
           ,[createdby]
           ,[Value]
           ,[TerpeneName]
           ,[BatchID]
           ,[Scale]
           ,[Index])
SELECT   v.created, v.createdBy,  left(v.[percent],len(v.[percent])-1) as perc,v.terpene,
(select top(1) isnull(b.BatchId,'') from Batch b where b.Name = (select top(1) RIGHT(v.batch,NULLIF(CHARINDEX('_',REVERSE(v1.batch)),0)-1) as extracted from vw_terpeneResults v1 where batch like '%COA%')) as batch,
RIGHT(v.batch,NULLIF(CHARINDEX('_',REVERSE(v.batch)),0)-1),
'',v.[Index] 
FROM vw_terpeneResults v
WHERE RIGHT(v.batch,NULLIF(CHARINDEX('_',REVERSE(v.batch)),0)-1) in (select name from batch) and ISNUMERIC( Replace(v.[percent],'%','') ) = 0 and dispensaryId = 1
order by terpeneResultId

INSERT INTO TerpeneValues ([created]
           ,[createdby]
           ,[Value]
           ,[TerpeneName]
           ,[BatchID]
           ,[Scale]
           ,[Index])
SELECT    v.created, v.createdBy,   Replace(v.[percent],'%','') as perc,v.terpene,(select top(1) isnull(b.BatchId,'') from Batch b where b.Name = v.batch) as batch,'',v.[Index] 
FROM vw_terpeneResults v 
WHERE v.batch in (select name from batch) and ISNUMERIC( Replace(v.[percent],'%','') ) = 1 and dispensaryId = 1
------

INSERT INTO TerpeneValues ([created]
           ,[createdby]
           ,[Value]
           ,[TerpeneName]
           ,[BatchID]
           ,[Scale]
           ,[Index])
SELECT   v.created, v.createdBy,  left(v.[percent],len(v.[percent])-1) as perc,v.terpene,(select top(1) isnull(b.BatchId,'') from Batch b where b.Name = v.batch) as batch,'',v.[Index] 
FROM vw_terpeneResults v
WHERE v.batch in (select name from batch) and ISNUMERIC( Replace(v.[percent],'%','') ) = 1 and dispensaryId = 2
order by terpeneResultId

INSERT INTO TerpeneValues ([created]
           ,[createdby]
           ,[Value]
           ,[TerpeneName]
           ,[BatchID]
           ,[Scale]
           ,[Index])
SELECT    v.created, v.createdBy,   Replace(v.[percent],'%','') as perc,v.terpene,(select top(1) isnull(b.BatchId,'') from Batch b where b.Name = v.batch) as batch,'',v.[Index] 
FROM vw_terpeneResults v 
WHERE v.batch in (select name from batch) and ISNUMERIC( Replace(v.[percent],'%','') ) = 1 and dispensaryId = 2



----

SELECT v.terpeneResultId, v.created, v.createdBy, ISNUMERIC(Replace(Replace(v.[percent],'%',''),' ','')),   Replace(Replace(v.[percent],'%',''),' ','') as perc,v.terpene,(select top(1) isnull(b.BatchId,'') from Batch b where b.Name = v.batch) as batch,'',v.[Index] 
FROM vw_terpeneResults v
WHERE v.batch  in (select name from batch) and ISNUMERIC(Replace(Replace(v.[percent],'%',''),' ','')) = 1
order by terpeneResultId

SELECT v.terpeneResultId, v.created, v.createdBy, ISNUMERIC(Replace(Replace(v.[percent],'%',''),' ','')),   Replace(Replace(v.[percent],'%',''),' ','') as perc,v.terpene,(select top(1) isnull(b.BatchId,'') from Batch b where b.Name = v.batch) as batch,'',v.[Index] 
FROM vw_terpeneResults v
WHERE v.batch not in (select name from batch) and ISNUMERIC(Replace(Replace(v.[percent],'%',''),' ','')) = 1
order by terpeneResultId

select * FROM vw_terpeneResults v
--delete from TerpeneValues
GO
'0.555 '0.5210.554 0.555 0.521

select * from batch