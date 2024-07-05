using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class States
    {
        public int Id { get; set; }
        public string StateName
        { get; set; }
        public string StateAbbreviation
        { get; set; }
        public string StateCapital
        { get; set; }
        public string StateRegion
        { get; set; }
        public ICollection<Grower> Growers { get; }

    }
}
