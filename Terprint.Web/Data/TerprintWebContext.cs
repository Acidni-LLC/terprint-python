using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;
using Terprint.Web.Models;

namespace Terprint.Web.Data
{
    public class ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : IdentityDbContext<ApplicationUser>(options)
    {
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {

            optionsBuilder
              //.EnableSensitiveDataLogging()

              .UseSqlServer(@"Data Source=terprintwebdbserver.database.windows.net;Initial Catalog=Terprint.Web_db;User ID=savitas;Password=sql1234%;Connect Timeout=60;Encrypt=True;Trust Server Certificate=False;Application Intent=ReadWrite;Multi Subnet Failover=False")
              ;
        }
    }
    public class TerprintWebContext2 : TerprintWebContext
    {
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {

            optionsBuilder
              //.EnableSensitiveDataLogging()

              .UseSqlServer(@"Data Source=terprintwebdbserver.database.windows.net;Initial Catalog=Terprint.Web_db;User ID=savitas;Password=sql1234%;Connect Timeout=60;Encrypt=True;Trust Server Certificate=False;Application Intent=ReadWrite;Multi Subnet Failover=False")
              ;
        }
        public TerprintWebContext2(DbContextOptions<TerprintWebContext> options)
            : base(options)
        {
        }
    }
    public class TerprintWebContext3 : TerprintWebContext
    {
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {


            optionsBuilder
               //.EnableSensitiveDataLogging()

               .UseSqlServer(@"Data Source=terprintwebdbserver.database.windows.net;Initial Catalog=Terprint.Web_db;User ID=savitas;Password=sql1234%;Connect Timeout=60;Encrypt=True;Trust Server Certificate=False;Application Intent=ReadWrite;Multi Subnet Failover=False")
               ;
        }
        public TerprintWebContext3(DbContextOptions<TerprintWebContext> options)
            : base(options)
        {
        }
    }
    public class TerprintWebContext : DbContext
    {
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            optionsBuilder
                //.EnableSensitiveDataLogging()

                .UseSqlServer(@"Data Source=terprintwebdbserver.database.windows.net;Initial Catalog=Terprint.Web_db;User ID=savitas;Password=sql1234%;Connect Timeout=60;Encrypt=True;Trust Server Certificate=False;Application Intent=ReadWrite;Multi Subnet Failover=False")
                ;
        }
        public TerprintWebContext (DbContextOptions<TerprintWebContext> options)
            : base(options )
        {
        }

        public DbSet<Terprint.Web.Models.TerpeneValue> TerpeneValues { get; set; } = default!;
        public DbSet<Terprint.Web.Models.Rating> Rating { get; set; } = default!;
        public DbSet<Terprint.Web.Models.Matrixes> Matrixes { get; set; } = default!;
        public DbSet<Terprint.Web.Models.Grower> Grower { get; set; } = default!;
        public DbSet<Terprint.Web.Models.RatingCategory> RatingCategory { get; set; } = default!;
        public DbSet<Terprint.Web.Models.Strain> Strain { get; set; } = default!;
        public DbSet<Terprint.Web.Models.Batch> Batch { get; set; } = default!;
        public DbSet<Terprint.Web.Models.THCValue> THCValues { get; set; } = default!;
        public DbSet<Terprint.Web.Models.States> States { get; set; } = default!;
    }
}
