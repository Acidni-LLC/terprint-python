using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class Grower
    {
        public int GrowerId { get; set; }
        [Required]
        public string Name
        { get; set; }
        public ICollection<States> States
        { get; set; }
        public ICollection<Batch> Batches { get; } 

    }
}
