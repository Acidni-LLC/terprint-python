
using System.ComponentModel.DataAnnotations;

namespace Terprint.Web.Models
{
    public class Matrixes
    {
        public int Id { get; set; }
        //Terpene	Matrix	Row	Column	Color
        public string Terpene { get; set; }
        public int Matrix { get; set; }
        public int Row { get; set; }
        public int Column { get; set; }
        public string Color { get; set; }

    }
}
