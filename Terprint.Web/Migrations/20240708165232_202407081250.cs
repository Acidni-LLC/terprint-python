using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Terprint.Web.Migrations
{
    /// <inheritdoc />
    public partial class _202407081250 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Growerid",
                table: "Rating");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "Growerid",
                table: "Rating",
                type: "int",
                nullable: false,
                defaultValue: 0);
        }
    }
}
