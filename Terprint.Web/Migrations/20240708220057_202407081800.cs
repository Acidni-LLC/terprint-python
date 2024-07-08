using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Terprint.Web.Migrations
{
    /// <inheritdoc />
    public partial class _202407081800 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<DateTime>(
                name: "created",
                table: "THCValues",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<DateTime>(
                name: "created",
                table: "TerpeneValues",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<DateTime>(
                name: "created",
                table: "Strain",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<DateTime>(
                name: "created",
                table: "RatingCategory",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<DateTime>(
                name: "created",
                table: "Matrixes",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<DateTime>(
                name: "created",
                table: "Grower",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));

            migrationBuilder.AddColumn<DateTime>(
                name: "created",
                table: "Batch",
                type: "datetime2",
                nullable: false,
                defaultValue: new DateTime(1, 1, 1, 0, 0, 0, 0, DateTimeKind.Unspecified));
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "created",
                table: "THCValues");

            migrationBuilder.DropColumn(
                name: "created",
                table: "TerpeneValues");

            migrationBuilder.DropColumn(
                name: "created",
                table: "Strain");

            migrationBuilder.DropColumn(
                name: "created",
                table: "RatingCategory");

            migrationBuilder.DropColumn(
                name: "created",
                table: "Matrixes");

            migrationBuilder.DropColumn(
                name: "created",
                table: "Grower");

            migrationBuilder.DropColumn(
                name: "created",
                table: "Batch");
        }
    }
}
