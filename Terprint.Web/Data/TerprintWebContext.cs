using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using Terprint.Web.Models;

namespace Terprint.Web.Data
{
    public class TerprintWebContext : DbContext
    {
        public TerprintWebContext (DbContextOptions<TerprintWebContext> options)
            : base(options)
        {
        }

        public DbSet<Terprint.Web.Models.TerpeneValue> TerpeneValues { get; set; } = default!;
        public DbSet<Terprint.Web.Models.Rating> Rating { get; set; } = default!;
        public DbSet<Terprint.Web.Models.Matrixes> Matrixes { get; set; } = default!;
        public DbSet<Terprint.Web.Models.Grower> Grower { get; set; } = default!;
        public DbSet<Terprint.Web.Models.RatingCategory> RatingCategory { get; set; } = default!;
        public DbSet<Terprint.Web.Models.Strain> Strain { get; set; } = default!;
        public DbSet<Terprint.Web.Models.Batch> Batch { get; set; } = default!;
        public DbSet<Terprint.Web.Models.THCLevel> THCLevels { get; set; } = default!;
        public DbSet<Terprint.Web.Models.States> States { get; set; } = default!;
    }
}
