
using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class THCLevel
    {

        public int Id { get; set; }

        public string Name { get; set; }
        public double Value { get; set; }
        public string Scale { get; set; }


    }
}
