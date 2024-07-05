using Microsoft.EntityFrameworkCore;
using Terprint.Web.Data;

namespace Terprint.Web.Models
{

    public static class SeedData
    {
        public static void Initialize(IServiceProvider serviceProvider)
        {
            using (var context = new TerprintWebContext(
                serviceProvider.GetRequiredService<DbContextOptions<TerprintWebContext>>()))
            {
                if (context == null || context.States == null)
                {
                    throw new ArgumentNullException("Null TerprintWebContext");
                }

                // Look for any movies.
                if (context.States.Any())
                {
                    return;   // DB has been seeded
                }

                #region snippet1
                context.States.AddRange(
                    new States { StateAbbreviation = "AL", StateName = "Alabama", StateCapital = "Montgomery", StateRegion = "South" },
                    new States { StateAbbreviation = "AK", StateName = "Alaska", StateCapital = "Juneau", StateRegion = "West" },
                    new States { StateAbbreviation = "AZ", StateName = "Arizona", StateCapital = "Phoenix", StateRegion = "West" },
                    new States { StateAbbreviation = "AR", StateName = "Arkansas", StateCapital = "Little Rock", StateRegion = "South" },
                    new States { StateAbbreviation = "CA", StateName = "California", StateCapital = "Sacramento", StateRegion = "West" },
                    new States { StateAbbreviation = "CO", StateName = "Colorado", StateCapital = "Denver", StateRegion = "West" },
                    new States { StateAbbreviation = "CT", StateName = "Connecticut", StateCapital = "Hartford", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "DE", StateName = "Delaware", StateCapital = "Dover", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "FL", StateName = "Florida", StateCapital = "Tallahassee", StateRegion = "South" },
                    new States { StateAbbreviation = "GA", StateName = "Georgia", StateCapital = "Atlanta", StateRegion = "South" },
                    new States { StateAbbreviation = "HI", StateName = "Hawaii", StateCapital = "Honolulu", StateRegion = "West" },
                    new States { StateAbbreviation = "ID", StateName = "Idaho", StateCapital = "Boise", StateRegion = "West" },
                    new States { StateAbbreviation = "IL", StateName = "Illinois", StateCapital = "Springfield", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "IN", StateName = "Indiana", StateCapital = "Indianapolis", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "IA", StateName = "Iowa", StateCapital = "Des Moines", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "KS", StateName = "Kansas", StateCapital = "Topeka", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "KY", StateName = "Kentucky", StateCapital = "Frankfort", StateRegion = "South" },
                    new States { StateAbbreviation = "LA", StateName = "Louisiana", StateCapital = "Baton Rouge", StateRegion = "South" },
                    new States { StateAbbreviation = "ME", StateName = "Maine", StateCapital = "Augusta", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "MD", StateName = "Maryland", StateCapital = "Annapolis", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "MA", StateName = "Massachusetts", StateCapital = "Boston", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "MI", StateName = "Michigan", StateCapital = "Lansing", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "MN", StateName = "Minnesota", StateCapital = "St. Paul", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "MS", StateName = "Mississippi", StateCapital = "Jackson", StateRegion = "South" },
                    new States { StateAbbreviation = "MO", StateName = "Missouri", StateCapital = "Jefferson City", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "MT", StateName = "Montana", StateCapital = "Helena", StateRegion = "West" },
                    new States { StateAbbreviation = "NE", StateName = "Nebraska", StateCapital = "Lincoln", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "NV", StateName = "Nevada", StateCapital = "Carson City", StateRegion = "West" },
                    new States { StateAbbreviation = "NH", StateName = "New Hampshire", StateCapital = "Concord", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "NJ", StateName = "New Jersey", StateCapital = "Trenton", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "NM", StateName = "New Mexico", StateCapital = "Santa Fe", StateRegion = "West" },
                    new States { StateAbbreviation = "NY", StateName = "New York", StateCapital = "Albany", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "NC", StateName = "North Carolina", StateCapital = "Raleigh", StateRegion = "South" },
                    new States { StateAbbreviation = "ND", StateName = "North Dakota", StateCapital = "Bismarck", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "OH", StateName = "Ohio", StateCapital = "Columbus", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "OK", StateName = "Oklahoma", StateCapital = "Oklahoma City", StateRegion = "South" },
                    new States { StateAbbreviation = "OR", StateName = "Oregon", StateCapital = "Salem", StateRegion = "West" },
                    new States { StateAbbreviation = "PA", StateName = "Pennsylvania", StateCapital = "Harrisburg", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "RI", StateName = "Rhode Island", StateCapital = "Providence", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "SC", StateName = "South Carolina", StateCapital = "Columbia", StateRegion = "South" },
                    new States { StateAbbreviation = "SD", StateName = "South Dakota", StateCapital = "Pierre", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "TN", StateName = "Tennessee", StateCapital = "Nashville", StateRegion = "South" },
                    new States { StateAbbreviation = "TX", StateName = "Texas", StateCapital = "Austin", StateRegion = "South" },
                    new States { StateAbbreviation = "UT", StateName = "Utah", StateCapital = "Salt Lake City", StateRegion = "West" },
                    new States { StateAbbreviation = "VT", StateName = "Vermont", StateCapital = "Montpelier", StateRegion = "Northeast" },
                    new States { StateAbbreviation = "VA", StateName = "Virginia", StateCapital = "Richmond", StateRegion = "South" },
                    new States { StateAbbreviation = "WA", StateName = "Washington", StateCapital = "Olympia", StateRegion = "West" },
                    new States { StateAbbreviation = "WV", StateName = "West Virginia", StateCapital = "Charleston", StateRegion = "South" },
                    new States { StateAbbreviation = "WI", StateName = "Wisconsin", StateCapital = "Madison", StateRegion = "Midwest" },
                    new States { StateAbbreviation = "WY", StateName = "Wyoming", StateCapital = "Cheyenne", StateRegion = "West" }

                #endregion

                    
                );
                context.SaveChanges();
            }
        }
    }
}
