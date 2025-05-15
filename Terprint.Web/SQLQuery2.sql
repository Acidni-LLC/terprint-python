select * from  RatingCategory

select Top(100)* from batch order by created desc

select * from TerpeneValues where  lower(terpenename) like '%caryophyllene%' order by BatchID desc
select top(100)* from thcvalues order by created desc
select top(100)* from thcvalues order by batchid desc
--delete from thcvalues where thcvalueid >= 789
select s.StrainName,b.* from batch b join strain s on b.StrainID=s.StrainId where b.BatchId not in (Select BatchId from THCValues) 

select * from THCValues where batchid = (select batchid from batch where name ='18347_0004 808376') 
select * from THCValues where [Percent] = 0
select * from TerpeneValues where Value = 0
select * from TerpeneValues where TerpeneName like '%Phellandrene%'
select tv.*,b.Name from TerpeneValues tv join batch b on tv.BatchID=b.BatchId where tv.TerpeneName = ''
--delete from THCValues where [batchid] = 87
--delete from thcvalues where batchid = 87 in (58,59,60,61,62,63,64,65,66,67,68)

select lower(tv.TerpeneName),count(tv.TerpeneName) from TerpeneValues tv group by tv.TerpeneName order by count(tv.TerpeneName )

select t.Analyte, count(t.Analyte) from THCValues t group by t.Analyte  order by count(t.Analyte)  desc
 
select b.Name,t.* from THCValues   t join batch b on t.BatchID = b.BatchId where t.analyte = 'Delta-'
select b.Name, t.* from THCValues  t join batch b on t.BatchID = b.BatchId where t.LOD like '%THC%'
select t.Analyte, t.BatchID ,count(t.Analyte) from THCValues t group by t.Analyte, t.BatchID order by count(t.Analyte)  desc
select t.* from THCValues t where t.BatchID = '44' 

select b.name,t.* from THCValues t join batch b on t.BatchID = b.BatchId where t.BatchID in (44,51,42,43,50,74,75,76,77,78,79,80,87) 
update TerpeneValues set TerpeneName = '3-CARENE' where TerpeneValueId=549



select tv.*,b.Name from TerpeneValues tv join batch b on tv.BatchID=b.BatchId where tv.TerpeneName = ''

 select s.StrainName,(select top (1) tv.*),b.Name from TerpeneValues tv 
join batch b on tv.BatchID=b.BatchId 
join strain s on b.StrainID=s.StrainId 
order by b.Name, tv.Value desc

select * from TerpeneValues tv 