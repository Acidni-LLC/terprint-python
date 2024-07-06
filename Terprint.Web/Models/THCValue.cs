
using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class THCValue
    {

        public int THCValueId { get; set; }
        [Required]
        public int? BatchID { get; set; }

        public string Name { get; set; }
        public double Value { get; set; }
        public string Scale { get; set; }


    }
}
