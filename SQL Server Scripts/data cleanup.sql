
select b.Name,t.* from THCValues   t join batch b on t.BatchID = b.BatchId where t.analyte like '%Delta-%'
select b.Name, t.* from THCValues  t join batch b on t.BatchID = b.BatchId where t.LOD like '%THC%' order by BatchId


 select name, batchid from batch where batchid not in(select batchid from THCValues  )
 --  delete from THCValues where Batchid = 87

 -----64811_0005291043,71209_0006052584,18365_0006095728,68679_0006027978,18347_0004 808376

-- 9628 5341 3355 9561
--63424_0004931218
--PRPFLW100150-2405-28420
--PRPFLW101375-2405-28415
--64811_0005291043
--71209_0006052584
--18365_0006095728
--68679_0006027978
--18347_0004 808376