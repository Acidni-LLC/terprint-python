using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace Terprint.Components
{
    public class Ratings
    {
        public List<UserRating> UserRatings { get; set; }

        public Ratings()
        {

            UserRatings = new List<UserRating>();
            loadRatings();
        }

        private void loadRatings()
        {
            UserRatings.Add(new UserRating("Blueberry Headband|9628 5341 3355 9561") { email = "jgill@savitas.net", batchin = "Blueberry Headband|9628 5341 3355 9561", BuyAgain = true, OverallRating = 8, Notes = "" });
            UserRatings.Add(new UserRating("G. Mints|9436 5391 1236 0974") { email = "jgill@savitas.net", batchin = "G. Mints|9436 5391 1236 0974", BuyAgain = true, OverallRating = 9, Notes = "" });
            UserRatings.Add(new UserRating("Purple Eclipse|5152 6368 4561 8754") { email = "jgill@savitas.net", batchin = "Purple Eclipse|5152 6368 4561 8754", BuyAgain = false, OverallRating = 6, Notes = "" });
            UserRatings.Add(new UserRating("Witch D.|6953 2390 9886 2373") { email = "jgill@savitas.net", batchin = "Witch D.|6953 2390 9886 2373", BuyAgain = false, OverallRating = 6, Notes = "" });
            UserRatings.Add(new UserRating("Z-Mintz|3370 0970 3898 2532") { email = "jgill@savitas.net", batchin = "Z-Mintz|3370 0970 3898 2532", BuyAgain = false, OverallRating = 6, Notes = "" });
            UserRatings.Add(new UserRating("DieselDough|63424_0004931218") { email = "jgill@savitas.net", batchin = "DieselDough|63424_0004931218", BuyAgain = true, OverallRating = 9, Taste = 8, Effect = 8, Notes = "" });
            UserRatings.Add(new UserRating("Space Age Cake|59727_0005068301") { email = "jgill@savitas.net", batchin = "Space Age Cake|59727_0005068301", BuyAgain = true, OverallRating = 9, Taste = 9, Effect = 9, Notes = "9" });
            UserRatings.Add(new UserRating("Ice Cream Cake| 64811_0005937028") { email = "jgill@savitas.net", batchin = "Ice Cream Cake| 64811_0005937028", BuyAgain = true, OverallRating = 10, Taste = 10, Effect = 10, Notes = "" });
            UserRatings.Add(new UserRating("Traffic Jam|68675_0005224528") { email = "jgill@savitas.net", batchin = "Traffic Jam|68675_0005224528", BuyAgain = true, OverallRating = 10, Taste = 10, Effect = 10, Notes = "" });
            UserRatings.Add(new UserRating("iCandy| 67279_0005905658") { email = "jgill@savitas.net", batchin = "iCandy| 67279_0005905658", BuyAgain = true, OverallRating = 10, Taste = 10, Effect = 10, Notes = "" });


        }
        public class UserRating
        {
            public UserRating (string batchin)
            {
                batch = batchin.Split(['|'])[1];
                strain = batchin.Split(['|'])[0];
            }
            public int id { get; set; }
            public string name { get; set; }
            public string batch { get; set; }
            public string strain { get; set; }
            public string batchin { get; set; }// Overall Rating	Taste	Effect	Notes	Buy Again

            public int OverallRating { get; set; }
            public int Taste { get; set; }
            public int Effect { get; set; }
            public string email { get; set; }
            public string Notes { get; set; }
            public bool BuyAgain { get; set; }
        }

    }
}
