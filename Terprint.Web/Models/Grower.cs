using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class Grower
    {
        public DateTime created { get; set; } = DateTime.Now;
        public int GrowerId { get; set; }
        [Required]
        public string Name
        { get; set; }
        public IList<States> States
        { get; set; }
        public IList<Batch> Batches { get; } 

    }
}
