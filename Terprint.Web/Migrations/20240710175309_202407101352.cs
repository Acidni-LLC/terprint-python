using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Terprint.Web.Migrations.TerprintWeb
{
    /// <inheritdoc />
    public partial class _202407101352 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "createdby",
                table: "THCValues",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "createdby",
                table: "TerpeneValues",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "createdby",
                table: "Strain",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "createdby",
                table: "States",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "createdby",
                table: "RatingCategory",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "createdby",
                table: "Rating",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "createdby",
                table: "Matrixes",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "createdby",
                table: "Grower",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<string>(
                name: "createdby",
                table: "Batch",
                type: "nvarchar(max)",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "createdby",
                table: "THCValues");

            migrationBuilder.DropColumn(
                name: "createdby",
                table: "TerpeneValues");

            migrationBuilder.DropColumn(
                name: "createdby",
                table: "Strain");

            migrationBuilder.DropColumn(
                name: "createdby",
                table: "States");

            migrationBuilder.DropColumn(
                name: "createdby",
                table: "RatingCategory");

            migrationBuilder.DropColumn(
                name: "createdby",
                table: "Rating");

            migrationBuilder.DropColumn(
                name: "createdby",
                table: "Matrixes");

            migrationBuilder.DropColumn(
                name: "createdby",
                table: "Grower");

            migrationBuilder.DropColumn(
                name: "createdby",
                table: "Batch");
        }
    }
}
