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

        public DbSet<Terprint.Web.Models.TerpeneValues> TerpeneValues { get; set; } = default!;
    }
}
