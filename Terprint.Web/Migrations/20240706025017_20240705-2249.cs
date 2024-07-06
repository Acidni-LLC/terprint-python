using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace Terprint.Web.Migrations
{
    /// <inheritdoc />
    public partial class _202407052249 : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Batch_Grower_GrowerId",
                table: "Batch");

            migrationBuilder.DropForeignKey(
                name: "FK_Batch_Strain_StrainId",
                table: "Batch");

            migrationBuilder.RenameColumn(
                name: "StrainId",
                table: "Batch",
                newName: "StrainID");

            migrationBuilder.RenameColumn(
                name: "GrowerId",
                table: "Batch",
                newName: "GrowerID");

            migrationBuilder.RenameIndex(
                name: "IX_Batch_StrainId",
                table: "Batch",
                newName: "IX_Batch_StrainID");

            migrationBuilder.RenameIndex(
                name: "IX_Batch_GrowerId",
                table: "Batch",
                newName: "IX_Batch_GrowerID");

            migrationBuilder.AlterColumn<int>(
                name: "GrowerID",
                table: "Batch",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AddForeignKey(
                name: "FK_Batch_Grower_GrowerID",
                table: "Batch",
                column: "GrowerID",
                principalTable: "Grower",
                principalColumn: "GrowerId");

            migrationBuilder.AddForeignKey(
                name: "FK_Batch_Strain_StrainID",
                table: "Batch",
                column: "StrainID",
                principalTable: "Strain",
                principalColumn: "StrainId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Batch_Grower_GrowerID",
                table: "Batch");

            migrationBuilder.DropForeignKey(
                name: "FK_Batch_Strain_StrainID",
                table: "Batch");

            migrationBuilder.RenameColumn(
                name: "StrainID",
                table: "Batch",
                newName: "StrainId");

            migrationBuilder.RenameColumn(
                name: "GrowerID",
                table: "Batch",
                newName: "GrowerId");

            migrationBuilder.RenameIndex(
                name: "IX_Batch_StrainID",
                table: "Batch",
                newName: "IX_Batch_StrainId");

            migrationBuilder.RenameIndex(
                name: "IX_Batch_GrowerID",
                table: "Batch",
                newName: "IX_Batch_GrowerId");

            migrationBuilder.AlterColumn<int>(
                name: "GrowerId",
                table: "Batch",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AddForeignKey(
                name: "FK_Batch_Grower_GrowerId",
                table: "Batch",
                column: "GrowerId",
                principalTable: "Grower",
                principalColumn: "GrowerId",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_Batch_Strain_StrainId",
                table: "Batch",
                column: "StrainId",
                principalTable: "Strain",
                principalColumn: "StrainId");
        }
    }
}
