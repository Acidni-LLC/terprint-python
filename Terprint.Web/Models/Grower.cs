using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization; // Add this using directive

namespace Terprint.Web.Models
{
    public class Grower
    {
        public DateTime created { get; set; } = DateTime.Now;
        public string? createdby { get; set; }
        public int GrowerId { get; set; }
        [Required]
        public string Name { get; set; }
        public IList<States> States { get; set; } = new List<States>();
        [JsonIgnore] // Ignore to prevent cycle during serialization
        public IList<Batch> Batches { get; } = new List<Batch>();

        // If no constructor exists, add this for initialization
        public Grower()
        {
            // Initialization already handled via property initializers above
        }
    }
}
