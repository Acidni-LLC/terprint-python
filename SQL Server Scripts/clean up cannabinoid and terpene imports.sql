select * from batch where batchid = 335.

delete from dbo.Batch where Batchid = 335;

select * from terpeneResults where Batchid = 339
delete from  terpeneResults where Batchid = 339

select top(25) * from cannabinoidResults 
where cannabinoidResultId > 22619 
order by created desc
delete from cannabinoidResults where cannabinoidResultId > 22619