using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Terprint.Web.Migrations
{
    /// <inheritdoc />
    public partial class _202407052325 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Grower",
                table: "TerpeneValues");

            migrationBuilder.DropColumn(
                name: "Material",
                table: "TerpeneValues");

            migrationBuilder.DropColumn(
                name: "Rating",
                table: "TerpeneValues");

            migrationBuilder.DropColumn(
                name: "Strain",
                table: "TerpeneValues");

            migrationBuilder.RenameColumn(
                name: "Id",
                table: "TerpeneValues",
                newName: "TerpeneValueId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "TerpeneValueId",
                table: "TerpeneValues",
                newName: "Id");

            migrationBuilder.AddColumn<string>(
                name: "Grower",
                table: "TerpeneValues",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<string>(
                name: "Material",
                table: "TerpeneValues",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<double>(
                name: "Rating",
                table: "TerpeneValues",
                type: "float",
                nullable: false,
                defaultValue: 0.0);

            migrationBuilder.AddColumn<string>(
                name: "Strain",
                table: "TerpeneValues",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");
        }
    }
}
