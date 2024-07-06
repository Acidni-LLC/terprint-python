using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Terprint.Web.Migrations
{
    /// <inheritdoc />
    public partial class _202407061339 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Value",
                table: "THCValues");

            migrationBuilder.RenameColumn(
                name: "Scale",
                table: "THCValues",
                newName: "Result");

            migrationBuilder.RenameColumn(
                name: "Name",
                table: "THCValues",
                newName: "Percent");

            migrationBuilder.AddColumn<string>(
                name: "Analyte",
                table: "THCValues",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<string>(
                name: "Dilution",
                table: "THCValues",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<string>(
                name: "LOD",
                table: "THCValues",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<string>(
                name: "LOQ",
                table: "THCValues",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Analyte",
                table: "THCValues");

            migrationBuilder.DropColumn(
                name: "Dilution",
                table: "THCValues");

            migrationBuilder.DropColumn(
                name: "LOD",
                table: "THCValues");

            migrationBuilder.DropColumn(
                name: "LOQ",
                table: "THCValues");

            migrationBuilder.RenameColumn(
                name: "Result",
                table: "THCValues",
                newName: "Scale");

            migrationBuilder.RenameColumn(
                name: "Percent",
                table: "THCValues",
                newName: "Name");

            migrationBuilder.AddColumn<double>(
                name: "Value",
                table: "THCValues",
                type: "float",
                nullable: false,
                defaultValue: 0.0);
        }
    }
}
