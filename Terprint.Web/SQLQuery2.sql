select * from  RatingCategory

select * from batch where name ='18347_0004 808376'

select * from thcvalues where  batchid = 87

select * from THCValues where batchid = (select batchid from batch where name ='1223298389111661') 
select * from THCValues where [Percent] = 0
select * from TerpeneValues where Value = 0
--delete from THCValues where [Percent] = 0
--delete from thcvalues where batchid = 87 in (58,59,60,61,62,63,64,65,66,67,68)